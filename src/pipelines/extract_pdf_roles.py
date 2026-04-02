"""
Extract PDF Roles Pipeline

Extrai informações de cargos de arquivos PDF e insere no banco.

Refatorado para usar:
- src.utils.pdf_reader → leitura multi-backend de PDFs
- src.utils.text_parser → limpeza de texto centralizada
- src.database.repositories → Repository pattern (DRY)
"""
import re
from pathlib import Path

from src.config import CARGOS_DIR, DB_PATH
from src.utils.pdf_reader import read_pdf
from src.utils.text_parser import clean_pdf_text, clean_section
from src.database.repositories import CargosRepository


def parse_cargo_sections(raw_text: str) -> dict:
    """
    Aplica RegEx homologadas para extrair seções vitais do PDF do cargo.

    Args:
        raw_text: Texto bruto extraído do PDF

    Returns:
        Dict com {area, desafios, responsabilidades, competencias}
    """
    # Limpa texto do PDF primeiro
    text = clean_pdf_text(raw_text)

    # 1. Área de Atuação (metadados do RH)
    area_atuacao = ""
    for pattern, label in [
        (r'Plataforma:\s*([^\n]+)', 'Plataforma'),
        (r'Diretoria:\s*([^\n]+)', 'Diretoria'),
        (r'Área:\s*([^\n]+)', 'Área')
    ]:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            area_atuacao += f"{label}: {match.group(1).strip()} | "

    # 2. Desafios do Cargo
    desafios = ""
    desafio_match = re.search(
        r'(?:3\.\s*)?DESAFIOS DO CARGO(.*?)(?:\n4\.\s*DIMENS[ÕO]ES|\n4\.\s|\n5\.\s|$)',
        text, re.IGNORECASE | re.DOTALL
    )
    if desafio_match:
        desafios = re.sub(r'\s+', ' ', desafio_match.group(1)).strip()

    # 3. Responsabilidades Principais
    responsabilidades = ""
    resp_match = re.search(
        r'(?:6\.\s*)?RESPONSABILIDADES PRINCIPAIS(.*?)(?:\n7\.\s*REQUISITOS|\n7\.\s|\n8\.\s|$)',
        text, re.IGNORECASE | re.DOTALL
    )
    if resp_match:
        responsabilidades = clean_section(resp_match.group(1), remove_compliance=True)

    # 4. Competências e Requisitos
    competencias = ""
    comp_match = re.search(
        r'(?:7\.\s*)?REQUISITOS M[ÍI]NIMOS DO CARGO(.*?)(?:\n8\.\s*REVIS[ÃA]O|$)',
        text, re.IGNORECASE | re.DOTALL
    )
    if comp_match:
        content = comp_match.group(1).strip()
        content = re.sub(r'\b\d+\.\s+', ' ', content)
        competencias = re.sub(r'\s+', ' ', content).strip()

    return {
        "area": area_atuacao.strip(" |") or "Corporativo Motiva",
        "desafios": desafios[:1200],
        "responsabilidades": responsabilidades[:2000],
        "competencias": competencias[:1200]
    }


def ingest_cargos():
    """
    Extrai informações de cargos de PDFs e insere no banco.

    Processo:
    1. Lista todos os PDFs na pasta de cargos
    2. Para cada PDF:
       - Extrai texto (pdfplumber → pymupdf → OCR)
       - Parseia seções (responsabilidades, competencias, etc)
       - Salva no banco
    """
    repo = CargosRepository(DB_PATH)
    cargo_files = list(CARGOS_DIR.rglob("*.pdf"))

    # Write truncate
    repo.delete_all()

    count = 0
    for pdf_path in cargo_files:
        filename = pdf_path.name
        titulo_cargo = filename.replace(".pdf", "")

        # 1. Extrai texto do PDF (multi-backend + OCR)
        result = read_pdf(pdf_path)
        texto_extraido = result.text

        # 2. Parseia seções
        parsed = parse_cargo_sections(texto_extraido)

        # 3. Salva no banco
        repo.insert({
            'titulo_cargo': titulo_cargo,
            'arquivo_pdf': filename,
            'texto_extraido': texto_extraido,
            'responsabilidades': parsed['responsabilidades'],
            'competencias': parsed['competencias'],
            'area_atuacao': parsed['area'],
            'desafios': parsed['desafios']
        })
        count += 1

    print(f"[SUCCESS] Ingested {count} PDF roles with structured sections.")


if __name__ == "__main__":
    ingest_cargos()
