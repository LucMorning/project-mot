import os
import dotenv
import google.generativeai as genai
from pydantic import BaseModel, Field

# Carrega o arquivo .env
dotenv.load_dotenv()

# Recupera a chave
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("[ERRO] GEMINI_API_KEY não encontrada no .env!")
    print("Certifique-se de que o arquivo .env existe e contém a sua chave.")
    exit(1)

print("[OK] Chave de API encontrada no .env!")

# Configura o Gemini
genai.configure(api_key=api_key)

# 1. Teste básico de conexão livre
print("\n--- Teste 1: Conexão e Geração Simples ---")
try:
    from src.config import AI_MODEL
    model = genai.GenerativeModel(AI_MODEL)
    print(f"Buscando modelo: {AI_MODEL}...")
    
    response = model.generate_content("Diga um 'Olá, mundo!' focado em engenharia de dados em 1 frase.")
    print("[BOT] Resposta do Gemini:")
    print(f"   > {response.text}")
    print("[OK] Teste 1 concluído com sucesso!")
except Exception as e:
    print(f"[ERRO] Teste 1 Falhou: {e}")


# 2. Teste de Structured Output (JSON/Pydantic) que é o que o nosso pipeline usa
print("\n--- Teste 2: Structured Output (JSON Schema) ---")
class TesteSchema(BaseModel):
    saudacao: str = Field(description="A saudação")
    sistema_citado: str = Field(description="Nome do sistema de banco de dados fictício")
    nivel_confianca: float = Field(description="Nível de 0 a 1")

try:
    prompt = "Crie uma saudação de bom dia que mencione o sistema PostgreSQL com nível de confiança 0.99."
    
    response_json = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=TesteSchema,
            temperature=0.1
        )
    )
    
    print("[BOT] Resposta Estruturada (JSON):")
    print(response_json.text)
    print("[OK] Teste 2 (Structured Output) concluído com sucesso!")
except Exception as e:
    print(f"[ERRO] Teste 2 Falhou: {e}")

print("\n[FIM] Se nenhum erro de chave ocorreu, a API está configurada no código!")
