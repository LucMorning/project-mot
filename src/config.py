"""
Configuração central do projeto MOTIVA.
Todos os paths, constantes e dicionários ficam aqui.
"""
from pathlib import Path

# ── PATHS ──────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent

# Dados de entrada
DATA_DIR         = PROJECT_ROOT / "data"
RAW_DIR          = DATA_DIR / "raw"
TRANSCRICOES_DIR = DATA_DIR / "transcricoes"
CARGOS_DIR       = DATA_DIR / "cargos"

# Dados de saída
OUTPUT_DIR       = DATA_DIR / "output"
EXCEL_OUTPUT_DIR = OUTPUT_DIR / "excel"
MD_OUTPUT_DIR    = OUTPUT_DIR / "markdown"
FICHAS_DIR       = MD_OUTPUT_DIR / "fichas"
CARGOS_MD_DIR    = MD_OUTPUT_DIR / "cargos"
PPTX_OUTPUT_DIR  = OUTPUT_DIR / "pptx"
DB_PATH          = OUTPUT_DIR / "motiva.db"

# Arquivos de referência
LISTA_ENTREVISTAS = RAW_DIR / "lista_entrevistas.xlsx"
RELATORIO_TI      = RAW_DIR / "relatorio_sistemas_ti_romulo.xlsx"

# ── PADRÕES DE NOME DE ARQUIVO DE TRANSCRIÇÃO ─────────────────
TRANSCRIPT_PREFIXES   = ["entrevista_as_is_", "aprofundamento_"]
TRANSCRIPT_EXTENSION  = ".docx"

# ── API / IA ───────────────────────────────────────────────────────────
AI_PROVIDER    = "gemini"  # "openai" | "gemini" | "anthropic" | "ollama"
AI_MODEL       = "gemini-flash-latest"  # Modelos disponíveis: gemini-flash-latest, gemini-pro-latest
AI_API_KEY_ENV = "GEMINI_API_KEY"
AI_MAX_RETRIES = 3
AI_RETRY_DELAY = 5         # segundos entre retries
AI_TEMPERATURE = 0.1       # temperatura para geração estruturada (JSON mode)
AI_AGENT_SLEEP = 2         # segundos entre chamadas de agente (rate limit intra-chunk)

# Pipeline Multi-Etapas
BATCH_SIZE             = 3   # Número de chunks processados em paralelo (via asyncio.gather)
BATCH_INTERVIEWEES     = 5   # Número de entrevistados buscados por rodada (SQL LIMIT)
BATCH_SLEEP            = 10  # Segundos entre batches de chunks
BATCH_ERROR_THRESHOLD  = 5   # Máximo de erros consecutivos (rate limit) antes de parar
CONTEXT_INSIGHTS_LIMIT = 15  # Número de insights anteriores usados como contexto

# Filtros e Fallbacks
INVALID_ENTITY_NAMES    = {'N/A', 'NÃO INFORMADO', 'NA', 'NONE', '', 'NI'}
AI_CONFIDENCE_DEFAULT   = 0.9
AI_CONFIDENCE_PROCESS   = 0.95
GLOSSARY_CARGOS_LIMIT   = 30
AGENT_FALLBACK          = 'pain_points'

# ── CHUNKING ────────────────────────────────────────────────────────────
CHUNK_MAX_SIZE     = 15000  # Caracteres por chunk (≈ 3k tokens Gemini Flash)
CHUNK_MIN_SIZE     = 5000   # Tamanho mínimo para um chunk ser persistido
CHUNK_OVERLAP_RATIO = 0.15  # Fração de overlap entre chunks consecutivos

# ── STATUS STRINGS (Single Source of Truth) ─────────────────────────────
class ChunkStatus:
    """Status de análise de um chunk de transcrição (tabela transcricao_chunks)."""
    PENDING = 'pendente'
    DONE    = 'concluido'
    ERROR   = 'erro'

class IntervieweeStatus:
    """Status de revisão de um entrevistado (tabela entrevistados.status_revisao)."""
    PENDING  = 'pendente'
    DONE     = 'concluida'
    EXTRA_QA = 'Extra QA'

# ── MAPEAMENTO DE COLUNAS DO EXCEL ───────────────────────────────────────
EXCEL_HEADER_ROW = 1  # Linha do cabeçalho (dados iniciam na linha seguinte)
EXCEL_COLUMNS = {
    'nome':              2,
    'cargo':             3,
    'diretoria':         4,
    'unidade_negocio':   5,  # era "plataforma" - padronizado com dim_processos
    'area':              6,
    'nivel':             7,
    'dt_entrevista':     8,
    'tipo_entrevista':   9,
}

