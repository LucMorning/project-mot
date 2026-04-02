"""
Pipeline Multi-Etapas de IA - MOTIVA CAPEX Analysis

Estrutura de 3 etapas progressivas:
1. Macro (isolada) - Resumo + tags grossas
2. Multi-Agent (4 agents paralelos: Dores, Sistemas, Relações, Processos)
3. Síntese Cruzada (com contexto acumulado) - Validação cruzada

Baseado no GEMINI.md - 4 pilares analíticos e 7 etapas da cadeia de valor.
"""
import os
import sqlite3
import json
import asyncio
import time
from typing import Dict, Any, Type, List, Optional
from pydantic import BaseModel, Field
from pathlib import Path

import google.generativeai as genai
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
import dotenv

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

class GeminiProvider:
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash-exp"):
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

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def get_pending_transcripts(self, limit: int = 5) -> List[tuple]:
        """Busca transcrições pendentes."""
        conn = self._get_conn()
        cursor = conn.cursor()
        query = """
            SELECT e.id, t.texto_completo, e.nome, e.cargo, e.area, e.nivel, e.diretoria, c.texto_extraido
            FROM entrevistados e
            JOIN transcricoes t ON t.entrevistado_id = e.id
            LEFT JOIN cargos c ON c.arquivo_pdf = e.arquivo_cargo_pdf
            WHERE e.status_revisao IN ('pendente', 'erro')
            ORDER BY e.id ASC
            LIMIT ?
        """
        cursor.execute(query, (limit,))
        data = cursor.fetchall()
        conn.close()
        return data

    def get_entrevistado_data(self, entrevistado_id: int) -> Optional[Dict]:
        """Retorna dados completos de um entrevistado."""
        conn = self._get_conn()
        cursor = conn.cursor()
        query = """
            SELECT e.id, e.nome, e.cargo, e.area, e.nivel, e.diretoria,
                   t.texto_completo, c.responsabilidades, c.competencias, c.desafios
            FROM entrevistados e
            JOIN transcricoes t ON t.entrevistado_id = e.id
            LEFT JOIN cargos c ON c.arquivo_pdf = e.arquivo_cargo_pdf
            WHERE e.id = ?
        """
        cursor.execute(query, (entrevistado_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        # Monta a string limpa do PDF de cargo p/ economizar tokens
        resp = row[7]
        comp = row[8]
        desafios = row[9]
        
        blocks = []
        if desafios: blocks.append(f"DESAFIOS:\n{desafios}")
        if resp: blocks.append(f"RESPONSABILIDADES:\n{resp}")
        if comp: blocks.append(f"COMPETÊNCIAS:\n{comp}")
        
        cargo_limpo = "\n\n".join(blocks) if blocks else None

        return {
            "id": row[0],
            "nome": row[1],
            "cargo": row[2],
            "area": row[3],
            "nivel": row[4],
            "diretoria": row[5],
            "texto_completo": row[6],
            "texto_cargo": cargo_limpo
        }

    def get_context_insights(self, limit: int = 20) -> List[Dict]:
        """Retorna insights de entrevistas JÁ PROCESSADAS para contexto acumulado."""
        conn = self._get_conn()
        cursor = conn.cursor()
        query = """
            SELECT i.categoria, i.subcategoria, i.descricao, i.severidade,
                   e.nome, e.cargo, e.area, i.etapa_cadeia_valor
            FROM insights_ia i
            JOIN entrevistados e ON e.id = i.entrevistado_id
            WHERE e.status_revisao = 'concluida'
            ORDER BY
                CASE i.severidade
                    WHEN 'Alta' THEN 1
                    WHEN 'Media' THEN 2
                    WHEN 'Baixa' THEN 3
                END,
                i.created_at DESC
            LIMIT ?
        """
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "categoria": r[0], "subcategoria": r[1],
                "descricao": r[2], "severidade": r[3],
                "entrevistado": r[4], "cargo": r[5], "area": r[6],
                "etapa": r[7]
            }
            for r in rows
        ]

    def get_systems_summary(self) -> Dict[str, int]:
        """Retorna contagem de menções de sistemas."""
        conn = self._get_conn()
        cursor = conn.cursor()
        query = """
            SELECT sistema, COUNT(*) as count
            FROM sistemas_uso
            GROUP BY sistema
            ORDER BY count DESC
        """
        cursor.execute(query)
        conn.close()
        return dict(cursor.fetchall())

    def save_multi_agent_analysis(self, entrevistado_id: int, analysis: Dict[str, Any], model_name: str):
        """Salva análise consolidada dos 4 agents."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            # Extrai análises individuais
            dores = analysis.get("dores_analysis", {})
            sistemas = analysis.get("sistemas_analysis", {})
            relacoes = analysis.get("relacoes_analysis", {})
            processos = analysis.get("processos_analysis", {})

            # ─────────────────────────────────────────────────────────────
            # 1. Salvar DORES (na tabela insights_ia)
            # ─────────────────────────────────────────────────────────────
            for dor in dores.get("dores", []):
                cursor.execute("""
                    INSERT INTO insights_ia (entrevistado_id, etapa_cadeia_valor, categoria, subcategoria,
                    descricao, citacao_direta, sistemas_envolvidos, severidade, confianca, modelo_ia)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    entrevistado_id,
                    dor.get("etapa_cadeia_valor"),
                    "Dor",
                    dor.get("subcategoria"),
                    dor.get("descricao"),
                    dor.get("citacao_direta"),
                    json.dumps(dor.get("sistemas_envolvidos", []), ensure_ascii=False),
                    {"Alto": "Alta", "Médio": "Media", "Baixo": "Baixa"}.get(dor.get("impacto", "Médio"), "Media"),
                    0.9,
                    model_name
                ))

            # ─────────────────────────────────────────────────────────────
            # 2. Salvar SISTEMAS (na tabela sistemas_uso)
            # ─────────────────────────────────────────────────────────────
            for sistema in sistemas.get("sistemas", []):
                cursor.execute("""
                    INSERT INTO sistemas_uso (entrevistado_id, sistema, como_usa, etapa_cadeia, satisfacao, workaround)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    entrevistado_id,
                    sistema.get("nome_sistema"),
                    f"{sistema.get('finalidade')}. {sistema.get('forma_uso')}",
                    sistema.get("etapa_cadeia"),
                    sistema.get("satisfacao"),
                    sistema.get("problema_principal") or "Nenhum"
                ))

            # ─────────────────────────────────────────────────────────────
            # 3. Salvar RELAÇÕES (na tabela relacoes)
            # ─────────────────────────────────────────────────────────────
            for rel in relacoes.get("relacoes", []):
                cursor.execute("""
                    INSERT INTO relacoes (entrevistado_id, tipo, pessoa_ou_area, contexto)
                    VALUES (?, ?, ?, ?)
                """, (
                    entrevistado_id,
                    rel.get("tipo"),
                    rel.get("contraparte"),
                    rel.get("contexto")
                ))

            # ─────────────────────────────────────────────────────────────
            # 4. Salvar PROCESSOS (na tabela insights_ia como "Processo")
            # ─────────────────────────────────────────────────────────────
            # Para cada fluxo, cria um insight
            for fluxo in processos.get("fluxos", []):
                for etapa in fluxo.get("etapas_envolvidas", []):
                    cursor.execute("""
                        INSERT INTO insights_ia (entrevistado_id, etapa_cadeia_valor, categoria, subcategoria,
                        descricao, citacao_direta, sistemas_envolvidos, severidade, confianca, modelo_ia)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        entrevistado_id,
                        etapa,
                        "Processo",
                        "Fluxo de Trabalho",
                        fluxo.get("descricao"),
                        ", ".join(fluxo.get("rupturas", [])) or "Sem rupturas identificadas",
                        json.dumps([], ensure_ascii=False),
                        "Media",
                        0.85,
                        model_name
                    ))

            # Update status
            cursor.execute("UPDATE entrevistados SET status_revisao = 'concluida', data_revisao = CURRENT_TIMESTAMP WHERE id = ?", (entrevistado_id,))

            conn.commit()
        except Exception as e:
            conn.rollback()
            cursor.execute("UPDATE entrevistados SET status_revisao = 'erro', notas_revisor = ? WHERE id = ?", (str(e), entrevistado_id))
            conn.commit()
            print(f"[BD ERRO] ID {entrevistado_id}: {e}")
        finally:
            conn.close()

    def save_cross_validation(self, entrevistado_id: int, data: Dict[str, Any], num_referencias: int):
        """Salva validação cruzada (Etapa 3)."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO cross_validation (entrevistado_id, padroes_confirmados, contradicoes,
                novos_insights, severidade_ajustada, num_referencias)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                entrevistado_id,
                json.dumps(data.get("padroes_confirmados", []), ensure_ascii=False),
                json.dumps(data.get("contradicoes", []), ensure_ascii=False),
                json.dumps(data.get("novos_insights", []), ensure_ascii=False),
                data.get("severidade_ajustada", "Media"),
                num_referencias
            ))
            conn.commit()
        except Exception as e:
            print(f"[BD ERRO] Cross-validation ID {entrevistado_id}: {e}")
        finally:
            conn.close()

    def mark_in_progress(self, entrevistado_id: int):
        """Marca entrevistado como em processamento."""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("UPDATE entrevistados SET status_revisao = 'em_progresso' WHERE id = ?", (entrevistado_id,))
        conn.commit()
        conn.close()


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
            macro_result = await self._stage1_macro(e_data)
            print(f"  ✓ Etapas: {', '.join(macro_result.get('etapas_principais', []))}")
            print(f"  ✓ Sistemas: {', '.join(macro_result.get('sistemas_citados', []))}")
            print(f"  ✓ Nível dor: {macro_result.get('nivel_dor', 'N/A')}")

            # ETAPA 2: Multi-Agent (4 agents em paralelo)
            print(f"[ETAPA 2/3] Multi-Agent analysis (4 agents paralelos)...")
            multi_agent_result = await self._stage2_multi_agent(e_data, macro_result)

            # Conta resultados dos agents
            dores_count = len(multi_agent_result.get("dores_analysis", {}).get("dores", []))
            sistemas_count = len(multi_agent_result.get("sistemas_analysis", {}).get("sistemas", []))
            relacoes_count = len(multi_agent_result.get("relacoes_analysis", {}).get("relacoes", []))
            fluxos_count = len(multi_agent_result.get("processos_analysis", {}).get("fluxos", []))

            print(f"  ✓ Dores: {dores_count}")
            print(f"  ✓ Sistemas: {sistemas_count}")
            print(f"  ✓ Relações: {relacoes_count}")
            print(f"  ✓ Fluxos: {fluxos_count}")

            # Salva resultados dos agents
            self.db.save_multi_agent_analysis(entrevistado_id, multi_agent_result, self.model_name)

            # ETAPA 3: Síntese cruzada (com contexto acumulado)
            print(f"[ETAPA 3/3] Síntese cruzada...")
            cross_result = await self._stage3_cross_validation(entrevistado_id, multi_agent_result)

            num_refs = len(self.db.get_context_insights(limit=20))
            print(f"  ✓ Padrões confirmados: {len(cross_result.get('padroes_confirmados', []))}")
            print(f"  ✓ Contradições: {len(cross_result.get('contradicoes', []))}")
            print(f"  ✓ Novos insights: {len(cross_result.get('novos_insights', []))}")
            print(f"  ✓ (baseado em {num_refs} insights anteriores)")

            self.db.save_cross_validation(entrevistado_id, cross_result, num_refs)

            print(f"✅ CONCLUÍDO: {e_data['nome']}")
            return True

        except Exception as e:
            print(f"❌ ERRO processando {entrevistado_id}: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def _stage1_macro(self, e_data: Dict) -> Dict:
        """
        Análise macro - resumo + tags grossas.
        Usa chunking se transcrição for muito grande.
        """
        transcript = e_data['texto_completo']
        transcript_size = len(transcript)

        # Se for pequeno, processa direto
        if transcript_size <= 12000:
            context = self._build_context(e_data, stage="macro")
            return await asyncio.to_thread(
                self.ai.analyze,
                system_prompt=SYSTEM_PROMPTS["macro"],
                user_content=context,
                schema=MacroAnalysisSchema
            )

        # Se for grande, usa só a primeira parte + última parte (estratégia simplificada)
        print(f"    Transcrição muito grande para Macro ({transcript_size} chars) - usando amostragem")
        chunk_size = 5000  # Reduzido para evitar timeout
        inicio = transcript[:chunk_size]
        fim = transcript[-chunk_size:]

        # Cria contexto amostrado
        amostrado_data = e_data.copy()
        amostrado_data['texto_completo'] = f"""
