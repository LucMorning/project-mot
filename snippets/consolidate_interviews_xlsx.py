import openpyxl
from openpyxl import load_workbook
from openpyxl.styles import Font, Fill, Alignment, PatternFill, Border, Side
import zipfile
import xml.etree.ElementTree as ET
import os
import re

# Configurações
EXCEL_TEMPLATE = "lista de entrevistas.xlsx"
TRANSCRICOES_DIR = "05. Transcrições Integrais"
OUTPUT_XLSX = "consolidado_entrevistas_motiva.xlsx"

def extract_text_from_docx(file_path):
    if not os.path.exists(file_path): return ""
    text = []
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            with zip_ref.open('word/document.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                for p in root.findall('.//w:p', ns):
                    para = "".join([t.text for t in p.findall('.//w:t', ns) if t.text])
                    if para: text.append(para)
    except: pass
    return "\n".join(text)

def analyze_content(text):
    if not text: return "Transcrição não encontrada", "", "", ""
    
    # Sistemas comuns citados
    sistemas_keywords = ["Archer", "SAP", "SIC", "VLT", "RDO", "RT", "Jacket", "Excel", "Outlook", "Teams"]
    sistemas_encontrados = sorted(list(set([s for s in sistemas_keywords if s.lower() in text.lower()])))
    
    # Busca por nomes (Interface) - Simplificada
    interfaces = re.findall(r'[A-Z][a-z]+ [A-Z][a-z]+', text)
    interfaces = list(set([i for i in interfaces if len(i) > 8 and i not in ["Paulo Cesar", "Priscila Galindo", "Vitor Pryzbeuka"]]))[:5]
    
    # Resumo Executivo (Skip metadata lines)
    lines = text.split("\n")
    cleaned_lines = [l for l in lines if "iniciou a transcrição" not in l.lower() and "Gravação de Reunião" not in l and len(l) > 10]
    resumo = " ".join(cleaned_lines[:5])[:500] + "..." if cleaned_lines else "Resumo não disponível"
    
    # Dores/Desafios (Keywords)
    dores_keywords = ["dificuldade", "desafio", "gargalo", "problema", "erro", "demora", "manual", "impossível", "limitação"]
    dores_encontradas = sorted(list(set([d for d in dores_keywords if d.lower() in text.lower()])))
    
    return resumo, ", ".join(sistemas_encontrados), ", ".join(interfaces), ", ".join(dores_encontradas)

def run_consolidation_xlsx():
    print("Iniciando consolidação em formato Excel (XLSX)...")
    
    # Carregar o template (original)
    wb = load_workbook(EXCEL_TEMPLATE)
    ws = wb.active
    
    # Definir novas colunas
    new_cols = [
        "Resumo Executivo",
        "Sistemas Citados",
        "Interfaces Principais",
        "Principais Dores/Desafios"
    ]
    
    last_col = ws.max_column
    
    # Estilo para os novos cabeçalhos (baseado no estilo da última coluna existente)
    template_cell = ws.cell(row=1, column=last_col)
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid") # Um azul bonito
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    for i, col_name in enumerate(new_cols):
        cell = ws.cell(row=1, column=last_col + i + 1, value=col_name)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
    
    # Listar arquivos
    files = os.listdir(TRANSCRICOES_DIR)
    
    # Processar linhas (assumindo que a coluna B tem o Nome)
    for row_idx in range(2, ws.max_row + 1):
        full_name = ws.cell(row=row_idx, column=2).value # Coluna B
        if not full_name or str(full_name) == '0': continue
        
        print(f"Processando: {full_name}")
        
        # Match file (mesma lógica)
        matched_file = None
        name_parts = str(full_name).lower().split()
        for f in files:
            f_lower = f.lower()
            if len(name_parts) >= 2:
                if name_parts[0] in f_lower and name_parts[-1] in f_lower:
                    matched_file = f
                    break
            elif len(name_parts) == 1:
                if name_parts[0] in f_lower:
                    matched_file = f
                    break
        
        text = ""
        if matched_file:
            text = extract_text_from_docx(os.path.join(TRANSCRICOES_DIR, matched_file))
        
        resumo, sistemas, interfaces, dores = analyze_content(text)
        
        # Inserir dados nas novas colunas
        ws.cell(row=row_idx, column=last_col + 1, value=resumo)
        ws.cell(row=row_idx, column=last_col + 2, value=sistemas)
        ws.cell(row=row_idx, column=last_col + 3, value=interfaces)
        ws.cell(row=row_idx, column=last_col + 4, value=dores)
        
        # Alinhamento vertical superior para melhor leitura
        for i in range(1, 5):
            ws.cell(row=row_idx, column=last_col + i).alignment = Alignment(vertical="top", wrap_text=True)

    # Configurações Dinâmicas de Estilo
    # 1. Ajustar largura das novas colunas
    ws.column_dimensions[openpyxl.utils.get_column_letter(last_col + 1)].width = 50 # Resumo
    ws.column_dimensions[openpyxl.utils.get_column_letter(last_col + 2)].width = 25 # Sistemas
    ws.column_dimensions[openpyxl.utils.get_column_letter(last_col + 3)].width = 30 # Interfaces
    ws.column_dimensions[openpyxl.utils.get_column_letter(last_col + 4)].width = 30 # Dores
    
    # 2. Congelar painel (se não estiver)
    ws.freeze_panes = "A2"
    
    # 3. Adicionar Filtros
    ws.auto_filter.ref = ws.dimensions

    # Salvar
    wb.save(OUTPUT_XLSX)
    print(f"\nSucesso! Arquivo Excel formatado gerado: {OUTPUT_XLSX}")

if __name__ == "__main__":
    run_consolidation_xlsx()
