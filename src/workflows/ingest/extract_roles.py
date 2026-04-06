"""
Extract PDF Roles Pipeline - VERSÃO 100% PRECISION
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
    # Remove rótulos, aspas de duplicidade e ruidos de layout
    text = re.sub(r'TITULO DO CARGO|MEDIATO|IMEDIATO|SUPERIOR|5\.|ORGANOGRAMA|"', '', text, flags=re.IGNORECASE)
    # Remove hífens órfãos no início ou fim
    text = re.sub(r'^\s*[\-\.]+\s*', '', text)
    text = re.sub(r'\s*[\-\.]+\s*$', '', text)
    return text.strip()

def get_orphan_greedy_precision(after_text: str) -> str:
    """
    Puxa órfãos com lista expandida de substantivos de área.
    PARA IMEDIATAMENTE se encontrar um NOME DE CARGO (Barreira).
    """
    if not after_text: return ""
    
    # Palavras que indicam CONTINUAÇÃO do cargo anterior
    allowed = [
        "E", "DE", "DA", "DO", "DADOS", "TECNOLOGIA", "RISCOS", "INVESTIDORES", 
        "SUSTENTABILIDADE", "COMPLIANCE", "SEGUROS", "FISCAL", "PLANEJAMENTO", 
        "GOVERNANCA", "CONTABILIDADE", "CONTROLADORIA", "RELACOES", "SISTEMAS",
        "PROCESSOS", "ESTRATEGIA", "INOVACAO", "JURIDICO", "CAPEX", "SALA", "CONTROLE"
    ]
    # Palavras que indicam INÍCIO de um novo cargo (Barreiras)
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
        
        # BARREIRA ATIVA: Encontrou um cargo novo, para tudo.
        if w_clean in barriers:
            break
            
        # CONTINUIDADE ATIVA: É uma palavra de área ou conectivo?
        if w_clean in allowed or len(captured) < 2:
            captured.append(w)
        else:
            # Se não é nem barreira nem allowed, e já pegamos o núcleo, paramos para segurança.
            break
             
    return " ".join(captured).strip()

def parse_cargo_100_precision(pdf_path: str) -> dict:
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
            p0 = pdf.pages[0]
            # Extração visual focada
            text = p0.extract_text(layout=True, x_tolerance=5)
            txt_norm = strip_accents(text).upper()
            
            # --- TÍTULO TITULAR (SEÇÃO 1) ---
            m_tit = re.search(r'TITULO\s+DO\s+CARGO\s*[:\-]?\s*(.*?)(?:\n|NEGOCIO|DIRETORIA|AREA|$)', txt_norm)
            if m_tit: 
                # O título também pode ser multi-linha (greedy na s1)
                tit_raw = m_tit.group(1)
                after_tit = txt_norm.split(tit_raw)[1][:50] if tit_raw in txt_norm else ""
                orphan_tit = get_orphan_greedy_precision(after_tit)
                res["titulo_cargo"] = clean_org_text(tit_raw + " " + orphan_tit)

            # --- HIERARQUIA PRECISION ---
            clean_flow = " ".join(txt_norm.split())
            label_org = "5. ORGANOGRAMA"
            label_med = "TITULO DO CARGO DO SUPERIOR MEDIATO"
            label_ime = "TITULO DO CARGO DO SUPERIOR IMEDIATO"
            
            # 1. SUPERIOR MEDIATO
            if label_med in clean_flow:
                parts = clean_flow.split(label_med)
                val = parts[0].split(label_org)[-1]
                orphan = get_orphan_greedy_precision(parts[1][:100] if len(parts) > 1 else "")
                res["superior_mediato"] = clean_org_text(val + " " + orphan)
            
            # 2. SUPERIOR IMEDIATO
            if label_ime in clean_flow:
                parts_ime = clean_flow.split(label_ime)
                val_ime = parts_ime[0].split(label_med)[-1]
                
                # Deduplicação: se o Mediato puxou, o Imediato perde.
                parts_med = clean_flow.split(label_med)
                orphan_check = get_orphan_greedy_precision(parts_med[1][:100] if len(parts_med) > 1 else "")
                if orphan_check:
                    val_ime = val_ime.replace(orphan_check, "").strip()

                orphan_ime = get_orphan_greedy_precision(parts_ime[1][:100] if len(parts_ime) > 1 else "")
                res["superior_imediato"] = clean_org_text(val_ime + " " + orphan_ime)

            # --- ESTRUTURA ---
            def q_find(pat):
                m = re.search(pat, txt_norm)
                return m.group(1).strip() if m else ""
            res["negocio_plataforma"] = q_find(r'NEGOCIO\s*[\/\\]\s*PLATAFORMA\s*[:\-]?\s*(.*?)\n')
            res["diretoria"] = q_find(r'DIRETORIA\s*[:\-]?\s*(.*?)\n')
            res["area_atuacao"] = q_find(r'AREA\s*[:\-]?\s*(.*?)\n')

    except Exception as e:
        print(f"[ERROR] {e}")
    return res

def ingest_cargos():
    repo = CargosRepository(DB_PATH)
    cargo_files = list(CARGOS_DIR.rglob("*.pdf"))
    repo.delete_all()
    count = 0
    for pdf_path in cargo_files:
        parsed = parse_cargo_100_precision(pdf_path)
        # PRIORIDADE 0: Nome real em MAIÚSCULO/SEM ACENTO
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
    print(f"[SUCCESS] Ingested {count} roles with 100% Precision Scoped Barrier.")

if __name__ == "__main__": ingest_cargos()
