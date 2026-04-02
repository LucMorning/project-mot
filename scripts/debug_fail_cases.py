import sqlite3
import re
from src.config import DB_PATH

def investigate():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    rows = cursor.execute("SELECT titulo_cargo, texto_extraido FROM cargos WHERE desafios = '' OR desafios IS NULL").fetchall()
    
    for row in rows:
        text = row['texto_extraido']
        # Procura qualquer coisa que se pareça com a seção 3
        m = re.search(r'([2345]\.\s*DESAFIO[S]?.*?)(?:\d+\.|$)', text, re.IGNORECASE | re.DOTALL)
        if m:
            content = m.group(1).replace('\n', ' ')
            print(f"[{row['titulo_cargo']}]: {content[:150]}")
        else:
            print(f"[{row['titulo_cargo']}]: CABEÇALHO NÃO ENCONTRADO")
    
    conn.close()

if __name__ == "__main__":
    investigate()
