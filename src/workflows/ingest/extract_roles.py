"""
Extract PDF Roles Pipeline

Extrai informações de cargos de arquivos PDF e insere no banco.

Refatorado para usar:
- src.utils.pdf_reader → leitura multi-backend de PDFs
- src.utils.text_parser → limpeza de texto centralizada
- src.database.repositories → Repository pattern (DRY)
"""
import re
import json
from pathlib import Path

from src.config import CARGOS_DIR, DB_PATH
from src.utils.pdf_reader import read_pdf
from src.utils.text_parser import clean_pdf_text, clean_section
from src.database.repositories import CargosRepository


def extract_responsabilidades_as_array(text: str) -> str:
    """
    Extrai responsabilidades como array JSON.

    O PDF tem formato: "1.\n texto da responsabilidade\n 2.\n ..."
    Precisamos capturar cada item numerado e juntar o texto quebrado.
    """
    # Encontra seção de responsabilidades
    match = re.search(
        r'(?:6\.\s*)?RESPONSABILIDADES PRINCIPAIS(.*?)(?:\n7\.\s*REQUISITOS|\n7\.\s|\n8\.\s|$)',
        text, re.IGNORECASE | re.DOTALL
    )
    if not match:
        return "[]"

    content = match.group(1)

    # Remove o bloco de compliance se existir
    compliance_match = re.search(
        r'Este colaborador tamb.m.*?(?:\n\d+\.|$)',
        content, re.IGNORECASE | re.DOTALL
    )
    if compliance_match:
        content = content[:compliance_match.start()] + content[compliance_match.end():]

    # Extrai itens numerados (1., 2., 3., etc)
    # O texto pode estar quebrado: "1.\n texto" ou "texto\n 2."
    responsabilidades = []

    # Divide por numeracao
    items = re.split(r'\n\s*(\d+)\.\s*', content)

    current_item = ""
    for i, part in enumerate(items):
        part = part.strip()
        if not part:
            continue

        # Se for apenas um numero, e o proximo tem conteudo
        if re.match(r'^\d+$', part) and i + 1 < len(items):
            continue

        # Se o comeco for letra maiuscula (inicio de frase)
        if part and part[0].isupper():
            if current_item and current_item != "-":
                responsabilidades.append(current_item.strip())
            current_item = part
        else:
            # Continuacao do item anterior
            current_item += " " + part

    # Adiciona ultimo item
    if current_item and current_item.strip() != "-":
        responsabilidades.append(current_item.strip())

    # Limpa itens vazios ou apenas com "-"
    responsabilidades = [r for r in responsabilidades if r and r.strip() != "-"]

    return json.dumps(responsabilidades, ensure_ascii=False)


def extract_requisitos_minimos(text: str) -> dict:
    """
    Extrai campos da seção 7 - Requisitos Mínimos do Cargo.

    Returns:
        Dict com {formacao, idiomas, experiencia}
    """
    match = re.search(
        r'(?:7\.\s*)?REQUISITOS M[ÍI]NIMOS DO CARGO(.*?)(?:\n8\.\s*REVIS[ÃA]O|$)',
        text, re.IGNORECASE | re.DOTALL
    )
    if not match:
        return {
            "formacao": "",
            "idiomas": "[]",
            "experiencia": ""
        }

    content = match.group(1)

    # Extrai Formação - padrão: "Formação <valor>\n Área"
    formacao = ""
    formacao_match = re.search(r'Forma..o\s+(.+?)\s*[Aa]rea', content, re.IGNORECASE)
    if formacao_match:
        formacao = formacao_match.group(1).strip()

    # Extrai Idiomas (pode ter mais de um)
    idiomas = []
    idioma_pattern = r'Idioma\s*[:\s]*([A-Za-z\u00C0-\u00FF\s\-]+?)\s*N[ií]vel\s*[:\s]*([^\n]+)'
    for idioma_match in re.finditer(idioma_pattern, content, re.IGNORECASE):
        idioma = idioma_match.group(1).strip()
        nivel = idioma_match.group(2).strip()
        if idioma and idioma.strip() != "-" and idioma.strip():
            idiomas.append({"idioma": idioma, "nivel": nivel})

    # Extrai Experiência
    experiencia = ""
    exp_match = re.search(
        r'Experi[êe]ncia\s*[:\s]+(.+?)(?:\n8\.|8\.|$)',
        content, re.IGNORECASE
    )
    if exp_match:
        experiencia = exp_match.group(1).strip()

    return {
        "formacao": formacao,
        "idiomas": json.dumps(idiomas, ensure_ascii=False),
        "experiencia": experiencia
    }


