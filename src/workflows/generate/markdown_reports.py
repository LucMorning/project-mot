"""
Markdown Reports Generator - Template-based (sem IA)

Gera relatórios markdown a partir de dados JÁ PROCESSADOS no banco.
IA já gerou insights, aqui só formatamos (Python puro, econômico).

Refatorado para usar:
- src.database.repositories → Repository pattern (DRY)
- Schema v2.8 (PT-BR Sênior)
"""
from pathlib import Path
from typing import List, Dict
import os
import sqlite3

import google.generativeai as genai
import dotenv

from src.config import FICHAS_DIR, DB_PATH
from src.database.repositories import (
    InsightsRepository, SistemasUsoRepository, RelacoesRepository,
    EntrevistadosRepository
)

dotenv.load_dotenv()


# ─────────────────────────────────────────────────────────────
# EXECUTIVE SUMMARY (único campo gerado por IA)
# ─────────────────────────────────────────────────────────────

def generate_executive_summary(
    entrevistado_id: int,
    insights: List[Dict],
    sistemas: List[Dict],
    relacoes: List[Dict]
) -> str:
    """
    Gera resumo executivo de 3-5 frases usando IA.
    """
    contexto = f"""
    Entrevistado ID: {entrevistado_id}

    DORES IDENTIFICADAS:
    {len(insights)} dores - categorias: {[i.get('categoria') for i in insights][:5]}

    SISTEMAS MAPEADOS:
    {len(sistemas)} sistemas - principais: {[s['sistema'] for s in sistemas[:5]]}

    RELAÇÕES:
    {len(relacoes)} relações mapeadas

    Gere um resumo executivo de 3-5 frases sobre o perfil CAPEX deste entrevistado,
    focando em: maturidade digital, principais dores e ecossistema de sistemas.
    Seja objetivo e profissional.
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(contexto)
        return response.text.strip()
    except Exception as e:
        return f"Entrevistado com {len(insights)} pontos de dor identificados e {len(sistemas)} sistemas mapeados no ecossistema CAPEX."


def get_emoji_severidade(severidade: str) -> str:
    """Retorna emoji baseado na severidade."""
    if "Alta" in (severidade or ""):
        return "🟥"
    elif "Media" in (severidade or ""):
        return "🟨"
    return "🟦"


def get_emoji_satisfacao(satisfacao: str) -> str:
    """Retorna emoji baseado na satisfação."""
    if "positiv" in str(satisfacao).lower():
        return "🟢"
    elif "negativ" in str(satisfacao).lower():
        return "🔴"
    return "🟡"


def generate_markdown_for_entrevistado(entrevistado_id: int, output_dir: Path = None) -> str:
    """
    Gera relatório markdown para um entrevistado usando TEMPLATE.
    """
    if output_dir is None:
        output_dir = FICHAS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    # Repositories
    entrevistado_repo = EntrevistadosRepository(DB_PATH)
    insights_repo = InsightsRepository(DB_PATH)
    sistemas_repo = SistemasUsoRepository(DB_PATH)
    relacoes_repo = RelacoesRepository(DB_PATH)

    # Busca dados do entrevistado
    conn = entrevistado_repo._get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, cargo, area, diretoria, nivel, dt_entrevista 
        FROM entrevistados 
        WHERE id = ?
    """, (entrevistado_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise ValueError(f"Entrevistado {entrevistado_id} não encontrado")

    e_id, nome, cargo, area, diretoria, nivel, dt_entrevista = row

    # Busca dados processados
    insights = insights_repo.get_by_entrevistado(entrevistado_id)
    sistemas = sistemas_repo.get_by_entrevistado(entrevistado_id)
    relacoes = relacoes_repo.get_by_entrevistado(entrevistado_id)

    # Gera markdown
    safe_name = nome.lower().replace(" ", "_").replace("/", "").replace("(", "").replace(")", "")
    file_path = output_dir / f"{safe_name}.md"

    # Gera resumo executivo com IA (apenas este campo!)
    resumo_executivo = generate_executive_summary(entrevistado_id, insights, sistemas, relacoes)

    with open(file_path, "w", encoding="utf-8") as f:
        # Header
        f.write(f"# CAPEX Diagnostic Report: {nome}\n\n")
        f.write(f"## 📋 Executive Summary\n\n")
        f.write(f"{resumo_executivo}\n\n")
        f.write(f"---\n\n")
        f.write(f"## 👤 Organizational Profile\n")
        f.write(f"- **Role**: {cargo or 'N/A'}\n")
        f.write(f"- **Area**: {area or 'N/A'}\n")
        f.write(f"- **Directorate**: {diretoria or 'N/A'}\n")
        f.write(f"- **Level**: {nivel or 'N/A'}\n")
        f.write(f"- **Interview Date**: {dt_entrevista or 'N/A'}\n\n")

        if not insights and not sistemas:
            f.write("> ⚠️ **Attention:** No AI-processed insights yet.\n\n")

        # Sistemas
        f.write("## 🖥️ Systems Ecosystem (As-Is)\n")
        if not sistemas:
            f.write("*No systems mapped for this interview.*\n")
        else:
            for s in sistemas:
                satisfacao_emoji = get_emoji_satisfacao(s.get('satisfacao', ''))
                f.write(f"- **{s['sistema']}** {satisfacao_emoji}\n")
                f.write(f"  - **Usage**: {s.get('como_usa', 'N/A')}\n")
                f.write(f"  - **CAPEX Stage**: {s.get('etapa_cadeia', 'N/A')}\n")
                workaround = s.get('workaround', '')
                if workaround and workaround.lower() != "nenhum":
                    f.write(f"  - ⚠️ **Workaround/ETL**: {workaround}\n")
            f.write("\n")

        # Dores
        f.write("## 🔥 Pain Points, Bottlenecks & Diagnostics\n")
        if not insights:
            f.write("*No pain points captured yet.*\n")
        else:
            # Ordena por severidade (Alta -> Media -> Baixa)
            sorted_insights = sorted(insights, key=lambda x: (
                0 if "Alta" in (x.get('severidade') or '') else
                1 if "Media" in (x.get('severidade') or '') else 2
            ))

            for i in sorted_insights:
                severidade = i.get('severidade', 'Media')
                sev_emoji = get_emoji_severidade(severidade)

                f.write(f"### {sev_emoji} [{i.get('categoria')}] {i.get('subcategoria')} (Stage: {i.get('etapa_cadeia')})\n")
                f.write(f"**Description:** {i.get('descricao')}\n\n")

                # Sistemas envolvidos
                sistemas_envolvidos = i.get('sistemas_envolvidos', [])
                if sistemas_envolvidos:
                    f.write(f"**Systems:** `{sistemas_envolvidos}`\n\n")

                # Citação
                citacao = i.get('citacao_direta')
                if citacao:
                    f.write(f"> *\"{citacao}\"*\n\n")

        # Relações
        f.write("## 🤝 Stakeholders & Relationships\n")
        if not relacoes:
            f.write("*No relationships mapped yet.*\n")
        else:
            for r in relacoes:
                # Usa o split sênior p/ exibir stakeholder
                stakeholder = r.get('pessoa_citada') or r.get('area_citada') or 'N/A'
                f.write(f"- **{r.get('tipo')}**: {stakeholder}\n")
                f.write(f"  - **Context**: {r.get('contexto', 'N/A')}\n")

        f.write("\n---\n*Generated by MOTIVA Senior Pipeline | v2.8 Standard | Veron Consulting*\n")

    print(f"  [MD] {file_path.name}")
    return str(file_path)


def generate_all_markdowns(output_dir: Path = None) -> int:
    """
    Gera relatórios markdown para TODOS os entrevistados com insights.
    """
    if output_dir is None:
        output_dir = FICHAS_DIR
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT e.id, e.nome
        FROM entrevistados e
        JOIN insights_ia i ON e.id = i.id_entrevistado
        ORDER BY e.nome
    """)
    entrevistados_com_dados = cursor.fetchall()
    conn.close()

    if not entrevistados_com_dados:
        print("[INFO] Nenhum entrevistado com insights para gerar relatórios.")
        return 0

    print(f"\n[MARKDOWN GENERATOR] Gerando {len(entrevistados_com_dados)} relatórios...")

    count = 0
    for e_id, e_nome in entrevistados_com_dados:
        try:
            generate_markdown_for_entrevistado(e_id, output_dir)
            count += 1
        except Exception as e:
            print(f"  [ERRO] Entrevistado {e_id} ({e_nome}): {e}")

    print(f"[DONE] {count} relatórios gerados em {output_dir}")
    return count


if __name__ == "__main__":
    generate_all_markdowns()
