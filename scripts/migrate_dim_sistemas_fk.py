"""
Migration: dim_sistemas etapa_processo → id_etapa_cadeia (FK)

Executa ALTER TABLE seguro sem apagar dados existentes.
"""
import sqlite3
from src.config import DB_PATH

CADEIA_VALOR_MAP = {
    # Nomes que aparecem no dim_cadeia_valor (com acentos) → ID
    "Novos Negócios & Demandas": 1,
    "Orçamento": 2,
    "Estruturação": 3,
    "Contratação & Execução": 4,
    "Medição": 5,
    "Tendência": 6,
    "Fiscal & Pagamento": 7,
}

# Mapeamento dos valores antigos (sem acento exato) para o ID correto
ETAPA_PROCESSO_TO_ID = {
    # Antigos valores de ingest_systems.py  → id dim_cadeia_valor
    "Estruturação PEP e EAP": 3,
    "Contratação": 4,
    "Planejamento e Execução": 4,
    "Medição": 5,
    "Tendência": 6,
    "Fiscal e NF": 7,
    "Pagamento": 7,
}


def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Verifica se a coluna já existe
    cursor.execute("PRAGMA table_info(dim_sistemas)")
    cols = [row[1] for row in cursor.fetchall()]
    print(f"Colunas atuais em dim_sistemas: {cols}")

    if "id_etapa_cadeia" not in cols:
        print("[MIGRATION] Adicionando coluna id_etapa_cadeia...")
        cursor.execute("ALTER TABLE dim_sistemas ADD COLUMN id_etapa_cadeia INTEGER REFERENCES dim_cadeia_valor(id)")
        conn.commit()
        print("[MIGRATION] Coluna adicionada.")
    else:
        print("[MIGRATION] Coluna id_etapa_cadeia já existe, pulando ALTER.")

    # 2. Popula id_etapa_cadeia a partir de etapa_processo existente (se houver)
    if "etapa_processo" in cols:
        print("[MIGRATION] Populando id_etapa_cadeia a partir de etapa_processo...")
        cursor.execute("SELECT id, nome, etapa_processo FROM dim_sistemas")
        sistemas = cursor.fetchall()
        updated = 0
        for sid, nome, etapa in sistemas:
            etapa_id = ETAPA_PROCESSO_TO_ID.get(etapa)
            if etapa_id:
                cursor.execute("UPDATE dim_sistemas SET id_etapa_cadeia = ? WHERE id = ?", (etapa_id, sid))
                updated += 1
            else:
                print(f"  [AVISO] Sistema '{nome}' tem etapa '{etapa}' sem mapeamento.")
        conn.commit()
        print(f"[MIGRATION] {updated}/{len(sistemas)} sistemas mapeados com FK.")
    else:
        print("[MIGRATION] Coluna etapa_processo não existe, populando direto via ingest_systems...")

    conn.close()
    print("[MIGRATION] Concluída com sucesso.")


if __name__ == "__main__":
    migrate()
