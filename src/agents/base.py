"""
Base Agent Interface - Interface para todos os agents.

Define o contrato que todo agent deve seguir.
"""
from abc import ABC, abstractmethod
from typing import Type
from pydantic import BaseModel


class IAgent(ABC):
    """Interface base para todos os agents."""

    @abstractmethod
    def get_name(self) -> str:
        """Nome do agent."""
        pass

    @abstractmethod
    def get_schema(self) -> Type[BaseModel]:
        """Schema Pydantic de saída."""
        pass

    @abstractmethod
    def get_system_prompt(self) -> str:
        """System prompt específico do agent."""
        pass

    def get_keywords(self) -> list[str]:
        """
        Palavras-chave que identificam se este agent é necessário.

        Usado pelo Orchestrator para decidir quais agents executar.

        Returns:
            Lista de keywords (ex: ['excel', 'planilha', 'manual'])
        """
        return []
