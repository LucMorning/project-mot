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
    Usa matching multidimensional (Cargo + Diretoria).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Busca PDFs de cargos oficiais com metadados
    cursor.execute("SELECT id, titulo_cargo, diretoria, arquivo_pdf FROM stg_cargos")
    cargos_oficiais = cursor.fetchall()

    # De/Para lookup: "diretor capex corporativo" -> (id, arquivo_pdf)
    role_lookup = {}
    for r in cargos_oficiais:
        # Criamos uma chave composta (Cargo + Diretoria) para máxima precisão
        role_norm = normalize_for_fuzzy(r['titulo_cargo'])
        diretoria_norm = normalize_for_fuzzy(r['diretoria'])
        chave = f"{role_norm} {diretoria_norm}".strip()
        role_lookup[chave] = (r['id'], r['arquivo_pdf'])
    
    chaves_cargos = list(role_lookup.keys())

    # 2. Busca entrevistados
    cursor.execute("SELECT id, cargo, diretoria FROM stg_entrevistados WHERE cargo IS NOT NULL")
    entrevistados = cursor.fetchall()

    count = 0
    not_found = []

    # 3. Match Multidimensional
    for p in entrevistados:
        # Prepara a query do Excel (NOME + DIRETORIA)
        excel_cargo = normalize_for_fuzzy(p['cargo'])
        excel_dir = normalize_for_fuzzy(p['diretoria'])
        query = f"{excel_cargo} {excel_dir}".strip()

        # Tenta match exato primeiro
        match = None
        if query in role_lookup:
            match = query
        else:
            # Fuzzy match (65% de similaridade na chave composta)
            matches = difflib.get_close_matches(query, chaves_cargos, n=1, cutoff=0.65)
            if matches:
                match = matches[0]
            else:
                # Fallback: Tenta match apenas por cargo se diretoria falhar
                role_only_matches = difflib.get_close_matches(excel_cargo, chaves_cargos, n=1, cutoff=0.75)
                if role_only_matches:
                    match = role_only_matches[0]

        if match:
            rid, rpdf = role_lookup[match]
            cursor.execute(
                "UPDATE stg_entrevistados SET id_cargo = ?, arquivo_cargo_pdf = ? WHERE id = ?",
                (rid, rpdf, p['id'])
            )
            count += 1
        else:
            not_found.append(f"{p['cargo']} ({p['diretoria']})")

    conn.commit()
    conn.close()

    print(f"[LINKER] {count} entrevistados vinculados a cargos oficiais.")
    if not_found:
        print(f"[AVISO] {len(not_found)} entrevistados não encontrados nos PDFs de cargo.")


def main():
    """Entry point para Poetry scripts."""
    link_roles_to_interviewees()


if __name__ == "__main__":
    main()
