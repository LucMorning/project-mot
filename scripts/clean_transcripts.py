import sqlite3
import re
from src.config import DB_PATH

def clean_transcript_text(text):
    if not text: return ""
    # Padrão: Nome da Pessoa   MM:SS ou HH:MM:SS
    # 1. Remove timestamps no meio de nomes: "Pessoa   0:05" ou "1:23:45"
    # Procura por 2 ou mais espaços seguidos de dígitos:dígitos:dígitos ou dígitos:Double-digits
    text = re.sub(r'\s{2,}\d{1,2}:\d{2}', ' ', text) # Remove "   0:05"
    text = re.sub(r'\s{2,}\d{1,2}:\d{2}:\d{2}', ' ', text) # Remove "   1:05:05"
    
    # 2. Remove timestamps isolados no início de frase ou sozinhos: "0:09Beleza" -> "Beleza"
    text = re.sub(r'\b\d{1,2}:\d{2}(?=[A-Z])', ' ', text)
    
    # 3. Remove marcas do tipo "54m 18s" do cabeçalho
    text = re.sub(r'\d+m\s+\d+s', '', text)
    
    # 4. Remove o lixo inicial de logs de quem começou a transcrição
    text = re.sub(r'.*começou a transcrição', '', text, flags=re.IGNORECASE)
    
    # 5. Normaliza excesso de espaços
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def run_cleaning_pipeline():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Adiciona a coluna se ainda não existir (segurança extra)
    try:
        cursor.execute("ALTER TABLE transcricoes ADD COLUMN texto_limpo TEXT")
    except:
        pass # Coluna já existe
        
    cursor.execute("SELECT id, texto_completo FROM transcricoes")
    rows = cursor.fetchall()
    
    count = 0
    for row_id, full_text in rows:
        clean_text = clean_transcript_text(full_text)
        cursor.execute("UPDATE transcricoes SET texto_limpo = ? WHERE id = ?", (clean_text, row_id))
        count += 1
        
    conn.commit()
    conn.close()
    print(f"[SUCCESS] Limpeza concluída! {count} transcrições purificadas com sucesso.")

if __name__ == "__main__":
    run_cleaning_pipeline()
