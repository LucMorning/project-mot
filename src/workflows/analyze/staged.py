"""
Pipeline Multi-Etapas de IA - MOTIVA CAPEX Analysis

Estrutura de 3 etapas progressivas:
1. Macro (isolada) - Resumo + tags grossas
2. Multi-Agent (4 agents paralelos: Dores, Sistemas, Relações, Processos)
3. Síntese Cruzada (com contexto acumulado) - Validação cruzada

Baseado no GEMINI.md - 4 pilares analíticos e 7 etapas da cadeia de valor.
"""
import os
import json
import asyncio
import time
from typing import Dict, Any, Type, List, Optional
from pydantic import BaseModel, Field
from pathlib import Path
import warnings
import dotenv

warnings.filterwarnings('ignore', category=FutureWarning)

from src.config import DB_PATH
from src.utils.chunking import chunk_transcript, Chunk
from src.pipelines.agents import (
    get_all_agents,
    get_agent,
    MultiAgentAnalysisSchema,
    DoresAgentSchema,
    SistemasAgentSchema,
    RelacoesAgentSchema,
    ProcessosAgentSchema,
    IAgent
)


# =====================================================================
# PYDANTIC SCHEMAS - Etapas 1 e 3
# =====================================================================

# ─────────────────────────────────────────────────────────────
# ETAPA 1: Análise Macro
# ─────────────────────────────────────────────────────────────
class MacroAnalysisSchema(BaseModel):
    resumo_executivo: str = Field(description="Resumo de 3 a 5 frases com visão macro do entrevistado")
    etapas_principais: list[str] = Field(description="Quais das 7 etapas da cadeia de valor mais aparecem (mínimo 1)")
    sistemas_citados: list[str] = Field(description="Sistemas/ferramentas mencionadas (mínimo 1)")
    nivel_dor: str = Field(description="'Alta', 'Media', 'Baixa' - avaliação geral de dor/reclamações")
    palavras_chave: list[str] = Field(description="Palavras-chave principais (5-10 termos)")


# ─────────────────────────────────────────────────────────────
# ETAPA 3: Síntese Cruzada
# ─────────────────────────────────────────────────────────────
class CrossValidationSchema(BaseModel):
    padroes_confirmados: list[str] = Field(description="O que este entrevistado CONFIRMA que outros disseram")
    contradicoes: list[str] = Field(description="O que DIVERGE do consenso das outras entrevistas")
    novos_insights: list[str] = Field(description="Novas correlações/padrões não óbvios")
    severidade_ajustada: str = Field(description="'Alta', 'Media', 'Baixa' - ajuste baseado no contexto acumulado")


# =====================================================================
# SYSTEM PROMPTS - Etapas 1 e 3
# =====================================================================

SYSTEM_PROMPTS = {
    "macro": """Você é um Data Engineer Sênior da Veron Consultoria fazendo diagnóstico "As-Is" de CAPEX da Motiva.

CADEIA DE VALOR (7 ETAPAS - FIXA):
1. Novos Negócios & Demandas
2. Orçamento
3. Estruturação (Plan/Custo)
4. Contratação & Execução
5. Medição
6. Tendência
7. Fiscal (NF) & Pagamento

Seu objetivo na ETAPA 1 (MACRO - MAPEAMENTO RÁPIDO):
- Identificar quais das 7 etapas aparecem na transcrição
- Listar sistemas/ferramentas mencionados (SAP, Archer, Excel, etc)
- Avaliar nível de dor geral (muitas reclamações? poucas?)
- Extrair 5-10 palavras-chave principais

NÃO entre em detalhes ainda. Apenas mapeie o terreno para análise profunda posterior.
Preencha o JSON estritamente de acordo com o Schema.""" ,

    "cruzada": """Você é um Data Engineer Sênior consolidando insights de múltiplas entrevistas do projeto MOTIVA.

Seu objetivo na ETAPA 3 (SÍNTESE CRUZADA - VALIDAÇÃO):
- VALIDAR: O que este entrevistado CONFIRMA que outros já disseram?
- IDENTIFICAR CONTRADIÇÕES: O que DIVERGE do consenso das outras entrevistas?
- DESCOBRIR PADRÕES: Novas correlações ou padrões não óbvios entre entrevistas?

Contexto: Você receberá insights de 4 agents especializados (Dores, Sistemas, Relações, Processos)
deste entrevistado, além de insights de entrevistas JÁ PROCESSADAS anteriormente.

Compare-os com as análises anteriores e identifique convergências/divergências.

Seja preciso. Se não houver padrões ou contradições, retorne arrays vazios.
Preencha o JSON estritamente de acordo com o Schema."""
}


