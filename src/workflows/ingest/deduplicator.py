"""
Deduplicator — Serviço de deduplicação de entrevistados.

Responsabilidade unica: detectar e remover registros duplicados na tabela
stg_entrevistados, com migracao CASCADE dos dados relacionados.

Nota: Com a nova estrutura, arquivos são gerenciados em stg_arquivos (1:N).
A deduplicação é baseada apenas em nome e tipo_entrevista.
"""
import sqlite3

from src.config import TRANSCRIPT_PREFIXES, TRANSCRIPT_EXTENSION
from src.utils.text_normalizer import normalize_interviewee_name


def cleanup_duplicate_interviewees(conn):
    """
    Remove duplicatas de stg_entrevistados mantendo apenas o registro principal.

    Estratégia:
    1. Agrupa por nome normalizado + tipo_entrevista
    2. Remove duplicatas, mantendo o ID mais baixo
    3. CASCADE: migra dados relacionados antes de deletar

    Args:
        conn: Conexão com o banco

    Returns:
        Dicionário com estatísticas
    """
    cursor = conn.cursor()

    # Busca todos
    cursor.execute("SELECT id, nome FROM stg_entrevistados ORDER BY nome")
    todos = cursor.fetchall()

    # Agrupa por nome normalizado
    grupos = {}
    for ent_id, nome in todos:
        if nome is None:
            continue

        norm = normalize_interviewee_name(nome)
        chave_grupo = norm

        if chave_grupo not in grupos:
            grupos[chave_grupo] = []
        grupos[chave_grupo].append((ent_id, nome))

    # Processa cada grupo - remove duplicatas
    migration_map = {}
    for norm, grupo in grupos.items():
        if len(grupo) > 1:
            # Ordena por ID (mantem o menor)
            grupo_ordenado = sorted(grupo, key=lambda x: x[0])
            id_mantido = grupo_ordenado[0][0]
            for ent_id, nome in grupo_ordenado[1:]:
                migration_map[ent_id] = id_mantido

    # CASCADE: Migrar dados antes de deletar
    stats = {
        "removed": 0,
        "migrated_stg_transcricoes": 0,
        "migrated_insights": 0,
        "migrated_relacoes": 0,
        "migrated_fato_sistemas_uso": 0
    }

    for id_deletado, id_mantido in migration_map.items():
        # 0. MERGE METADATA: Se o mantido tem campos nulos, pega do deletado
        cursor.execute("SELECT cargo, diretoria, unidade_negocio, area, nivel, dt_entrevista FROM stg_entrevistados WHERE id = ?", (id_deletado,))
        del_data = cursor.fetchone()
        
        cursor.execute("SELECT cargo, diretoria, unidade_negocio, area, nivel, dt_entrevista FROM stg_entrevistados WHERE id = ?", (id_mantido,))
        keep_data = cursor.fetchone()
        
        if del_data and keep_data:
            updates = []
            vals = []
            cols = ["cargo", "diretoria", "unidade_negocio", "area", "nivel", "dt_entrevista"]
            for i, col in enumerate(cols):
                # Se o atual é nulo e o deletado tem valor, migra o valor
                if (not keep_data[i] or str(keep_data[i]).strip() in ("", "None", "0")) and (del_data[i] and str(del_data[i]).strip() not in ("", "None", "0")):
                    updates.append(f"{col} = ?")
                    vals.append(del_data[i])
            
            if updates:
                vals.append(id_mantido)
                cursor.execute(f"UPDATE stg_entrevistados SET {', '.join(updates)} WHERE id = ?", vals)

        # 1. Migrar arquivos (stg_arquivos)
        # Todos os arquivos que apontavam para o deletado agora apontam para o mantido
        cursor.execute("UPDATE stg_arquivos SET id_entrevistado = ? WHERE id_entrevistado = ?", (id_mantido, id_deletado))

        # 2. Migrar insights
        cursor.execute("UPDATE fato_insights SET id_entrevistado = ? WHERE id_entrevistado = ?", (id_mantido, id_deletado))
        stats["migrated_insights"] += cursor.rowcount

        # 3. Migrar relações
        cursor.execute("UPDATE fato_relacoes SET id_entrevistado = ? WHERE id_entrevistado = ?", (id_mantido, id_deletado))
        stats["migrated_relacoes"] += cursor.rowcount

        # 4. Migrar sistemas_uso
        cursor.execute("UPDATE fato_sistemas_uso SET id_entrevistado = ? WHERE id_entrevistado = ?", (id_mantido, id_deletado))
        stats["migrated_fato_sistemas_uso"] += cursor.rowcount

        # 5. Só agora DELETA o entrevistado
        cursor.execute("DELETE FROM stg_entrevistados WHERE id = ?", (id_deletado,))
        stats["removed"] += 1

    # Log de migração
    if stats["removed"] > 0:
        print(f"  [CASCADE] {stats['removed']} duplicatas removidas:")
        if stats["migrated_insights"] > 0:
            print(f"    - {stats['migrated_insights']} insights migrados")
        if stats["migrated_relacoes"] > 0:
            print(f"    - {stats['migrated_relacoes']} relações migradas")
        if stats["migrated_fato_sistemas_uso"] > 0:
            print(f"    - {stats['migrated_fato_sistemas_uso']} fato_sistemas_uso migrados")

    return stats


def find_existing_interviewee(conn, nome: str) -> int:
    """
    Busca stg_entrevistado existente com nome similar.

    Args:
        conn: Conexão com o banco
        nome: Nome a buscar

    Returns:
        ID do entrevistado encontrado ou None
    """
    cursor = conn.cursor()

    # Busca todos os entrevistados
    cursor.execute("SELECT id, nome FROM stg_entrevistados")
    todos = cursor.fetchall()

    nome_normalizado = normalize_interviewee_name(nome)
    nome_lower = nome.lower()
    primeiro_nome = nome.split()[0].lower() if nome.split() else ""

    for ent_id, ent_nome in todos:
        if ent_nome is None:
            continue
        ent_nome_norm = normalize_interviewee_name(ent_nome)
        ent_nome_lower = ent_nome.lower()
        ent_primeiro_nome = ent_nome.split()[0].lower() if ent_nome.split() else ""

        # Match exato de nome normalizado
        if nome_normalizado == ent_nome_norm:
            return ent_id

        # Match por substring do NOME COMPLETO (não normalizado)
        if nome_lower in ent_nome_lower or ent_nome_lower in nome_lower:
            # Verifica se o primeiro nome é o mesmo
            if primeiro_nome == ent_primeiro_nome:
                return ent_id

    return None


def main():
    """Entry point para Poetry scripts - Remove duplicatas de entrevistados."""
    import sqlite3

    conn = sqlite3.connect(DB_PATH)
    stats = cleanup_duplicate_interviewees(conn)
    conn.commit()
    conn.close()

    print(f"[DEDUPLICATOR] {stats['removed']} duplicatas removidas.")
    print(f"  - Insights migrados: {stats['migrated_insights']}")
    print(f"  - Relações migradas: {stats['migrated_relacoes']}")
    print(f"  - Sistemas uso migrados: {stats['migrated_fato_sistemas_uso']}")


if __name__ == "__main__":
    main()
