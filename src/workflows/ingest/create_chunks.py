"""
Create Chunks Pipeline

Lê transcrições de stg_transcricoes, divide em chunks via TranscriptChunker
e persiste em stg_chunks.

Esta é a etapa 4 do ingestion pipeline — deve ser executada APÓS
extract_transcripts (que popula stg_transcricoes).
"""
import sqlite3
import hashlib

from src.config import DB_PATH, CHUNK_MAX_SIZE, CHUNK_OVERLAP_RATIO, ChunkStatus
from src.utils.chunking import TranscriptChunker


def _checksum(text: str) -> str:
    """SHA-256 dos primeiros 1000 chars do chunk (identidade única para dedup)."""
    return hashlib.sha256(text[:1000].encode()).hexdigest()[:16]


def create_chunks() -> None:
    """
    Divide transcrições de stg_transcricoes em chunks e persiste em stg_chunks.

    Estratégia: write-truncate — recria todos os chunks a cada execução
    para garantir consistência com parâmetros atuais (CHUNK_MAX_SIZE, etc).
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Write-truncate: limpa chunks existentes antes de recriar
        cursor.execute("DELETE FROM stg_chunks")
        conn.commit()
        print("[CHUNKS] Chunks existentes removidos.")

        # Busca todas as transcrições com conteúdo
        # Nova cadeia de FK: stg_transcricoes → stg_arquivos_transcricao → stg_entrevistados
        cursor.execute("""
            SELECT t.id, a.id_entrevistado, t.texto_limpo, e.nome
            FROM stg_transcricoes t
            JOIN stg_arquivos_transcricao a ON a.id = t.id_arquivo_transcricao
            JOIN stg_entrevistados e ON e.id = a.id_entrevistado
            WHERE t.texto_limpo IS NOT NULL AND LENGTH(t.texto_limpo) > 0
            ORDER BY t.id
        """)
        transcricoes = cursor.fetchall()

        if not transcricoes:
            print("[CHUNKS] Nenhuma transcrição encontrada em stg_transcricoes.")
            print("         Execute primeiro: python -m src.workflows ingestion")
            return

        chunker = TranscriptChunker(
            max_chunk_size=CHUNK_MAX_SIZE,
            overlap_ratio=CHUNK_OVERLAP_RATIO
        )

        total_chunks = 0
        for transcricao_id, entrevistado_id, texto, nome in transcricoes:
            chunks = chunker.chunk(texto)

            for chunk in chunks:
                cursor.execute("""
                    INSERT INTO stg_chunks (id_transcricao, ordem, conteudo, checksum, status_analise)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    transcricao_id,
                    chunk.index,
                    chunk.text,
                    _checksum(chunk.text),
                    ChunkStatus.PENDING
                ))

            total_chunks += len(chunks)
            print(f"  [OK] {nome}: {len(chunks)} chunk(s) ({len(texto):,} chars)")

        conn.commit()
        print(f"\n[CHUNKS] {total_chunks} chunks criados para {len(transcricoes)} transcrições.")

    except Exception as e:
        conn.rollback()
        print(f"[ERRO] Falha ao criar chunks: {e}")
        raise
    finally:
        conn.close()


def main():
    """Entry point para Poetry scripts."""
    create_chunks()


if __name__ == "__main__":
    main()
