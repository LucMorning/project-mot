"""
AI Analysis Workflow - Estágio 2: Análise com IA.

Orquestra os pipelines de análise com IA.

Opções disponíveis:
- batch: Processamento em lote de chunks (robusto, produção)
- staged: Multi-stage com 3 etapas (macro → multi-agent → cruzamento)

Uso:
    python -m src.workflows ai --mode batch
    python -m src.workflows ai --mode staged
"""
from pathlib import Path
import sys
import argparse

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import condicional para evitar erros se Gemini não estiver configurado
try:
    from src.workflows.analyze.batch import run_batch_pipeline
    AI_BATCH_AVAILABLE = True
except Exception as e:
    AI_BATCH_AVAILABLE = False
    BATCH_ERROR = str(e)

try:
    from src.workflows.analyze.staged import MultiStageAnalysisPipeline, GeminiProvider, DatabaseService
    AI_STAGED_AVAILABLE = True
except Exception as e:
    AI_STAGED_AVAILABLE = False
    STAGED_ERROR = str(e)


def run_ai_batch():
    """Executa o pipeline batch de IA."""
    if not AI_BATCH_AVAILABLE:
        print(f"[ERRO] Pipeline batch não disponível: {BATCH_ERROR}")
        return False

    print("\n" + "="*60)
    print("AI WORKFLOW - Modo: BATCH (Produção)")
    print("="*60 + "\n")

    import asyncio
    asyncio.run(run_batch_pipeline())

    return True


def run_ai_staged():
    """Executa o pipeline staged de IA (3 etapas)."""
    if not AI_STAGED_AVAILABLE:
        print(f"[ERRO] Pipeline staged não disponível: {STAGED_ERROR}")
        return False

    print("\n" + "="*60)
    print("AI WORKFLOW - Modo: STAGED (3 Etapas)")
    print("="*60 + "\n")

    import asyncio
    import os
    import dotenv
    from src.config import DB_PATH, AI_MODEL

    dotenv.load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[ERRO] GEMINI_API_KEY não configurada!")
        return False

    model_name = os.getenv("GEMINI_MODEL", AI_MODEL)
    batch_size = int(os.getenv("BATCH_SIZE", "3"))

    provider = GeminiProvider(api_key=api_key, model_name=model_name)
    db = DatabaseService(DB_PATH)
    pipeline = MultiStageAnalysisPipeline(
        ai_provider=provider,
        db_service=db,
        model_name=model_name
    )

    # Loop de processamento
    while True:
        pending = db.get_pending_transcripts(limit=batch_size)
        if not pending:
            print("\n[PIPELINE] Todas as transcrições foram processadas!")
            break

        asyncio.run(pipeline.run_batch(batch_size=batch_size))

    return True


def run_ai_analysis(mode: str = "batch"):
    """
    Executa o workflow de análise com IA.

    Args:
        mode: 'batch' ou 'staged'
    """
    print(f"\n[INFO] Modo selecionado: {mode.upper()}")

    if mode == "batch":
        return run_ai_batch()
    elif mode == "staged":
        return run_ai_staged()
    else:
        print(f"[ERRO] Modo inválido: {mode}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Workflow de análise com IA - MOTIVA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python -m src.workflows ai --mode batch
  python -m src.workflows ai --mode staged
        """
    )

    parser.add_argument(
        "--mode",
        choices=["batch", "staged"],
        default="batch",
        help="Modo de execução (default: batch)"
    )

    args = parser.parse_args()
    run_ai_analysis(mode=args.mode)
