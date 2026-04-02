import sqlite3
import json
from pathlib import Path
from src.config import DB_PATH, FICHAS_DIR
from src.utils.matching import normalize_name

def build_markdown_fichas():
    FICHAS_DIR.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Pega todos os entrevistados
    cursor.execute("SELECT * FROM entrevistados ORDER BY nome")
    entrevistados = cursor.fetchall()
    
    count = 0
    for e in entrevistados:
        e_id = e['id']
        nome = e['nome']
        cargo = e['cargo'] or "Não informado"
        area = e['area'] or "Não informada"
        status = e['status_revisao']
        
        # Ignora se não passou pela IA ainda e não tem dados brutos (opcional)
        # Mas vamos gerar a ficha vazia com aviso se for o caso
        
        # Pega Insights
        cursor.execute("SELECT * FROM insights_ia WHERE entrevistado_id=?", (e_id,))
        insights = cursor.fetchall()
        
        # Pega Sistemas
        cursor.execute("SELECT * FROM sistemas_uso WHERE entrevistado_id=?", (e_id,))
        sistemas = cursor.fetchall()
        
        # Pega Relações
        cursor.execute("SELECT * FROM relacoes WHERE entrevistado_id=?", (e_id,))
        relacoes = cursor.fetchall()
        
        # Nome do arquivo Markdown
        safe_name = nome.lower().replace(" ", "_").replace("/", "").replace("(", "").replace(")", "")
        file_path = FICHAS_DIR / f"{safe_name}.md"
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# Ficha: {nome}\n\n")
            
            f.write(f"## 👤 Perfil Organizacional\n")
            f.write(f"- **Cargo**: {cargo}\n")
            f.write(f"- **Área**: {area}\n")
            f.write(f"- **Diretoria**: {e['diretoria'] or 'N/A'}\n")
            f.write(f"- **Nível**: {e['nivel'] or 'N/A'}\n")
            f.write(f"- **Status de Revisão IA**: `{status.upper()}`\n\n")
            
            if status != 'concluida':
                f.write("> ⚠️ **Atenção:** Esta entrevista ainda não foi processada pela Inteligência Artificial. Os insights detalhados não estão disponíveis.\n\n")
            
            f.write("## 🖥️ Ecossistema e Sistemas (As-Is)\n")
            if not sistemas:
                f.write("*Nenhum sistema registrado.*\n")
            else:
                for s in sistemas:
                    satisfacao = s["satisfacao"]
                    emoji = "🟢" if "positiv" in str(satisfacao).lower() else "🔴" if "negativ" in str(satisfacao).lower() else "🟡"
                    f.write(f"- **{s['sistema']}** {emoji} *(Uso: {s['como_usa']})*\n")
                    if s["workaround"] and s["workaround"].strip() and s["workaround"].lower() != "nenhum":
                        f.write(f"  - ⚠️ *Workaround / ETL Humano:* {s['workaround']}\n")
            f.write("\n")
            
            f.write("## 🔥 Dores, Gargalos e Insights Principais\n")
            if not insights:
                f.write("*Nenhum insight capturado.*\n")
            else:
                for i in insights:
                    severidade = i['severidade'] or 'Media'
                    sev_emoji = "🟥" if "Alta" in severidade else "🟨" if "Media" in severidade else "🟦"
                    f.write(f"### {sev_emoji} [{i['categoria']}] {i['subcategoria']} (Etapa: {i['etapa_cadeia_valor']})\n")
                    f.write(f"**Descrição:** {i['descricao']}\n\n")
                    if i["sistemas_envolvidos"]:
                        f.write(f"**Sistemas:** `{i['sistemas_envolvidos']}`\n\n")
                    if i["citacao_direta"]:
                        f.write(f"> *\"{i['citacao_direta']}\"*\n\n")
            
            f.write("## 🤝 Mapa de Relações (Stakeholders)\n")
            if not relacoes:
                f.write("*Nenhuma relação mapeada.*\n")
            else:
                for r in relacoes:
                    f.write(f"- **{r['tipo']}**: {r['pessoa_ou_area']} *(Contexto: {r['contexto']})*\n")
            
            f.write("\n---\n*Ficha gerada automaticamente pelo Pipeline Analyzer da MOTIVA/Veron.*\n")
            
        count += 1
        
    conn.close()
    print(f"[GERADOR] [SUCESSO] Exportadas {count} Fichas em Markdown em {FICHAS_DIR}")

if __name__ == "__main__":
    build_markdown_fichas()
