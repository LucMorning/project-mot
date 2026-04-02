"""
Exporta TODOS os dados do SQLite para JSON/Pandas - TRANSICOES, ENTREVISTADOS, CARGOS
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data/output/motiva.db")

def export_all():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Todas as tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]

    export_dir = Path("data/output/exports")
    export_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    all_data = {}

    for table in tables:
        cursor.execute(f"SELECT * FROM {table};")
        rows = cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({table});")
        cols = [c[1] for c in cursor.fetchall()]

        # Converte para lista de dicts
        table_data = [dict(zip(cols, row)) for row in rows]
        all_data[table] = table_data

        # Salva individualmente
        with open(export_dir / f"{table}_{timestamp}.json", 'w', encoding='utf-8') as f:
            json.dump(table_data, f, ensure_ascii=False, indent=2, default=str)

        print(f"{table}: {len(rows)} registros")

    # Salva tudo junto
    with open(export_dir / f"motiva_full_export_{timestamp}.json", 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2, default=str)

    conn.close()
    print(f"\nExportado para: {export_dir}")

if __name__ == "__main__":
    export_all()
