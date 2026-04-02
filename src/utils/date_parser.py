"""
Parser de datas para transcrições MOTIVA.

Extrai datas de múltiplos formatos (ISO, MS Teams, compacto) e
normaliza para formato padrão do banco.
"""
import re
from datetime import datetime
from typing import Tuple, Optional


# Mapeamento de meses por extenso para números
MONTH_MAP = {
    'janeiro': '01', 'jan': '01',
    'fevereiro': '02', 'fev': '02',
    'marco': '03', 'março': '03', 'mar': '03',
    'abril': '04', 'abr': '04',
    'maio': '05', 'mai': '05',
    'junho': '06', 'jun': '06',
    'julho': '07', 'jul': '07',
    'agosto': '08', 'ago': '08',
    'setembro': '09', 'set': '09',
    'outubro': '10', 'out': '10',
    'novembro': '11', 'nov': '11',
    'dezembro': '12', 'dez': '12'
}


class DateParser:
    """
    Parser de datas para transcrições.

    Formatos suportados:
    - ISO: 2025-01-15 14:30:00
    - MS Teams: 15 de Janeiro de 2025, 2:30PM
    - Compacto: 20250115_143000
    """

    def __init__(self):
        # Padrões regex (compilados uma vez)
        self._iso_pattern = re.compile(r'(\d{4})-(\d{2})-(\d{2})\s+(\d{2}:\d{2}:\d{2})')
        self._teams_pattern = re.compile(r'(\d{1,2})\s+de\s+([a-zçãíA-Z]+)\s+de\s+(\d{4}),\s+(\d{1,2}:\d{2})(AM|PM)?')
        self._compact_pattern = re.compile(r'(\d{4})(\d{2})(\d{2})(?:_(\d{2})(\d{2})(\d{2}))?')

    def parse(self, text: str) -> Tuple[str, str]:
        """
        Extrai data e hora do texto e limpa o texto.

        Args:
            text: Texto que pode conter data/hora

        Returns:
            Tupla (texto_limpo, data_iso) onde data_iso = "YYYY-MM-DD HH:MM:SS"
            Se não encontrar data, retorna ("texto", "0000-00-00 00:00:00")
        """
        if not text:
            return "", "0000-00-00 00:00:00"

        data_final, hora_final = "0000-00-00", "00:00:00"
        text_clean = text

        # 1. Tenta formato ISO: 2025-01-15 14:30:00
        match = self._iso_pattern.search(text)
        if match:
            data_final = f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
            hora_final = match.group(4)
            text_clean = self._iso_pattern.sub(' ', text)

        # 2. Tenta formato MS Teams: 15 de Janeiro de 2025, 2:30PM
        elif data_final == "0000-00-00":
            match = self._teams_pattern.search(text)
            if match:
                dia, mes_str, ano = match.group(1), match.group(2), match.group(3)
                mes_num = self._normalize_month(mes_str)

                # Parse hora
                h, m = map(int, match.group(4).split(':'))
                period = match.group(5)
                if period and period.upper() == 'PM' and h < 12:
                    h += 12
                elif period and period.upper() == 'AM' and h == 12:
                    h = 0

                data_final = f"{ano}-{mes_num}-{dia.zfill(2)}"
                hora_final = f"{h:02d}:{m:02d}:00"
                text_clean = self._teams_pattern.sub(' ', text, flags=re.IGNORECASE)

        # 3. Tenta formato compacto: 20250115_143000
        elif data_final == "0000-00-00":
            match = self._compact_pattern.search(text)
            if match:
                data_final = f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
                if match.group(4):
                    hora_final = f"{match.group(4)}:{match.group(5)}:{match.group(6)}"
                text_clean = self._compact_pattern.sub(' ', text)

        return text_clean.strip(), f"{data_final} {hora_final}"

    def _normalize_month(self, month_str: str) -> str:
        """Normaliza nome do mês para número (01-12)."""
        month_key = month_str.lower()
        month_key = month_key.replace('ç', 'c').replace('ã', 'a').replace('í', 'i')
        return MONTH_MAP.get(month_key, '01')

    def is_valid_date(self, date_str: str) -> bool:
        """Verifica se uma data é válida (não é o default)."""
        return not date_str.startswith("0000-00-00")


# ─────────────────────────────────────────────────────────────
# FUNÇÕES CONVENIÊNCIA
# ─────────────────────────────────────────────────────────────

_default_parser: Optional[DateParser] = None


def get_parser() -> DateParser:
    """Retorna o parser singleton."""
    global _default_parser
    if _default_parser is None:
        _default_parser = DateParser()
    return _default_parser


def parse_date(text: str) -> Tuple[str, str]:
    """
    Extrai data/hora do texto e limpa.

    Args:
        text: Texto que pode conter data/hora

    Returns:
        (texto_limpo, data_iso)

    Example:
        >>> from src.utils.date_parser import parse_date
        >>> clean, date = parse_date("Reunião em 15 de Janeiro de 2025, 2:30PM")
        >>> print(date)  # "2025-01-15 14:30:00"
    """
    return get_parser().parse(text)


if __name__ == "__main__":
    # Teste
    test_cases = [
        "Reunião em 2025-01-15 14:30:00",
        "15 de Janeiro de 2025, 2:30PM",
        "20250115_143000",
        "Sem data aqui"
    ]

    parser = DateParser()
    for test in test_cases:
        clean, date = parser.parse(test)
        print(f"Input:  {test}")
        print(f"Data:   {date}")
        print(f"Clean:  {clean}")
        print()
