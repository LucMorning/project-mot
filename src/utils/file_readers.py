import zipfile
import xml.etree.ElementTree as ET
import os

def extract_text_from_docx(file_path: str) -> str:
    """Extrai texto bruto de um arquivo .docx sem usar dependências externas."""
    if not os.path.exists(file_path):
        return ""
    
    text = []
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            with zip_ref.open('word/document.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                for p in root.findall('.//w:p', ns):
                    para = "".join([t.text for t in p.findall('.//w:t', ns) if t.text])
                    if para:
                        text.append(para)
    except Exception as e:
        print(f"Erro ao ler docx {file_path}: {e}")
        return ""
        
    return "\n".join(text)

def read_pdf_plumber(file_path: str) -> str:
    """Extrai texto legível de PDF utilizando pdfplumber.
    Isso é crítico para lermos os PDFs de Cargo e alimentarmos a IA.
    """
    if not os.path.exists(file_path):
        return ""
    
    try:
        import pdfplumber
        text = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        return "\n".join(text)
    except ImportError:
        print("Biblioteca pdfplumber não instalada. Instale via requirements.txt")
        return ""
    except Exception as e:
        print(f"Erro ao ler pdf {file_path}: {e}")
        return ""
