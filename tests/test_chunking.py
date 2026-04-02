"""
Teste 2: Chunking - Validar divisão de transcrições
"""
import sys
sys.path.insert(0, '.')

from src.utils.chunking import chunk_transcript, TranscriptChunker

def test_chunking():
    print("="*60)
    print("TESTE 2: Chunking")
    print("="*60)

    # Tenta ler arquivo grande, senão usa texto hardcoded
    from pathlib import Path
    arquivo_teste = Path("tests/trans_teste_grande.txt")

    if arquivo_teste.exists():
        print(f"\n[1] Lendo arquivo grande: {arquivo_teste}")
        with open(arquivo_teste, 'r', encoding='utf-8') as f:
            texto_grande = f.read()
    else:
        print(f"\n[1] Criando transcrição de teste (hardcoded)...")
        texto_grande = "Parágrafo de teste. " * 100
        for i in range(50):
            texto_grande += f"\n\nParágrafo {i+1} com conteúdo sobre CAPEX. "
        texto_grande += "Menciona SAP, Archer, planilhas, manual, gargalos, integração. "

    print(f"   Tamanho: {len(texto_grande)} caracteres")

    # Testa chunking
    print("\n[2] Testando chunking...")
    chunks = chunk_transcript(texto_grande, max_size=15000, overlap=0.15)

    print(f"   Dividido em {len(chunks)} chunks")

    # Mostra estatísticas
    print(f"\n[3] Estatísticas:")
    chunker = TranscriptChunker()
    stats = chunker.get_chunk_stats(chunks)
    print(f"   Total chunks: {stats['total_chunks']}")
    print(f"   Tamanho médio: {stats['avg_chunk_size']} chars")
    print(f"   Menor chunk: {stats['min_chunk_size']} chars")
    print(f"   Maior chunk: {stats['max_chunk_size']} chars")

    # Mostra primeiros chunks
    print(f"\n[4] Primeiros 3 chunks (primeira linha):")
    for i, chunk in enumerate(chunks[:3]):
        primeira_linha = chunk.text.split('\n')[0][:60]
        print(f"   Chunk {i+1}: {primeira_linha}... ({len(chunk.text)} chars)")

    print(f"\n[RESULTADO] Chunking funcionou!" if len(chunks) > 1 else "\n[RESULTADO] FALHOU!")
    return len(chunks) > 1


if __name__ == "__main__":
    test_chunking()
