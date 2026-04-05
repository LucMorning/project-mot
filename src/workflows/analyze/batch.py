"""
Batch AI Pipeline - Processa chunks em lote com glossário integrado.

Pipeline robusto testado em produção para processamento massivo de
transcrições com tratamento de erros e rate limiting.

Refatorado para usar:
- src.database.repositories → Repository pattern (DRY)
- src.pipelines.agents → Multi-agent system
"""
import asyncio
import os
import json
from typing import Dict, Any, List

from google import genai
import warnings
import dotenv

from src.config import DB_PATH
from src.agents import get_all_agents
from src.database.repositories import (
    InsightsRepository, SistemasUsoRepository, RelacoesRepository, ChunksRepository
)
from src.providers.gemini_provider import GeminiProvider

warnings.filterwarnings('ignore', category=FutureWarning)

# Configurações de escala blindada


# ─────────────────────────────────────────────────────────────
# AGENT ORCHESTRATOR - Filtro Inteligente
# ─────────────────────────────────────────────────────────────

class AgentOrchestrator:
    """
    Decide quais agents executar para cada chunk baseado em keywords.

    Economiza chamadas à API pulando agents irrelevantes.
    """

    def analyze_chunk(self, chunk_text: str) -> List[str]:
        """
        Retorna quais agents executar para este chunk.

        Args:
            chunk_text: Texto do chunk a analisar

        Returns:
            Lista de nomes de agents a executar (ex: ['dores', 'sistemas'])
        """
        chunk_lower = chunk_text.lower()

        # Busca keywords de cada agent
        needed = []

        for agent in get_all_agents():
            keywords = agent.get_keywords()
            if any(kw in chunk_lower for kw in keywords):
                needed.append(agent.get_name())

        # Sempre executa pelo menos 1 (pain_points como fallback)
        return needed if needed else ['pain_points']


# ─────────────────────────────────────────────────────────────
# GLOSSARY BUILDER
# ─────────────────────────────────────────────────────────────

def build_integrated_glossary() -> str:
    """Monta glossário integrado com sistemas e cargos do banco."""
    import sqlite3

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Sistemas oficiais
    cursor.execute("SELECT nome, etapa_processo FROM sistemas_ti")
    sistemas = [f"{r[0]} ({r[1]})" for r in cursor.fetchall()]

    # Cargos do ecossistema
    cursor.execute("SELECT DISTINCT cargo FROM entrevistados WHERE cargo IS NOT NULL")
    cargos = [r[0] for r in cursor.fetchall()]

    conn.close()

    return f"SISTEMAS OFICIAIS: {', '.join(sistemas)}\nCARGOS: {', '.join(cargos[:30])}"


# ─────────────────────────────────────────────────────────────
# CHUNK PROCESSOR
# ─────────────────────────────────────────────────────────────

async def process_one_chunk(
    chunk_id: int,
    entrevistado_id: int,
    content: str,
    metadata: Dict,
    glossary: str,
    ai: GeminiProvider,
    orchestrator: AgentOrchestrator = None
) -> bool:
    """
    Processa um único chunk com os agentes selecionados pelo Orchestrator.

    Args:
        orchestrator: Se fornecido, filtra quais agents executar. Se None, executa todos.

    Returns:
        True se processou com sucesso, False caso contrário
    """
    global consecutive_errors

    # Orchestrator decide quais agents executar
    if orchestrator:
        agents_to_run = orchestrator.analyze_chunk(content)
        agents_list = [a for a in get_all_agents() if a.get_name() in agents_to_run]
        print(f"      [ORCHESTRATOR] Agents: {agents_to_run} ({len(agents_list)}/{len(get_all_agents())})")
    else:
        agents_list = get_all_agents()

    contexto = f"CONTEXTO MESTRE:\n{glossary}\n\nENTREVISTADO: {metadata['nome']} ({metadata['cargo']})\nFALA:\n{content}"

    # Mapeia results por agent name
    results_map = {}

    for agent in agents_list:
        agent_name = agent.get_name()
        try:
            res = await asyncio.to_thread(
                ai.analyze,
                agent.get_system_prompt(),
                contexto,
                agent.get_schema()
            )
            results_map[agent_name] = res
            await asyncio.sleep(2)  # Rate limiting entre agentes
        except Exception as e:
            print(f"      [ERRO AGENTE {agent_name}]: {e}")
            results_map[agent_name] = {}
            if "429" in str(e):  # Rate limit
                consecutive_errors += 1

    # Converte para lista ordenado (pain_points, systems, relations, processes)
    ordered_names = ['pain_points', 'systems', 'relations', 'processes']
    results_list = [results_map.get(name, {}) for name in ordered_names]

    has_data = any(results_list)

    if has_data:
        save_successful_results(entrevistado_id, chunk_id, results_list)
        consecutive_errors = 0
        return True

    return False


