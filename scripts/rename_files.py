import os
import shutil
import json
import re
from pathlib import Path
from unidecode import unidecode
from src.config import DATA_DIR, RAW_DIR, TRANSCRICOES_DIR, CARGOS_DIR

def slugify(text: str) -> str:
    """Converte nome limpo para snake_case"""
    text = unidecode(text).lower()
    text = re.sub(r'[\(\)\[\]]', '', text) # remove parênteses
    text = re.sub(r'[^a-z0-9]+', '_', text) # troca o que não é alfa-numérico por '_'
    return text.strip('_')

def rename_and_move_transcriptions(old_dir="05. Transcrições Integrais"):
    if not os.path.exists(old_dir):
        print(f"Diretório {old_dir} não encontrado.")
        return

    transcriptions = [f for f in os.listdir(old_dir) if f.endswith('.docx')]
    rename_map = {}
    
    TRANSCRICOES_DIR.mkdir(parents=True, exist_ok=True)
    
    for filename in transcriptions:
        # Regex pra limpar os prefixos padrão
        clean_name = filename.replace(".docx", "")
        tipo = "entrevista_as_is_"
        
        if "reunião de aprofundamento" in clean_name.lower():
            tipo = "aprofundamento_"
            clean_name = re.sub(r'(?i)reunião de aprofundamento - (planejamento físico - )?', '', clean_name)
        elif "diagnóstico" in clean_name.lower():
            # Tira os prefixos Diagnóstico Cenário Atual _ (pode ter variação de hífens, travessão, underline)
            clean_name = re.sub(r'(?i)diagnóstico[^_]+_', '', clean_name)
        
        # Tira (Link Atualizado), (1) e "Parte X" do fim se houver muito sujo
        clean_name = clean_name.replace("Link Atualizado", "").replace("Parte 2", "_parte_2")
        
        # Converte pro kebab/snake (estamos seguindo snake_case p/ Python safety)
        final_slug = slugify(clean_name)
        
        # Monta prefixo_ + nome_da_pessoa.docx
        new_filename = f"{tipo}{final_slug}.docx"
        
        old_path = os.path.join(old_dir, filename)
        new_path = TRANSCRICOES_DIR / new_filename
        
        # Copy
        shutil.copy2(old_path, new_path)
        rename_map[filename] = new_filename

    # Salva o mapa
    map_file = DATA_DIR / "rename_map.json"
    with open(map_file, 'w', encoding='utf-8') as f:
        json.dump(rename_map, f, indent=4, ensure_ascii=False)
        
    print(f"[SUCESSO] {len(transcriptions)} arquivos renomados e padronizados com sucesso!")
    print(f"Mapa salvo em {map_file}")

def move_raw_data():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    to_move = [
        ("lista de entrevistas.xlsx", "lista_entrevistas.xlsx"),
        ("Relatório Sistemas TI Romulo - Prints 1.xlsx", "relatorio_sistemas_ti_romulo.xlsx")
    ]
    for old, new in to_move:
        if os.path.exists(old):
            shutil.copy2(old, RAW_DIR / new)
            print(f"[SUCESSO] Arquivo raw {old} movido -> {new}")

if __name__ == "__main__":
    print("Iniciando organização e padronização (Dry-Run fake = False)")
    rename_and_move_transcriptions()
    move_raw_data()
    # Em um passo seguinte, moveremos os PDFs
