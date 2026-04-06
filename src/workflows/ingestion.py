"""
Ingestion Workflow - Estágio 1: Ingestão de dados base.

Orquestra os pipelines de ingestão na ordem correta para
construir as relações entre os dados.

Ordem de execução:
1. ingest_metadata → Entrevistados (base)
2. extract_roles → Cargos (PDFs)
3. extract_transcripts → Transcrições (DOCX)
4. ingest_systems → Sistemas TI (catálogo)
5. link_roles → Links (cargo ↔ pessoa)

Uso:
    python -m src.workflows ingest
"""
from pathlib import Path
import sys

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.workflows.ingest.ingest_metadata import ingest_master_spreadsheet
from src.workflows.ingest.extract_roles import ingest_cargos
from src.workflows.ingest.extract_transcripts import ingest_transcripts
from src.workflows.ingest.create_chunks import create_chunks
from src.workflows.ingest.ingest_systems import map_sistemas_ti_to_db
from src.workflows.ingest.link_roles import link_roles_to_interviewees


def run_ingestion(skip_existing: bool = False):
    """
    Executa o workflow completo de ingestão.

    Args:
        skip_existing: Se True, pula etapas que já têm dados no banco
    """
    print("\n" + "="*60)
    print("INGESTION WORKFLOW - Estágio 1: Dados Base")
    print("="*60 + "\n")

    # 1. Entrevistados (base - tudo depende disso)
    print("[1/6] Ingestao de metadados (Excel -> stg_entrevistados)...")
    ingest_master_spreadsheet()

    # 2. Cargos (PDFs)
    print("\n[2/6] Extracao de PDFs (Cargos -> stg_cargos)...")
    ingest_cargos()

    # 3. Transcrições (DOCX)
    print("\n[3/6] Extracao de DOCX (Transcricoes -> stg_transcricoes)...")
    ingest_transcripts()

    # 4. Chunks (divide transcrições em stg_chunks para análise IA)
    print("\n[4/6] Criacao de chunks (stg_transcricoes -> stg_chunks)...")
    create_chunks()

    # 5. Sistemas TI (catálogo)
    print("\n[5/6] Ingestao de catalogo de Sistemas TI (dim_sistemas)...")
    map_sistemas_ti_to_db()

    # 6. Links (cargo <-> pessoa)
    print("\n[6/6] Linkagem de stg_entrevistados <-> stg_cargos...")
    link_roles_to_interviewees()

    print("\n" + "="*60)
    print("INGESTION WORKFLOW - Concluido!")
    print("="*60 + "\n")


def main():
    """Entry point para Poetry scripts."""
    import argparse

    parser = argparse.ArgumentParser(description="Workflow de ingestão de dados MOTIVA")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Pula etapas que já têm dados")

    args = parser.parse_args()
    run_ingestion(skip_existing=args.skip_existing)


if __name__ == "__main__":
    main()
