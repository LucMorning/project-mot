"""
Leitor de PDFs com suporte a OCR para extração de texto.
Lida com PDFs com texto selecionável e PDFs escaneados (imagens).
"""
import os
from pathlib import Path
from typing import Optional, Literal
from dataclasses import dataclass


@dataclass
class PDFExtractionResult:
    """Resultado da extração de PDF."""
    text: str
    method: Literal["text", "ocr", "mixed"]
    num_pages: int
    has_images: bool = False
    confidence: float = 1.0


class PDFReader:
    """
    Leitor de PDFs com fallback para OCR.

    Prioridade de métodos:
    1. pdfplumber - para PDFs com texto (rápido)
    2. pymupdf/fitz - fallback para texto
    3. pdf2image + pytesseract - OCR para PDFs escaneados
    """

    def __init__(self, prefer_ocr: bool = False):
        self.prefer_ocr = prefer_ocr
        self._plumber = None
        self._fitz = None
        self._ocr_available = False

        self._init_backends()

    def _init_backends(self):
        """Inicializa as bibliotecas disponíveis."""
        try:
            import pdfplumber
            self._plumber = pdfplumber
        except ImportError:
            pass

        try:
            import fitz  # PyMuPDF
            self._fitz = fitz
        except ImportError:
            pass

        try:
            import pytesseract
            from pdf2image import convert_from_path
            self._pytesseract = pytesseract
            self._convert_from_path = convert_from_path
            self._ocr_available = True
        except ImportError:
            self._ocr_available = False

    def read(self, pdf_path: Path | str) -> PDFExtractionResult:
        """
        Lê um PDF e retorna o texto extraído.

        Tenta extrair texto primeiro; se falhar ou pouco texto for encontrado,
        usa OCR como fallback.
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF não encontrado: {pdf_path}")

        # Tenta extração direta de texto primeiro
        if not self.prefer_ocr:
            result = self._extract_text(pdf_path)
            if result and len(result.strip()) > 100:
                # Texto suficiente, provavelmente não escaneado
                return PDFExtractionResult(
                    text=result,
                    method="text",
                    num_pages=self._count_pages(pdf_path)
                )

        # Fallback para OCR
        if self._ocr_available:
            text = self._extract_ocr(pdf_path)
            return PDFExtractionResult(
                text=text,
                method="ocr",
                num_pages=self._count_pages(pdf_path),
                confidence=0.85
            )

        # Último recurso: pymupdf
        if self._fitz:
            return self._extract_fitz(pdf_path)

        raise RuntimeError(
            "Nenhuma biblioteca de PDF disponível. Instale: "
            "pip install pdfplumber pymupdf pdf2image pytesseract"
        )

    def _extract_text(self, pdf_path: Path) -> str:
        """Extrai texto usando pdfplumber."""
        if not self._plumber:
            return ""

        text_parts = []
        try:
            with self._plumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    text_parts.append(page_text)
        except Exception as e:
            print(f"Erro com pdfplumber: {e}")
            return ""

        return "\n\n".join(text_parts)

    def _extract_fitz(self, pdf_path: Path) -> PDFExtractionResult:
        """Extrai texto usando PyMuPDF (fitz)."""
        doc = self._fitz.open(pdf_path)
        text_parts = []

        for page in doc:
            text_parts.append(page.get_text())

        doc.close()

        return PDFExtractionResult(
            text="\n\n".join(text_parts),
            method="text",
            num_pages=len(text_parts)
        )

    def _extract_ocr(self, pdf_path: Path) -> str:
        """
        Extrai texto usando OCR (pdf2image + pytesseract).

        Nota: Requer Tesseract instalado no sistema.
        Windows: choco install tesseract
        Linux: apt-get install tesseract-ocr
        Mac: brew install tesseract
        """
        # Configura o caminho do Tesseract no Windows se necessário
        if os.name == "nt":
            tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            if os.path.exists(tesseract_path):
                self._pytesseract.pytesseract.tesseract_cmd = tesseract_path

        # Converte PDF para imagens
        images = self._convert_from_path(
            pdf_path,
            dpi=200,
            fmt='png'
        )

        text_parts = []
        for i, img in enumerate(images):
            try:
                page_text = self._pytesseract.image_to_string(
                    img,
                    lang='por+eng',  # Português + Inglês
                    config='--psm 6'  # Assume uma coluna de texto uniforme
                )
                text_parts.append(f"--- PÁGINA {i+1} ---\n{page_text}")
            except Exception as e:
                print(f"Erro no OCR da página {i+1}: {e}")
                text_parts.append(f"--- PÁGINA {i+1} --- [Erro no OCR]")

        return "\n\n".join(text_parts)

    def _count_pages(self, pdf_path: Path) -> int:
        """Conta o número de páginas do PDF."""
        if self._plumber:
            try:
                with self._plumber.open(pdf_path) as pdf:
                    return len(pdf.pages)
            except:
                pass

        if self._fitz:
            try:
                doc = self._fitz.open(pdf_path)
                count = len(doc)
                doc.close()
                return count
            except:
                pass

        return 0

    def is_available(self, method: str = "all") -> bool:
        """Verifica se um método específico está disponível."""
        if method == "text":
            return self._plumber is not None or self._fitz is not None
        if method == "ocr":
            return self._ocr_available
        if method == "all":
            return (
                self._plumber is not None or
                self._fitz is not None or
                self._ocr_available
            )
        return False


# Singleton para reutilização
_default_reader: Optional[PDFReader] = None


def get_reader(prefer_ocr: bool = False) -> PDFReader:
    """Retorna o reader singleton."""
    global _default_reader
    if _default_reader is None:
        _default_reader = PDFReader(prefer_ocr=prefer_ocr)
    return _default_reader


def read_pdf(pdf_path: Path | str, prefer_ocr: bool = False) -> PDFExtractionResult:
    """
    Função conveniente para ler um PDF.

    Args:
        pdf_path: Caminho para o arquivo PDF
        prefer_ocr: Se True, usa OCR diretamente sem tentar extração de texto

    Returns:
        PDFExtractionResult com o texto extraído

    Example:
        >>> from src.utils.pdf_reader import read_pdf
        >>> result = read_pdf("cargo.pdf")
        >>> print(result.text)
        >>> print(f"Método usado: {result.method}")
    """
    reader = get_reader(prefer_ocr=prefer_ocr)
    return reader.read(pdf_path)


# CLI para testes rápidos
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python pdf_reader.py <caminho_pdf> [--ocr]")
        sys.exit(1)

    pdf_file = sys.argv[1]
    use_ocr = "--ocr" in sys.argv

    print(f"Lendo: {pdf_file}")
    print(f"Prefer OCR: {use_ocr}\n")

    reader = PDFReader(prefer_ocr=use_ocr)

    print("Backends disponíveis:")
    print(f"  - pdfplumber: {reader._plumber is not None}")
    print(f"  - pymupdf: {reader._fitz is not None}")
    print(f"  - OCR: {reader._ocr_available}")
    print()

    result = reader.read(pdf_file)

    print(f"Método: {result.method}")
    print(f"Páginas: {result.num_pages}")
    print(f"Confiança: {result.confidence}")
    print(f"\n--- CONTEÚDO ---\n")
    print(result.text[:1000])
    if len(result.text) > 1000:
        print(f"\n... ({len(result.text)} caracteres totais)")