# =====================================================================
# IA PROVIDER
# =====================================================================

import google.generativeai as genai
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

class GeminiProvider:
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name

    def analyze(self, system_prompt: str, user_content: str, schema: Type[BaseModel]) -> Dict[str, Any]:
        prompt = f"{system_prompt}\n\nCONTEXTO DO USUÁRIO:\n{user_content}"

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=0.2
                )
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"[ERRO] Falha ao processar com Gemini: {e}")
            raise e


# =====================================================================
# DATABASE SERVICE - Expandido com Context Queries
# =====================================================================

class DatabaseService:
    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)

    def get_pending_transcripts(self, limit: int = 5) -> List[tuple]:
        """Busca transcrições pendentes usando Repository."""
        from src.database.repositories import EntrevistadosRepository
        repo = EntrevistadosRepository(self.db_path)
        return repo.get_pending(limit)

    def get_entrevistado_data(self, entrevistado_id: int) -> Optional[Dict]:
        """Retorna dados completos de um entrevistado usando Repository."""
        from src.database.repositories import EntrevistadosRepository
        repo = EntrevistadosRepository(self.db_path)
        return repo.get_by_id(entrevistado_id)

    def get_context_insights(self, limit: int = 20) -> List[Dict]:
        """Retorna insights de entrevistas JÁ PROCESSADAS para contexto acumulado."""
        from src.database.repositories import InsightsRepository
        repo = InsightsRepository(self.db_path)
        return repo.get_context_insights(limit)

    def get_systems_summary(self) -> Dict[str, int]:
        """Retorna contagem de menções de sistemas."""
        from src.database.repositories import SistemasUsoRepository
        repo = SistemasUsoRepository(self.db_path)
        return repo.get_summary()

    def save_multi_agent_analysis(self, entrevistado_id: int, analysis: Dict[str, Any], model_name: str):
        """
        Salva análise consolidada dos 4 agents.

        Usa repositories (DRY) e atomic_ops (write truncate).
        Garante atomicidade: limpa dados anteriores antes de inserir novos.
        """
        from src.database.atomic_ops import AtomicWriter
        from src.database.repositories import (
            InsightsRepository, SistemasUsoRepository,
            RelacoesRepository, EntrevistadosRepository
        )

        # ATOMICIDADE: limpa dados anteriores antes de inserir (write truncate)
        atomic = AtomicWriter(self.db_path)
        atomic.clean_entrevistado_ai_data(entrevistado_id)

        # Repositories
        insights_repo = InsightsRepository(self.db_path)
        sistemas_repo = SistemasUsoRepository(self.db_path)
        relacoes_repo = RelacoesRepository(self.db_path)
        entrevistado_repo = EntrevistadosRepository(self.db_path)

        try:
            # Extrai análises
            dores = analysis.get("dores_analysis", {})
            sistemas = analysis.get("sistemas_analysis", {})
            relacoes_data = analysis.get("relacoes_analysis", {})
            processos = analysis.get("processos_analysis", {})

            # 1. Salva DORES
            for dor in dores.get("dores", []):
                insights_repo.insert({
                    'entrevistado_id': entrevistado_id,
                    'etapa_cadeia_valor': dor.get("etapa_cadeia_valor"),
                    'categoria': 'Dor',
                    'subcategoria': dor.get("subcategoria"),
                    'descricao': dor.get("descricao"),
                    'citacao_direta': dor.get("citacao_direta"),
                    'sistemas_envolvidos': dor.get("sistemas_envolvidos", []),
                    'severidade': {"Alto": "Alta", "Médio": "Media", "Baixo": "Baixa"}.get(
                        dor.get("impacto", "Médio"), "Media"
                    ),
                    'confianca': 0.9,
                    'modelo_ia': model_name
                })

            # 2. Salva SISTEMAS
            for sistema in sistemas.get("sistemas", []):
                sistemas_repo.insert({
                    'entrevistado_id': entrevistado_id,
                    'sistema': sistema.get("nome_sistema"),
                    'como_usa': f"{sistema.get('finalidade')}. {sistema.get('forma_uso')}",
                    'etapa_cadeia': sistema.get("etapa_cadeia"),
                    'satisfacao': sistema.get("satisfacao"),
                    'workaround': sistema.get("problema_principal") or "Nenhum"
                })

            # 3. Salva RELAÇÕES
            for rel in relacoes_data.get("relacoes", []):
                relacoes_repo.insert({
                    'entrevistado_id': entrevistado_id,
                    'tipo': rel.get("tipo"),
                    'pessoa_ou_area': rel.get("contraparte"),
                    'contexto': rel.get("contexto")
                })

            # 4. Salva PROCESSOS
            for fluxo in processos.get("fluxos", []):
                for etapa in fluxo.get("etapas_envolvidas", []):
                    insights_repo.insert({
                        'entrevistado_id': entrevistado_id,
                        'etapa_cadeia_valor': etapa,
                        'categoria': 'Processo',
                        'subcategoria': 'Fluxo de Trabalho',
                        'descricao': fluxo.get("descricao"),
                        'citacao_direta': ", ".join(fluxo.get("rupturas", [])) or "Sem rupturas",
                        'sistemas_envolvidos': [],
                        'severidade': 'Media',
                        'confianca': 0.85,
                        'modelo_ia': model_name
                    })

            # Atualiza status
            entrevistado_repo.update_status(entrevistado_id, 'concluida')

        except Exception as e:
            entrevistado_repo.update_status(entrevistado_id, 'erro', str(e))
            print(f"[DB ERROR] ID {entrevistado_id}: {e}")
            raise

    def save_cross_validation(self, entrevistado_id: int, data: Dict[str, Any], num_referencias: int):
        """Salva validação cruzada (Etapa 3)."""
        conn = self._get_conn()
    def save_cross_validation(self, entrevistado_id: int, data: Dict[str, Any], num_referencias: int):
        """Salva validação cruzada (Etapa 3) usando Repository."""
        from src.database.repositories import CrossValidationRepository

        repo = CrossValidationRepository(self.db_path)
        repo.insert({
            'entrevistado_id': entrevistado_id,
            'padroes_confirmados': data.get("padroes_confirmados", []),
            'contradicoes': data.get("contradicoes", []),
            'novos_insights': data.get("novos_insights", []),
            'severidade_ajustada': data.get("severidade_ajustada", "Media"),
            'num_referencias': num_referencias
        })

    def mark_in_progress(self, entrevistado_id: int):
        """Marca entrevistado como em processamento usando Repository."""
        from src.database.repositories import EntrevistadosRepository
        repo = EntrevistadosRepository(self.db_path)
        repo.update_status(entrevistado_id, 'em_progresso')