def save_successful_results(
    entrevistado_id: int,
    chunk_id: int,
    results_list: List[Dict]
) -> None:
    """
    Salva resultados dos 4 agentes usando repositories com UPSERT.

    - Sistemas: consolida por (entrevistado, sistema) evitando duplicatas
    - Relações: filtra "N/A" e consolida por (entrevistado, pessoa_citada)
    - Insights: mantém por chunk (cada dor é única)
    """
    insights_repo = InsightsRepository(DB_PATH)
    sistemas_repo = SistemasUsoRepository(DB_PATH)
    relacoes_repo = RelacoesRepository(DB_PATH)

    try:
        # 1. Dores (mantém insert - cada insight é único)
        dores = results_list[0].get("dores", [])
        for dor in dores:
            insights_repo.insert({
                'id_entrevistado': entrevistado_id,
                'id_bloco': chunk_id,
                'etapa_cadeia': dor.get("etapa_cadeia_valor"),
                'categoria': 'Dor',
                'subcategoria': dor.get("subcategoria"),
                'descricao': dor.get("descricao"),
                'citacao_direta': dor.get("citacao_direta"),
                'sistemas_envolvidos': dor.get("sistemas_envolvidos", []),
                'severidade': dor.get("impacto"),
                'confianca': dor.get("confianca", 0.9),
                'modelo_ia': MODEL_NAME
            })

        # 2. Sistemas (UPSERT - consolida por entrevistado + sistema)
        sistemas = results_list[1].get("sistemas", [])
        sistemas_upserted = 0
        for sis in sistemas:
            result_id = sistemas_repo.upsert({
                'id_entrevistado': entrevistado_id,
                'id_bloco': chunk_id,
                'sistema': sis.get("nome_sistema"),
                'como_usa': f"{sis.get('finalidade')} {sis.get('forma_uso')}",
                'etapa_cadeia': sis.get("etapa_cadeia"),
                'satisfacao': sis.get("satisfacao"),
                'workaround': sis.get("problema_principal")
            })
            if result_id:
                sistemas_upserted += 1

        # 3. Relações (UPSERT - consolida por pessoa, filtra N/A)
        _INVALID_NAMES = {'N/A', 'NÃO INFORMADO', 'NA', 'NONE', ''}
        relacoes = results_list[2].get("relacoes", [])
        relacoes_upserted = 0
        for rel in relacoes:
            pessoa = (rel.get("pessoa_citada") or '').strip().upper()
            if pessoa in _INVALID_NAMES:
                continue
            result_id = relacoes_repo.upsert({
                'id_entrevistado': entrevistado_id,
                'id_bloco': chunk_id,
                'tipo': rel.get("tipo"),
                'pessoa_citada': rel.get("pessoa_citada"),
                'area_citada': rel.get("area_citada"),
                'contexto': rel.get("contexto")
            })
            if result_id:
                relacoes_upserted += 1

        # 4. Processos (mantém insert - cada fluxo é único)
        processos = results_list[3].get("fluxos", [])
        for fluxo in processos:
            insights_repo.insert({
                'id_entrevistado': entrevistado_id,
                'id_bloco': chunk_id,
                'categoria': 'Processo',
                'subcategoria': 'Fluxo',
                'descricao': fluxo.get("descricao"),
                'citacao_direta': f"Rupturas: {', '.join(fluxo.get('rupturas', []))}",
                'sistemas_envolvidos': [],
                'severidade': 'Media',
                'confianca': 0.95,
                'modelo_ia': MODEL_NAME
            })

        # Marca chunk como processado via repository
        ChunksRepository(DB_PATH).mark_done(chunk_id)

        print(f"      [SALVO] Chunk {chunk_id} - {len(dores)} dores, {sistemas_upserted} sist. (upsert), {relacoes_upserted} rel. (upsert, N/A filtrados)")

    except Exception as e:
        print(f"      [ERRO PERSISTÊNCIA]: {e}")


