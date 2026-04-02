import sqlite3
import os
from pathlib import Path
from src.config import DB_PATH, CARGOS_DIR
from src.utils.file_readers import read_pdf_plumber

def slugify(text: str) -> str:
    from unidecode import unidecode
    import re
    text = unidecode(text).lower()
    text = re.sub(r'[\(\)\[\]]', '', text)
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')

def ingest_cargos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cargo_files = list(CARGOS_DIR.rglob("*.pdf"))
    
    # Limpa tabela para modo idempotente
    cursor.execute("DELETE FROM cargos")
    
    count = 0
    for pdf_path in cargo_files:
        filename = pdf_path.name
        
        # O nome do arquivo costuma ser o próprio titulo do cargo
        titulo_cargo = filename.replace(".pdf", "")
        
        # Extrai o texto limpo, isso demora um pouquinho
        texto_limpo = read_pdf_plumber(str(pdf_path))
        
        # Insere no DB
        cursor.execute("""
            INSERT INTO cargos (titulo_cargo, arquivo_pdf, texto_extraido)
            VALUES (?, ?, ?)
        """, (titulo_cargo, filename, texto_limpo))
        count += 1
        
    conn.commit()
    conn.close()
    
    print(f"[SUCESSO] Feita a extração e ingestão do texto de {count} PDFs de Cargo.")

if __name__ == "__main__":
    ingest_cargos()
