"""
Chunking Strategy para Transcrições Longas - MOTIVA

Divide transcrições grandes em chunks mantendo contexto através de:
- Overlap entre chunks (sobreposição)
- Resumo cumulativo do contexto
- Tamanho máximo configurável

Isso permite processar transcripts de 60k+ caracteres sem perder contexto.
"""
import re
from typing import List, Dict
from dataclasses import dataclass

from src.config import CHUNK_MAX_SIZE, CHUNK_MIN_SIZE, CHUNK_OVERLAP_RATIO


@dataclass
class Chunk:
    """Representa um chunk de texto com metadados."""
    index: int
    text: str
    start_char: int
    end_char: int
    context_summary: str = ""  # Resumo dos chunks anteriores


class TranscriptChunker:
    """
    Divide transcrições longas em chunks com preservação de contexto.

    Estratégia:
    1. Divide por parágrafos (quebras naturais)
    2. Agrupa até atingir max_chunk_size
    3. Adiciona overlap entre chunks
    4. Mantém resumo cumulativo
    """

    def __init__(
        self,
        max_chunk_size: int = CHUNK_MAX_SIZE,
        overlap_ratio: float = CHUNK_OVERLAP_RATIO,
        min_chunk_size: int = CHUNK_MIN_SIZE
    ):
        self.max_chunk_size = max_chunk_size
        self.overlap_ratio = overlap_ratio
        self.min_chunk_size = min_chunk_size

    def chunk(self, transcript: str) -> List[Chunk]:
        """
        Divide a transcrição em chunks.

        Args:
            transcript: Texto completo da transcrição

        Returns:
            Lista de chunks ordenados
        """
        # Se for pequeno, retorna chunk único
        if len(transcript) <= self.max_chunk_size:
            return [Chunk(index=0, text=transcript, start_char=0, end_char=len(transcript))]

        # Divide em parágrafos
        paragraphs = self._split_paragraphs(transcript)

        # Agrupa parágrafos em chunks
        chunks = self._group_paragraphs(paragraphs)

        # Adiciona overlap entre chunks
        chunks = self._add_overlap(chunks, transcript)

        return chunks

    def _split_paragraphs(self, text: str) -> List[str]:
        """Divide texto em parágrafos."""
        # Tenta dividir por quebras de parágrafo duplas
        paragraphs = re.split(r'\n\s*\n', text)

        # Se não funcionou bem, divide por quebras simples
        if len(paragraphs) < 3:
            paragraphs = text.split('\n')

        # Filtra parágrafos vazios
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        return paragraphs

    def _group_paragraphs(self, paragraphs: List[str]) -> List[Dict]:
        """Agrupa parágrafos em chunks respeitando max_chunk_size."""
        chunks = []
        current_chunk = []
        current_size = 0
        chunk_index = 0

        for para in paragraphs:
            para_size = len(para)

            # Se parágrafo individual for maior que max, precisa dividir
            if para_size > self.max_chunk_size:
                # Salva chunk atual se existir
                if current_chunk:
                    chunks.append({
                        'index': chunk_index,
                        'paragraphs': current_chunk.copy(),
                        'size': current_size
                    })
                    chunk_index += 1
                    current_chunk = []
                    current_size = 0

                # Divide parágrafo grande
                sub_paras = self._split_long_paragraph(para)
                for sub_para in sub_paras:
                    chunks.append({
                        'index': chunk_index,
                        'paragraphs': [sub_para],
                        'size': len(sub_para)
                    })
                    chunk_index += 1
                continue

            # Se adicionar parágrafo excede max_size, salva chunk
            if current_size + para_size > self.max_chunk_size and current_chunk:
                chunks.append({
                    'index': chunk_index,
                    'paragraphs': current_chunk.copy(),
                    'size': current_size
                })
                chunk_index += 1
                current_chunk = []
                current_size = 0

            current_chunk.append(para)
            current_size += para_size

        # Último chunk
        if current_chunk:
            chunks.append({
                'index': chunk_index,
                'paragraphs': current_chunk,
                'size': current_size
            })

        return chunks

    def _split_long_paragraph(self, text: str) -> List[str]:
        """Divide um parágrafo muito longo."""
        # Divide por sentenças
        sentences = re.split(r'[.!?]+', text)

        chunks = []
        current = ""
        for sent in sentences:
            if len(current) + len(sent) <= self.max_chunk_size:
                current += sent + ". "
            else:
                if current:
                    chunks.append(current.strip())
                current = sent + ". "

        if current:
            chunks.append(current.strip())

        return chunks if chunks else [text[:self.max_chunk_size]]

    def _add_overlap(self, chunks: List[Dict], original_text: str) -> List[Chunk]:
        """Adiciona overlap entre chunks para preservar contexto."""
        result = []
        overlap_size = int(self.max_chunk_size * self.overlap_ratio)

        for i, chunk_data in enumerate(chunks):
            # Junta parágrafos do chunk
            chunk_text = '\n\n'.join(chunk_data['paragraphs'])

            # Encontra posição no texto original (aproximada)
            start_para = chunk_data['paragraphs'][0]
            start_char = original_text.find(start_para)

            # Adiciona overlap do chunk anterior (se não for o primeiro)
            context_prefix = ""
            if i > 0 and start_char > overlap_size:
                overlap_start = start_char - overlap_size
                context_prefix = original_text[overlap_start:start_char]
                chunk_text = f"...{context_prefix}\n\n{chunk_text}"

            result.append(Chunk(
                index=i,
                text=chunk_text,
                start_char=start_char,
                end_char=start_char + len(chunk_text)
            ))

        return result

    def get_chunk_stats(self, chunks: List[Chunk]) -> Dict:
        """Retorna estatísticas dos chunks."""
        return {
            'total_chunks': len(chunks),
            'total_chars': sum(c.end_char - c.start_char for c in chunks),
            'avg_chunk_size': sum(len(c.text) for c in chunks) // len(chunks) if chunks else 0,
            'min_chunk_size': min(len(c.text) for c in chunks) if chunks else 0,
            'max_chunk_size': max(len(c.text) for c in chunks) if chunks else 0,
        }


