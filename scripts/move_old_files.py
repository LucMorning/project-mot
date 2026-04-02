import os
import shutil
from pathlib import Path
from src.config import PROJECT_ROOT

def move_old_legacy_files():
    """
    Função de cleanup que roda NO FINAL de todo o projeto.
    Ela captura os "entulhos" soltos na raiz (arquivos raw ou prints) e lança tudo para _old 
    para preservar a história do projeto limpa.
    """
    old_dir = PROJECT_ROOT / "_old"
    old_dir.mkdir(parents=True, exist_ok=True)
    
    origem_transcricoes = PROJECT_ROOT / "05. Transcrições Integrais"
    origem_holding = PROJECT_ROOT / "01. Holding Corporativo"
    
    pastas_antigas = [origem_transcricoes, origem_holding]
    arquivos_antigos_raiz = [
        "lista de entrevistas.xlsx",
        "consolidado_entrevistas_motiva.xlsx",
        "diagnostico_referencia_ti.md",
        "resumo_executivo_intervistas.md",
        "Mapa_Diagnostico_Compilado.r4.xlsx",
        "diagnostico_as_is_detalhado.xlsx",
        "diagnostico_consolidado_tematico.xlsx",
        "Report_Diagnostico_AsIs_MOTIVA.pptx",
        "DIAGNOSTICO_ESTRATEGICO_CAPEX_MOTIVA.pptx",
        "Relatório Sistemas TI Romulo - Prints 1.xlsx",
        "file_list.txt"
    ]
    
    count_files = 0
    count_dirs = 0
    
    for arq in arquivos_antigos_raiz:
        path_arq = PROJECT_ROOT / arq
        if path_arq.exists():
            shutil.copy2(path_arq, old_dir / arq)
            path_arq.unlink() # Limpeza ativa
            count_files += 1

    for d in pastas_antigas:
        if d.exists() and d.is_dir():
            target_d = old_dir / d.name
            if not target_d.exists():
                shutil.copytree(d, target_d)
                shutil.rmtree(d) # Limpeza ativa de pastas originais copiadas
            count_dirs += 1
            
    # Move os scripts legados (snippets / _antigos)
    snippets = PROJECT_ROOT / "snippets"
    if snippets.exists():
        target_snip = old_dir / "snippets"
        if not target_snip.exists():
            shutil.copytree(snippets, target_snip)
        shutil.rmtree(snippets)
        
    print(f"[CLEANUP] Movidos/opiados para _old: {count_files} arquivos soltos, {count_dirs} diretórios originais brutos.")
    print("Nota: Usei copy ao invés de unlink localmente nas pastas para mitigar perdas. Ative unlink se quiser limpeza hard.")

if __name__ == "__main__":
    move_old_legacy_files()
