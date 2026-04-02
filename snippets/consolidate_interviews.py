import zipfile
import xml.etree.ElementTree as ET
import os
import csv
import re

# Configurações
EXCEL_PATH = "lista de entrevistas.xlsx"
TRANSCRICOES_DIR = "05. Transcrições Integrais"
OUTPUT_CSV = "consolidado_entrevistas_motiva.csv"

def get_shared_strings(zip_ref):
    try:
        with zip_ref.open('xl/sharedStrings.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
            return [t.text for t in root.findall('.//ns:t', ns)]
    except KeyError:
        return []

def read_excel_data(file_path):
    data = []
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        shared_strings = get_shared_strings(zip_ref)
        try:
            with zip_ref.open('xl/worksheets/sheet1.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                
                # Mapeamento de colunas (A=0, B=1, ...)
                # ['entrevista_id', 'Nome', 'Cargo', 'Diretoria', 'Plataforma', 'Área', 'Nível', 'Data', 'Entrevista']
                rows = root.findall('.//ns:row', ns)
                header_row = rows[0]
                # Skip header
                for row_elem in rows[1:]:
                    row_dict = {}
                    cells = row_elem.findall('ns:c', ns)
                    for c in cells:
                        ref = c.get('r')
                        col = re.match(r'([A-Z]+)', ref).group(1)
                        v_elem = c.find('ns:v', ns)
                        if v_elem is not None:
                            val = v_elem.text
                            if c.get('t') == 's':
                                val = shared_strings[int(val)] if int(val) < len(shared_strings) else val
                            row_dict[col] = val
                    data.append(row_dict)
        except Exception as e:
            print(f"Erro ao ler Excel: {e}")
    return data

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
    sistemas_encontrados = [s for s in sistemas_keywords if s.lower() in text.lower()]
    
    # Busca por nomes (Interface) - Simplificada
    interfaces = re.findall(r'[A-Z][a-z]+ [A-Z][a-z]+', text)
    interfaces = list(set([i for i in interfaces if len(i) > 8 and i not in ["Paulo Cesar", "Priscila Galindo", "Vitor Pryzbeuka"]]))[:5]
    
    # Resumo Executivo (Primeiras linhas ou extrato)
    resumo = text[:300].replace("\n", " ") + "..."
    
    # Dores/Desafios (Keywords)
    dores_keywords = ["dificuldade", "desafio", "gargalo", "problema", "erro", "demora", "manual", "impossível", "limitação"]
    dores_encontradas = [d for d in dores_keywords if d.lower() in text.lower()]
    
    return resumo, ", ".join(sistemas_encontrados), ", ".join(interfaces), ", ".join(dores_encontradas)

def run_consolidation():
    print("Iniciando consolidação...")
    excel_data = read_excel_data(EXCEL_PATH)
    files = os.listdir(TRANSCRICOES_DIR)
    
    results = []
    
    for i, row in enumerate(excel_data):
        full_name = row.get('B', '')
        if not full_name or full_name == '0': continue
        
        print(f"Processando ({i+1}/{len(excel_data)}): {full_name}")
        
        # Match file
        matched_file = None
        name_parts = full_name.lower().split()
        for f in files:
            f_lower = f.lower()
            if len(name_parts) >= 2:
                if name_parts[0] in f_lower and name_parts[-1] in f_lower:
                    matched_file = f
                    break
        
        text = ""
        if matched_file:
            text = extract_text_from_docx(os.path.join(TRANSCRICOES_DIR, matched_file))
        
        resumo, sistemas, interfaces, dores = analyze_content(text)
        
        # Construir linha final
        final_row = {
            'entrevista_id': row.get('A', ''),
            'Nome': full_name,
            'Cargo': row.get('C', ''),
            'Diretoria': row.get('D', ''),
            'Plataforma': row.get('E', ''),
            'Área': row.get('F', ''),
            'Nível': row.get('G', ''),
            'Data': row.get('H', ''),
            'Entrevista': row.get('I', ''),
            'Resumo Executivo': resumo,
            'Sistemas Citados': sistemas,
            'Interfaces Principais': interfaces,
            'Principais Dores/Desafios': dores
        }
        results.append(final_row)

    # Escrever CSV
    keys = results[0].keys()
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8-sig') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys, delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(results)
    
    print(f"\nSucesso! Arquivo gerado: {OUTPUT_CSV}")

if __name__ == "__main__":
    run_consolidation()
