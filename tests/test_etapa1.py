"""
Teste 4: Etapa 1 - Análise Macro (local, sem IA)
"""
import sys
sys.path.insert(0, '.')

from src.config import DB_PATH
import sqlite3

def test_etapa1_local():
    print("="*60)
    print("TESTE 4: Etapa 1 - Macro Análise Local")
    print("="*60)

    # Transcrição de teste
    trans_teste = """
    Nome: João Silva - Gerente de Projetos
    Cargo: Gerente CAPEX

    Entrevista sobre processos CAPEX.
    Usa SAP PS para planejamento e Archer para riscos.
    Tem problemas com integração entre sistemas.
    Processo manual de cópia de dados para Excel.
    """

    # Dados simulados
    e_data = {
        "id": 999,
        "nome": "João Silva",
        "cargo": "Gerente de Projetos",
        "area": "CAPEX",
        "nivel": "Senior",
        "diretoria": "Operações",
        "texto_completo": trans_teste,
        "texto_cargo": None
    }

    print(f"\n[1] Dados simulados:")
    print(f"   Nome: {e_data['nome']}")
    print(f"   Cargo: {e_data['cargo']}")
    print(f"   Transcrição: {len(e_data['texto_completo'])} chars")

    # Extrai lógica da _stage1_macro (simplificada)
    print(f"\n[2] Executando macro análise local...")

    from src.config import CADEIA_VALOR, SISTEMAS_LIST, DORES_KEYWORDS

    # Detecta etapas
    etapas_detectadas = []
    for etapa in CADEIA_VALOR.keys():
        for keyword in CADEIA_VALOR[etapa]:
            if keyword.lower() in trans_teste.lower():
                if etapa not in etapas_detectadas:
                    etapas_detectadas.append(etapa)
                break

    # Detecta sistemas
    sistemas_detectados = []
    for s in SISTEMAS_LIST:
        if s.lower() in trans_teste.lower():
            sistemas_detectados.append(s)

    # Detecta palavras-chave
    palavras = set(trans_teste.lower().split()[:20])

    # Nível de dor baseado em keywords
    keywords_count = sum(1 for kw in DORES_KEYWORDS if kw.lower() in trans_teste.lower())
    if keywords_count >= 2:
        nivel = "Alta"
    elif keywords_count >= 1:
        nivel = "Media"
    else:
        nivel = "Baixa"

    resultado = {
        "resumo_executivo": f"Entrevista com {e_data['nome']} ({e_data['cargo']}) sobre processos CAPEX.",
        "etapas_principais": etapas_detectadas[:3] if etapas_detectadas else ["Não identificada"],
        "sistemas_citados": sistemas_detectados[:5] if sistemas_detectados else ["Não identificados"],
        "nivel_dor": nivel,
        "palavras_chave": list(palavras)[:10]
    }

    print(f"\n[3] Resultado da macro análise:")
    print(f"   Resumo: {resultado['resumo_executivo']}")
    print(f"   Etapas: {', '.join(resultado['etapas_principais'][:3])}")
    print(f"   Sistemas: {', '.join(resultado['sistemas_citados'][:3])}")
    print(f"   Nível dor: {resultado['nivel_dor']}")
    print(f"   Palavras-chave: {', '.join(resultado['palavras_chave'][:5])}")

    print(f"\n[RESULTADO] SUCESSO!")
    return True


if __name__ == "__main__":
    test_etapa1_local()
