"""
DOCX Reader - Extrai texto de arquivos .docx sem dependências externas.

Usa zipfile para ler o XML interno do DOCX.
"""
import zipfile
import xml.etree.ElementTree as ET
import os


def extract_text_from_docx(file_path: str) -> str:
    """
    Extrai texto bruto de um arquivo .docx.

    Args:
        file_path: Caminho para o arquivo .docx

    Returns:
        Texto extraído ou string vazia em caso de erro
    """
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


if __name__ == "__main__":
    # Teste rápido
    import sys
    if len(sys.argv) > 1:
        result = extract_text_from_docx(sys.argv[1])
        print(f"Extraído: {len(result)} caracteres")
        print(result[:500])
