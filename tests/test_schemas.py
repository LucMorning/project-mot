"""
Teste 3: Pydantic Schemas - Validar estruturas de dados
"""
import sys
sys.path.insert(0, '.')

from src.pipelines.agents import (
    DoresAgentSchema, SistemasAgentSchema,
    RelacoesAgentSchema, ProcessosAgentSchema
)
from src.pipelines.run_ai_diagnostic import MacroAnalysisSchema
import json

def test_schemas():
    print("="*60)
    print("TESTE 3: Pydantic Schemas")
    print("="*60)

    # Testa MacroAnalysisSchema
    print("\n[1] Testando MacroAnalysisSchema...")
    try:
        macro = MacroAnalysisSchema(
            resumo_executivo="Resumo de teste da entrevista",
            etapas_principais=["1. Novos Negócios & Demandas", "2. Orçamento"],
            sistemas_citados=["SAP", "Archer"],
            nivel_dor="Alta",
            palavras_chave=["manual", "planilha", "gargalo"]
        )
        print(f"   MacroAnalysisSchema: OK")
        print(f"   JSON: {json.dumps(macro.model_dump(), ensure_ascii=False, indent=2)[:200]}...")
    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    # Testa DoresAgentSchema
    print("\n[2] Testando DoresAgentSchema...")
    try:
        dores = DoresAgentSchema(
            resumo_dores="2 dores encontradas",
            dores=[],
            nivel_maturidade="Em Transição"
        )
        print(f"   DoresAgentSchema: OK")
    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    # Testa SistemasAgentSchema
    print("\n[3] Testando SistemasAgentSchema...")
    try:
        sistemas = SistemasAgentSchema(
            resumo_ecossistema="2 sistemas",
            sistemas=[],
            integracoes=[],
            sistemas_criticados=["SAP"]
        )
        print(f"   SistemasAgentSchema: OK")
    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    # Testa RelacoesAgentSchema
    print("\n[4] Testando RelacoesAgentSchema...")
    try:
        relacoes = RelacoesAgentSchema(
            resumo_rede="Rede simples",
            relacoes=[],
            stakeholders=[],
            areas_mencionadas=[]
        )
        print(f"   RelacoesAgentSchema: OK")
    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    # Testa ProcessosAgentSchema
    print("\n[5] Testando ProcessosAgentSchema...")
    try:
        processos = ProcessosAgentSchema(
            resumo_processos="Processos mapeados",
            etapas_mapeadas=[],
            fluxos=[],
            cadeia_valor_abrangencia=["1. Novos Negócios"]
        )
        print(f"   ProcessosAgentSchema: OK")
    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    print(f"\n[RESULTADO] Todos schemas OK!")
    return True


if __name__ == "__main__":
    test_schemas()
