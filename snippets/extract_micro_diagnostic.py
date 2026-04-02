import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
import zipfile
import xml.etree.ElementTree as ET
import os
import re

# CONFIGURAÇÕES
TRANSCRICOES_DIR = "05. Transcrições Integrais"
LISTA_REF = "lista de entrevistas.xlsx"
OUTPUT_XLSX = "diagnostico_as_is_detalhado.xlsx"

# DICIONÁRIO DE SISTEMAS E SUAS "DOENÇAS" COMUNS (Baseado no contexto Motiva)
SISTEMAS_INFO = {
    "SAP": ["ERP principal", "Financeiro", "Contratos"],
    "Archer": ["Gestão de Riscos", "Compliance"],
    "SIC": ["Sistema de Investimentos/Custos"],
    "VLT": ["Especificamente mencionado em contextos de medição?"],
    "RDO": ["Relatório Diário de Obra (Geralmente manual)"],
    "P6": ["Primavera - Cronograma"],
    "Excel": ["A grande planilha de apoio", "Sombra do sistema"],
    "Jacket": ["Sistema específico de acompanhamento?"]
}

# TEMAS PARA "MICRO VISION"
TEMAS_FILTRO = {
    "Integração Sistêmica": ["exportar", "importar", "manual", "digitar", "extrair", "colar", "alimentar", "sistema não fala"],
    "Gargalos de Processo": ["demora", "atraso", "aguardando", "aprovação", "e-mail", "workflow", "parado"],
    "Qualidade do Dado": ["erro", "divergência", "confiança", "duplicidade", "conferir", "bater o dado", "diferença"],
    "Gestão Contratual/Pleitos": ["pleito", "reivindicação", "aditivo", "atraso de obra", "medição", "faturamento"]
}

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
    except: return ""
    return "\n".join(text)

def find_evidence(text):
    evidencias = []
    paragraphs = text.split("\n")
    for i, para in enumerate(paragraphs):
        para_lower = para.lower()
        # Busca por falhas de integração (Sistema A vs Sistema B / Planilha)
        if "excel" in para_lower and any(sys.lower() in para_lower for sys in ["sap", "archer", "p6", "sic"]):
             evidencias.append({"tipo": "Integração Falha", "texto": para.strip()})
        
        # Busca por termos de "Manualidade"
        if any(term in para_lower for term in ["manualmente", "digitado", "e-mail", "e-mails"]):
             if len(para) > 40:
                evidencias.append({"tipo": "Processo Manual", "texto": para.strip()})
                
        # Busca por conflitos/dores específicas
        if any(term in para_lower for term in ["desafio", "dificuldade", "gargalo", "problema"]):
             evidencias.append({"tipo": "Dor/Gargalo", "texto": para.strip()})
             
    return evidencias

def run_micro_diagnostic():
    print("Iniciando Diagnóstico Micro (As-Is)...")
    
    # 1. Mapeamento de Pessoas
    mapping_people = {}
    try:
        wb_ref = openpyxl.load_workbook(LISTA_REF)
        ws_ref = wb_ref.active
        for r in range(2, ws_ref.max_row + 1):
            name = ws_ref.cell(row=r, column=2).value
            area = ws_ref.cell(row=r, column=6).value
            if name: mapping_people[str(name).lower()] = str(area)
    except: pass

    # 2. Processamento
    all_findings = []
    files = [f for f in os.listdir(TRANSCRICOES_DIR) if f.endswith('.docx')]
    
    for filename in files:
        path = os.path.join(TRANSCRICOES_DIR, filename)
        text = extract_text_from_docx(path)
        if not text: continue
        
        # Identificar Área
        area_found = "Geral"
        for p_name, p_area in mapping_people.items():
            parts = p_name.split()
            if parts[0] in filename.lower() and parts[-1] in filename.lower():
                area_found = p_area
                break
        
        evidencias = find_evidence(text)
        for ev in evidencias:
            all_findings.append({
                "Área": area_found,
                "Tipo de Falha": ev["tipo"],
                "Descrição do Problema (Evidência Real)": ev["texto"],
                "Sistemas Envolvidos": ", ".join([s for s in SISTEMAS_INFO if s.lower() in ev["texto"].lower()])
            })

    # 3. Gerar Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Diagnóstico Micro As-Is"
    
    headers = ["Área Responsável", "Tipo de Problema/Falha", "Evidência Extraída da Transcrição", "Sistemas Impactados"]
    
    header_fill = PatternFill(start_color="C00000", end_color="C00000", fill_type="solid") # Vermelho (para Problemas)
    header_font = Font(bold=True, color="FFFFFF")
    
    for col, head in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=head)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for idx, f in enumerate(all_findings, 2):
        ws.cell(row=idx, column=1, value=f["Área"])
        ws.cell(row=idx, column=2, value=f["Tipo de Falha"])
        ws.cell(row=idx, column=3, value=f["Descrição do Problema (Evidência Real)"])
        ws.cell(row=idx, column=4, value=f["Sistemas Envolvidos"])
        
        for col in range(1, 5):
            ws.cell(row=idx, column=col).alignment = Alignment(vertical="top", wrap_text=True)

    # Ajustes
    ws.column_dimensions['A'].width = 25
    ws.column_dimensions['B'].width = 25
    ws.column_dimensions['C'].width = 80
    ws.column_dimensions['D'].width = 20
    
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    
    wb.save(OUTPUT_XLSX)
    print(f"Diagnóstico Micro concluído: {OUTPUT_XLSX}")

if __name__ == "__main__":
    run_micro_diagnostic()
