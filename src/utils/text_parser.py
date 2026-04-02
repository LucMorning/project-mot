"""
Parser de texto para limpeza e normalização.

Centraliza toda a lógica de limpeza de texto que estava espalhada
pelos pipelines (transcrições, PDFs, etc).
"""
import re
import unidecode
from typing import Optional


class TextParser:
    """
    Parser de texto para limpeza e normalização.

    Funcionalidades:
    - Normalização de caracteres (UTF-8, acentos)
    - Remoção de ruído (timestamps, metadados)
    - Limpeza de espaços em excesso
    - Remoção de cláusulas padrão (compliance, ISO)
    """

    def __init__(self):
        # Padrões regex compilados
        self._time_pattern = re.compile(r'(\d{2}:)?\d{1,2}:\d{2}\s+')
        self._time_pattern2 = re.compile(r'\s{2,}\d{1,2}:\d{2}(:\d{2})?')
        self._duration_pattern = re.compile(r'\d+m\s+\d+s')
        self._metadata_patterns = [
            re.compile(r'.*começou a transcrição', re.IGNORECASE),
            re.compile(r'Diagnóstico – Cenário Atual.*Gravação de Reunião', re.IGNORECASE),
            re.compile(r'Transcrição gerada por.*', re.IGNORECASE),
        ]
        self._bullet_pattern = re.compile(r'^\d+\.\s*-\s*$', re.MULTILINE)
        self._numbering_pattern = re.compile(r'\b\d+\.\s+')

        # Cláusulas de compliance a remover (case-insensitive, multiline)
        self._compliance_patterns = [
            re.compile(r'\d+\.\s*Este colaborador tamb[ée]m.*', re.IGNORECASE | re.DOTALL),
            re.compile(r'Este colaborador tamb[ée]m.*', re.IGNORECASE | re.DOTALL),
            re.compile(r'Cumprir e fazer cumprir normas.*', re.IGNORECASE | re.DOTALL),
        ]

    def clean_transcript(self, text: str) -> str:
        """
        Limpeza completa de transcrição de entrevista.

        Remove:
        - Timestamps
        - Metadados de transcrição automática
        - Espaços excessivos

        Args:
            text: Texto da transcrição

        Returns:
            Texto limpo
        """
        if not text:
            return ""

        # 1. Remove timestamps
        clean = self._time_pattern.sub(' ', text)
        clean = self._time_pattern2.sub(' ', clean)
        clean = self._duration_pattern.sub(' ', clean)

        # 2. Remove metadados
        for pattern in self._metadata_patterns:
            clean = pattern.sub(' ', clean)

        # 3. Normaliza espaços
        clean = re.sub(r'\s+', ' ', clean).strip()

        return clean

    def clean_pdf_text(self, text: str) -> str:
        """
        Limpeza de texto extraído de PDF.

        PDFs frequentemente têm problemas de encoding e formatação.
        Usa unidecode para normalizar caracteres.

        Args:
            text: Texto bruto do PDF

        Returns:
            Texto limpo e normalizado
        """
        if not text:
            return ""

        # 1. Normaliza encoding (remove caracteres problemáticos)
        clean = text.encode('utf-8', 'ignore').decode('utf-8')

        # 2. Remove acentos (para matching mais robusto)
        clean = unidecode.unidecode(clean)

        return clean

    def clean_section(self, text: str, remove_compliance: bool = True) -> str:
        """
        Limpeza de seção de texto (ex: seção de responsabilidades).

        Remove:
        - Cláusulas de compliance
        - Numeração de bullets
        - Espaços excessivos

        Args:
            text: Texto da seção
            remove_compliance: Se True, remove cláusulas padrão de compliance

        Returns:
            Texto limpo
        """
        if not text:
            return ""

        clean = text

        # 1. Remove cláusulas de compliance
        if remove_compliance:
            for pattern in self._compliance_patterns:
                clean = pattern.sub(' ', clean)

        # 2. Remove bullets vazios ("1. - ", "2. - ", etc)
        lines = [l for l in clean.split('\n') if not self._bullet_pattern.match(l.strip())]
        clean = " ".join(lines)

        # 3. Remove numeração
        clean = self._numbering_pattern.sub(' ', clean)

        # 4. Normaliza espaços
        clean = re.sub(r'\s+', ' ', clean).strip()

        return clean

    def normalize_spaces(self, text: str) -> str:
        """Normaliza espaços em branco (quebras múltiplas → espaço único)."""
        if not text:
            return ""
        return re.sub(r'\s+', ' ', text).strip()

    def extract_numbered_items(self, text: str) -> list[str]:
        """
        Extrai itens numerados de um texto.

        Args:
            text: Texto com itens numerados (ex: "1. Item um\n2. Item dois")

        Returns:
            Lista de itens (strings)
        """
        # Divide por numeração no início da linha
        items = re.split(r'\n\s*\d+\.\s+', text)
        # Remove primeiro item (geralmente é o título)
        return [item.strip() for item in items[1:] if item.strip()]

    def truncate(self, text: str, max_length: int, suffix: str = "...") -> str:
        """
        Trunca texto se exceder tamanho máximo.

        Args:
            text: Texto a truncar
            max_length: Tamanho máximo
            suffix: Sufixo a adicionar se truncar

        Returns:
            Texto truncado (ou original se menor que max)
        """
        if not text or len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix


# ─────────────────────────────────────────────────────────────
# FUNÇÕES CONVENIÊNCIA
# ─────────────────────────────────────────────────────────────

_default_parser: Optional[TextParser] = None


def get_parser() -> TextParser:
    """Retorna o parser singleton."""
    global _default_parser
    if _default_parser is None:
        _default_parser = TextParser()
    return _default_parser


def clean_transcript(text: str) -> str:
    """Limpa transcrição de entrevista."""
    return get_parser().clean_transcript(text)


def clean_pdf_text(text: str) -> str:
    """Limpa texto de PDF."""
    return get_parser().clean_pdf_text(text)


def clean_section(text: str, remove_compliance: bool = True) -> str:
    """Limpa seção de texto (responsabilidades, etc)."""
    return get_parser().clean_section(text, remove_compliance)


if __name__ == "__main__":
    # Teste
    parser = TextParser()

    test_transcript = "14:30 Começou a transcrição  Olá, tudo bem?  15m 30s"
    print(f"Transcrição limpa: {parser.clean_transcript(test_transcript)}")

    test_pdf = "Este colaborador também deve cumprir normas ISO 9001."
    print(f"PDF limpo: {parser.clean_section(test_pdf)}")
