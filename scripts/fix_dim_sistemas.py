"""
Fix dim_sistemas: remove etapa_processo, deduplica, garante FK id_etapa_cadeia.
Usa recreação de tabela (único jeito de DROP COLUMN no SQLite).
Rode: python scripts/fix_dim_sistemas.py
"""
import sqlite3
import sys

DB = "data/output/motiva.db"

ETAPA_MAP = {
    "Estruturação PEP e EAP": 3,
    "Estruturacao PEP e EAP": 3,
    "Contratação": 4,
    "Contratacao": 4,
    "Planejamento e Execução": 4,
    "Planejamento e Execucao": 4,
    "Medição": 5,
    "Medicao": 5,
    "Tendência": 6,
    "Tendencia": 6,
    "Fiscal e NF": 7,
    "Pagamento": 7,
}

conn = sqlite3.connect(DB)
conn.execute("PRAGMA foreign_keys = OFF")
cur = conn.cursor()

# ── 1. Lê todos os sistemas atuais ────────────────────────────
cur.execute("PRAGMA table_info(dim_sistemas)")
cols = [r[1] for r in cur.fetchall()]
print(f"Colunas atuais: {cols}")

has_etapa_processo = "etapa_processo" in cols
has_fk = "id_etapa_cadeia" in cols

cur.execute("SELECT id, nome, etapa_processo, id_etapa_cadeia, area_responsavel FROM dim_sistemas"
            if has_etapa_processo else
            "SELECT id, nome, NULL, id_etapa_cadeia, area_responsavel FROM dim_sistemas")
rows = cur.fetchall()
print(f"Total de registros lidos: {len(rows)}")

# ── 2. Deduplica (case-insensitive, mantém menor ID) ─────────
seen = {}  # nome_lower -> (id, nome, etapa_processo, id_etapa_cadeia, area)
for sid, nome, etapa_proc, etapa_fk, area in rows:
    key = nome.strip().lower() if nome else ""
    if key not in seen or sid < seen[key][0]:
        seen[key] = (sid, nome, etapa_proc, etapa_fk, area)

clean_rows = list(seen.values())
print(f"Registros após deduplicação: {len(clean_rows)}")

# ── 3. Resolve id_etapa_cadeia para quem ainda não tem ───────
resolved = []
for sid, nome, etapa_proc, etapa_fk, area in clean_rows:
    if not etapa_fk and etapa_proc:
        etapa_fk = ETAPA_MAP.get(etapa_proc)
        if not etapa_fk:
            # Tenta normalizado sem acento
            from unicodedata import normalize, category
            def strip_accents(s):
                return ''.join(c for c in normalize('NFD', s) if category(c) != 'Mn')
            etapa_fk = ETAPA_MAP.get(strip_accents(etapa_proc))
    resolved.append((sid, nome, etapa_fk, area))

nulls = sum(1 for r in resolved if r[2] is None)
print(f"Com id_etapa_cadeia NULL após resolução: {nulls}")

# ── 4. Recria dim_sistemas SEM etapa_processo ────────────────
cur.execute("DROP TABLE IF EXISTS dim_sistemas_new")
cur.execute("""
    CREATE TABLE dim_sistemas_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE,
        id_etapa_cadeia INTEGER,
        area_responsavel TEXT,
        dt_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_etapa_cadeia) REFERENCES dim_cadeia_valor (id)
    )
""")

for sid, nome, etapa_fk, area in resolved:
    cur.execute(
        "INSERT INTO dim_sistemas_new (id, nome, id_etapa_cadeia, area_responsavel) VALUES (?, ?, ?, ?)",
        (sid, nome, etapa_fk, area)
    )
print(f"Inseridos em dim_sistemas_new: {len(resolved)}")

# ── 5. Substitui a tabela antiga ─────────────────────────────
cur.execute("DROP TABLE dim_sistemas")
cur.execute("ALTER TABLE dim_sistemas_new RENAME TO dim_sistemas")

conn.execute("PRAGMA foreign_keys = ON")
conn.commit()

# ── 6. Verificação final ──────────────────────────────────────
cur.execute("PRAGMA table_info(dim_sistemas)")
cols_final = [r[1] for r in cur.fetchall()]
cur.execute("SELECT COUNT(*), SUM(CASE WHEN id_etapa_cadeia IS NULL THEN 1 ELSE 0 END) FROM dim_sistemas")
total, nulls = cur.fetchone()

conn.close()

print(f"\n[OK] Colunas finais: {cols_final}")
print(f"[OK] Total sistemas: {total} | NULLs restantes: {nulls}")
