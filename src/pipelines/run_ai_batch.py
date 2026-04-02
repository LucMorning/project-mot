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
from src.pipelines.agents import get_all_agents
from src.database.repositories import (
    InsightsRepository, SistemasUsoRepository, RelacoesRepository
)

warnings.filterwarnings('ignore', category=FutureWarning)

# Configurações de escala blindada
BATCH_SIZE = 5
BATCH_SLEEP = 30
MODEL_NAME = "gemini-1.5-flash"
ERROR_THRESHOLD = 3

# Contador de erros consecutivos
consecutive_errors = 0


# ─────────────────────────────────────────────────────────────
# IA PROVIDER
# ─────────────────────────────────────────────────────────────

class GeminiProvider:
    def __init__(self, api_key: str, model_name: str = MODEL_NAME):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def analyze(self, system_prompt: str, user_content: str, schema) -> Dict[str, Any]:
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_content,
                config={
                    'system_instruction': system_prompt,
                    'response_mime_type': 'application/json',
                    'response_schema': schema,
                    'temperature': 0.1
                }
            )
            
            # O novo SDK retorna o objeto já parseado ou acessível via .parsed
            if hasattr(response, 'parsed') and response.parsed:
                # Converte o objeto Pydantic retornado em dicionário
                return response.parsed.model_dump() if hasattr(response.parsed, 'model_dump') else response.parsed
                
            return json.loads(response.text)
        except Exception as e:
            print(f"[ERRO] Novo SDK Gemini: {e}")
            raise e


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
    ai: GeminiProvider
) -> bool:
    """
    Processa um único chunk com os 4 agentes.

    Returns:
        True se processou com sucesso, False caso contrário
    """
    global consecutive_errors

    agents = get_all_agents()
    contexto = f"CONTEXTO MESTRE:\n{glossary}\n\nENTREVISTADO: {metadata['nome']} ({metadata['cargo']})\nFALA:\n{content}"

    results = []
    has_data = False

    for agent in agents:
        try:
            res = await asyncio.to_thread(
                ai.analyze,
                agent.get_system_prompt(),
                contexto,
                agent.get_schema()
            )
            if res and any(res.get(k) for k in res.keys()):
                results.append(res)
                has_data = True
            else:
                results.append({})
            await asyncio.sleep(2)  # Rate limiting entre agentes
        except Exception as e:
            print(f"      [ERRO AGENTE {agent.get_name()}]: {e}")
            results.append({})
            if "429" in str(e):  # Rate limit
                consecutive_errors += 1

    if has_data and len(results) == 4:
        save_successful_results(entrevistado_id, chunk_id, results)
        consecutive_errors = 0
        return True

    return False


def save_successful_results(
    entrevistado_id: int,
    chunk_id: int,
    results_list: List[Dict]
) -> None:
    """
    Salva resultados dos 4 agentes usando repositories.

    Aplica DRY: SQL não se repite, usa repositories.
    """
    insights_repo = InsightsRepository(DB_PATH)
    sistemas_repo = SistemasUsoRepository(DB_PATH)
    relacoes_repo = RelacoesRepository(DB_PATH)

    try:
        # 1. Dores
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

        # 2. Sistemas
        sistemas = results_list[1].get("sistemas", [])
        for sis in sistemas:
            sistemas_repo.insert({
                'id_entrevistado': entrevistado_id,
                'id_bloco': chunk_id,
                'sistema': sis.get("nome_sistema"),
                'como_usa': f"{sis.get('finalidade')} {sis.get('forma_uso')}",
                'etapa_cadeia': sis.get("etapa_cadeia"),
                'satisfacao': sis.get("satisfacao"),
                'workaround': sis.get("problema_principal")
            })

        # 3. Relações
        relacoes = results_list[2].get("relacoes", [])
        for rel in relacoes:
            relacoes_repo.insert({
                'id_entrevistado': entrevistado_id,
                'id_bloco': chunk_id,
                'tipo': rel.get("tipo"),
                'pessoa_ou_area': rel.get("contraparte"),
                'contexto': rel.get("contexto")
            })

        # 4. Processos (como insights)
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

        # Marca chunk como processado
        import sqlite3
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE transcricao_chunks SET status_analise = 'concluido' WHERE id = ?",
            (chunk_id,)
        )
        conn.commit()
        conn.close()

        print(f"      [SALVO] Chunk {chunk_id} - {len(dores)} dores, {len(sistemas)} sistemas")

    except Exception as e:
        print(f"      [ERRO PERSISTÊNCIA]: {e}")


# ─────────────────────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────────────────────

async def run_batch_pipeline():
    """
    Executa o pipeline batch em lotes com tratamento de erros.

    Processa chunks pendentes em batches com rate limiting entre batches.
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

    # Busca chunks pendentes
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
        SELECT c.id, c.conteudo, e.id as ent_id, e.nome, e.cargo
        FROM transcricao_chunks c
        JOIN transcricoes t ON c.id_transcricao = t.id
        JOIN entrevistados e ON t.id_entrevistado = e.id
        WHERE c.status_analise = 'pendente'
        ORDER BY e.id, c.ordem
    """
    cursor.execute(query)
    chunks = cursor.fetchall()
    conn.close()

    if not chunks:
        print("[INFO] Nenhum chunk pendente para processar.")
        return

    print(f"\n{'='*60}")
    print(f"[BATCH PIPELINE] {len(chunks)} chunks pendentes")
    print(f"{'='*60}")
    print(f"Modelo: {MODEL_NAME}")
    print(f"Batch Size: {BATCH_SIZE}")
    print(f"Sleep entre batches: {BATCH_SLEEP}s")
    print(f"{'='*60}\n")

    for i in range(0, len(chunks), BATCH_SIZE):
        if consecutive_errors >= ERROR_THRESHOLD:
            print(f"\n[PARADA] Muitos erros consecutivos ({consecutive_errors})")
            break

        batch = chunks[i:i + BATCH_SIZE]
        print(f"\n[BATCH {i//BATCH_SIZE + 1}] Processando {len(batch)} chunks...")

        tasks = [
            process_one_chunk(
                c["id"], c["ent_id"], c["conteudo"],
                {"nome": c["nome"], "cargo": c["cargo"]},
                glossary, ai
            )
            for c in batch
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)
        success = sum(1 for r in results if r is True)
        errors = sum(1 for r in results if r is not True)

        print(f"  Resultado: {success} sucessos, {errors} erros")

        if i + BATCH_SIZE < len(chunks):
            print(f"  Aguardando {BATCH_SLEEP}s antes do próximo batch...")
            await asyncio.sleep(BATCH_SLEEP)

    print(f"\n{'='*60}")
    print(f"[BATCH PIPELINE] Concluído")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    asyncio.run(run_batch_pipeline())
