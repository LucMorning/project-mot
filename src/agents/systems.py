"""
Systems Agent - Especialista em mapear ecossistema de sistemas e integrações.

Foco: Uso de ferramentas, integração (ou falta dela), satisfação.

WHITELIST: Apenas sistemas do catálogo oficial dim_sistemas (fonte='relatorio_ti')
são considerados válidos. Documentos, pessoas e processos são ignorados.
"""
from pydantic import BaseModel, Field
from typing import List
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
    inputs: str = Field(description="De onde vêm os dados (origem)")
    outputs: str = Field(description="Para onde vão os dados (destino)")
    is_excel_bridge: bool = Field(description="True se for uma planilha Excel usada como ponte entre sistemas")
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

Your EXCLUSIVE FOCUS: Map the systems/tools ecosystem used in Motiva's CAPEX and their DATA FLOW.

DATA LINEAGE FOCUS:
For each system, you MUST extract:
- **INPUTS**: Where does data come from? (e.g. from a PDF, from SAP MM, from manual entry).
- **OUTPUTS**: Where does data go? (e.g. to Power BI, to another Excel, to SAP FI).
- **EXCEL BRIDGE**: Detect if it's a "shadow spreadsheet" used to connect two systems.

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
- Excel Bridge: Excel makes the connection (mark is_excel_bridge=True)

PROBLEM SIGNS:
- "doesn't integrate", "doesn't talk", "have to copy"
- "spreadsheet bridge", "Excel intermediary"
- "have to access two systems"

Fill the JSON strictly according to the Schema."""


# ─────────────────────────────────────────────────────────────
# AGENT CLASS
# ─────────────────────────────────────────────────────────────

class SystemsAgent(IAgent):
    """Agent especializado em mapear ecossistema de sistemas e integrações.

    Whitelist: Usa apenas sistemas do catálogo oficial dim_sistemas.
    """

    def __init__(self, sistemas_oficiais: List[str] = None):
        """
        Inicializa o agente com whitelist de sistemas oficiais.

        Args:
            sistemas_oficiais: Lista de nomes de sistemas do catálogo TI.
                              Se None, usa lista hardcoded (fallback).
        """
        self.sistemas_oficiais = sistemas_oficiais or self._get_fallback_list()

    def _get_fallback_list(self) -> List[str]:
        """Lista de fallback caso não seja fornecida."""
        return [
            "SAP PS", "SAP FI", "SAP BW", "SAP BPC", "SAP MM",
            "Prisma", "Project", "P6", "Primavera", "Excel",
            "Compor 90", "Coupa", "Netlex", "Flexchain", "Docusign",
            "Teams", "Kartado", "SharePoint", "Power Apps", "Power BI",
            "Conecta", "Fulcrum", "Archer", "V360", "Atlas",
            "Forms", "SIC", "RDO", "Outlook", "Jacket", "VLT"
        ]

    def get_name(self) -> str:
        return "systems"

    def get_schema(self) -> type:
        return SystemsAgentSchema

    def get_system_prompt(self) -> str:
        """Retorna prompt com whitelist de sistemas oficiais."""
        sistemas_str = ", ".join(self.sistemas_oficiais[:30])  # Primeiros 30

        return f"""You are a Solutions Architect at Veron Consulting specialized in SAP ecosystems and integrations.

Your EXCLUSIVE FOCUS: Map the systems/tools ecosystem used in Motiva's CAPEX and their DATA FLOW.

CRITICAL CONSTRAINT - WHITELIST ONLY:
You MUST ONLY identify systems from this official catalog:
{sistemas_str}

If a mentioned tool is NOT in this list, DO NOT create a new entry.
Examples of what to IGNORE:
- Documents (Boletim, RDO, RNC, PowerPoint, Word)
- Communication channels (E-mail, Teams chat)
- People (Engenheiro, Gestor)
- Generic tools used for specific purposes (Excel for X, Planilha de Y)

DATA LINEAGE FOCUS:
For each system, you MUST extract:
- **INPUTS**: Where does data come from? (e.g. from a PDF, from SAP MM, from manual entry).
- **OUTPUTS**: Where does data go? (e.g. to Power BI, to another Excel, to SAP FI).
- **EXCEL BRIDGE**: Detect if it's a "shadow spreadsheet" used to connect two systems.

For EACH system from the whitelist, extract:
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
- Excel Bridge: Excel makes the connection (mark is_excel_bridge=True)

Fill the JSON strictly according to the Schema."""

    def get_keywords(self) -> list[str]:
        """Keywords que identificam se este agent é necessário."""
        return [
            'sap', 'sistema', 'aplicativo', 'ferramenta', 'software',
            'plataforma', 'uso', 'utiliza', 'acessa',
            'integra', 'conversa', 'conecta'
        ]
