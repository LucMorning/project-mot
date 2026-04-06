"""
Extract PDF Roles Pipeline - VERSÃO 110% (MULTI-PAGE CROSS-FLOW)
Finalizada para o Diagnóstico As-Is da Motiva.
"""
import re
import unicodedata
import pdfplumber
from pathlib import Path
from src.config import CARGOS_DIR, DB_PATH
from src.database.repositories import CargosRepository

def strip_accents(s: str) -> str:
    if not s: return ""
    return str(''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn'))

def clean_org_text(text: str) -> str:
    if not text: return ""
    # Remove rótulos, aspas e números de página isolados que podem vir no cross-page
    text = re.sub(r'TITULO DO CARGO|MEDIATO|IMEDIATO|SUPERIOR|5\.|ORGANOGRAMA|"', '', text, flags=re.IGNORECASE)
    # Remove rodapés comuns (ex: Página 1 de 2)
    text = re.sub(r'PAGINA\s+\d+\s+DE\s+\d+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^\s*[\-\.]+\s*', '', text)
    text = re.sub(r'\s*[\-\.]+\s*$', '', text)
    return text.strip()

def get_orphan_greedy_precision(after_text: str) -> str:
    """Busca órfãos em fluxo contínuo."""
    if not after_text: return ""
    allowed = [
        "E", "DE", "DA", "DO", "DADOS", "TECNOLOGIA", "RISCOS", "INVESTIDORES", 
        "SUSTENTABILIDADE", "COMPLIANCE", "SEGUROS", "FISCAL", "PLANEJAMENTO", 
        "GOVERNANCA", "CONTABILIDADE", "CONTROLADORIA", "RELACOES", "SISTEMAS",
        "PROCESSOS", "ESTRATEGIA", "INOVACAO", "JURIDICO", "CAPEX", "SALA", "CONTROLE"
    ]
    barriers = [
        "GERENTE", "DIRETOR", "VICE", "COORDENADOR", "SUPERVISOR", "CONSULTOR", 
        "ANALISTA", "ASSISTENTE", "TECNICO", "AUXILIAR", "ESTAGIARIO", "PRESIDENTE",
        "EXECUTIVO", "ARQUITETO", "ESPECIALISTA"
    ]
    words = after_text.split()
    captured = []
    for w in words:
        w_clean = re.sub(r'[^A-Z]', '', w)
        if not w_clean: continue
        if w_clean in barriers: break
        if w_clean in allowed or len(captured) < 2:
            captured.append(w)
        else: break
    return " ".join(captured).strip()

def parse_cargo_multi_page(pdf_path: str) -> dict:
    """
    Concatena o fluxo de texto de múltiplas páginas para lidar com quebras de organograma.
    """
    res = {
        "titulo_cargo": "",
        "superior_mediato": "",
        "superior_imediato": "",
        "negocio_plataforma": "",
        "diretoria": "",
        "area_atuacao": ""
    }
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # --- CAPTURA DE FLUXO UNIFICADO (Páginas 1 a 3) ---
            full_text_list = []
            for page in pdf.pages[:3]:
                page_text = page.extract_text(layout=True, x_tolerance=5)
                if page_text:
                    # Remove ruidos de quebra de página manual
                    clean_page = re.sub(r'\x0c', '', page_text)
                    full_text_list.append(clean_page)
            
            combined_text = "\n".join(full_text_list)
            txt_norm = strip_accents(combined_text).upper()
            clean_flow = " ".join(txt_norm.split())

            # 1. TÍTULO PRIORITÁRIO (SEÇÃO 1)
            m_tit = re.search(r'TITULO\s+DO\s+CARGO\s*[:\-]?\s*(.*?)(?:\n|NEGOCIO|DIRETORIA|AREA|$)', txt_norm)
            if m_tit: 
                tit_raw = m_tit.group(1).strip()
                after_tit = txt_norm.split(tit_raw)[1][:50] if tit_raw in txt_norm else ""
                orphan_tit = get_orphan_greedy_precision(after_tit)
                res["titulo_cargo"] = clean_org_text(tit_raw + " " + orphan_tit)

            # 2. HIERARQUIA MULTI-PÁGINA (Wall-Splitter no Fluxo Unificado)
            label_org = "5. ORGANOGRAMA"
            label_med = "TITULO DO CARGO DO SUPERIOR MEDIATO"
            label_ime = "TITULO DO CARGO DO SUPERIOR IMEDIATO"
            
            # SUPERIOR MEDIATO (Pode estar em páginas diferentes)
            if label_med in clean_flow:
                parts = clean_flow.split(label_med)
                val = parts[0].split(label_org)[-1]
                orphan = get_orphan_greedy_precision(parts[1][:100] if len(parts) > 1 else "")
                res["superior_mediato"] = clean_org_text(val + " " + orphan)
            
            # SUPERIOR IMEDIATO
            if label_ime in clean_flow:
                parts_ime = clean_flow.split(label_ime)
                val_ime = parts_ime[0].split(label_med)[-1]
                # Poda de overlap do Mediato
                parts_med = clean_flow.split(label_med)
                orphan_check = get_orphan_greedy_precision(parts_med[1][:100] if len(parts_med) > 1 else "")
                if orphan_check:
                    val_ime = val_ime.replace(orphan_check, "").strip()

                orphan_ime = get_orphan_greedy_precision(parts_ime[1][:100] if len(parts_ime) > 1 else "")
                res["superior_imediato"] = clean_org_text(val_ime + " " + orphan_ime)

            # 3. ESTRUTURA
            def q_find(pat):
                m = re.search(pat, txt_norm)
                return m.group(1).strip() if m else ""
            res["negocio_plataforma"] = q_find(r'NEGOCIO\s*[\/\\]\s*PLATAFORMA\s*[:\-]?\s*(.*?)\n')
            res["diretoria"] = q_find(r'DIRETORIA\s*[:\-]?\s*(.*?)\n')
            res["area_atuacao"] = q_find(r'AREA\s*[:\-]?\s*(.*?)\n')

    except Exception as e:
        print(f"[ERROR] Multi-page failed: {e}")
    return res

def ingest_cargos():
    repo = CargosRepository(DB_PATH)
    cargo_files = list(CARGOS_DIR.rglob("*.pdf"))
    repo.delete_all()
    count = 0
    for pdf_path in cargo_files:
        parsed = parse_cargo_multi_page(pdf_path)
        titulo = parsed['titulo_cargo'] or pdf_path.stem.upper().replace("_", " ")

        repo.insert({
            'titulo_cargo': titulo,
            'arquivo_pdf': pdf_path.name,
            'texto_extraido': "",
            'negocio_plataforma': parsed['negocio_plataforma'] or "CORPORATIVO",
            'diretoria': parsed['diretoria'],
            'area_atuacao': parsed['area_atuacao'],
            'superior_mediato': parsed['superior_mediato'],
            'superior_imediato': parsed['superior_imediato']
        })
        count += 1
    print(f"[SUCCESS] Ingested {count} PDF roles with Cross-Page Context Awareness.")

if __name__ == "__main__": ingest_cargos()
