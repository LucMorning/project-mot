import sqlite3
import re
from pathlib import Path
from src.config import DB_PATH, CARGOS_DIR
from src.utils.file_readers import read_pdf_plumber

def clean_text(text):
    if not text: return ""
    import unidecode
    # Normalização segura de caracteres PDF quebraveis
    t = text.encode('utf-8', 'ignore').decode('utf-8')
    t = unidecode.unidecode(t)
    return t

def parse_cargo_content(raw_text):
    """
    Aplica as RegEx homologadas para extrair seções vitais do PDF do cargo.
    """
    text = clean_text(raw_text)
    
    # 1. Área de Atuação (Metadados FIXOS do RH)
    area_atuacao = ""
    plat_match = re.search(r'Plataforma:\s*([^\n]+)', text, re.IGNORECASE)
    dir_match  = re.search(r'Diretoria:\s*([^\n]+)', text, re.IGNORECASE)
    area_match = re.search(r'Área:\s*([^\n]+)' if 'Área:' in text else r'Area:\s*([^\n]+)', text, re.IGNORECASE)
    
    if plat_match: area_atuacao += f"{plat_match.group(1).strip()} | "
    if dir_match:  area_atuacao += f"{dir_match.group(1).strip()} | "
    if area_match: area_atuacao += f"{area_match.group(1).strip()}"
    
    # 2. Desafios do Cargo
    desafios = ""
    desafio_match = re.search(r'(?:3\.\s*)?DESAFIOS DO CARGO(.*?)(?:\n4\.\s*DIMENS[ÕO]ES|\n4\.\s|\n5\.\s|$)', text, re.IGNORECASE | re.DOTALL)
    if desafio_match:
        desafios = re.sub(r'\s+', ' ', desafio_match.group(1)).strip()
        
    # 3. Responsabilidades Principais (Filtra lixos de compliance e numeração PDFPlumber)
    responsabilidades = ""
    resp_match = re.search(r'(?:6\.\s*)?RESPONSABILIDADES PRINCIPAIS(.*?)(?:\n7\.\s*REQUISITOS|\n7\.\s|\n8\.\s|$)', text, re.IGNORECASE | re.DOTALL)
    if resp_match:
        content = resp_match.group(1).strip()
        # Remove cláusulas padrão de compliance / ISO / Normas
        content = re.sub(r'\d+\.\s*Este colaborador tamb[ée]m.*', '', content, flags=re.IGNORECASE | re.DOTALL)
        content = re.sub(r'Este colaborador tamb[ée]m.*', '', content, flags=re.IGNORECASE | re.DOTALL)
        content = re.sub(r'Cumprir e fazer cumprir normas.*', '', content, flags=re.IGNORECASE | re.DOTALL)
        
        # Limpa linhas vazias e números de bullets zoados
        linhas = [l for l in content.split('\n') if not re.match(r'^\d+\.\s*-\s*$', l.strip())]
        content = " ".join(linhas)
        content = re.sub(r'\b\d+\.\s+', ' ', content) # Remove numeração "1. ", "2. "
        responsabilidades = re.sub(r'\s+', ' ', content).strip()
        
    # 4. Competências e Requisitos
    competencias = ""
    comp_match = re.search(r'(?:7\.\s*)?REQUISITOS M[ÍI]NIMOS DO CARGO(.*?)(?:\n8\.\s*REVIS[ÃA]O|$)', text, re.IGNORECASE | re.DOTALL)
    if comp_match:
        content = comp_match.group(1).strip()
        # Junta tudo, removendo quebras pois o PDF é tabular/colunado
        content = re.sub(r'\b\d+\.\s+', ' ', content)
        competencias = re.sub(r'\s+', ' ', content).strip()

    return {
        "area": area_atuacao.strip(" |") or "Corporativo Motiva",
        "desafios": desafios[:1200],
        "responsabilidades": responsabilidades[:2000],
        "competencias": competencias[:1200]
    }

def ingest_cargos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cargo_files = list(CARGOS_DIR.rglob("*.pdf"))
    
    # Modo Idempotente
    cursor.execute("DELETE FROM cargos")
    
    count = 0
    for pdf_path in cargo_files:
        filename = pdf_path.name
        titulo_cargo = filename.replace(".pdf", "")
        
        # 1. Extração bruta
        texto_limpo = read_pdf_plumber(str(pdf_path))
        
        # 2. Parsing das seções
        parsed = parse_cargo_content(texto_limpo)
        
        # 3. Inserção c/ colunas novas
        cursor.execute("""
            INSERT INTO cargos (
                titulo_cargo, arquivo_pdf, texto_extraido, 
                responsabilidades, competencias, area_atuacao, desafios
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            titulo_cargo, 
            filename, 
            texto_limpo, 
            parsed["responsabilidades"],
            parsed["competencias"],
            parsed["area"],
            parsed["desafios"]
        ))
        count += 1
        
    conn.commit()
    conn.close()
    
    print(f"[SUCESSO] Ingeridos e Normalizados {count} PDFs de Cargo no DB.")

if __name__ == "__main__":
    ingest_cargos()
