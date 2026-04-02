"""
Pain Points Agent - Especialista em identificar dores, gargalos e ETLs humanos.

Foco: ETL Humano, silos de informação, gargalos, workarounds.
"""
from pydantic import BaseModel, Field
from .base import IAgent


# ─────────────────────────────────────────────────────────────
# PYDANTIC SCHEMA
# ─────────────────────────────────────────────────────────────

class DorIdentificada(BaseModel):
    """Representa uma dor/ponto de dor identificado."""
    etapa_cadeia_valor: str = Field(description="Qual das 7 etapas da cadeia de valor")
    subcategoria: str = Field(description="Tipo específico: 'ETL Humano', 'Silo', 'Gargalo', 'Erro Manual', 'Falta Integração', etc")
    descricao: str = Field(description="Descrição detalhada do problema")
    citacao_direta: str = Field(description="Trecho EXATO em aspas que comprova a dor")
    sistemas_envolvidos: list[str] = Field(description="Sistemas mencionados neste contexto")
    impacto: str = Field(description="'Alto', 'Médio', 'Baixo' - impacto no negócio/CAPEX")


class DoresAgentSchema(BaseModel):
    """Schema de saída do Agent de Dores."""
    resumo_dores: str = Field(description="Resumo de 2-3 frases sobre o cenário geral de dores")
    dores: list[DorIdentificada]
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

class DoresAgent(IAgent):
    """Agent especializado em identificar dores, gargalos e ETLs humanos."""

    def get_name(self) -> str:
        return "dores"

    def get_schema(self) -> type:
        return DoresAgentSchema

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
