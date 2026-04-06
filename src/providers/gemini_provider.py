"""
Gemini AI Provider - Wrapper centralizado para a API Gemini.

Usado por todos os pipelines de IA (batch, staged, agents).
Usa o SDK moderno: google-genai (genai.Client).
"""
import json
import warnings
from typing import Dict, Any, Type

from google import genai

from src.config import AI_TEMPERATURE

warnings.filterwarnings('ignore', category=FutureWarning)


def _clean_schema(schema_dict: dict) -> None:
    """
    Remove campos não suportados pelo Gemini structured output.

    O Gemini rejeita 'additionalProperties' em JSON Schema.
    Operação in-place recursiva.
    """
    if not isinstance(schema_dict, dict):
        return
    schema_dict.pop("additionalProperties", None)
    for value in schema_dict.values():
        if isinstance(value, dict):
            _clean_schema(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    _clean_schema(item)


class GeminiProvider:
    """
    Wrapper para a API Gemini com suporte a structured output.

    Attributes:
        model_name: Nome do modelo (ex: gemini-2.5-flash)
    """

    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        """
        Inicializa o provider Gemini.

        Args:
            api_key: Chave da API Gemini
            model_name: Nome do modelo a usar
        """
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def analyze(
        self,
        system_prompt: str,
        user_content: str,
        schema=None
    ) -> Dict[str, Any]:
        """
        Executa análise com a API Gemini.

        Args:
            system_prompt: Prompt de sistema (instruções do agent)
            user_content: Conteúdo do usuário (transcrição, contexto)
            schema: Pydantic schema para structured output (opcional)

        Returns:
            Dict com o resultado da análise
        """
        config: Dict[str, Any] = {
            'system_instruction': system_prompt,
            'temperature': AI_TEMPERATURE,
        }

        if schema is not None:
            # Converte schema Pydantic → JSON Schema e limpa para o Gemini
            if hasattr(schema, "model_json_schema"):
                json_schema = schema.model_json_schema()
            else:
                json_schema = schema.schema()

            _clean_schema(json_schema)
            config['response_mime_type'] = 'application/json'
            config['response_schema'] = json_schema

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_content,
                config=config
            )
            return json.loads(response.text)

        except Exception as e:
            print(f"[ERRO] Gemini API ({self.model_name}): {e}")
            raise


def create_provider(model_name: str = None) -> GeminiProvider:
    """
    Factory function para criar GeminiProvider com config do .env.

    Args:
        model_name: Nome do modelo (opcional, usa AI_MODEL do config)

    Returns:
        Instância de GeminiProvider configurada
    """
    import os
    import dotenv
    from src.config import AI_API_KEY_ENV, AI_MODEL

    dotenv.load_dotenv()

    api_key = os.getenv(AI_API_KEY_ENV)
    if not api_key:
        raise ValueError(f"{AI_API_KEY_ENV} não configurada no .env")

    return GeminiProvider(
        api_key=api_key,
        model_name=model_name or os.getenv("GEMINI_MODEL", AI_MODEL)
    )