# ── CADEIA DE VALOR (7 ETAPAS) ─────────────────────────────────────────
CADEIA_VALOR = {
    "Novos Negócios & Demandas":    ["abertura", "demanda", "aprovacao", "viabilidade", "novo negócio", "proposta"],
    "Orçamento":                      ["orçamento", "budget", "custos", "capex", "estimativa", "valor"],
    "Estruturação":                    ["planejamento", "cronograma", "eap", "wbs", "físico", "financeiro", "compor 90", "prisma", "project", "p6"],
    "Contratação & Execução":         ["contrato", "aditivo", "compras", "coupa", "netlex", "flexchain", "docusign", "suprimentos"],
    "Medição":                         ["medição", "boletim", "rdo", "relatório diário", "conecta", "fulcrum", "kartado", "validação"],
    "Tendência":                        ["tendência", "projeção", "forecast", "risco", "archer", "bw", "bpc", "power bi"],
    "Fiscal & Pagamento":              ["nota fiscal", "nf", "pagamento", "v360", "atlas", "conciliação", "fi", "ap"],
}

# ── SISTEMAS (25+ ferramentas identificadas) ──────────────────────────
SISTEMAS_LIST = [
    "SAP PS", "SAP FI", "SAP BW", "SAP BPC", "SAP MM",
    "Prisma", "Project", "P6", "Primavera", "Excel",
    "Compor 90", "Coupa", "Netlex", "Flexchain", "Docusign",
    "Teams", "Kartado", "SharePoint", "Power Apps", "Power BI",
    "Conecta", "Fulcrum", "Archer", "V360", "Atlas",
    "Forms", "SIC", "RDO", "Outlook", "Jacket", "VLT"
]

# ── KEYWORDS DE DORES ─────────────────────────────────────────────────
DORES_KEYWORDS = [
    "manual", "duplicidade", "erro", "demora", "não integra",
    "planilha", "paralelo", "sombra", "falta", "difícil",
    "retrabalho", "gargalo", "dificuldade", "impossível",
    "limitação", "burocracia", "desafio", "problema",
]

# ── TEMAS PARA ANÁLISE TEMÁTICA ───────────────────────────────────────
TEMAS_MAP = {
    "Governança de Portfólio": ["governança", "priorização", "portfólio", "pipeline", "aprovação", "alocação", "investimento"],
    "Ciclo de Vida e Gates": ["ciclo", "gates", "gate", "fase", "viabilidade", "planejamento", "execução"],
    "PMO e Plataformas": ["pmo", "plataforma", "ferramenta", "gestão", "acompanhamento"],
    "Monitoramento Físico-Financeiro": ["custo", "prazo", "físico", "financeiro", "orçamento", "capex", "médio"],
    "Tecnologia e Dados": ["sistema", "integração", "dashboard", "power bi", "relatório", "conector", "excel", "manual", "erro de dado"],
    "Arquitetura de Sistemas": ["sap", "archer", "sic", "vlt", "ferramenta", "software", "api", "banco de dados"],
    "Gestão Contratual": ["contrato", "pleito", "reivindicação", "jurídico", "faturamento", "fornecedor", "aditivo", "reajuste"],
    "Processos e Procedimentos": ["norma", "manual", "procedimento", "burocracia", "fluxo", "padrão", "instrução"],
    "Gestão de Mudança e Pessoas": ["comunicação", "equipe", "treinamento", "capacitação", "cultura", "resistência", "mudança"],
    "Riscos e Compliance": ["risco", "auditoria", "compliance", "mitigação", "controle", "falha", "segurança"]
}

# ── UNIDADES DE NEGÓCIO (Domínio centralizado) ───────────────────────────
# Usado em: stg_entrevistados.plataforma e dim_processos.unidade_negocio
UNIDADES_NEGOCIO = [
    "CORPORATIVO",
    "TRILHOS",
    "RODOVIAS",
]


def normalize_unidade(value: str) -> str | None:
    """
    Normaliza nome de unidade de negócio para formato padrão UPPERCASE.

    Aplica fuzzy match para variações como "trilhos", "TRILHOS", "Trilhos",
    garantindo consistência entre stg_entrevistados.plataforma e
    dim_processos.unidade_negocio.

    Args:
        value: Valor bruto do Excel/relatório

    Returns:
        Nome normalizado (UPPERCASE) ou None se vazio
    """
    if not value or str(value).strip() in ["", "0", "None", "NA", "N/A"]:
        return None

    normalized = str(value).strip().upper()

    # Fuzzy match para variações comuns
    for unidade in UNIDADES_NEGOCIO:
        if unidade in normalized or normalized in unidade:
            return unidade

    # Fallback: retorna o valor normalizado (útil para descobrir novos valores)
    return normalized