# ─────────────────────────────────────────────────────────────
# FUNÇÃO CONVENIÊNCIA
# ─────────────────────────────────────────────────────────────

def chunk_transcript(
    transcript: str,
    max_size: int = CHUNK_MAX_SIZE,
    overlap: float = CHUNK_OVERLAP_RATIO
) -> List[Chunk]:
    """
    Divide uma transcrição em chunks com overlap.

    Args:
        transcript: Texto da transcrição
        max_size: Tamanho máximo de cada chunk (padrão: 15000)
        overlap: Razão de sobreposição (padrão: 0.15 = 15%)

    Returns:
        Lista de chunks
    """
    chunker = TranscriptChunker(max_chunk_size=max_size, overlap_ratio=overlap)
    return chunker.chunk(transcript)


if __name__ == "__main__":
    # Teste
    sample = """
    Este é um parágrafo de exemplo.

    Este é outro parágrafo com um pouco mais de texto para demonstrar
    como funciona o chunking.

    E aqui temos um terceiro parágrafo que também será incluído no
    processo de divisão da transcrição em partes menores.
    """ * 100  # Repete para criar texto grande

    chunks = chunk_transcript(sample, max_size=5000)
    stats = TranscriptChunker().get_chunk_stats(chunks)

    print(f"Total chunks: {stats['total_chunks']}")
    print(f"Tamanho médio: {stats['avg_chunk_size']} caracteres")
    print(f"Tamanho mínimo: {stats['min_chunk_size']}")
    print(f"Tamanho máximo: {stats['max_chunk_size']}")

    for i, chunk in enumerate(chunks[:3]):
        print(f"\nChunk {i}: {len(chunk.text)} caracteres")
        print(f"  Preview: {chunk.text[:100]}...")