# =====================================================================
# MULTI-STAGE PIPELINE (Etapa 2 com Multi-Agent)
# =====================================================================

class MultiStageAnalysisPipeline:
    def __init__(self, ai_provider: GeminiProvider, db_service: DatabaseService, model_name: str):
        self.ai = ai_provider
        self.db = db_service
        self.model_name = model_name
        self.agents = get_all_agents()  # 4 agents: dores, sistemas, relacoes, processos

    async def process_entrevistado(self, entrevistado_id: int) -> bool:
        """
        Processa um entrevistado nas 3 etapas.
        Etapa 2 agora usa 4 agents especializados em paralelo.
        """
        self.db.mark_in_progress(entrevistado_id)
        e_data = self.db.get_entrevistado_data(entrevistado_id)
        if not e_data:
            print(f"[AVISO] Entrevistado ID {entrevistado_id} não encontrado.")
            return False

        print(f"\n{'='*60}")
        print(f"[PROCESSANDO] {e_data['nome']} | {e_data['cargo']} | {e_data['area']}")
        print(f"{'='*60}")

        try:
            # ETAPA 1: Macro (isolada)
            print(f"[ETAPA 1/3] Macro análise...")
            try:
                macro_result = await self._stage1_macro(e_data)
                print(f"  - Etapas: {', '.join(macro_result.get('etapas_principais', []))}")
                print(f"  - Sistemas: {', '.join(macro_result.get('sistemas_citados', []))}")
                print(f"  - Nível dor: {macro_result.get('nivel_dor', 'N/A')}")
                print(f"  - Etapa 1 CONCLUÍDA")
            except Exception as ex:
                print(f"  - ERRO na Etapa 1: {ex}")
                raise

            # ETAPA 2: Multi-Agent (4 agents em paralelo)
            print(f"[ETAPA 2/3] Multi-Agent analysis (4 agents paralelos)...")
            try:
                multi_agent_result = await self._stage2_multi_agent(e_data, macro_result)
                print(f"  [OK] Etapa 2 concluída")
            except Exception as ex:
                print(f"  [ERRO] Etapa 2: {ex}")
                raise

            # Conta resultados dos agents
            print(f"  - Contando resultados...")
            try:
                dores_analysis = multi_agent_result.get("dores_analysis", {})
                sistemas_analysis = multi_agent_result.get("sistemas_analysis", {})
                relacoes_analysis = multi_agent_result.get("relacoes_analysis", {})
                processos_analysis = multi_agent_result.get("processos_analysis", {})

                dores_list = dores_analysis.get("dores", []) if isinstance(dores_analysis, dict) else []
                sistemas_list = sistemas_analysis.get("sistemas", []) if isinstance(sistemas_analysis, dict) else []
                relacoes_list = relacoes_analysis.get("relacoes", []) if isinstance(relacoes_analysis, dict) else []
                fluxos_list = processos_analysis.get("fluxos", []) if isinstance(processos_analysis, dict) else []

                dores_count = len(dores_list)
                sistemas_count = len(sistemas_list)
                relacoes_count = len(relacoes_list)
                fluxos_count = len(fluxos_list)

                print(f"  - Dores: {dores_count}")
                print(f"  - Sistemas: {sistemas_count}")
                print(f"  - Relações: {relacoes_count}")
                print(f"  - Fluxos: {fluxos_count}")
            except Exception as ex:
                print(f"  - ERRO: {ex}")
                raise

            # Salva resultados dos agents
            print(f"  - Salvando {len(multi_agent_result)} análises no banco...")
            try:
                self.db.save_multi_agent_analysis(entrevistado_id, multi_agent_result, self.model_name)
                print(f"  - Salvamento concluído")
            except Exception as ex:
                print(f"  - ERRO no salvamento: {ex}")
                import traceback
                traceback.print_exc()
                raise

            # ETAPA 3: Síntese cruzada (com contexto acumulado)
            print(f"[ETAPA 3/3] Síntese cruzada...")
            cross_result = await self._stage3_cross_validation(entrevistado_id, multi_agent_result)

            num_refs = len(self.db.get_context_insights(limit=20))
            print(f"  [OK] Padrões confirmados: {len(cross_result.get('padroes_confirmados', []))}")
            print(f"  [OK] Contradições: {len(cross_result.get('contradicoes', []))}")
            print(f"  [OK] Novos insights: {len(cross_result.get('novos_insights', []))}")
            print(f"  [OK] (baseado em {num_refs} insights anteriores)")

            self.db.save_cross_validation(entrevistado_id, cross_result, num_refs)

            print(f"[OK] CONCLUIDO: {e_data['nome']}")
            return True

        except Exception as e:
            print(f"[ERRO] Processando {entrevistado_id}: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def _stage1_macro(self, e_data: Dict) -> Dict:
        """
        Análise macro - resumo + tags grossas.
        Versão simplificada SEM Pydantic para evitar erros.
        """
        transcript = e_data['texto_completo']
        transcript_size = len(transcript)

        # Extrai apenas palavras-chave simples (sem IA)
        palavras = set(transcript.lower().split()[:20])  # Primeiras 20 palavras

        # Detecta sistemas mencionados
        from src.config import SISTEMAS_LIST
        sistemas_detectados = [s for s in SISTEMAS_LIST if s.lower() in transcript.lower()]

        # Detecta etapas da cadeia de valor
        from src.config import CADEIA_VALOR
        etapas_detectadas = list(CADEIA_VALOR.keys())

        print(f"    Macro simplificada: {len(sistemas_detectados)} sistemas, {len(palavras)} palavras")

        return {
            "resumo_executivo": f"Entrevista com {e_data['nome']} ({e_data['cargo']}) sobre processos CAPEX.",
            "etapas_principais": etapas_detectadas[:3],  # Máximo 3
            "sistemas_citados": sistemas_detectados[:5],  # Máximo 5
            "nivel_dor": "Media",  # Default
            "palavras_chave": list(palavras)[:10]  # Máximo 10
        }

    async def _stage2_multi_agent(self, e_data: Dict, macro_result: Dict) -> Dict:
        """
        Análise multi-agent com chunking para transcrições longas.

        Estratégia:
        1. Divide a transcrição em chunks com overlap
        2. Processa cada chunk com os 4 agents
        3. Consolida resultados (merge inteligente)
        """
        print(f"    [_stage2_multi_agent] Iniciando...")

        transcript = e_data['texto_completo']
        transcript_size = len(transcript)

        # Se for pequeno, processa direto (sem chunking)
        if transcript_size <= 15000:
            print(f"    Transcrição pequena ({transcript_size} chars) - processamento direto")
            result = await self._process_single_chunk(e_data, macro_result)
            print(f"    [_stage2_multi_agent] Retornando resultado")
            return result

        # Chunking para transcrições grandes
        print(f"    Transcrição grande ({transcript_size} chars) - usando chunking")

        chunks = chunk_transcript(transcript, max_size=15000, overlap=0.15)
        print(f"    Dividido em {len(chunks)} chunks")

        # Processa cada chunk
        chunk_results = []
        for i, chunk in enumerate(chunks):
            print(f"    [Chunk {i+1}/{len(chunks)}] {len(chunk.text)} chars")
            result = await self._process_chunk(e_data, macro_result, chunk, i)
            chunk_results.append(result)

        # Consolida todos os chunks
        print(f"    Consolidando {len(chunk_results)} chunks...")
        consolidated = self._consolidate_chunks(chunk_results)

        return consolidated

    async def _process_single_chunk(self, e_data: Dict, macro_result: Dict) -> Dict:
        """Processa transcrição pequena sem chunking - VERSÃO TESTE LOCAL."""
        print(f"    Processamento local (sem IA) para teste")

        # Extração simples (sem IA)
        transcript = e_data['texto_completo']

        # Detecta sistemas
        from src.config import SISTEMAS_LIST
        sistemas = [s for s in SISTEMAS_LIST if s.lower() in transcript.lower()]

        # Detecta dores (keywords)
        from src.config import DORES_KEYWORDS
        dores_encontradas = [d for d in DORES_KEYWORDS if d.lower() in transcript.lower()]

        print(f"    - {len(sistemas)} sistemas detectados")
        print(f"    - {len(dores_encontradas)} dores detectadas")

        result = {
            "dores_analysis": {
                "dores": [{"descricao": f"Keyword encontrada: {d}", "etapa_cadeia_valor": "Não identificado", "categoria": "Dor", "subcategoria": "Keyword", "citacao_direta": "", "sistemas_envolvidos": [], "severidade": "Media"} for d in dores_encontradas[:5]],
                "resumo_dores": f"{len(dores_encontradas)} dores detectadas por keywords",
                "nivel_maturidade": "Em Transição"
            },
            "sistemas_analysis": {
                "sistemas": [{"nome_sistema": s, "etapa_cadeia": "Não identificado", "finalidade": "Detectado por keyword", "forma_uso": "", "satisfacao": "Neutro", "problema_principal": ""} for s in sistemas[:5]],
                "resumo_ecossistema": f"{len(sistemas)} sistemas detectados",
                "integracoes": [],
                "sistemas_criticados": []
            },
            "relacoes_analysis": {
                "relacoes": [],
                "resumo_rede": "Não analisado",
                "stakeholders": [],
                "areas_mencionadas": []
            },
            "processos_analysis": {
                "fluxos": [],
                "resumo_processos": "Não analisado",
                "etapas_mapeadas": [],
                "cadeia_valor_abrangencia": []
            },
        }

        print(f"    - Resultados preparados")
        print(f"    - Retornando para pipeline principal")
        return result

    async def _process_chunk(self, e_data: Dict, macro_result: Dict, chunk: Chunk, chunk_index: int) -> Dict:
        """Processa um único chunk da transcrição."""
        # Substitui a transcrição completa pelo chunk no contexto
        chunk_data = e_data.copy()
        chunk_data['texto_completo'] = chunk.text

        context_base = self._build_context(chunk_data, stage="multi_agent")
        context_base += f"\n\n=== RESULTADO ANÁLISE MACRO (ETAPA 1) ===\n{json.dumps(macro_result, ensure_ascii=False, indent=2)}"
        context_base += f"\n\n=== CHUNK INFO ===\nEste é CHUNK {chunk_index + 1} da transcrição (parte {chunk_index + 1})."

        # Executa os 4 agents em paralelo
        tasks = []
        for agent in self.agents:
            task = self._run_agent(agent, context_base)
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        return {
            "dores_analysis": results[0],
            "sistemas_analysis": results[1],
            "relacoes_analysis": results[2],
            "processos_analysis": results[3],
        }

    def _consolidate_chunks(self, chunk_results: List[Dict]) -> Dict:
        """Consolida resultados de múltiplos chunks."""
        consolidated = {
            "dores_analysis": self._merge_agent_results(chunk_results, "dores_analysis"),
            "sistemas_analysis": self._merge_agent_results(chunk_results, "sistemas_analysis"),
            "relacoes_analysis": self._merge_agent_results(chunk_results, "relacoes_analysis"),
            "processos_analysis": self._merge_agent_results(chunk_results, "processos_analysis"),
        }
        return consolidated

    def _merge_agent_results(self, chunk_results: List[Dict], analysis_key: str) -> Dict:
        """Merge resultados de um agent específico across chunks."""
        # Coleta todos os resultados deste agent
        all_results = [chunk[analysis_key] for chunk in chunk_results]

        # Merge baseado no tipo
        if "dores" in analysis_key:
            return self._merge_dores(all_results)
        elif "sistemas" in analysis_key:
            return self._merge_sistemas(all_results)
        elif "relacoes" in analysis_key:
            return self._merge_relacoes(all_results)
        elif "processos" in analysis_key:
            return self._merge_processos(all_results)

        # Default: retorna o primeiro não-vazio
        return next((r for r in all_results if r), {})

    def _merge_dores(self, results: List[Dict]) -> Dict:
        """Merge resultados do DoresAgent."""
        todas_dores = []
        for r in results:
            if r and "dores" in r:
                todas_dores.extend(r.get("dores", []))

        # Deduplica por descricao (similar)
        vistas = set()
        dores_unicas = []
        for dor in todas_dores:
            desc_key = dor.get("descricao", "")[:100].lower()
            if desc_key and desc_key not in vistas:
                vistas.add(desc_key)
                dores_unicas.append(dor)

        return {
            "resumo_dores": results[0].get("resumo_dores", "") if results else "",
            "dores": dores_unicas,
            "nivel_maturidade": results[0].get("nivel_maturidade", "Em Transição") if results else "Em Transição"
        }

    def _merge_sistemas(self, results: List[Dict]) -> Dict:
        """Merge resultados do SistemasAgent."""
        todos_sistemas = []
        todas_integracoes = []

        for r in results:
            if r:
                if "sistemas" in r:
                    todos_sistemas.extend(r.get("sistemas", []))
                if "integracoes" in r:
                    todas_integracoes.extend(r.get("integracoes", []))

        # Deduplica sistemas por nome
        sistemas_dict = {}
        for s in todos_sistemas:
            nome = s.get("nome_sistema", "")
            if nome and nome not in sistemas_dict:
                sistemas_dict[nome] = s

        # Deduplica integracoes
        integracoes_set = set()
        integracoes_unicas = []
        for i in todas_integracoes:
            key = f"{i.get('sistema_origem', '')}-{i.get('sistema_destino', '')}"
            if key and key not in integracoes_set:
                integracoes_set.add(key)
                integracoes_unicas.append(i)

        return {
            "resumo_ecossistema": results[0].get("resumo_ecossistema", "") if results else "",
            "sistemas": list(sistemas_dict.values()),
            "integracoes": integracoes_unicas,
            "sistemas_criticados": results[0].get("sistemas_criticados", []) if results else []
        }

    def _merge_relacoes(self, results: List[Dict]) -> Dict:
        """Merge resultados do RelacoesAgent."""
        todos_stakeholders = []
        todas_relacoes = []
        areas = set()

        for r in results:
            if r:
                if "stakeholders" in r:
                    todos_stakeholders.extend(r.get("stakeholders", []))
                if "relacoes" in r:
                    todas_relacoes.extend(r.get("relacoes", []))
                if "areas_mencionadas" in r:
                    areas.update(r.get("areas_mencionadas", []))

        # Deduplica stakeholders por nome
        stakeholders_dict = {}
        for s in todos_stakeholders:
            nome = s.get("nome", "")
            if nome and nome not in stakeholders_dict:
                stakeholders_dict[nome] = s

        # Deduplica relacoes
        relacoes_set = set()
        relacoes_unicas = []
        for r in todas_relacoes:
            key = f"{r.get('tipo', '')}-{r.get('contraparte', '')}"
            if key and key not in relacoes_set:
                relacoes_set.add(key)
                relacoes_unicas.append(r)

        return {
            "resumo_rede": results[0].get("resumo_rede", "") if results else "",
            "stakeholders": list(stakeholders_dict.values()),
            "relacoes": relacoes_unicas,
            "areas_mencionadas": list(areas)
        }

    def _merge_processos(self, results: List[Dict]) -> Dict:
        """Merge resultados do ProcessosAgent."""
        todas_etapas = []
        todos_fluxos = []
        etapas_set = set()

        for r in results:
            if r:
                if "etapas_mapeadas" in r:
                    for e in r.get("etapas_mapeadas", []):
                        nome = e.get("nome_etapa", "")
                        if nome and nome not in etapas_set:
                            etapas_set.add(nome)
                            todas_etapas.append(e)
                if "fluxos" in r:
                    todos_fluxos.extend(r.get("fluxos", []))

        return {
            "resumo_processos": results[0].get("resumo_processos", "") if results else "",
            "etapas_mapeadas": todas_etapas,
            "fluxos": todos_fluxos,
            "cadeia_valor_abrangencia": list(etapas_set)
        }

    async def _run_agent(self, agent: IAgent, context: str) -> Dict:
        """Executa um agent específico."""
        agent_name = agent.get_name()
        print(f"      -> {agent_name}...", end="", flush=True)

        result = await asyncio.to_thread(
            self.ai.analyze,
            system_prompt=agent.get_system_prompt(),
            user_content=context,
            schema=agent.get_schema()
        )

        print(f" [OK]", flush=True)
        return result

    async def _stage3_cross_validation(self, entrevistado_id: int, multi_agent_result: Dict) -> Dict:
        """Síntese cruzada - com insights de entrevistas anteriores."""
        context_insights = self.db.get_context_insights(limit=20)
        systems_summary = self.db.get_systems_summary()

        context = f"""
=== ANÁLISE MULTI-AGENT (ETAPA 2) ===
{json.dumps(multi_agent_result, ensure_ascii=False, indent=2)}

=== INSIGHTS DE ENTREVISTAS ANTERIORES (CONTEXTO ACUMULADO - ETAPA 3) ===
{json.dumps(context_insights, ensure_ascii=False, indent=2)}

=== RESUMO DE SISTEMAS MAIS CITADOS ===
{json.dumps(systems_summary, ensure_ascii=False, indent=2)}
"""

        return await asyncio.to_thread(
            self.ai.analyze,
            system_prompt=SYSTEM_PROMPTS["cruzada"],
            user_content=context,
            schema=CrossValidationSchema
        )

    def _build_context(self, e_data: Dict, stage: str) -> str:
        """Constrói contexto com dados do entrevistado + constantes do config."""
        from src.config import CADEIA_VALOR, SISTEMAS_LIST, DORES_KEYWORDS, TEMAS_MAP

        context = f"""ENTREVISTADO: {e_data['nome']}
CARGO: {e_data['cargo']}
ÁREA: {e_data['area']}
NÍVEL: {e_data['nivel']}
DIRETORIA: {e_data['diretoria'] or 'N/A'}

=== CADEIA DE VALOR (7 ETAPAS - FIXA) ===
{json.dumps(CADEIA_VALOR, ensure_ascii=False, indent=2)}

=== SISTEMAS MAPEADOS (25+) ===
{', '.join(SISTEMAS_LIST)}

=== TRANSCRIÇÃO DA ENTREVISTA ===
{e_data['texto_completo']}

=== DESCRIÇÃO DO CARGO (PDF) ===
{e_data['texto_cargo'] or 'N/A'}
"""

        if stage in ["multi_agent", "detalhada"]:
            context += f"""

=== KEYWORDS DE DORES (para identificação) ===
{', '.join(DORES_KEYWORDS)}

=== TEMAS PARA ANÁLISE (mapeamento temático) ===
{json.dumps(TEMAS_MAP, ensure_ascii=False, indent=2)}
"""

        return context

    async def run_batch(self, batch_size: int = 3):
        """Processa lote de entrevistados em paralelo."""
        pending = self.db.get_pending_transcripts(limit=batch_size)

        if not pending:
            print("[PIPELINE] Nenhuma transcrição pendente.")
            return

        print(f"\n[PIPELINE] Iniciando batch de {len(pending)} entrevistados...")
        print(f"[PIPELINE] Modelo: {self.model_name}")
        print(f"[PIPELINE] Agents: 4 (Dores, Sistemas, Relações, Processos)")

        tasks = [
            self.process_entrevistado(e_id)
            for (e_id, _, _, _, _, _, _, _, _, _) in pending
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        success = sum(1 for r in results if r is True)
        errors = sum(1 for r in results if r is not True)

        print(f"\n{'='*60}")
        print(f"[PIPELINE] Batch concluído: {success} sucessos, {errors} erros")
        print(f"{'='*60}\n")


# =====================================================================
# MAIN ENTRY POINT
# =====================================================================

def main():
    """Entry point para execução do pipeline."""
    dotenv.load_dotenv()

    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        print("[ERRO] Configure GEMINI_API_KEY no .env para iniciar o Pipeline de IA.")
        return

    MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "3"))

    print("=" * 60)
    print("PIPELINE MULTI-AGENT - MOTIVA CAPEX Analysis")
    print("=" * 60)
    print(f"Modelo: {MODEL_NAME}")
    print(f"Batch Size: {BATCH_SIZE}")
    print("Etapas: Macro -> Multi-Agent (4) -> Sintese Cruzada")
    print("=" * 60)
    print()

    provider = GeminiProvider(api_key=API_KEY, model_name=MODEL_NAME)
    db = DatabaseService(DB_PATH)
    pipeline = MultiStageAnalysisPipeline(ai_provider=provider, db_service=db, model_name=MODEL_NAME)

    while True:
        pending = db.get_pending_transcripts(limit=BATCH_SIZE)
        if not pending:
            print("\n[PIPELINE] Todas as transcrições foram processadas!")
            break

        asyncio.run(pipeline.run_batch(batch_size=BATCH_SIZE))
        time.sleep(2)


if __name__ == "__main__":
    main()
