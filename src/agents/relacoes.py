"""
Relations Agent - Especialista em mapear rede de stakeholders e relacionamentos.

Foco: Hierarquia, dependências, comunicação entre áreas/pessoas.
"""
from pydantic import BaseModel, Field
from .base import IAgent


# ─────────────────────────────────────────────────────────────
# PYDANTIC SCHEMA
# ─────────────────────────────────────────────────────────────

class RelacaoMapeada(BaseModel):
    """Representa uma relação/dependência identificada."""
    tipo: str = Field(description="'responde_a', 'se_relaciona_com', 'depende_de', 'approva', 'fornece_dados_para'")
    contraparte: str = Field(description="Nome da pessoa ou área mencionada")
    contexto: str = Field(description="Por que existe essa relação")


class RelacoesAgentSchema(BaseModel):
    """Schema de saída do Agent de Relações."""
    resumo_rede: str = Field(description="Resumo de 2-3 frases sobre a rede de relacionamentos")
    relacoes: list[RelacaoMapeada]
    stakeholders: list[str] = Field(description="Pessoas e áreas mencionadas")
    areas_mencionadas: list[str] = Field(description="Áreas/departamentos citados")


# ─────────────────────────────────────────────────────────────
# SYSTEM PROMPT
# ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a Stakeholder Management and Organizational Analysis specialist at Veron Consulting.

Your EXCLUSIVE FOCUS: Map the network of relationships and dependencies in the Motiva CAPEX context.

RELATIONSHIP TYPES:
- **responde_a**: Direct hierarchy (subordinate → superior)
- **se_relaciona_com**: Collaborative communication
- **depende_de**: Dependency on data/approval/resource
- **approva**: Who approves (gates, decisions)
- **fornece_dados_para**: Who generates data for another

For EACH relationship, extract SEPARATELY:
- Counterpart (person name, or area name)
- Context (why this relationship exists)

STAKEHOLDERS:
Identify mentioned PEOPLE and AREAS in a structured way.

Fill the JSON strictly according to the Schema."""


# ─────────────────────────────────────────────────────────────
# AGENT CLASS
# ─────────────────────────────────────────────────────────────

class RelationsAgent(IAgent):
    """Agent especializado em mapear rede de stakeholders e relacionamentos."""

    def get_name(self) -> str:
        return "relacoes"

    def get_schema(self) -> type:
        return RelacoesAgentSchema

    def get_system_prompt(self) -> str:
        return SYSTEM_PROMPT

    def get_keywords(self) -> list[str]:
        """Keywords que identificam se este agent é necessário."""
        return [
            'falar com', 'aprova', 'departamento', 'equipe', 'gestor',
            'coordenador', 'gerente', 'diretor', 'líder',
            'depende', 'precisa de', 'passa por', 'relaciona',
            'comunica', 'interage', 'trabalha com'
        ]
