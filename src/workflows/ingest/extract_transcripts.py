"""
Extract DOCX Transcripts Pipeline

Extrai transcrições de arquivos .docx e insere no banco.

NOVA ESTRUTURA:
- stg_arquivos_transcricao: metadados do arquivo (1:N com entrevistados)
- stg_transcricoes: conteúdo da transcrição (FK para stg_arquivos_transcricao)
"""
from pathlib import Path
import os

from src.config import TRANSCRICOES_DIR, DB_PATH
from src.utils.docx_reader import extract_text_from_docx
from src.utils.date_parser import parse_date
from src.utils.text_parser import clean_transcript
from src.utils.text_normalizer import normalize_interviewee_name


def find_entrevistado_for_file(conn, file_name: str) -> int:
    """
    Encontra o entrevistado correspondente ao arquivo.

    Estratégia (em ordem de precisão):
    1. Match exato de nome normalizado
    2. Match por substring bidirecional + primeiro nome igual
    3. Match por tokens: todos os tokens do arquivo estão no nome do banco
    """
    cursor = conn.cursor()

    # Extrai nome base do arquivo
    nome_base = file_name.lower()
    nome_base = nome_base.replace("entrevista_as_is_", "").replace("aprofundamento_", "")
    nome_base = nome_base.replace(".docx", "").replace("_", " ").strip()
    nome_normalizado = normalize_interviewee_name(nome_base)
    tokens_arquivo = set(nome_base.split())
    primeiro_nome = nome_base.split()[0].lower() if nome_base.split() else ""

    # Busca todos os entrevistados
    cursor.execute("SELECT id, nome FROM stg_entrevistados")
    todos = cursor.fetchall()

    for ent_id, ent_nome in todos:
        if not ent_nome:
            continue

        ent_nome_norm = normalize_interviewee_name(ent_nome)
        ent_nome_lower = ent_nome.lower()
        ent_tokens = set(ent_nome_lower.split())
        ent_primeiro_nome = ent_nome.split()[0].lower() if ent_nome.split() else ""

        # 1. Match exato de nome normalizado
        if nome_normalizado == ent_nome_norm:
            return ent_id

        # 2. Match por substring bidirecional + primeiro nome igual
        if nome_base in ent_nome_lower or ent_nome_lower in nome_base:
            if primeiro_nome and primeiro_nome == ent_primeiro_nome:
                return ent_id

        # 3. Match por tokens (todos os tokens do arquivo presentes no nome do banco)
        #    ex: {"marcela", "ventura"} ⊆ {"marcela", "alice", "ventura", "pinto"}
        if len(tokens_arquivo) >= 2 and tokens_arquivo.issubset(ent_tokens):
            if primeiro_nome and primeiro_nome == ent_primeiro_nome:
                return ent_id

    return None



def ingest_transcripts():
    """
    Extrai transcrições de arquivos .docx e insere no banco.

    Processo:
    1. Lista todos os arquivos .docx no diretório
    2. Para cada arquivo:
       - Encontra o entrevistado correspondente
       - Extrai texto do DOCX
       - Cria registro em stg_arquivos_transcricao
       - Cria registro em stg_transcricoes
    """
    import sqlite3

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Limpa tabelas antes de reingetar
    cursor.execute("DELETE FROM stg_transcricoes")
    cursor.execute("DELETE FROM stg_arquivos_transcricao")
    conn.commit()

    # Lista todos os arquivos .docx
    arquivos = list(TRANSCRICOES_DIR.glob('*.docx'))

    count = 0
    for file_path in sorted(arquivos):
        file_name = file_path.name

        # Encontra o entrevistado
        id_entrevistado = find_entrevistado_for_file(conn, file_name)

        if not id_entrevistado:
            print(f"[AVISO] Entrevistado não encontrado para: {file_name}")
            continue

        # Determina tipo de entrevista
        tipo = 'Aprofundamento' if 'aprofundamento' in file_name.lower() else 'Coleta de Dados'

        # Extrai texto do DOCX
        text_raw = extract_text_from_docx(file_path)

        # Parseia data/hora e limpa texto
        text_with_date, timestamp = parse_date(text_raw)
        text_clean = clean_transcript(text_with_date)

        # 1. Cria registro em stg_arquivos_transcricao
        cursor.execute('''
            INSERT INTO stg_arquivos_transcricao (id_entrevistado, nome_arquivo, tipo_entrevista)
            VALUES (?, ?, ?)
        ''', (id_entrevistado, file_name, tipo))

        id_arquivo_transcricao = cursor.lastrowid

        # 2. Cria registro em stg_transcricoes
        cursor.execute('''
            INSERT INTO stg_transcricoes (id_arquivo_transcricao, texto_completo, texto_limpo, dt_gravacao)
            VALUES (?, ?, ?, ?)
        ''', (id_arquivo_transcricao, text_raw, text_clean, timestamp))

        count += 1

    conn.commit()
    conn.close()

    print(f"[SUCCESS] Ingested {count} transcripts with file tracking.")


def main():
    """Entry point para Poetry scripts."""
    ingest_transcripts()


if __name__ == "__main__":
    main()
