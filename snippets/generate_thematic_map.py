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
OUTPUT_XLSX = "diagnostico_consolidado_tematico.xlsx"

# TEMAS E PALAVRAS-CHAVE PARA MAPEAMENTO
TEMAS_MAP = {
    "Governana de Portflio": ["governana", "priorizao", "portflio", "pipeline", "aprovao", "alocao", "investimento"],
    "Ciclo de Vida e Gates": ["ciclo", "gates", "gate", "fase", "viabilidade", "planejamento", "execuo"],
    "PMO e Plataformas": ["pmo", "plataforma", "ferramenta", "gesto", "acompanhamento"],
    "Monitoramento Fsico-Financeiro": ["custo", "prazo", "fsico", "financeiro", "orcamento", "capex", "medio"],
    "Tecnologia e Dados": ["sistema", "integrao", "dashboard", "power bi", "relatrio", "conector", "excel", "manual", "erro de dado"],
    "Arquitetura de Sistemas": ["sap", "archer", "sic", "vlt", "ferramenta", "software", "api", "banco de dados"],
    "Gesto Contratual": ["contrato", "pleito", "reivindicao", "jurdico", "faturamento", "fornecedor", "aditivo", "reajuste"],
    "Processos e Procedimentos": ["norma", "manual", "procedimento", "burocracia", "fluxo", "padro", "instruo"],
    "Gesto de Mudana e Pessoas": ["comunicao", "equipe", "treinamento", "capacitao", "cultura", "resistncia", "mudana"],
    "Riscos e Compliance": ["risco", "auditoria", "compliance", "mitigao", "controle", "falha", "segurana"]
}

SISTEMAS_KEYWORDS = ["SAP", "Archer", "SIC", "VLT", "RDO", "RT", "Jacket", "Excel", "Outlook", "Teams", "Power BI", "P6", "Primavera"]
DORES_KEYWORDS = ["dificuldade", "desafio", "gargalo", "problema", "erro", "demora", "manual", "impossvel", "limitao", "burocracia", "falta de integrao", "retrabalho"]

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

def run_thematic_analysis():
    print("Iniciando Anlise Temtica das Transcries...")
    
    # 1. Mapear Entrevistados a suas reas (Contexto)
    # Vou ler a lista de entrevistas para saber de quem so as dores
    try:
        wb_ref = openpyxl.load_workbook(LISTA_REF)
        ws_ref = wb_ref.active
        mapping_people = {} # Nome -> Area/Cargo
        for r in range(2, ws_ref.max_row + 1):
            name = ws_ref.cell(row=r, column=2).value
            area = ws_ref.cell(row=r, column=6).value
            cargo = ws_ref.cell(row=r, column=3).value
            if name: mapping_people[str(name).lower()] = f"{cargo} ({area})"
    except:
        print("Aviso: No foi possvel carregar o mapeamento de pessoas.")
        mapping_people = {}

    # 2. Processar cada transcrio e agrupar por tema
    temas_results = {tema: {"resumo": [], "sistemas": set(), "dores": set(), "fontes": set()} for tema in TEMAS_MAP}
    
    files = [f for f in os.listdir(TRANSCRICOES_DIR) if f.endswith('.docx')]
    
    for filename in files:
        path = os.path.join(TRANSCRICOES_DIR, filename)
        text = extract_text_from_docx(path)
        if not text: continue
        
        # Identificar o autor (se possível pelo nome do arquivo)
        autor = "Desconhecido"
        for p_name, p_info in mapping_people.items():
            first = p_name.split()[0]
            last = p_name.split()[-1]
            if first in filename.lower() and last in filename.lower():
                autor = p_info
                break

        paragraphs = text.split("\n")
        
        for para in paragraphs:
            if len(para) < 30: continue
            para_lower = para.lower()
            
            # Checar em qual tema o pargrafo se encaixa
            for tema, kws in TEMAS_MAP.items():
                if any(kw in para_lower for kw in kws):
                    # Se achou uma dor
                    if any(dkw in para_lower for dkw in DORES_KEYWORDS):
                        temas_results[tema]["dores"].add(para[:200] + "...")
                        temas_results[tema]["fontes"].add(autor)
                    
                    # Se achou um sistema
                    for skw in SISTEMAS_KEYWORDS:
                        if skw.lower() in para_lower:
                            temas_results[tema]["sistemas"].add(skw)
                    
                    # Adicionar ao resumo do cenário
                    if len(para) > 50 and len(temas_results[tema]["resumo"]) < 10:
                        temas_results[tema]["resumo"].append(para)

    # 3. Gerar o XLSX
    wb = Workbook()
    ws = wb.active
    ws.title = "Diagnstico Temtico"
    
    headers = ["Tema / Disciplina", "Resumo do Cenrio (Insights)", "Dores e Desafios", "Sistemas Citados", "Origem/Impacto (reas)"]
    
    # Estilos
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid") # Azul Escuro
    header_font = Font(bold=True, color="FFFFFF", size=11)
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    top_align = Alignment(vertical="top", wrap_text=True)
    border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

    for col, head in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=head)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align

    current_row = 2
    for tema, data in temas_results.items():
        if not data["dores"] and not data["resumo"]: continue # Pula temas sem dados
        
        resumo_txt = "\n\n".join(data["resumo"][:3]) # Pega os 3 mais relevantes
        dores_list = "\n".join([f"- {d}" for d in list(data["dores"])[:5]])
        sistemas_list = ", ".join(sorted(list(data["sistemas"])))
        fontes_list = ", ".join(sorted(list(data["fontes"])))

        ws.cell(row=current_row, column=1, value=tema).alignment = top_align
        ws.cell(row=current_row, column=2, value=resumo_txt).alignment = top_align
        ws.cell(row=current_row, column=3, value=dores_list).alignment = top_align
        ws.cell(row=current_row, column=4, value=sistemas_list).alignment = top_align
        ws.cell(row=current_row, column=5, value=fontes_list).alignment = top_align
        
        for col in range(1, 6):
            ws.cell(row=current_row, column=col).border = border
            
        current_row += 1

    # Ajuste de larguras
    ws.column_dimensions['A'].width = 25
    ws.column_dimensions['B'].width = 60
    ws.column_dimensions['C'].width = 50
    ws.column_dimensions['D'].width = 20
    ws.column_dimensions['E'].width = 30

    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions

    wb.save(OUTPUT_XLSX)
    print(f"Sucesso! Gerado: {OUTPUT_XLSX}")

if __name__ == "__main__":
    run_thematic_analysis()
