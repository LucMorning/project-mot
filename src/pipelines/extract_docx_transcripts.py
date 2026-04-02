import sqlite3
import os
from pathlib import Path
from src.config import DB_PATH, TRANSCRICOES_DIR
from src.utils.file_readers import extract_text_from_docx

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def ingest_transcripts():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Busca quem tem um arquivo linkado
    cursor.execute("SELECT id, arquivo_transcricao FROM entrevistados WHERE arquivo_transcricao IS NOT NULL")
    linhas = cursor.fetchall()
    
    count = 0
    # Limpa dados se rodar de novo
    cursor.execute("DELETE FROM transcricoes")
    
    for row in linhas:
        entrevistado_id, file_name = row
        file_path = TRANSCRICOES_DIR / file_name
        
        if file_path.exists():
            text = extract_text_from_docx(file_path)
            
            # Conta paragraphs básicos e length
            num_chars = len(text)
            num_paras = len([p for p in text.split("\n") if len(p.strip()) > 5])
            
            cursor.execute("""
                INSERT INTO transcricoes (entrevistado_id, texto_completo, num_paragrafos, num_caracteres)
                VALUES (?, ?, ?, ?)
            """, (entrevistado_id, text, num_paras, num_chars))
            count += 1
            
            # Atualiza o status
            cursor.execute("UPDATE entrevistados SET status_revisao = 'em_progresso' WHERE id = ?", (entrevistado_id,))
            
    conn.commit()
    conn.close()
    
    print(f"[SUCESSO] Feita a ingestão do texto completo de {count} transcrições no SQLite.")

if __name__ == "__main__":
    ingest_transcripts()
