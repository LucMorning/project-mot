"""
Schema MOTIVA - Estrutura de tabelas.

CONVENÇÕES DE NOMENCLATURA:
----------------------------
stg_*  = Staging/Dados brutos ingeridos (transcrições, PDFs, metadados)
dim_*  = Dimensões/Catálogos master (etapas, sistemas, processos, domínios/enum)
fato_* = Fatos/Análises da IA (insights, uso de sistemas, relações)

NOTA sobre stg_entrevistados:
------------------------------
  arquivo_cargo_pdf  → ponteiro operacional: qual PDF de cargo corresponde a esta pessoa
  CONTEÚDO (texto) vive em stg_transcricoes.texto_limpo e stg_cargos.texto_extraido,
  nunca duplicado em stg_entrevistados.

  ARQUIVOS de transcrição vivem em stg_arquivos (relação 1:N).

ESTRUTURA:
----------
stg_* → Dados ingeridos brutos (fonte: arquivos)
  • stg_entrevistados  = Metadados do Excel (lista_entrevistas.xlsx)
  • stg_arquivos       = Arquivos de transcrição (1:N com entrevistados)
  • stg_transcricoes   = Transcrições DOCX extraídas
  • stg_chunks         = Chunks para análise IA
  • stg_cargos         = PDFs de cargos extraídos

dim_* → Catálogos master (tabelas de referência)
  • dim_cadeia_valor   = 7 etapas da cadeia de valor (FIXAS)
  • dim_sistemas       = Catálogo oficial de sistemas TI
  • dim_processos      = Catálogo de processos internos

fato_* → Dados analisados pela IA (métricas, descobertas)
  • fato_insights       = Dores/processos identificados
  • fato_sistemas_uso   = Como cada sistema é usado
  • fato_relacoes       = Rede de stakeholders
"""
import sqlite3

# Dados master
# (id, nome_limpo, descricao, ordem)
CADEIA_VALOR_ETAPAS = [
    (1, "Novos Negócios & Demandas",
         "Da abertura, definição da demanda à aprovação",
         1),
    (2, "Orçamento",
         "Definição e aprovação dentro dos custos da estrutura da Motiva",
         2),
    (3, "Estruturação",
         "Planejamento Físico, Econômico e Financeiro",
         3),
    (4, "Contratação & Execução",
         "Gestão de contratos (Compra, Pedido, Aditivos, Garantia, Penalidades, Auditoria) e gestão de prazos, avanças e pleitos",
         4),
    (5, "Medição",
         "Boletim de medição, RDO, Diário de Obra, Validação Técnica e Financeira, Qualidade, Inspeções e Controle de Custo",
         5),
    (6, "Tendência",
         "Projeção das medições do físico, econômico e financeiro; Gestão de Risco",
         6),
    (7, "Fiscal & Pagamento",
         "Processo fiscal entre Motiva e Fornecedor; emissão de NF, conciliação e pagamento (AP/FI)",
         7),
]



