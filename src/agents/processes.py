"""
Processes Agent - Especialista em mapear processos e fluxos de trabalho.

Foco: Fluxos de trabalho, cadeia de valor, etapas, rupturas.
"""
from pydantic import BaseModel, Field
from .base import IAgent


# ─────────────────────────────────────────────────────────────
# PYDANTIC SCHEMA
# ─────────────────────────────────────────────────────────────

class EtapaProcesso(BaseModel):
    """Representa uma etapa da cadeia de valor mencionada."""
    nome_etapa: str = Field(description="Nome da etapa (ex: '5. Medição')")
    atividades: list[str] = Field(description="Atividades principais nesta etapa")
    sistemas_envolvidos: list[str] = Field(description="Sistemas usados nesta etapa")
    pontos_atencao: list[str] = Field(description="Pontos de atenção, gargalos ou riscos")


class FluxoTrabalho(BaseModel):
    """Representa um fluxo de trabalho identificado."""
    nome_fluxo: str = Field(description="Nome descritivo do fluxo")
    etapas_envolvidas: list[str] = Field(description="Quais das 7 etapas da cadeia de valor estão envolvidas")
    descricao: str = Field(description="Descrição do fluxo de ponta a ponta")
    rupturas: list[str] = Field(description="Onde o fluxo quebra ou tem problemas")


class ProcessesAgentSchema(BaseModel):
    """Output schema for Processes Agent."""
    resumo_processos: str = Field(description="Resumo de 2-3 frases sobre os processos mencionados")
    etapas_mapeadas: list[EtapaProcesso]
    fluxos: list[FluxoTrabalho]
    cadeia_valor_abrangencia: list[str] = Field(description="Quais das 7 etapas foram mencionadas")


# ─────────────────────────────────────────────────────────────
# SYSTEM PROMPT
# ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a Business Process Analyst specialized in CAPEX and Engineering at Veron Consulting.

Your EXCLUSIVE FOCUS: Map workflows and value chain processes across the 7 CAPEX value chain stages.

VALUE CHAIN (7 STAGES - FIXED):
1. Novos Negócios & Demandas
2. Orçamento
3. Estruturação (Plan/Custo)
4. Contratação & Execução
5. Medição
6. Tendência
7. Fiscal (NF) & Pagamento

For EACH stage mentioned, extract:
- Main activities
- Systems involved
- Pain points, bottlenecks or risks

WORKFLOWS:
Identify point-to-point workflows that cross multiple stages:
- Descriptive workflow name
- Which stages are involved
- Complete workflow description
- WHERE the workflow breaks or has problems (ruptures)

PROCESS SIGNS:
- "processo", "fluxo", "workflow"
- "etapa", "fase", "gate"
- "passo", "atividade", "tarefa"
- "depois", "antes", "sequência"

Fill the JSON strictly according to the Schema."""


# ─────────────────────────────────────────────────────────────
# AGENT CLASS
# ─────────────────────────────────────────────────────────────

class ProcessesAgent(IAgent):
    """Agent especializado em mapear processos e fluxos de trabalho."""

    def get_name(self) -> str:
        return "processes"

    def get_schema(self) -> type:
        return ProcessesAgentSchema

    def get_system_prompt(self) -> str:
        return SYSTEM_PROMPT

    def get_keywords(self) -> list[str]:
        """Keywords que identificam se este agent é necessário."""
        return [
            'processo', 'fluxo', 'workflow', 'etapa', 'fase',
            'gate', 'passo', 'atividade', 'tarefa',
            'depois', 'antes', 'sequência', 'pipeline',
            'aprova', 'valida', 'revisa'
        ]
