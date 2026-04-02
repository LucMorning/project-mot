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

# ── API / IA ───────────────────────────────────────────────────────────
AI_PROVIDER = "gemini"  # "openai" | "gemini" | "anthropic" | "ollama"
AI_MODEL    = "gemini-2.0-flash"  # Modelos disponíveis: gemini-2.0-flash, gemini-2.5-flash
AI_API_KEY_ENV = "GEMINI_API_KEY"
AI_MAX_RETRIES = 3
AI_RETRY_DELAY = 5  # segundos

# Pipeline Multi-Etapas
BATCH_SIZE = 3  # Número de entrevistados processados em paralelo
CONTEXT_INSIGHTS_LIMIT = 15  # Número de insights anteriores usados como contexto

# ── CADEIA DE VALOR (7 ETAPAS) ─────────────────────────────────────────
CADEIA_VALOR = {
    "1. Novos Negócios & Demandas": ["abertura", "demanda", "aprovacao", "viabilidade", "novo negócio", "proposta"],
    "2. Orçamento": ["orçamento", "budget", "custos", "capex", "estimativa", "valor"],
    "3. Estruturação (Plan/Custo)": ["planejamento", "cronograma", "eap", "wbs", "físico", "financeiro", "compor 90", "prisma", "project", "p6"],
    "4. Contratação & Execução": ["contrato", "aditivo", "compras", "coupa", "netlex", "flexchain", "docusign", "suprimentos"],
    "5. Medição": ["medição", "boletim", "rdo", "relatório diário", "conecta", "fulcrum", "kartado", "validação"],
    "6. Tendência": ["tendência", "projeção", "forecast", "risco", "archer", "bw", "bpc", "power bi"],
    "7. Fiscal (NF) & Pagamento": ["nota fiscal", "nf", "pagamento", "v360", "atlas", "conciliação", "fi", "ap"],
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
    "Governança de Portfólio": ["governana", "priorizao", "portflio", "pipeline", "aprovao", "alocao", "investimento"],
    "Ciclo de Vida e Gates": ["ciclo", "gates", "gate", "fase", "viabilidade", "planejamento", "execuo"],
    "PMO e Plataformas": ["pmo", "plataforma", "ferramenta", "gesto", "acompanhamento"],
    "Monitoramento Físico-Financeiro": ["custo", "prazo", "fsico", "financeiro", "orcamento", "capex", "medio"],
    "Tecnologia e Dados": ["sistema", "integrao", "dashboard", "power bi", "relatrio", "conector", "excel", "manual", "erro de dado"],
    "Arquitetura de Sistemas": ["sap", "archer", "sic", "vlt", "ferramenta", "software", "api", "banco de dados"],
    "Gestão Contratual": ["contrato", "pleito", "reivindicao", "jurdico", "faturamento", "fornecedor", "aditivo", "reajuste"],
    "Processos e Procedimentos": ["norma", "manual", "procedimento", "burocracia", "fluxo", "padro", "instruo"],
    "Gestão de Mudança e Pessoas": ["comunicao", "equipe", "treinamento", "capacitao", "cultura", "resistncia", "mudana"],
    "Riscos e Compliance": ["risco", "auditoria", "compliance", "mitigao", "controle", "falha", "segurana"]
}
