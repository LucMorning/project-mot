import os
from google import genai
import dotenv

dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("[ERRO] GEMINI_API_KEY não configurada!")
    exit(1)

client = genai.Client(api_key=api_key)

def test_model(model_name):
    print(f"\n--- TESTANDO: {model_name} ---")
    try:
        response = client.models.generate_content(
            model=model_name,
            contents="Diga: 'Cota OK'",
            config={'temperature': 0.1}
        )
        print(f"  [RESULTADO]: {response.text.strip()}")
        return True
    except Exception as e:
        print(f"  [FALHA]: {e}")
        return False

# 1. Testar COM o prefixo models/
test_model("models/gemini-2.0-flash")

# 2. Testar SEM o prefixo
test_model("gemini-2.0-flash")

# 3. Testar o 2.5 tbm c/ prefixo
test_model("models/gemini-2.5-flash")
