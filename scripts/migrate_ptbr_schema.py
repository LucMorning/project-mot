import sqlite3
import os
from src.config import DB_PATH

def migrate_schema():
    """
    Renomeia colunas para o padrão PT-BR snake_case no motiva.db físico.
    """
    print(f"--- INICIANDO MIGRAÇÃO DO SCHEMA (PT-BR) no {DB_PATH} ---")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Mapeamento de Mudanças por Tabela
    migrations = {
        "transcricoes": [
            ("entrevistado_id", "id_entrevistado")
        ],
        "transcricao_chunks": [
            ("transcricao_id", "id_transcricao"),
            ("sequencia", "ordem")
        ],
        "insights_ia": [
            ("entrevistado_id", "id_entrevistado"),
            ("chunk_id", "id_bloco"),
            ("etapa_cadeia_valor", "fase_capex"),
            ("sistemas_envolvidos", "sistemas_relacionados"),
            ("severidade", "impacto_negocio"),
            ("modelo_ia", "motor_execucao")
        ],
        "sistemas_uso": [
            ("entrevistado_id", "id_entrevistado"),
            ("chunk_id", "id_bloco"),
            ("etapa_cadeia", "fase_capex"),
            ("como_usa", "finalidade_uso"),
            ("workaround", "alternativa_manual")
        ],
        "relacoes": [
            ("entrevistado_id", "id_entrevistado"),
            ("chunk_id", "id_bloco"),
            ("pessoa_ou_area", "ator_envolvido")
        ]
    }

    for table, changes in migrations.items():
        print(f"\nMigrando Tabela: {table}")
        for old_name, new_name in changes:
            try:
                # Tenta renomear a coluna
                cursor.execute(f"ALTER TABLE {table} RENAME COLUMN {old_name} TO {new_name}")
                print(f"  [OK] {old_name} -> {new_name}")
            except sqlite3.OperationalError as e:
                # Se der erro, geralmente é porque a coluna já tem o nome novo ou não existe
                if "no such column" in str(e) or "already exists" in str(e):
                    print(f"  [PULADO] {old_name} (Já renomeado ou inexistente)")
                else:
                    print(f"  [ERRO]: {e}")

    conn.commit()
    conn.close()
    print("\n--- MIGRAÇÃO CONCLUÍDA ---")

if __name__ == "__main__":
    migrate_schema()