=== INÍCIO DA TRANSCRIÇÃO (primeiros {chunk_size} chars) ===
{inicio}

...

=== FINAL DA TRANSCRIÇÃO (últimos {chunk_size} chars) ===
{fim}

NOTA: Esta é uma amostragem. Transcrição completa tem {transcript_size} caracteres.
"""

        context = self._build_context(amostrado_data, stage="macro")
        return await asyncio.to_thread(
            self.ai.analyze,
            system_prompt=SYSTEM_PROMPTS["macro"],
            user_content=context,
            schema=MacroAnalysisSchema
        )

    async def _stage2_multi_agent(self, e_data: Dict, macro_result: Dict) -> Dict:
        """
        Análise multi-agent com chunking para transcrições longas.

        Estratégia:
        1. Divide a transcrição em chunks com overlap
        2. Processa cada chunk com os 4 agents
        3. Consolida resultados (merge inteligente)
        """
        transcript = e_data['texto_completo']
        transcript_size = len(transcript)

        # Se for pequeno, processa direto (sem chunking)
        if transcript_size <= 15000:
            print(f"    Transcrição pequena ({transcript_size} chars) - processamento direto")
            return await self._process_single_chunk(e_data, macro_result)

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
        """Processa transcrição pequena sem chunking."""
        context_base = self._build_context(e_data, stage="multi_agent")
        context_base += f"\n\n=== RESULTADO ANÁLISE MACRO (ETAPA 1) ===\n{json.dumps(macro_result, ensure_ascii=False, indent=2)}"

        # Executa os 4 agents em paralelo
        tasks = []
        for agent in self.agents:
            task = self._run_agent(agent, context_base)
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        # Consolida resultados
        return {
            "dores_analysis": results[0],
            "sistemas_analysis": results[1],
            "relacoes_analysis": results[2],
            "processos_analysis": results[3],
        }

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
        print(f"      ↳ {agent_name}...", end="", flush=True)

        result = await asyncio.to_thread(
            self.ai.analyze,
            system_prompt=agent.get_system_prompt(),
            user_content=context,
            schema=agent.get_schema()
        )

        print(f" ✓", flush=True)
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
            for (e_id, _, _, _, _, _, _, _) in pending
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
