import sqlite3
import difflib
from src.config import DB_PATH

def normalize_text(text):
    if not text: return ""
    import unidecode
    import re
    t = unidecode.unidecode(str(text)).lower()
    t = re.sub(r'[\(\)\[\]]', '', t)
    t = re.sub(r'[^a-zA-Z0-9\s]', ' ', t)
    return " ".join(t.split())

def map_roles_to_pdfs():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Busca nomes de todos os cargos oficiais dos PDFs
    cursor.execute("SELECT titulo_cargo, arquivo_pdf FROM cargos")
    cargos_pdfs = cursor.fetchall()
    
    # De/Para para busca: "diretor capex corporativo" -> "capex_diretor_a_capex_corporativo.pdf"
    pdf_lookup = {normalize_text(r['titulo_cargo']): r['arquivo_pdf'] for r in cargos_pdfs}
    chaves_pdf = list(pdf_lookup.keys())
    
    # Busca quem tem um cargo preenchido no Excel
    cursor.execute("SELECT id, cargo FROM entrevistados WHERE cargo IS NOT NULL AND cargo != 'Não Identificado (Arquivo Extra)'")
    pessoas = cursor.fetchall()
    
    mapped_count = 0
    
    for p in pessoas:
        cargo_excel = normalize_text(p['cargo'])
        
        # Tenta match exato ou parcial direto primeiro
        best_match = None
        for k in chaves_pdf:
            if k == cargo_excel:
                best_match = k
                break
        
        # Se não achou exato, usa biblioteca de proximidade
        if not best_match:
            matches = difflib.get_close_matches(cargo_excel, chaves_pdf, n=1, cutoff=0.7)
            if matches:
                best_match = matches[0]
                
        # Update no banco se bater legal
        if best_match:
            pdf_filename = pdf_lookup[best_match]
            cursor.execute("UPDATE entrevistados SET arquivo_cargo_pdf = ? WHERE id = ?", (pdf_filename, p['id']))
            mapped_count += 1
            
    conn.commit()
    conn.close()
    print(f"[MATCHER] Concluído! [OK] {mapped_count} entrevistados agora possuem seu PDF de cargo anexado para a análise do Gemini.")

if __name__ == "__main__":
    map_roles_to_pdfs()
