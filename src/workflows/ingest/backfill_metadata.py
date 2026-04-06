"""
Backfill Metadata Pipeline

Responsabilidade unica: usar stg_cargos (fonte da verdade oficial) para
preencher lacunas (campoes vazios ou '0') em stg_entrevistados.
"""
import sqlite3
from src.config import DB_PATH

def backfill_metadata():
    """
    Sincroniza metadados oficiais dos cargos vinculados para os entrevistados.
    
    Lógica:
    - Se stg_entrevistados.area for NULL/vazio -> Pega stg_cargos.area_atuacao
    - Se stg_entrevistados.diretoria for NULL/vazio -> Pega stg_cargos.diretoria
    - Se stg_entrevistados.unidade_negocio for NULL/vazio -> Pega stg_cargos.negocio_plataforma
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("[BACKFILL] Iniciando saneamento de metadados...")

    # 1. Busca todos que têm vínculo com ID de cargo
    cursor.execute("""
        SELECT 
            e.id as ent_id, 
            e.diretoria as ent_dir, 
            e.area as ent_area, 
            e.unidade_negocio as ent_unid,
            c.diretoria as oficial_dir,
            c.area_atuacao as oficial_area,
            c.negocio_plataforma as oficial_unid,
            c.titulo_cargo
        FROM stg_entrevistados e
        JOIN stg_cargos c ON e.id_cargo = c.id
    """)
    vincos = cursor.fetchall()

    count_dir = 0
    count_area = 0
    count_unid = 0

    for r in vincos:
        updates = []
        vals = []

        # Saneamento de Diretoria
        if not r['ent_dir'] or str(r['ent_dir']).strip() in ('', '0', 'None', '#N/A'):
             if r['oficial_dir']:
                 updates.append("diretoria = ?")
                 vals.append(r['oficial_dir'])
                 count_dir += 1
        
        # Saneamento de Área
        if not r['ent_area'] or str(r['ent_area']).strip() in ('', '0', 'None', '#N/A'):
             if r['oficial_area']:
                 updates.append("area = ?")
                 vals.append(r['oficial_area'])
                 count_area += 1

        # Saneamento de Unidade de Negócio
        if not r['ent_unid'] or str(r['ent_unid']).strip() in ('', '0', 'None', '#N/A'):
             if r['oficial_unid']:
                 updates.append("unidade_negocio = ?")
                 vals.append(r['oficial_unid'])
                 count_unid += 1

        if updates:
            vals.append(r['ent_id'])
            cursor.execute(f"UPDATE stg_entrevistados SET {', '.join(updates)} WHERE id = ?", vals)

    conn.commit()
    conn.close()

    print(f"[SUCCESS] Saneamento completo:")
    print(f"  - {count_dir} diretorias preenchidas")
    print(f"  - {count_area} áreas preenchidas")
    print(f"  - {count_unid} unidades de negócio preenchidas")

if __name__ == "__main__":
    backfill_metadata()
""",Description:
