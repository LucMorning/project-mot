"""
Text Normalizer - Centraliza lógica de normalização de texto (DRY).

Usado por pipelines de matching, fuzzy search, etc.
"""
import re
import unidecode


def normalize_text(text: str) -> str:
    """
    Normaliza texto para comparação fuzzy matching.

    Transformações:
    - Remove acentos (á → a)
    - Lowercase
    - Remove caracteres especiais (), [], {}
    - Remove pontuação excessiva
    - Normaliza espaços

    Args:
        text: Texto a normalizar

    Returns:
        Texto normalizado para comparação

    Examples:
        >>> normalize_text("Diretor CAPEX Corporativo")
        'diretor capex corporativo'
        >>> normalize_text("Eng. de Custos (Qualidade)")
        'eng de custos qualidade'
    """
    if not text:
        return ""

    # Remove acentos
    t = unidecode.unidecode(str(text))

    # Lowercase
    t = t.lower()

    # Remove parênteses, colchetes, chaves
    t = re.sub(r'[\(\)\[\]\{\}]', '', t)

    # Remove pontuação excessiva (mantém apenas alphanuméricos e espaços)
    t = re.sub(r'[^a-zA-Z0-9\s]', ' ', t)

    # Normaliza espaços (remove duplicados)
    t = " ".join(t.split())

    return t


def normalize_for_fuzzy(text: str) -> str:
    """
    Normalização específica para fuzzy matching com difflib.

    Versão mais agressiva que normalize_text().

    Args:
        text: Texto a normalizar

    Returns:
        Texto normalizado para fuzzy matching
    """
    if not text:
        return ""

    # Aplica normalização básica
    t = normalize_text(text)

    # Remove artigos comuns
    articles = [' da ', ' de ', ' do ', ' das ', ' dos ', ' a ', ' o ', ' as ', ' os ']
    for article in articles:
        t = t.replace(article, ' ')

    # Normaliza espaços novamente
    t = " ".join(t.split())

    return t


def normalize_interviewee_name(text: str) -> str:
    """
    Normaliza nomes de entrevistados para deduplicação.

    Remove:
    - Sufixos de reunião (" - Parte X", " - A", etc)
    - Acentos
    - Pontuação

    Args:
        text: Nome do entrevistado

    Returns:
        Nome normalizado para comparação
    """
    if not text:
        return ""

    t = str(text).strip()

    # Remove sufixos de reunião e partes
    t = re.sub(r'\s*-\s*Parte\s+\d+', '', t, flags=re.IGNORECASE)
    t = re.sub(r'\s+Parte\s+\d+$', '', t, flags=re.IGNORECASE)
    t = re.sub(r'\s*-\s*[A-Z]$', '', t)

    # Aplica normalização básica (acentos, case, etc)
    t = normalize_text(t)

    return t.upper()
