"""
Reports Workflow - Gera relatórios markdown/pptx.

Uso:
    python -m src.workflows reports --format markdown
    python -m src.workflows reports --format pptx
"""
from pathlib import Path
import sys
import argparse

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.workflows.generate.markdown_reports import generate_all_markdowns
from src.workflows.generate.excel_reports import generate_excel_report
from src.config import FICHAS_DIR, PPTX_OUTPUT_DIR


def run_reports(format: str = "markdown"):
    """
    Executa a geração de relatórios.

    Args:
        format: 'markdown', 'excel' ou 'pptx'
    """
    print("\n" + "="*60)
    print(f"REPORTS WORKFLOW - Format: {format.upper()}")
    print("="*60 + "\n")

    if format == "markdown":
        count = generate_all_markdowns(output_dir=FICHAS_DIR)
        print(f"\n[DONE] {count} relatórios markdown gerados em {FICHAS_DIR}")

    elif format == "excel":
        path = generate_excel_report()
        print(f"\n[DONE] Relatório Excel gerado: {path}")

    elif format == "pptx":
        print("[INFO] Geração de PPTX ainda não implementada.")
        print("[INFO] Use --format excel ou --format markdown por enquanto.")
        return False

    return True


def main():
    """Entry point para Poetry scripts."""
    parser = argparse.ArgumentParser(
        description="Workflow de geração de relatórios - MOTIVA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  poetry run reports --format markdown
  poetry run reports --format excel
  poetry run reports --format pptx
        """
    )

    parser.add_argument(
        "--format",
        choices=["markdown", "excel", "pptx"],
        default="markdown",
        help="Formato de saída (default: markdown)"
    )

    args = parser.parse_args()
    run_reports(format=args.format)


if __name__ == "__main__":
    main()
