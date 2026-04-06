"""
Deduplicator — Servico de deduplicacao de entrevistados.

Responsabilidade unica: detectar e remover registros duplicados na tabela
entrevistados, com migracao CASCADE dos dados relacionados.

Duas estrategias complementares:
  1. Por nome base do arquivo DOCX (mais confiavel)
  2. Por primeiro nome + substring do nome completo
"""
import sqlite3
import re
import openpyxl
from pathlib import Path

from src.config import DB_PATH, LISTA_ENTREVISTAS, TRANSCRIPT_PREFIXES, TRANSCRIPT_EXTENSION
from src.utils.name_matcher import build_name_file_map
from src.utils.text_normalizer import normalize_interviewee_name


def cleanup_duplicate_interviewees(conn):
    """
    Remove duplicatas de entrevistados mantendo apenas o registro principal.

    Estratégia: baseada no nome do ARQUIVO (mais confiável).
    Se dois arquivos têm o mesmo nome base, são a mesma pessoa.

    Args:
        conn: Conexão com o banco

    Returns:
        Número de duplicatas removidas
    """
    cursor = conn.cursor()

    # Busca todos com arquivo de transcricao
    cursor.execute("""
        SELECT id, nome, arquivo_transcricao
        FROM stg_entrevistados
        WHERE arquivo_transcricao IS NOT NULL
        ORDER BY nome
    """)
    todos = cursor.fetchall()

    # Agrupa por nome base do arquivo + tipo de entrevista
    # (as_is e aprofundamento da MESMA pessoa sao REGISTROS DIFERENTES)
    grupos = {}
    for ent_id, nome, arquivo in todos:
        if nome is None or arquivo is None:
            continue

        # Extrai nome base do arquivo e o tipo
        nome_arquivo = arquivo.lower()
        tipo = "aprofundamento" if "aprofundamento" in nome_arquivo else "as_is"

        for prefix in TRANSCRIPT_PREFIXES:
            nome_arquivo = nome_arquivo.replace(prefix, "")
        nome_arquivo = nome_arquivo.replace(TRANSCRIPT_EXTENSION, "").replace("_", " ").strip()

        # Chave do grupo inclui o TIPO para diferenciar as_is de aprofundamento
        chave_grupo = (nome_arquivo, tipo)

        if chave_grupo not in grupos:
            grupos[chave_grupo] = []
        grupos[chave_grupo].append((ent_id, nome, arquivo))

    # Processa cada grupo - remove duplicatas reais (mesmo nome + mesmo tipo)
    para_remover = set()
    for (nome_arquivo, tipo), grupo in grupos.items():
        if len(grupo) > 1:
            # Ordena por ID (mantem o menor)
            grupo_ordenado = sorted(grupo, key=lambda x: x[0])
            # Mantém o primeiro, remove os demais
            for ent_id, nome, arquivo in grupo_ordenado[1:]:
                para_remover.add(ent_id)

    # SEGUNDA ESTRATÉGIA: Primeiro nome igual + substring do nome completo
    # Para casos como "Lucas Giraldi" vs "Lucas Giraldi Rapchan Aguilar"
    cursor.execute("SELECT id, nome, arquivo_transcricao FROM stg_entrevistados ORDER BY nome")
    todos_nomes = cursor.fetchall()

    # Agrupa por primeiro nome
    por_primeiro_nome = {}
    for ent_id, nome, arquivo in todos_nomes:
        if nome is None or ent_id in para_remover:
            continue
        primeiro_nome = nome.split()[0].lower()
        if primeiro_nome not in por_primeiro_nome:
            por_primeiro_nome[primeiro_nome] = []
        por_primeiro_nome[primeiro_nome].append((ent_id, nome, arquivo))

    # Verifica grupos com mesmo primeiro nome
    for primeiro, grupo in por_primeiro_nome.items():
        if len(grupo) > 1:
            for i, (ent_id1, nome1, arq1) in enumerate(grupo):
                if ent_id1 in para_remover:
                    continue

                for ent_id2, nome2, arq2 in grupo[i+1:]:
                    if ent_id2 in para_remover:
                        continue

                    # Checa se são a mesma pessoa
                    norm1 = normalize_interviewee_name(nome1)
                    norm2 = normalize_interviewee_name(nome2)

                    nome1_lower = nome1.lower()
                    nome2_lower = nome2.lower()

                    # Verifica tipo de entrevista
                    tipo1 = "aprofundamento" if "aprofundamento" in (arq1 or "").lower() else "as_is"
                    tipo2 = "aprofundamento" if "aprofundamento" in (arq2 or "").lower() else "as_is"

                    # Se nomes normalizados são EXATAMENTE IGUAIS → mesma pessoa
                    # Se são apenas substrings → só mescla se for o MESMO tipo
                    if norm1 == norm2:
                        # Mesma pessoa - SÓ mescla se for o MESMO tipo
                        # (as_is e aprofundamento da mesma pessoa devem ser mantidos separados)
                        if tipo1 == tipo2:
                            # Mesmo tipo - pode mesclar
                            if ent_id1 < ent_id2:
                                menor, maior = ent_id1, ent_id2
                            else:
                                menor, maior = ent_id2, ent_id1
                            print(f"  [CLEANUP] Mesclando {norm1} (ID {maior} -> {menor})")
                            para_remover.add(maior)
                        else:
                            # Tipos diferentes - mantém separado
                            pass
                    elif nome1_lower in nome2_lower or nome2_lower in nome1_lower:
                        # Substring - só mescla se for o MESMO tipo
                        if tipo1 == tipo2:
                            if ent_id1 < ent_id2:
                                menor, maior = ent_id1, ent_id2
                            else:
                                menor, maior = ent_id2, ent_id1
                            para_remover.add(maior)

    # Mapeamento: {id_deletado: id_mantido}
    migration_map = {}

    # Converte para dicionário (primeira estratégia)
    for (nome_arquivo, tipo), grupo in grupos.items():
        if len(grupo) > 1:
            grupo_ordenado = sorted(grupo, key=lambda x: x[0])
            id_mantido = grupo_ordenado[0][0]
            for ent_id, nome, arquivo in grupo_ordenado[1:]:
                migration_map[ent_id] = id_mantido

    # Converte para dicionário (segunda estratégia)
    for primeiro, grupo in por_primeiro_nome.items():
        if len(grupo) > 1:
            for i, (ent_id1, nome1, arq1) in enumerate(grupo):
                if ent_id1 in migration_map:
                    continue

                for ent_id2, nome2, arq2 in grupo[i+1:]:
                    if ent_id2 in migration_map:
                        continue

                    norm1 = normalize_interviewee_name(nome1)
                    norm2 = normalize_interviewee_name(nome2)

                    nome1_lower = nome1.lower()
                    nome2_lower = nome2.lower()

                    # Se nomes normalizados são EXATAMENTE IGUAIS → mesma pessoa
                    # Se são apenas substrings → só mescla se for o MESMO tipo
                    if norm1 == norm2:
                        # Mesma pessoa - SÓ mescla se for o MESMO tipo
                        if tipo1 == tipo2:
                            # Mesmo tipo - pode mesclar
                            if ent_id1 < ent_id2:
                                migration_map[ent_id2] = ent_id1
                            else:
                                migration_map[ent_id1] = ent_id2
                        # else: tipos diferentes - mantém separado (não adiciona ao map)
                    elif nome1_lower in nome2_lower or nome2_lower in nome1_lower:
                        # Substring - só mescla se for o MESMO tipo
                        if tipo1 == tipo2:
                            if ent_id1 < ent_id2:
                                migration_map[ent_id2] = ent_id1
                            else:
                                migration_map[ent_id1] = ent_id2

    # ─────────────────────────────────────────────────────────────
    # CASCADE: Migrar dados antes de deletar
    # ─────────────────────────────────────────────────────────────
    stats = {
        "removed": 0,
        "migrated_stg_transcricoes": 0,
        "migrated_insights": 0,
        "migrated_relacoes": 0,
        "migrated_fato_sistemas_uso": 0
    }

    for id_deletado, id_mantido in migration_map.items():
        # 1. Migrar transcrições
        cursor.execute("""
            UPDATE stg_stg_transcricoes SET id_entrevistado = ? WHERE id_entrevistado = ?
        """, (id_mantido, id_deletado))
        stats["migrated_stg_transcricoes"] += cursor.rowcount

        # 2. Migrar insights
        cursor.execute("""
            UPDATE fato_insights SET id_entrevistado = ? WHERE id_entrevistado = ?
        """, (id_mantido, id_deletado))
        stats["migrated_insights"] += cursor.rowcount

        # 3. Migrar relações
        cursor.execute("""
            UPDATE fato_relacoes SET id_entrevistado = ? WHERE id_entrevistado = ?
        """, (id_mantido, id_deletado))
        stats["migrated_relacoes"] += cursor.rowcount

        # 4. Migrar fato_sistemas_uso
        cursor.execute("""
            UPDATE fato_sistemas_uso SET id_entrevistado = ? WHERE id_entrevistado = ?
        """, (id_mantido, id_deletado))
        stats["migrated_fato_sistemas_uso"] += cursor.rowcount

        # 5. Só agora DELETA o entrevistado
        cursor.execute("DELETE FROM stg_entrevistados WHERE id = ?", (id_deletado,))
        stats["removed"] += 1

    # Log de migração
    if stats["removed"] > 0:
        print(f"  [CASCADE] {stats['removed']} duplicatas removidas:")
        if stats["migrated_stg_transcricoes"] > 0:
            print(f"    - {stats['migrated_stg_transcricoes']} transcrições migradas")
        if stats["migrated_insights"] > 0:
            print(f"    - {stats['migrated_insights']} insights migrados")
        if stats["migrated_relacoes"] > 0:
            print(f"    - {stats['migrated_relacoes']} relações migradas")
        if stats["migrated_fato_sistemas_uso"] > 0:
            print(f"    - {stats['migrated_fato_sistemas_uso']} fato_sistemas_uso migrados")

    return stats


def find_existing_interviewee(conn, nome: str) -> int:
    """
    Busca entrevistado existente com nome similar.

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
        # Para casos como "Lucas Giraldi" vs "Lucas Giraldi Rapchan Aguilar"
        if nome_lower in ent_nome_lower or ent_nome_lower in nome_lower:
            # Verifica se o primeiro nome é o mesmo
            if primeiro_nome == ent_primeiro_nome:
                return ent_id

    return None
