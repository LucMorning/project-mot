"""
Link Roles to Interviewees Pipeline

Conecta entrevistados aos seus respectivos PDFs de cargo usando
fuzzy matching entre o cargo descrito no Excel e o título do PDF.

Refatorado para usar:
- src.utils.text_normalizer → normalização centralizada (DRY)
- src.database.repositories → Repository pattern
"""
import sqlite3
import difflib
from pathlib import Path

from src.config import DB_PATH
from src.utils.text_normalizer import normalize_for_fuzzy


def link_roles_to_interviewees():
    """
    Conecta entrevistados aos PDFs de cargo correspondentes.

    Processo:
    1. Busca todos os PDFs de cargos no banco
    2. Busca entrevistados com cargo preenchido
    3. Para cada entrevistado:
       - Normaliza o cargo do Excel
       - Tenta match exato ou fuzzy (difflib)
       - Atualiza arquivo_cargo_pdf
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Busca PDFs de cargos oficiais
    cursor.execute("SELECT titulo_cargo, arquivo_pdf FROM stg_cargos")
    cargos_pdfs = cursor.fetchall()

    # De/Para: "diretor capex" -> "capex_diretor_a_capex_corporativo.pdf"
    pdf_lookup = {
        normalize_for_fuzzy(r['titulo_cargo']): r['arquivo_pdf']
        for r in cargos_pdfs
    }
    chaves_pdf = list(pdf_lookup.keys())

    # 2. Busca entrevistados com cargo preenchido
    cursor.execute(
        "SELECT id, cargo FROM stg_entrevistados WHERE cargo IS NOT NULL "
        "AND cargo != 'Não Identificado (Arquivo Extra)'"
    )
    pessoas = cursor.fetchall()

    count = 0
    not_found = []

    # 3. Match fuzzy
    for p in pessoas:
        cargo_excel = normalize_for_fuzzy(p['cargo'])

        if "extra" in cargo_excel:
            continue  # Pula arquivos órfãos

        # Tenta match exato primeiro
        match = None
        if cargo_excel in pdf_lookup:
            match = cargo_excel
        else:
            # Fuzzy match (70% de similaridade)
            matches = difflib.get_close_matches(cargo_excel, chaves_pdf, n=1, cutoff=0.7)
            if matches:
                match = matches[0]

        if match:
            pdf_filename = pdf_lookup[match]
            cursor.execute(
                "UPDATE stg_entrevistados SET arquivo_cargo_pdf = ? WHERE id = ?",
                (pdf_filename, p['id'])
            )
            count += 1
        else:
            not_found.append(p['cargo'])

    conn.commit()
    conn.close()

    print(f"[LINKER] {count} entrevistados vinculados aos PDFs de cargo.")
    if not_found:
        print(f"[AVISO] {len(not_found)} cargos não encontraram correspondência.")


if __name__ == "__main__":
    link_roles_to_interviewees()
