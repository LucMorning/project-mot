"""
MOTIVA Workflows - Entry point para execução de workflows.

Uso:
    python -m src.workflows ingest
    python -m src.workflows ai --mode batch
    python -m src.workflows ai --mode staged
    python -m src.workflows reports --format markdown
"""
import sys
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.workflows.ingestion import run_ingestion
from src.workflows.ai_analysis import run_ai_analysis
from src.workflows.reports import run_reports


def main():
    """Entry point para execução de workflows."""
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python -m src.workflows ingest")
        print("  python -m src.workflows ai --mode batch")
        print("  python -m src.workflows ai --mode staged")
        print("  python -m src.workflows reports --format markdown")
        sys.exit(1)

    command = sys.argv[1]

    if command == "ingest":
        run_ingestion()
    elif command == "ai":
        # Pega o modo (batch ou staged)
        mode = "batch"
        if "--mode" in sys.argv:
            idx = sys.argv.index("--mode")
            if idx + 1 < len(sys.argv):
                mode = sys.argv[idx + 1]

        run_ai_analysis(mode=mode)
    elif command == "reports":
        # Pega o formato (markdown ou pptx)
        format = "markdown"
        if "--format" in sys.argv:
            idx = sys.argv.index("--format")
            if idx + 1 < len(sys.argv):
                format = sys.argv[idx + 1]

        run_reports(format=format)
    else:
        print(f"Comando desconhecido: {command}")
        print("Comandos disponíveis: ingest, ai, reports")
        sys.exit(1)


if __name__ == "__main__":
    main()
