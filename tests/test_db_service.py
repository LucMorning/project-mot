"""
Teste 1: DatabaseService - Validar salvamento no banco
"""
import sys
sys.path.insert(0, '.')

from src.database.schema import init_db
from src.config import DB_PATH
from src.pipelines.run_ai_diagnostic import DatabaseService

def test_db_service():
    print("="*60)
    print("TESTE 1: DatabaseService")
    print("="*60)

    # Inicializa banco
    print("\n[1] Inicializando banco...")
    init_db(DB_PATH)
    print(f"   Banco criado em: {DB_PATH}")

    # Cria dados de teste
    print("\n[2] Criando dados de teste...")
    test_data = {
        "dores_analysis": {
            "dores": [
                {
                    "descricao": "Dor de teste - ETL manual",
                    "etapa_cadeia_valor": "3. Estruturação (Plan/Custo)",
                    "categoria": "ETL Humano",
                    "subcategoria": "Copy/Paste",
                    "citacao_direta": "Tenho que copiar do Excel",
                    "sistemas_envolvidos": ["SAP"],
                    "severidade": "Alta"
                }
            ],
            "resumo_dores": "1 dor encontrada",
            "nivel_maturidade": "Em Transição"
        },
        "sistemas_analysis": {
            "sistemas": [
                {
                    "nome_sistema": "SAP PS",
                    "etapa_cadeia": "3. Estruturação (Plan/Custo)",
                    "finalidade": "Planejamento de projetos",
                    "forma_uso": "Gestão de cronograma",
                    "satisfacao": "Negativo",
                    "problema_principal": "Lento e complexo"
                }
            ],
            "resumo_ecossistema": "1 sistema",
            "integracoes": [],
            "sistemas_criticados": ["SAP PS"]
        },
        "relacoes_analysis": {
            "relacoes": [
                {
                    "tipo": "depende_de",
                    "contraparte": "GP",
                    "contexto": "Aprovação de projetos"
                }
            ],
            "resumo_rede": "1 relação",
            "stakeholders": [],
            "areas_mencionadas": []
        },
        "processos_analysis": {
            "fluxos": [],
            "resumo_processos": "Não analisado",
            "etapas_mapeadas": [],
            "cadeia_valor_abrangencia": []
        }
    }

    # Testa salvamento
    print("\n[3] Testando salvamento...")
    db = DatabaseService(DB_PATH)

    try:
        db.save_multi_agent_analysis(999, test_data, "teste-local")
        print("   Salvamento bem sucedido!")
    except Exception as e:
        print(f"   ERRO no salvamento: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Verifica se salvou
    print("\n[4] Verificando dados salvos...")
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM insights_ia WHERE entrevistado_id = 999')
    insights = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM sistemas_uso WHERE entrevistado_id = 999')
    sistemas = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM relacoes WHERE entrevistado_id = 999')
    relacoes = cursor.fetchone()[0]

    print(f"   Insights salvos: {insights}")
    print(f"   Sistemas salvos: {sistemas}")
    print(f"   Relações salvas: {relacoes}")

    conn.close()

    # Limpa teste
    print("\n[5] Limpando dados de teste...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM insights_ia WHERE entrevistado_id = 999')
    cursor.execute('DELETE FROM sistemas_uso WHERE entrevistado_id = 999')
    cursor.execute('DELETE FROM relacoes WHERE entrevistado_id = 999')
    conn.commit()
    conn.close()

    print("\n[RESULTADO] SUCESSO!" if insights > 0 else "\n[RESULTADO] FALHOU!")
    return insights > 0 or sistemas > 0 or relacoes > 0


if __name__ == "__main__":
    test_db_service()
