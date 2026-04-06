"""
Pain Points Agent - Especialista em identificar dores, gargalos e ETLs humanos.

Foco: ETL Humano, silos de informação, gargalos, workarounds.
"""
from pydantic import BaseModel, Field
from .base import IAgent


# ─────────────────────────────────────────────────────────────
# PYDANTIC SCHEMA
# ─────────────────────────────────────────────────────────────

class PainPoint(BaseModel):
    """Represents a pain point identified."""
    etapa_cadeia_valor: str = Field(description="Qual das 7 etapas da cadeia de valor")
    subcategoria: str = Field(description="Tipo específico: 'ETL Humano', 'Silo', 'Gargalo', 'Erro Manual', 'Falta Integração', etc")
    descricao: str = Field(description="Descrição detalhada do problema")
    citacao_direta: str = Field(description="Trecho EXATO em aspas que comprova a dor")
    linhagem_dado: str = Field(description="De onde o dado vem e para onde vai (ex: 'Sai do SAP PS pro Excel')")
    risco_ao_negocio: str = Field(description="Qual o risco real: 'Financeiro', 'Compliance', 'Atraso', 'Dados Errados'")
    area_impactada: str = Field(description="Qual área interna da Motiva sofre com isso")
    sistemas_envolvidos: list[str] = Field(description="Sistemas mencionados neste contexto")
    impacto: str = Field(description="'Alto', 'Médio', 'Baixo' - impacto no negócio/CAPEX")


class PainPointsAgentSchema(BaseModel):
    """Output schema for Pain Points Agent."""
    resumo_dores: str = Field(description="Resumo de 2-3 frases sobre o cenário geral de dores")
    dores: list[PainPoint]
    nivel_maturidade: str = Field(description="'Imaturo', 'Em Transição', 'Maduro' - avaliação geral da maturidade digital")


# ─────────────────────────────────────────────────────────────
# SYSTEM PROMPT (inglês = ok, mas dados retornados em pt-br)
# ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a Change Management and Systems Architecture specialist at Veron Consulting.

Your EXCLUSIVE FOCUS: Identify pain points, bottlenecks and problems in the CAPEX ecosystem of Motiva.

4 TYPES OF PAIN TO HUNT:
1. **MANUAL ETL**: Moments where someone copies data from one system and pastes into another (Excel, copy-paste, shadow spreadsheet)
2. **INFORMATION SILOS**: Systems that don't communicate, isolated data
3. **BOTTLENECKS**: Waiting points, delays, bureaucracy, slow approvals
4. **MANUAL ERROR**: Sensitive processes dependent on human validation (formula error risk, etc)

DATA LINEAGE & RISK FOCUS:
For each pain point, you MUST identify:
- **DATA LINEAGE**: Where the data starts and where it ends (e.g. from SAP PS to Excel).
- **BUSINESS RISK**: Identify if it's a financial risk, compliance, delay or wrong data.
- **IMPACTED AREA**: Mention the area (e.g. Engineering, Procurement, Finance).

Signs of Manual ETL to HUNT:
- "Excel", "spreadsheet", "copy", "paste", "consolidate", "merge"
- "parallel", "shadow", "outside the system"
- "manual", "by hand", "little spreadsheet"
- "doesn't integrate", "doesn't talk", "have to"

IMPORTANT:
- Use DIRECT QUOTES in quotes to prove each pain point
- Identify which SYSTEMS are involved
- Assess BUSINESS IMPACT (High/Medium/Low)

Fill the JSON strictly according to the Schema."""


# ─────────────────────────────────────────────────────────────
# AGENT CLASS
# ─────────────────────────────────────────────────────────────

class PainPointsAgent(IAgent):
    """Agent especializado em identificar dores, gargalos e ETLs humanos."""

    def get_name(self) -> str:
        return "pain_points"

    def get_schema(self) -> type:
        return PainPointsAgentSchema

    def get_system_prompt(self) -> str:
        return SYSTEM_PROMPT

    def get_keywords(self) -> list[str]:
        """
        Keywords que identificam se este agent é necessário.

        Usado pelo Orchestrator para decidir quais agents executar.
        """
        return [
            'excel', 'planilha', 'copiar', 'colar', 'consolidar',
            'manual', 'à mão', 'gargalo', 'lento', 'demora',
            'erro', 'errado', 'problema', 'dificuldade', 'travar',
            'não integra', 'não conversa', 'ter que'
        ]
