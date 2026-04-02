import sqlite3
from pathlib import Path

def init_db(db_path: Path):
    """
    Inicializa as tabelas no banco de dados SQLite para o MOTIVA.
    Se o banco já existir, as tabelas só serão criadas se não existirem (IF NOT EXISTS).
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tabela 1: Entrevistados (inclui tracking)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entrevistados (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        cargo TEXT,
        diretoria TEXT,
        plataforma TEXT,
        area TEXT,
        nivel TEXT,
        data_entrevista TEXT,
        tipo_entrevista TEXT,
        arquivo_transcricao TEXT,
        arquivo_cargo_pdf TEXT,
        
        -- Tracking fields para a IA / Workflow
        status_revisao TEXT DEFAULT 'pendente', -- 'pendente', 'em_progresso', 'concluida', 'erro'
        notas_revisor TEXT,
        data_revisao TEXT,
        tipo_analise_concluida TEXT
    );
    """)

    # Tabela 2: Transcrições originais (Raw text)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transcricoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entrevistado_id INTEGER REFERENCES entrevistados(id),
        texto_completo TEXT,
        num_paragrafos INTEGER,
        num_caracteres INTEGER
    );
    """)

    # Tabela 3: Cargos mapeados (PDF extrator)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cargos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo_cargo TEXT,
        arquivo_pdf TEXT,
        texto_extraido TEXT,
        responsabilidades TEXT,
        competencias TEXT,
        area_atuacao TEXT
    );
    """)

    # Tabela 4: Insights IA
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS insights_ia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entrevistado_id INTEGER REFERENCES entrevistados(id),
        etapa_cadeia_valor TEXT,
        categoria TEXT,         -- 'Sistema', 'Dor', 'Processo', 'ETL Humano', 'Insight Entrelinhas'
        subcategoria TEXT,
        descricao TEXT,         -- Texto gerado pela IA
        citacao_direta TEXT,    -- Citação do texto original extraída pela IA
        sistemas_envolvidos TEXT, -- JSON array
        severidade TEXT,        -- 'Alta', 'Media', 'Baixa'
        confianca REAL,
        modelo_ia TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Tabela 5: Relações Hierárquicas e Funcionais
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS relacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entrevistado_id INTEGER REFERENCES entrevistados(id),
        tipo TEXT,              -- 'responde_a', 'se_relaciona_com', 'depende_de'
        pessoa_ou_area TEXT,
        contexto TEXT
    );
    """)

    # Tabela 6:Sistemas e Uso
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sistemas_uso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entrevistado_id INTEGER REFERENCES entrevistados(id),
        sistema TEXT,
        como_usa TEXT,
        etapa_cadeia TEXT,
        satisfacao TEXT,        -- 'Positivo', 'Neutro', 'Negativo'
        workaround TEXT         -- O que ele faz pra contornar (Planilha, Copy/Paste)
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    from src.config import DB_PATH
    init_db(DB_PATH)
    print(f"Banco de dados inicializado em: {DB_PATH}")
