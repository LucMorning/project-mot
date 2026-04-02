import sqlite3
import difflib
import unidecode
import re
from src.config import DB_PATH

def normalize_text(text):
    if not text: return ""
    t = unidecode.unidecode(str(text)).lower()
    t = re.sub(r'[\(\)\[\]]', '', t)
    t = re.sub(r'[^a-zA-Z0-9\s]', ' ', t)
    return " ".join(t.split())

def match_roles_to_entrevistados():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 1. Pega os PDFs oficiais e seus titulos do DB (conforme ingestao do pipeline)
    cursor.execute("SELECT titulo_cargo, arquivo_pdf FROM cargos")
    cargos_pdfs = cursor.fetchall()
    pdf_lookup = {normalize_text(r['titulo_cargo']): r['arquivo_pdf'] for r in cargos_pdfs}
    chaves_pdf = list(pdf_lookup.keys())
    
    # 2. Pega as pessoas e seus cargos descritos no Excel
    cursor.execute("SELECT id, cargo FROM entrevistados WHERE cargo IS NOT NULL")
    pessoas = cursor.fetchall()
    
    count = 0
    not_found = []
    
    for p in pessoas:
        cargo_excel = normalize_text(p['cargo'])
        if "extra" in cargo_excel: continue # Pula arquivos órfãos não identificados
        
        # Tenta match exato primeiro
        match = None
        if cargo_excel in pdf_lookup:
            match = cargo_excel
        else:
            # Fuzzy match se não for exato
            matches = difflib.get_close_matches(cargo_excel, chaves_pdf, n=1, cutoff=0.7)
            if matches:
                match = matches[0]
                
        if match:
            pdf_filename = pdf_lookup[match]
            cursor.execute("UPDATE entrevistados SET arquivo_cargo_pdf = ? WHERE id = ?", (pdf_filename, p['id']))
            count += 1
        else:
            not_found.append(p['cargo'])
            
    conn.commit()
    conn.close()
    
    print(f"[MATCHER] Sucesso: {count} entrevistados vinculados a PDFs de Cargo.")
    if not_found:
        print(f"[AVISO] {len(not_found)} cargos do Excel não encontraram PDF correspondente.")

if __name__ == "__main__":
    match_roles_to_entrevistados()
