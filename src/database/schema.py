import sqlite3
import os

def create_database(db_path):
    """
    Cria a estrutura de tabelas do banco de dados MOTIVA com nomes claros e objetivos.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Tabela de Atores (Entrevistados)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS entrevistados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cargo TEXT,
        diretoria TEXT,
        plataforma TEXT,
        area TEXT,
        nivel TEXT,
        dt_entrevista TEXT,
        tipo_entrevista TEXT,
        arquivo_transcricao TEXT,
        arquivo_cargo_pdf TEXT,
        texto_cargo TEXT,
        status_revisao TEXT DEFAULT 'pendente',
        dt_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 2. Tabela de Transcrições
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transcricoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_entrevistado INTEGER,
        texto_completo TEXT,        -- Texto original com datas
        texto_limpo TEXT,           -- Texto sem cabeçalhos/datas (IA Ready)
        dt_gravacao TEXT,
        arquivo_origem TEXT,
        dt_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_entrevistado) REFERENCES entrevistados (id)
    )
    ''')

    # 3. Tabela de Blocos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transcricao_chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_transcricao INTEGER,
        ordem INTEGER,
        conteudo TEXT,
        checksum TEXT,
        status_analise TEXT DEFAULT 'pendente',
        dt_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_transcricao) REFERENCES transcricoes (id)
    )
    ''')

    # 4. Tabela de Insights IA (O Coração do Diagnóstico)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS insights_ia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_entrevistado INTEGER,
        id_bloco INTEGER,
        etapa_cadeia TEXT,
        categoria TEXT,
        subcategoria TEXT,
        descricao TEXT,
        citacao_direta TEXT,
        sistemas_envolvidos TEXT,
        severidade TEXT,
        confianca REAL,
        modelo_ia TEXT,
        dt_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_entrevistado) REFERENCES entrevistados (id),
        FOREIGN KEY (id_bloco) REFERENCES transcricao_chunks (id)
    )
    ''')

    # 5. Tabela de Sistemas Uso (Workarounds e Ferramentas)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sistemas_uso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_entrevistado INTEGER,
        id_bloco INTEGER,
        sistema TEXT,
        como_usa TEXT,
        etapa_cadeia TEXT,
        satisfacao TEXT,
        workaround TEXT,
        dt_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_entrevistado) REFERENCES entrevistados (id),
        FOREIGN KEY (id_bloco) REFERENCES transcricao_chunks (id)
    )
    ''')

    # 6. Tabela de Relações
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS relacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_entrevistado INTEGER,
        id_bloco INTEGER,
        tipo TEXT,                  -- Interna, Externa, Sistema, Fornecedor
        pessoa_citada TEXT,         -- Nome do Stakeholder
        area_citada TEXT,           -- Nome da Área/Departamento
        contexto TEXT,
        dt_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_entrevistado) REFERENCES entrevistados (id),
        FOREIGN KEY (id_bloco) REFERENCES transcricao_chunks (id)
    )
    ''')

    # 7. Tabela de Cargos (PDFs de descrição de cargo)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cargos (
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

    # 8. Tabelas Auxiliares
    cursor.execute('''CREATE TABLE IF NOT EXISTS sistemas_ti (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT UNIQUE, etapa_processo TEXT, area_responsavel TEXT, dt_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS processos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT UNIQUE, area_responsavel TEXT, unidade_negocio TEXT, dt_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    conn.commit()
    conn.close()
    print(f"Banco de Dados [Schema Perfeito v2.8] inicializado em: {db_path}")

if __name__ == "__main__":
    from src.config import DB_PATH
    create_database(DB_PATH)
