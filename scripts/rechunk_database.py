import sqlite3
import os
from src.config import DB_PATH
from src.utils.chunking import chunk_transcript

def rechunk_all_transcripts(max_size=10000, overlap=0.15):
    """
    Limpa chunks antigos e recria com a nova estratégia 10k/15%.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print(f"--- INICIANDO RE-CHUNKING (Estratégia: {max_size} chars / {int(overlap*100)}% overlap) ---")
    
    # 1. Limpa chunks e insights antigos de teste para começar do zero
    # (AVISO: Isso deleta apenas as análises de IA temporárias que fizemos)
    print("Limpando dados de teste anteriores...")
    cursor.execute("DELETE FROM insights_ia")
    cursor.execute("DELETE FROM sistemas_uso")
    cursor.execute("DELETE FROM relacoes")
    cursor.execute("DELETE FROM transcricao_chunks")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('transcricao_chunks', 'insights_ia', 'sistemas_uso', 'relacoes')")
    
    # 2. Busca todas as transcrições originais
    cursor.execute("SELECT id, id_entrevistado, texto_limpo FROM transcricoes")
    transcripts = cursor.fetchall()
    
    total_new_chunks = 0
    for t_id, ent_id, texto in transcripts:
        if not texto: continue
        
        # Gera os novos chunks
        chunks = chunk_transcript(texto, max_size=max_size, overlap=overlap)
        
        # Salva no banco
        for c in chunks:
            cursor.execute("""
                INSERT INTO transcricao_chunks (id_transcricao, ordem, conteudo, checksum, status_analise)
                VALUES (?, ?, ?, ?, 'pendente')
            """, (t_id, c.index, c.text, str(hash(c.text)),))
            total_new_chunks += 1
            
    conn.commit()
    conn.close()
    print(f"SUCESSO: {len(transcripts)} entrevistas re-processadas em {total_new_chunks} chunks otimizados.")

if __name__ == "__main__":
    rechunk_all_transcripts()
