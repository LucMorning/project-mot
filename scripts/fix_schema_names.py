import sqlite3
import os
from src.config import DB_PATH

def fix_schema():
    """
    Restaura os nomes técnicos (etapa_cadeia, workaround, etc) no banco físico.
    """
    print(f"--- ANALISANDO E CONSERTANDO SCHEMA (V2.1) no {DB_PATH} ---")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Mudanças de Reversão para Limpar a Cagada
    reversions = {
        "insights_ia": [
            ("fase_capex", "etapa_cadeia"),
            ("sistemas_relacionados", "sistemas_envolvidos"),
            ("impacto_negocio", "severidade"),
            ("motor_execucao", "modelo_ia")
        ],
        "sistemas_uso": [
            ("finalidade_uso", "como_usa"),
            ("fase_capex", "etapa_cadeia"),
            ("alternativa_manual", "workaround")
        ],
        "relacoes": [
            ("ator_envolvido", "pessoa_ou_area")
        ]
    }

    for table, changes in reversions.items():
        for old_name, new_name in changes:
            try:
                cursor.execute(f"ALTER TABLE {table} RENAME COLUMN {old_name} TO {new_name}")
                print(f"  [FIX] {table}: {old_name} -> {new_name}")
            except sqlite3.OperationalError as e:
                # Se não encontrar o nome antigo, talvez ele já esteja com o certo
                print(f"  [PULADO] {table}: {old_name} -> {new_name} (Já corrigido ou inexistente)")

    # Garante que a coluna de CONFIANÇA no Diagnóstico foi restaurada
    try:
        cursor.execute("ALTER TABLE insights_ia ADD COLUMN confianca REAL")
        print("  [FIX] Coluna de CONFIANÇA adicionada com sucesso.")
    except Exception:
        pass # Caso ela já exista

    conn.commit()
    conn.close()
    print("\n--- SCHEMA CONSERTADO E PADRONIZADO ---")

if __name__ == "__main__":
    fix_schema()
