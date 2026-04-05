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
    - Sufixos de reunião (" - A", " - B", etc)
    - Acentos
    - Artigos comuns
    - Sobrenomes do meio (Terra, Rapchan, etc)

    Args:
        text: Nome do entrevistado

    Returns:
        Nome normalizado para comparação

    Examples:
        >>> normalize_interviewee_name("Guilherme Tellis - A")
        'guilherme tellis'
        >>> normalize_interviewee_name("Tiago Terra Esteves")
        'tiago esteves'
        >>> normalize_interviewee_name("Lucas Giraldi Rapchan Aguilar")
        'lucas aguilar'
        >>> normalize_interviewee_name("Lucas Giraldi")
        'lucas giraldi'
    """
    if not text:
        return ""

    t = str(text)

    # Remove sufixos de reunião (" - A", " - B", " - C", etc)
    t = re.sub(r'\s*-\s*[A-Z]$', '', t)

    # Aplica normalização padrão
    t = normalize_for_fuzzy(t)

    # Pega primeira + última parte (remove sobrenomes do meio)
    # Ex: "tiago terra esteves" → "tiago esteves"
    # Ex: "lucas giraldi rapchan aguilar" → "lucas aguilar"
    palavras = t.split()

    if len(palavras) > 2:
        t = f"{palavras[0]} {palavras[-1]}"
    else:
        t = " ".join(palavras)

    return t
