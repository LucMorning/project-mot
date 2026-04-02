import zipfile
import xml.etree.ElementTree as ET
import os
import re

def get_text_from_docx(file_path):
    text = []
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        with zip_ref.open('word/document.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            for p in root.findall('.//w:p', ns):
                para = "".join([t.text for t in p.findall('.//w:t', ns) if t.text])
                if para:
                    text.append(para)
    return text

def find_file_and_extract(pattern, folder):
    regex = re.compile(pattern, re.IGNORECASE)
    for f in os.listdir(folder):
        if regex.search(f):
            full_path = os.path.join(folder, f)
            print(f"Lendo arquivo: {f}")
            return get_text_from_docx(full_path)
    return None

if __name__ == "__main__":
    folder = "05. Transcrições Integrais"
    # Procurando por Flavio Pimentel
    content = find_file_and_extract(r"Fl.vio.*Pimentel", folder)
    if content:
        for line in content:
            print(line)
    else:
        print("Arquivo não encontrado.")
