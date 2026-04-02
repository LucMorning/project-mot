import os
import asyncio
from dotenv import load_dotenv
from google import genai
from src.pipelines.agents import RelacoesAgent
from src.config import DB_PATH

async def test_relacoes_extraction():
    load_dotenv()
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    agent = RelacoesAgent()
    
    # Exemplo de fala com relação clara
    contexto = """FALA: 'Eu como Diretor de Capex (Sérgio), reporto diretamente ao Ricardo, que é nosso CEO.
    Dependo muito da área de Suprimentos para fechar os aditivos da Serra das Araras.'"""
    
    print("\n[DEBUG] Testando Extração v2.2 (Sênior Relacional)...")
    res = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contexto,
        config={
            'system_instruction': agent.get_system_prompt(),
            'response_mime_type': 'application/json',
            'response_schema': agent.get_schema(),
            'temperature': 0.1
        }
    )
    
    if res.parsed:
        print("\nRESPOSTA PARSEADA OK!")
        # Debugging the list of relations
        for r in res.parsed.relacoes:
            print(f"  - Tipo: {r.tipo}")
            print(f"  - Pessoa: {r.pessoa_citada}")
            print(f"  - Área: {r.area_citada}")

if __name__ == "__main__":
    asyncio.run(test_relacoes_extraction())
