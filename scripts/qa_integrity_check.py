import sqlite3
import os
from pathlib import Path
from src.config import DB_PATH, TRANSCRICOES_DIR, RAW_DIR, CARGOS_DIR

def run_integrity_check():
    print("====================================")
    print("[QA] INICIANDO QA DE INTEGRIDADE (AS-IS)")
    print("====================================\n")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # QA 1: Entrevistados vs Planilha
    cursor.execute("SELECT count(*) FROM entrevistados")
    total_entrevistados = cursor.fetchone()[0]
    print(f"[QA 1] Pessoas Mapeadas (Tabela Entrevistados): {total_entrevistados} (Esperado: ~69)")
    
    # QA 2: Transcrições .docx perdidas ou não mapeadas
    cursor.execute("SELECT count(*) FROM transcricoes")
    total_textos_extraidos = cursor.fetchone()[0]
    
    cursor.execute("SELECT count(*) FROM entrevistados WHERE arquivo_transcricao IS NOT NULL")
    encontraram_match = cursor.fetchone()[0]
    print(f"[QA 2] Entrevistados COM arquivo DOCX associado: {encontraram_match}")
    print(f"[QA 2] Textos Brutos armazenados (Tabela Transcricoes): {total_textos_extraidos}")
    
    arquivos_docx_fisicos = list(TRANSCRICOES_DIR.glob("*.docx")) if TRANSCRICOES_DIR.exists() else []
    print(f"[QA 2] Arquivos físicos na pasta /transcricoes: {len(arquivos_docx_fisicos)}")
    
    if len(arquivos_docx_fisicos) != total_textos_extraidos:
        print("\n[ALERTA] Há uma diferença entre os arquivos mapeados e os físicos.")
        cursor.execute("SELECT arquivo_transcricao FROM entrevistados WHERE arquivo_transcricao IS NOT NULL")
        arquivos_banco = [row[0] for row in cursor.fetchall() if row[0]]
        
        fisicos_nomes = [f.name for f in arquivos_docx_fisicos]
        orfaos = set(fisicos_nomes) - set(arquivos_banco)
        
        if orfaos:
            print(f"-> Arquivos na pasta sem dono no banco ({len(orfaos)}):")
            for o in list(orfaos)[:10]:
                print(f"    - {o}")
    else:
        print("[OK] Todas as transcrições físicas estão 100% integradas no Banco.")
        
    print("")

    # QA 3: Cargos PDF
    cursor.execute("SELECT count(*) FROM cargos")
    total_cargos_extraidos = cursor.fetchone()[0]
    
    arquivos_pdf_fisicos = list(CARGOS_DIR.rglob("*.pdf")) if CARGOS_DIR.exists() else []
    print(f"[QA 3] PDFs físicos na pasta /cargos: {len(arquivos_pdf_fisicos)}")
    print(f"[QA 3] Textos Extraídos (Tabela Cargos): {total_cargos_extraidos}")
    
    if len(arquivos_pdf_fisicos) != total_cargos_extraidos:
        print("[ALERTA] Diferença entre PDFs na pasta e PDFs no BD.")
    else:
        print("[OK] Todos os PDFs estão com texto mapeado no BD.")
        
    print("\n====================================")
    print("[FIM] QA CONCLUÍDO")
    print("====================================")
    
    conn.close()

if __name__ == "__main__":
    run_integrity_check()
