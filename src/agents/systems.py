"""
Systems Agent - Especialista em mapear ecossistema de sistemas e integrações.

Foco: Uso de ferramentas, integração (ou falta dela), satisfação.
"""
from pydantic import BaseModel, Field
from .base import IAgent


# ─────────────────────────────────────────────────────────────
# PYDANTIC SCHEMA
# ─────────────────────────────────────────────────────────────

class SystemMapped(BaseModel):
    """Represents a system/tool mapped."""
    nome_sistema: str = Field(description="Nome do sistema ou ferramenta")
    etapa_cadeia: str = Field(description="Em qual das 7 etapas é usado")
    finalidade: str = Field(description="Para quê é usado (objetivo)")
    forma_uso: str = Field(description="Como é usado no dia a dia (workflow)")
    satisfacao: str = Field(description="'Positivo', 'Neutro', 'Negativo'")
    problema_principal: str = Field(description="Principal problema citado ou 'Nenhum'")


class SystemsAgentSchema(BaseModel):
    """Output schema for Systems Agent."""
    resumo_ecossistema: str = Field(description="Resumo de 2-3 frases sobre o ecossistema de sistemas")
    sistemas: list[SystemMapped]
    integracoes: list[dict]
    sistemas_criticados: list[str] = Field(description="Lista de sistemas mais criticados")


# ─────────────────────────────────────────────────────────────
# SYSTEM PROMPT
# ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a Solutions Architect at Veron Consulting specialized in SAP ecosystems and integrations.

Your EXCLUSIVE FOCUS: Map the systems/tools ecosystem used in Motiva's CAPEX.

25+ KNOWN SYSTEMS (reference):
SAP PS, SAP FI, SAP BW, SAP BPC, SAP MM, Prisma, Project, P6, Primavera,
Compor 90, Coupa, Netlex, Flexchain, Docusign, Kartado, Conecta, Fulcrum,
Archer, V360, Atlas, Power BI, SharePoint, Teams, Excel, SIC, RDO

For EACH system mentioned, extract:
- Value chain stage (1 to 7)
- Purpose (what it's for)
- Usage form (how it's used day-to-day)
- Satisfaction (Positive/Neutral/Negative)
- Main problem

INTEGRATIONS:
Identify how data flows between systems:
- API: Automated communication
- Integrated: System "talks" to another
- Manual: Someone copies/pastes (manual ETL)
- Not Integrated: Information silos
- Excel Bridge: Excel makes the connection

PROBLEM SIGNS:
- "doesn't integrate", "doesn't talk", "have to copy"
- "spreadsheet bridge", "Excel intermediary"
- "have to access two systems"

Fill the JSON strictly according to the Schema."""


# ─────────────────────────────────────────────────────────────
# AGENT CLASS
# ─────────────────────────────────────────────────────────────

class SystemsAgent(IAgent):
    """Agent especializado em mapear ecossistema de sistemas e integrações."""

    def get_name(self) -> str:
        return "systems"

    def get_schema(self) -> type:
        return SystemsAgentSchema

    def get_system_prompt(self) -> str:
        return SYSTEM_PROMPT

    def get_keywords(self) -> list[str]:
        """Keywords que identificam se este agent é necessário."""
        return [
            'sap', 'sistema', 'aplicativo', 'ferramenta', 'software',
            'plataforma', 'uso', 'utiliza', 'acessa',
            'integra', 'conversa', 'conecta'
        ]