def parse_cargo_sections(raw_text: str) -> dict:
    """
    Aplica RegEx homologadas para extrair seções vitais do PDF do cargo.

    Args:
        raw_text: Texto bruto extraído do PDF

    Returns:
        Dict com campos estruturados do cargo
    """
    # Limpa texto do PDF primeiro
    text = clean_pdf_text(raw_text)

    # 1. Metadados de Identificação (seção 1) - NORMALIZAR PARA UPPERCASE
    negocio_plataforma = ""
    diretoria = ""
    area_atuacao = ""

    match = re.search(r'Neg[óo]cio/Plataforma:\s*([^\n]+)', text, re.IGNORECASE)
    if match:
        negocio_plataforma = match.group(1).strip().upper()

    match = re.search(r'Diretoria:\s*([^\n]+)', text, re.IGNORECASE)
    if match:
        diretoria = match.group(1).strip().upper()

    match = re.search(r'[Aa]rea:\s*([^\n]+)', text, re.IGNORECASE)
    if match:
        area_atuacao = match.group(1).strip().upper()

    # 2. Missão do Cargo (seção 2)
    missao = ""
    missao_match = re.search(
        r'(?:2\.\s*)?MISS[ÃA]O DO CARGO(.*?)(?:\n3\.\s*DESAFIOS|\n3\.\s|$)',
        text, re.IGNORECASE | re.DOTALL
    )
    if missao_match:
        missao = re.sub(r'\s+', ' ', missao_match.group(1)).strip()

    # 3. Desafios do Cargo (seção 3)
    desafios = ""
    desafio_match = re.search(
        r'(?:3\.\s*)?DESAFIOS DO CARGO(.*?)(?:\n4\.\s*DIMENS[ÕO]ES|\n4\.\s|\n5\.\s|$)',
        text, re.IGNORECASE | re.DOTALL
    )
    if desafio_match:
        desafios = re.sub(r'\s+', ' ', desafio_match.group(1)).strip()

    # 4. Responsabilidades Principais (seção 6) - COMO ARRAY JSON
    responsabilidades = extract_responsabilidades_as_array(text)

    # 5. Requisitos Mínimos (seção 7)
    requisitos = extract_requisitos_minimos(text)

    return {
        "negocio_plataforma": negocio_plataforma or "CORPORATIVO MOTIVA",
        "diretoria": diretoria,
        "area_atuacao": area_atuacao,
        "missao": missao[:1500],
        "desafios": desafios[:1500],
        "responsabilidades": responsabilidades,
        "formacao": requisitos["formacao"],
        "idiomas": requisitos["idiomas"],
        "experiencia": requisitos["experiencia"]
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
            'negocio_plataforma': parsed['negocio_plataforma'],
            'diretoria': parsed['diretoria'],
            'area_atuacao': parsed['area_atuacao'],
            'missao': parsed['missao'],
            'desafios': parsed['desafios'],
            'responsabilidades': parsed['responsabilidades'],
            'formacao': parsed['formacao'],
            'idiomas': parsed['idiomas'],
            'experiencia': parsed['experiencia']
        })
        count += 1

    print(f"[SUCCESS] Ingested {count} PDF roles with structured sections.")


if __name__ == "__main__":
    ingest_cargos()
