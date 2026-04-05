"""
Ingest Metadata - ETL da planilha mestre para a tabela entrevistados.

Responsabilidade unica: ler lista_entrevistas.xlsx e popular o banco,
delegando deduplicacao ao modulo deduplicator.
"""
import re
import os
import sqlite3
import openpyxl
import unidecode as _unidecode

from src.config import (
    DB_PATH, LISTA_ENTREVISTAS, TRANSCRICOES_DIR,
    TRANSCRIPT_PREFIXES, TRANSCRIPT_EXTENSION,
)
from src.utils.name_matcher import build_name_file_map, get_best_match
from src.workflows.ingest.deduplicator import (
    cleanup_duplicate_interviewees,
    find_existing_interviewee,
)


def ingest_master_spreadsheet():

    """
    Lê a planilha lista_entrevistas.xlsx e insere no banco.

    Processo:
    1. Limpa duplicatas existentes
    2. Insere/atualiza dados do Excel
    3. Adiciona arquivos soltos não mapeados
    """
    if not LISTA_ENTREVISTAS.exists():
        print(f"Erro: Arquivo não encontrado: {LISTA_ENTREVISTAS}")
        return

    # Inicia conexão
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. LIMPA DUPLICATAS ANTES DE INGERIR (com cascade)
    print("\n[CLEANUP] Removendo duplicatas existentes...")
    stats_before = cleanup_duplicate_interviewees(conn)
    print(f"[CLEANUP] {stats_before['removed']} duplicatas removidas.\n")

    # Pega o mapa de nomes => arquivo renomeado .docx
    map_files = build_name_file_map()

    wb = openpyxl.load_workbook(LISTA_ENTREVISTAS)
    ws = wb.active

    # Lista de arquivos disponíveis — declarada uma vez, fora do loop
    available = os.listdir(TRANSCRICOES_DIR) if TRANSCRICOES_DIR.exists() else []

    count_inserted = 0
    count_updated = 0
    count_skipped = 0

    for row in range(2, ws.max_row + 1):
        nome = ws.cell(row=row, column=2).value
        # Filtra os vazios ou zeros
        if not nome or str(nome).strip() in ["", "0", "None"]:
            continue

        # Nome: UPPERCASE + sem acentos
        nome = _unidecode.unidecode(str(nome).strip()).upper()

        # Remove sufixos como " - Parte 2", " - A", "PARTE 2"
        nome = re.sub(r'\s*-\s*Parte\s+\d+', '', nome, flags=re.IGNORECASE)
        nome = re.sub(r'\s+Parte\s+\d+$', '', nome, flags=re.IGNORECASE)
        nome = re.sub(r'\s*-\s*[A-Z]$', '', nome)

        cargo = ws.cell(row=row, column=3).value
        diretoria = ws.cell(row=row, column=4).value
        plataforma = ws.cell(row=row, column=5).value
        area = ws.cell(row=row, column=6).value
        nivel = ws.cell(row=row, column=7).value
        dt_entrevista = ws.cell(row=row, column=8).value

        # Diretoria: NULL se for "0", "#N/A", vazio
        if diretoria and str(diretoria).strip() in ["0", "#N/A", "", "None", "NA"]:
            diretoria = None

        # Pode ser datetime, formata para string
        if hasattr(dt_entrevista, "strftime"):
            dt_entrevista = dt_entrevista.strftime("%Y-%m-%d %H:%M")
        elif dt_entrevista:
            dt_entrevista = str(dt_entrevista)

        tipo_entrevista = ws.cell(row=row, column=9).value

        arquivo_docx = get_best_match(nome, available)

        # Verifica se já existe (UPDATE ou INSERT)
        existing_id = find_existing_interviewee(conn, nome)

        if existing_id:
            # UPDATE do existente - usa o nome mais longo (mais completo)
            cursor.execute("SELECT nome FROM entrevistados WHERE id = ?", (existing_id,))
            current_nome = cursor.fetchone()[0]
            # Mantém o nome mais longo
            nome_to_use = nome if len(nome) > len(current_nome) else current_nome

            cursor.execute("""
                UPDATE entrevistados
                SET nome = ?, cargo = ?, diretoria = ?, plataforma = ?, area = ?, nivel = ?,
                    dt_entrevista = ?, tipo_entrevista = ?
                WHERE id = ?
            """, (nome_to_use, cargo, diretoria, plataforma, area, nivel, dt_entrevista, tipo_entrevista, existing_id))
            count_updated += 1
        else:
            # INSERT novo
            cursor.execute("""
                INSERT INTO entrevistados
                (nome, cargo, diretoria, plataforma, area, nivel, dt_entrevista, tipo_entrevista, arquivo_transcricao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (nome, cargo, diretoria, plataforma, area, nivel, dt_entrevista, tipo_entrevista, arquivo_docx))
            count_inserted += 1

    # Lógica QA Integridade: Inserir DOCXs físicos que sobraram e não estão no Excel
    used_files = [x[0] for x in cursor.execute("SELECT arquivo_transcricao FROM entrevistados WHERE arquivo_transcricao IS NOT NULL").fetchall()]
    for arquivo_solto in available:
        if arquivo_solto not in used_files:
            nome_base = arquivo_solto
            for prefix in TRANSCRIPT_PREFIXES:
                nome_base = nome_base.replace(prefix, "")
            nome_base = nome_base.replace(TRANSCRIPT_EXTENSION, "").replace("_", " ").strip()
            nome_assumed = _unidecode.unidecode(nome_base).upper()

            # Determinar tipo de entrevista a partir do nome do arquivo
            tipo_entrevista = 'Aprofundamento' if 'aprofundamento' in arquivo_solto.lower() else 'Coleta de Dados'

            # DEDUPLICAÇÃO também para arquivos soltos
            existing_id = find_existing_interviewee(conn, nome_assumed)

            if existing_id:
                # Verifica se é a mesma pessoa com tipo DIFERENTE de entrevista
                cursor.execute("SELECT tipo_entrevista, arquivo_transcricao FROM entrevistados WHERE id = ?", (existing_id,))
                existente = cursor.fetchone()
                tipo_existente = existente[0] if existente else None
                arquivo_existente = existente[1] if existente else None

                # Se é a mesma pessoa mas tipo diferente (as_is vs aprofundamento), cria novo registro
                if tipo_entrevista != tipo_existente:
                    print(f"  [CRIAR NOVO] {nome_assumed} já existe como {tipo_existente} (ID: {existing_id}), mas este é {tipo_entrevista}")
                else:
                    print(f"  [SKIP EXTRA] {nome_assumed} já existe como {tipo_existente} (ID: {existing_id})")
                    continue

            cursor.execute("""
                INSERT INTO entrevistados
                (nome, cargo, arquivo_transcricao, tipo_entrevista, status_revisao)
                VALUES (?, 'Não Identificado (Arquivo Extra)', ?, 'Extra QA', 'pendente')
            """, (nome_assumed, arquivo_solto))
            count_inserted += 1

    # 2. LIMPA DUPLICATAS DEPOIS DE INGERIR (para lidar com duplicatas do Excel)
    print("\n[CLEANUP] Removendo duplicatas criadas pelo Excel...")
    stats_after = cleanup_duplicate_interviewees(conn)
    print(f"[CLEANUP] {stats_after['removed']} duplicatas removidas.\n")

    conn.commit()
    conn.close()
    total_removed = stats_before['removed'] + stats_after['removed']
    print(f"[SUCESSO] Ingestão completa! {total_removed} duplicatas removidas, {count_inserted} novos, {count_updated} atualizados.")


if __name__ == "__main__":
    ingest_master_spreadsheet()