def create_database(db_path: str) -> None:
    """Cria estrutura de tabelas MOTIVA."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Deleta tabelas antigas (se existirem)
    tabelas_antigas = [
        "entrevistados", "transcricoes", "transcricao_chunks",
        "insights_ia", "sistemas_uso", "relacoes", "cargos", "sistemas_ti",
        "processos"
    ]
    for tabela in tabelas_antigas:
        cursor.execute(f"DROP TABLE IF EXISTS {tabela}")

    # STAGING
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stg_entrevistados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cargo TEXT,
        diretoria TEXT,
        unidade_negocio TEXT,      -- mesmo domínio que dim_processos.unidade_negocio
        area TEXT,
        nivel TEXT,
        dt_entrevista TEXT,
        tipo_entrevista TEXT,
        arquivo_cargo_pdf TEXT,     -- ponteiro operacional (qual PDF de cargo)
        status_revisao TEXT DEFAULT 'pendente',
        dt_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stg_arquivos_transcricao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_entrevistado INTEGER,
        nome_arquivo TEXT NOT NULL,
        tipo_entrevista TEXT,
        dt_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_entrevistado) REFERENCES stg_entrevistados (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stg_transcricoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_arquivo_transcricao INTEGER,
        texto_completo TEXT,
        texto_limpo TEXT,
        dt_gravacao TEXT,
        dt_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_arquivo_transcricao) REFERENCES stg_arquivos_transcricao (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stg_chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_transcricao INTEGER,
        ordem INTEGER,
        conteudo TEXT,
        checksum TEXT,
        status_analise TEXT DEFAULT 'pendente',
        dt_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_transcricao) REFERENCES stg_transcricoes (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stg_cargos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo_cargo TEXT,
        arquivo_pdf TEXT,
        texto_extraido TEXT,
        negocio_plataforma TEXT,
        diretoria TEXT,
        area_atuacao TEXT,
        missao TEXT,
        desafios TEXT,
        responsabilidades TEXT,
        formacao TEXT,
        idiomas TEXT,
        experiencia TEXT,
        dt_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # DIMENSOES
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dim_cadeia_valor (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL UNIQUE,      -- label limpo sem prefixo numérico
        descricao TEXT,                 -- contexto do que acontece nessa etapa
        ordem INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dim_sistemas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE,
        id_etapa_cadeia INTEGER,
        area_responsavel TEXT,
        fonte TEXT DEFAULT 'relatorio_ti', -- 'relatorio_ti' | 'ia_analise'
        dt_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_etapa_cadeia) REFERENCES dim_cadeia_valor (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dim_dominios (
        tipo TEXT NOT NULL,
        valor TEXT NOT NULL,
        PRIMARY KEY (tipo, valor)
    )
    ''')

    # FATOS
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fato_insights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_entrevistado INTEGER,
        id_bloco INTEGER,
        id_etapa_cadeia INTEGER,
        categoria TEXT,
        subcategoria TEXT,
        descricao TEXT,
        citacao_direta TEXT,
        severidade TEXT,
        linhagem_dados TEXT,           -- Ex: "Origem: Kartado -> Destino: SAP PS"
        risco_estimado TEXT,           -- Ex: "Alto risco de erro manual no Excel"
        area_impactada TEXT,           -- Área da Motiva que sofre a dor
        confianca REAL,
        modelo_ia TEXT,
        dt_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_entrevistado) REFERENCES stg_entrevistados (id),
        FOREIGN KEY (id_bloco) REFERENCES stg_chunks (id),
        FOREIGN KEY (id_etapa_cadeia) REFERENCES dim_cadeia_valor (id),
        CHECK (severidade IN ('Alto', 'Medio', 'Baixo'))
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fato_sistemas_uso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_entrevistado INTEGER,
        id_bloco INTEGER,
        id_sistema INTEGER,
        como_usa TEXT,
        satisfacao TEXT,
        workaround TEXT,
        entradas TEXT,                  -- De onde vêm os dados para este sistema
        saidas TEXT,                    -- Para onde vão os dados deste sistema
        is_excel_bridge INTEGER DEFAULT 0, -- 1 se for uma planilha-ponte
        dt_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_entrevistado) REFERENCES stg_entrevistados (id),
        FOREIGN KEY (id_bloco) REFERENCES stg_chunks (id),
        FOREIGN KEY (id_sistema) REFERENCES dim_sistemas (id),
        CHECK (satisfacao IN ('Positivo', 'Neutro', 'Negativo'))
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fato_relacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_entrevistado INTEGER,
        id_bloco INTEGER,
        tipo TEXT,
        pessoa_citada TEXT,
        area_citada TEXT,
        contexto TEXT,
        dt_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_entrevistado) REFERENCES stg_entrevistados (id),
        FOREIGN KEY (id_bloco) REFERENCES stg_chunks (id),
        CHECK (tipo IN ('responde_a', 'se_relaciona_com', 'depende_de', 'approva', 'fornece_dados_para'))
    )
    ''')

    # OUTRAS TABELAS
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dim_processos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE,
        area_responsavel TEXT,
        unidade_negocio TEXT,
        dt_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # INDICES
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_stg_chunks_status ON stg_chunks(status_analise)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_fato_insights_severidade ON fato_insights(severidade)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_fato_insights_etapa ON fato_insights(id_etapa_cadeia)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_fato_sistemas_sistema ON fato_sistemas_uso(id_sistema)')

    # POPULA MASTER
    for id, nome, descricao, ordem in CADEIA_VALOR_ETAPAS:
        cursor.execute(
            'INSERT OR IGNORE INTO dim_cadeia_valor (id, nome, descricao, ordem) VALUES (?, ?, ?, ?)',
            (id, nome, descricao, ordem)
        )

    conn.commit()
    conn.close()

    print(f"[SCHEMA] Banco criado: {db_path}")


if __name__ == "__main__":
    from src.config import DB_PATH
    create_database(str(DB_PATH))
