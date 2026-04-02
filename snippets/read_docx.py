import zipfile
import xml.etree.ElementTree as ET
import os

def read_docx(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return ""

    text = []
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            with zip_ref.open('word/document.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                # The namespace for Word documents is 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
                ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                for p in root.findall('.//w:p', ns):
                    paragraph_text = ""
                    for t in p.findall('.//w:t', ns):
                        paragraph_text += t.text
                    if paragraph_text:
                        text.append(paragraph_text)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return "\n".join(text)

if __name__ == "__main__":
    file_name = "05. Transcrições Integrais/Diagnóstico – Cenário Atual _ Paulo Amaral.docx"
    content = read_docx(file_name)
    print(content)