# ─────────────────────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────────────────────

async def run_batch_pipeline():
    """
    Executa o pipeline batch em lotes com tratamento de erros.

    Processa chunks de 5 entrevistados por vez com rate limiting entre batches.
    Para se houver muitos erros consecutivos (429 rate limit).
    """
    global consecutive_errors

    dotenv.load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("[ERRO] GEMINI_API_KEY não configurada!")
        return

    ai = GeminiProvider(api_key=api_key)
    glossary = build_integrated_glossary()
    orchestrator = AgentOrchestrator()  # Filtro inteligente

    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print(f"\n{'='*60}")
    print(f"[BATCH PIPELINE] Modo: 5 entrevistados por vez")
    print(f"{'='*60}")
    print(f"Modelo: {MODEL_NAME}")
    print(f"Batch Size: {BATCH_SIZE}")
    print(f"Sleep entre batches: {BATCH_SLEEP}s")
    print(f"{'='*60}\n")

    # Loop: processa 5 entrevistados por vez
    round_num = 0
    while True:
        if consecutive_errors >= ERROR_THRESHOLD:
            print(f"\n[PARADA] Muitos erros consecutivos ({consecutive_errors})")
            break

        # Busca IDs de 5 entrevistados com chunks pendentes
        cursor.execute("""
            SELECT DISTINCT e.id, e.nome
            FROM transcricao_chunks c
            JOIN transcricoes t ON c.id_transcricao = t.id
            JOIN entrevistados e ON t.id_entrevistado = e.id
            WHERE c.status_analise = 'pendente'
            ORDER BY e.id
            LIMIT 5
        """)
        entrevistados = cursor.fetchall()

        if not entrevistados:
            print("\n[INFO] Todos os chunks foram processados!")
            break

        round_num += 1
        ent_ids = [e["id"] for e in entrevistados]
        ent_nomes = [e["nome"] for e in entrevistados]

        print(f"\n[RODADA {round_num}] Entrevistados: {ent_nomes}")
        print(f"  IDs: {ent_ids}")

        # Busca chunks desses entrevistados
        query = """
            SELECT c.id, c.conteudo, e.id as ent_id, e.nome, e.cargo
            FROM transcricao_chunks c
            JOIN transcricoes t ON c.id_transcricao = t.id
            JOIN entrevistados e ON t.id_entrevistado = e.id
            WHERE c.status_analise = 'pendente'
            AND e.id IN ({})
            ORDER BY e.id, c.ordem
        """.format(','.join(map(str, ent_ids)))
        cursor.execute(query)
        chunks = cursor.fetchall()

        if not chunks:
            print(f"  [AVISO] Nenhum chunk pendente encontrado para esses entrevistados")
            continue

        print(f"  Chunks para processar: {len(chunks)}")

        # Processa em batches
        for i in range(0, len(chunks), BATCH_SIZE):
            if consecutive_errors >= ERROR_THRESHOLD:
                print(f"\n[PARADA] Muitos erros consecutivos ({consecutive_errors})")
                break

            batch = chunks[i:i + BATCH_SIZE]
            print(f"\n  [BATCH {i//BATCH_SIZE + 1}] Processando {len(batch)} chunks...")

            tasks = [
                process_one_chunk(
                    c["id"], c["ent_id"], c["conteudo"],
                    {"nome": c["nome"], "cargo": c["cargo"]},
                    glossary, ai, orchestrator
                )
                for c in batch
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)
            success = sum(1 for r in results if r is True)
            errors = sum(1 for r in results if r is not True)

            print(f"    Resultado: {success} sucessos, {errors} erros")

            if i + BATCH_SIZE < len(chunks):
                print(f"    Aguardando {BATCH_SLEEP}s...")
                await asyncio.sleep(BATCH_SLEEP)

        if consecutive_errors >= ERROR_THRESHOLD:
            break

    conn.close()

    print(f"\n{'='*60}")
    print(f"[BATCH PIPELINE] Concluído após {round_num} rodadas")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    asyncio.run(run_batch_pipeline())
