import os
import json
import re
from src.config import DATA_DIR, TRANSCRICOES_DIR

def normalize_name(name: str) -> list[str]:
    """Retorna partes de um nome em lowercase para facilitar busca."""
    if not name: return []
    return str(name).lower().split()

def build_name_file_map() -> dict:
    """Carrega o mapa pre-calculado gerado no rename_files.py 
       e associa ao NOME COMPLETO do Excel.
    """
    map_file = DATA_DIR / "rename_map.json"
    rename_map = {}
    if map_file.exists():
        with open(map_file, 'r', encoding='utf-8') as f:
            rename_map = json.load(f) # ex: {"Diagnóstico _ Flávio...docx": "entrevista_as_is_flavio.docx"}
            
    # Cria o map: Nome do Excel => arquivo_slug.docx
    # Em um banco real isso estaria rodando 1 vez. No processo atual, a gente já renomeou as transcrições.
    # Então vamos listar o repo_atual e tentar "matchar":
    
    arquivos_renomeados = os.listdir(TRANSCRICOES_DIR) if TRANSCRICOES_DIR.exists() else []
    
    return rename_map

def get_best_match(full_name: str, available_files: list[str]) -> str:
    """
    Dado um nome completo e uma lista de arquivos DOCX já renomeados (ex: entrevista_as_is_maria_silva.docx)
    Devem corresponder ao primeiro E último nome.
    """
    if not full_name: return None
    
    # CUSTOM HARD MAPS para exceções reportadas pelo QA
    name_l = full_name.lower()
    if 'bonin' in name_l: return 'aprofundamento_jean_bonin.docx' if 'aprofundamento_jean_bonin.docx' in available_files else 'entrevista_as_is_jean_bonin.docx'
    if 'marcela' in name_l and 'ventura' in name_l: return 'entrevista_as_is_marcela_ventura.docx'
    if 'teixeira' in name_l and 'freitas' in name_l: return 'entrevista_as_is_andre_teixeira.docx'
    if 'pita' in name_l: return 'entrevista_as_is_joao_pita_1.docx'
    
    parts = name_l.split()
    if not parts: return None
    
    first = parts[0]
    last = parts[-1] if len(parts) > 1 else ""
    
    for f in available_files:
        if first in f:
            if last and last in f:
                return f
            elif not last:
                return f
                
    # fallback se só bater 1 nome importante (ex: 2 nomes que viraram 1 no arquivo)
    for f in available_files:
        if len(parts) >= 2 and parts[0] in f and parts[1] in f:
            return f

    return None
