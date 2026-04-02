"""
Extract DOCX Transcripts Pipeline

Extrai transcrições de arquivos .docx e insere no banco.

Refatorado para usar:
- src.utils.date_parser → parse de datas
- src.utils.text_parser → limpeza de texto
- src.database.repositories → Repository pattern (DRY)
"""
from pathlib import Path

from src.config import TRANSCRICOES_DIR
from src.utils.docx_reader import extract_text_from_docx
from src.utils.date_parser import parse_date
from src.utils.text_parser import clean_transcript
from src.database.repositories import TranscricoesRepository, EntrevistadosRepository
from src.config import DB_PATH


def ingest_transcripts():
    """
    Extrai transcrições de arquivos .docx e insere no banco.

    Processo:
    1. Busca entrevistados com arquivo_transcricao
    2. Para cada arquivo:
       - Extrai texto do DOCX
       - Parseia data/hora
       - Limpa ruído da transcrição
       - Salva no banco
    """
    # Repositories
    transcript_repo = TranscricoesRepository(DB_PATH)
    entrevistado_repo = EntrevistadosRepository(DB_PATH)

    # Busca entrevistados com transcrições
    conn = EntrevistadosRepository(DB_PATH)._get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, arquivo_transcricao FROM entrevistados WHERE arquivo_transcricao IS NOT NULL"
    )
    rows = cursor.fetchall()
    conn.close()

    # Write truncate: limpa transcrições antes de reingetar
    transcript_repo.delete_all()

    count = 0
    for entrevistado_id, file_name in rows:
        file_path = TRANSCRICOES_DIR / file_name

        if not file_path.exists():
            print(f"[AVISO] Arquivo não encontrado: {file_path}")
            continue

        # 1. Extrai texto do DOCX
        text_raw = extract_text_from_docx(file_path)

        # 2. Parseia data/hora e limpa texto (utils reutilizáveis)
        text_with_date, timestamp = parse_date(text_raw)
        text_clean = clean_transcript(text_with_date)

        # 3. Salva no banco (Repository pattern - DRY)
        transcript_repo.insert({
            'id_entrevistado': entrevistado_id,
            'texto_completo': text_raw,
            'texto_limpo': text_clean,
            'dt_gravacao': timestamp,
            'arquivo_origem': file_name
        })

        # 4. Atualiza status
        entrevistado_repo.update_status(entrevistado_id, 'em_progresso')
        count += 1

    print(f"[SUCCESS] Ingested {count} transcripts with file tracking.")


if __name__ == "__main__":
    ingest_transcripts()
