"""
Gemini AI Provider - Wrapper centralizado para a API Gemini.

Usado por todos os pipelines de IA (batch, staged, agents).
"""
import json
import warnings
from typing import Dict, Any, Type
from pathlib import Path

import google.generativeai as genai

warnings.filterwarnings('ignore', category=FutureWarning)


class GeminiProvider:
    """
    Wrapper para a API Gemini com suporte a structured output.

    Attributes:
        model_name: Nome do modelo (ex: gemini-2.5-flash)
    """

    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        """
        Inicializa o provider Gemini.

        Args:
            api_key: Chave da API Gemini
            model_name: Nome do modelo a usar
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name

    def analyze(
        self,
        system_prompt: str,
        user_content: str,
        schema: Type[BaseModel] = None
    ) -> Dict[str, Any]:
        """
        Executa análise com a API Gemini.

        Args:
            system_prompt: Prompt de sistema (instruções)
            user_content: Conteúdo do usuário (transcrição, contexto)
            schema: Pydantic schema para structured output (opcional)

        Returns:
            Dict com o resultado da análise
        """
        prompt = f"{system_prompt}\n\nCONTEXTO DO USUÁRIO:\n{user_content}"

        try:
            if schema:
                # Structured output com schema
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json",
                        response_schema=schema,
                        temperature=0.2
                    )
                )
            else:
                # Texto livre
                response = self.model.generate_content(prompt)

            return json.loads(response.text)

        except Exception as e:
            print(f"[ERRO] Gemini API: {e}")
            raise


def create_provider(model_name: str = None) -> GeminiProvider:
    """
    Factory function para criar GeminiProvider com config do .env.

    Args:
        model_name: Nome do modelo (opcional, usa GEMINI_MODEL do .env)

    Returns:
        Instância de GeminiProvider configurada
    """
    import os
    import dotenv

    dotenv.load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY não configurada no .env")

    if model_name is None:
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    return GeminiProvider(api_key=api_key, model_name=model_name)
