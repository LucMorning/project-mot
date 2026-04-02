# Setup OCR para PDFs Escaneados

O módulo `src/utils/pdf_reader.py` suporta extração de texto de PDFs escaneados usando OCR.

## Instalação das Dependências Python

```bash
pip install -r requirements.txt
```

## Instalação do Tesseract OCR

O Tesseract precisa ser instalado no sistema operacional.

### Windows

```powershell
# Usando Chocolatey
choco install tesseract

# Ou baixar manualmente:
# https://github.com/UB-Mannheim/tesseract/wiki
```

Caminho padrão: `C:\Program Files\Tesseract-OCR\tesseract.exe`

### macOS

```bash
brew install tesseract
brew install tesseract-lang  # Pacotes de idiomas adicionais
```

### Linux (Debian/Ubuntu)

```bash
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-por  # Português
sudo apt-get install tesseract-ocr-eng  # Inglês
```

### Linux (Fedora/RHEL)

```bash
sudo dnf install tesseract
sudo dnf install tesseract-langpack-por
```

## Uso

```python
from src.utils.pdf_reader import read_pdf

# PDF com texto (método automático)
result = read_pdf("cargo.pdf")
print(result.text)
print(f"Método: {result.method}")

# Forçar OCR (para PDFs escaneados)
result = read_pdf("escaneado.pdf", prefer_ocr=True)
```

## Troubleshooting

**Erro: `tesseract is not installed`**
- Instale o Tesseract conforme instruções acima

**Erro: `tesseract.exe not found` (Windows)**
- Verifique o caminho em `src/utils/pdf_reader.py` linha 128
- Ajuste para seu caminho de instalação

**OCR com baixa precisão**
- Aumente o DPI: `convert_from_path(pdf_path, dpi=300)`
- Use imagem pré-processada (contraste, grayscale)
