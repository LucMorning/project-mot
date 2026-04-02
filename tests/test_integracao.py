"""
Teste 5: Integração Completa - Fluxo ponta a ponta
"""
import sys
import os
sys.path.insert(0, '.')

import dotenv
dotenv.load_dotenv()

# Verifica API key
if not os.getenv("GEMINI_API_KEY"):
    print("ERRO: GEMINI_API_KEY não configurada!")
    print("Configure no .env antes de rodar este teste.")
    sys.exit(1)

from src.database.schema import init_db
from src.config import DB_PATH
from src.pipelines.run_ai_diagnostic import DatabaseService
import sqlite3

def test_integracao():
    print("="*60)
    print("TESTE 5: Integração Completa")
    print("="*60)

    # Limpa dados anteriores
    print("\n[1] Limpando banco...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Deleta dados de teste se existirem
    cursor.execute('DELETE FROM insights_ia WHERE entrevistado_id = 999')
    cursor.execute('DELETE FROM sistemas_uso WHERE entrevistado_id = 999')
    cursor.execute('DELETE FROM relacoes WHERE entrevistado_id = 999')
    cursor.execute('DELETE FROM entrevistados WHERE id = 999')
    cursor.execute('DELETE FROM transcricoes WHERE entrevistado_id = 999')

    conn.commit()
    conn.close()

    # Insera dados de teste
    print("[2] Inserindo dados de teste no banco...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Entrevistado
    cursor.execute("""
        INSERT INTO entrevistados (id, nome, cargo, area, status_revisao)
        VALUES (?, ?, ?, ?, ?)
    """, (999, "Teste Integração", "Analista", "TI", "pendente"))

    # Transcrição
    cursor.execute("""
        INSERT INTO transcricoes (entrevistado_id, texto_completo, texto_limpo, num_paragrafos, num_caracteres)
        VALUES (?, ?, ?, ?, ?)
    """, (999,
        "Transcrição de teste. Usa SAP PS, Archer. Processo manual de Excel.",
        "Transcrição de teste. Usa SAP PS, Archer. Processo manual de Excel.",
        1, len("Transcrição de teste. Usa SAP PS, Archer. Processo manual de Excel.")))

    conn.commit()
    conn.close()

    print("   Entrevistado ID 999 criado")
    print("   Transcrição inserida")

    # Importa pipeline
    print("\n[3] Testando pipeline completo...")
    from src.pipelines.run_ai_diagnostic import MultiStageAnalysisPipeline, GeminiProvider

    # Cria componentes
    ai = GeminiProvider(api_key=os.getenv("GEMINI_API_KEY"), model_name="gemini-2.5-flash")
    db = DatabaseService(DB_PATH)
    pipeline = MultiStageAnalysisPipeline(ai_provider=ai, db_service=db, model_name="gemini-2.5-flash")

    # Testa process_entrevistado
    import asyncio

    async def test_process():
        print("\n   Processando ID 999...")
        resultado = await pipeline.process_entrevistado(999)
        return resultado

    try:
        resultado = asyncio.run(test_process())
        print(f"\n[4] Verificando dados salvos...")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM insights_ia WHERE entrevistado_id = 999')
        insights = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM sistemas_uso WHERE entrevistado_id = 999')
        sistemas = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM relacoes WHERE entrevistado_id = 999')
        relacoes = cursor.fetchone()[0]

        cursor.execute('SELECT status_revisao FROM entrevistados WHERE id = 999')
        status = cursor.fetchone()[0]

        conn.close()

        print(f"   Status: {status}")
        print(f"   Insights: {insights}")
        print(f"   Sistemas: {sistemas}")
        print(f"   Relações: {relacoes}")

        sucesso = resultado and (insights > 0 or sistemas > 0 or relacoes > 0)

        print(f"\n[RESULTADO] {'SUCESSO!' if sucesso else 'FALHOU!'}")
        return sucesso

    except Exception as e:
        print(f"\n[ERRO] {e}")
        import traceback
        traceback.print_exc()

        # Verifica status mesmo com erro
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT status_revisao, notas_revisor FROM entrevistados WHERE id = 999')
        row = cursor.fetchone()
        print(f"\n[INFO] Status final: {row[0]}")
        if row[1]:
            print(f"[INFO] Notas: {row[1]}")
        conn.close()

        return False


if __name__ == "__main__":
    test_integracao()
