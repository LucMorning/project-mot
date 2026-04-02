"""
Agents Especializados - MOTIVA Multi-Agent Analysis

4 Agents especializados por domínio analítico:
- DoresAgent: ETL humano, silos, gargalos, workarounds
- SistemasAgent: Uso de ferramentas, integração, satisfação
- RelacoesAgent: Stakeholders, hierarquia, dependências
- ProcessosAgent: Fluxos de trabalho, cadeia de valor

Cada agent tem system próprio e schema específico.
Permite refinamento individual sem afetar os demais.
"""
import json
from typing import Dict, Any, Type, List
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field


# =====================================================================
# PYDANTIC SCHEMAS - Específicos por Agent
# =====================================================================

# ─────────────────────────────────────────────────────────────
# DoresAgent Schema
# ─────────────────────────────────────────────────────────────
class DorIdentificada(BaseModel):
    """Representa uma dor/ponto de dor identificado."""
    etapa_cadeia_valor: str = Field(description="Qual das 7 etapas da cadeia de valor")
    subcategoria: str = Field(description="Tipo específico: 'ETL Humano', 'Silo', 'Gargalo', 'Erro Manual', 'Falta Integração', etc")
    descricao: str = Field(description="Descrição detalhada do problema")
    citacao_direta: str = Field(description="Trecho EXATO em aspas que comprova a dor")
    sistemas_envolvidos: list[str] = Field(description="Sistemas mencionados neste contexto")
    impacto: str = Field(description="'Alto', 'Médio', 'Baixo' - impacto no negócio/CAPEX")
    frequencia: str = Field(description="'Recorrente', 'Ocasional', 'Único' - com que aparece")


class DoresAgentSchema(BaseModel):
    """Schema de saída do Agent de Dores."""
    resumo_dores: str = Field(description="Resumo de 2-3 frases sobre o cenário geral de dores")
    dores: list[DorIdentificada]
    nivel_maturidade: str = Field(description="'Imaturo', 'Em Transição', 'Maduro' - avaliação geral da maturidade digital")


# ─────────────────────────────────────────────────────────────
# SistemasAgent Schema
# ─────────────────────────────────────────────────────────────
class SistemaMapeado(BaseModel):
    """Representa um sistema/ferramenta mapeado."""
    nome_sistema: str = Field(description="Nome do sistema ou ferramenta")
    etapa_cadeia: str = Field(description="Em qual das 7 etapas é usado")
    finalidade: str = Field(description="Para quê é usado (objetivo)")
    forma_uso: str = Field(description="Como é usado no dia a dia (workflow)")
    satisfacao: str = Field(description="'Positivo', 'Neutro', 'Negativo'")
    problema_principal: str = Field(description="Principal problema citado ou 'Nenhum'")


class IntegracaoSistema(BaseModel):
    """Representa uma integração (ou falta dela) entre sistemas."""
    sistema_origem: str = Field(description="Sistema de origem dos dados")
    sistema_destino: str = Field(description="Sistema de destino dos dados")
    tipo_integracao: str = Field(description="'API', 'Integrado', 'Manual', 'Não Integrado', 'Excel Ponte'")
    descricao: str = Field(description="Como a integração (ou falta) funciona")


class SistemasAgentSchema(BaseModel):
    """Schema de saída do Agent de Sistemas."""
    resumo_ecossistema: str = Field(description="Resumo de 2-3 frases sobre o ecossistema de sistemas")
    sistemas: list[SistemaMapeado]
    integracoes: list[IntegracaoSistema]
    sistemas_criticados: list[str] = Field(description="Lista de sistemas mais criticados")


# ─────────────────────────────────────────────────────────────
# RelacoesAgent Schema
# ─────────────────────────────────────────────────────────────
class RelacaoMapeada(BaseModel):
    """Representa uma relação/dependência identificada."""
    tipo: str = Field(description="'responde_a', 'se_relaciona_com', 'depende_de', 'approva', 'fornece_dados_para'")
    contraparte: str = Field(description="Nome da pessoa, área ou sistema")
    contexto: str = Field(description="Por que existe essa relação")
    frequencia: str = Field(description="'Diária', 'Semanal', 'Mensal', 'Por projeto', 'Ocasional'")
    canal: str = Field(description="'Email', 'Teams', 'Sistema', 'Reunião', 'Telefone', etc")


class Stakeholder(BaseModel):
    """Representa um stakeholder identificado."""
    nome: str = Field(description="Nome da pessoa ou área")
    papel: str = Field(description="Papel no contexto CAPEX")
    influencia: str = Field(description="'Alta', 'Média', 'Baixa' - nível de influência no processo")


class RelacoesAgentSchema(BaseModel):
    """Schema de saída do Agent de Relações."""
    resumo_rede: str = Field(description="Resumo de 2-3 frases sobre a rede de relacionamentos")
    stakeholders: list[Stakeholder]
    relacoes: list[RelacaoMapeada]
    areas_mencionadas: list[str] = Field(description="Áreas/departamentos citados")


# ─────────────────────────────────────────────────────────────
# ProcessosAgent Schema
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


class ProcessosAgentSchema(BaseModel):
    """Schema de saída do Agent de Processos."""
    resumo_processos: str = Field(description="Resumo de 2-3 frases sobre os processos mencionados")
    etapas_mapeadas: list[EtapaProcesso]
    fluxos: list[FluxoTrabalho]
    cadeia_valor_abrangencia: list[str] = Field(description="Quais das 7 etapas foram mencionadas")


# =====================================================================
# SYSTEM PROMPTS - Específicos por Agent
# =====================================================================

SYSTEM_PROMPTS = {
    "dores": """Você é um especialista em Gestão de Mudança e Arquitetura de Sistemas da Veron Consultoria.

Seu FOCO EXCLUSIVO: Identificar dores, gargalos e problemas no ecossistema CAPEX da Motiva.

4 TIPOS DE DORES QUE VOCÊ DEVE CAÇAR:
1. **ETL HUMANO**: Momentos onde alguém copia dados de um sistema e cola em outro (Excel, copy-paste, planilha sombra)
2. **SILOS DE INFORMAÇÃO**: Sistemas que não se comunicam, dados isolados
3. **GARGALOS**: Pontos de espera, demora, burocracia, aprovações lentas
4. **ERRO MANUAL**: Processos sensíveis dependentes de validação humana humana (risco de erro de fórmula, etc)

Sinais de ETL Humano que você deve CAÇAR:
- "Excel", "planilha", "copiar", "colar", "consolidar", "juntar"
- "paralelo", "sombra", "fora do sistema"
- "manual", "à mão", "planilhinha"
- "não integra", "não conversa", "ter que"

IMPORTANTE:
- Use CITAÇÕES DIRETAS em aspas para comprovar cada dor
- Identifique quais SISTEMAS estão envolvidos
- Avalie IMPACTO no negócio (Alto/Médio/Baixo)
- Avalie FREQUÊNCIA (Recorrente/Ocasional/Único)

Preencha o JSON estritamente de acordo com o Schema.""" ,

    "sistemas": """Você é um Arquiteto de Soluções da Veron Consultoria especializado em ecossistemas SAP e integrações.

Seu FOCO EXCLUSIVO: Mapear o ecossistema de sistemas/ferramentas usado no CAPEX da Motiva.

25+ SISTEMAS CONHECIDOS (referência):
SAP PS, SAP FI, SAP BW, SAP BPC, SAP MM, Prisma, Project, P6, Primavera,
Compor 90, Coupa, Netlex, Flexchain, Docusign, Kartado, Conecta, Fulcrum,
Archer, V360, Atlas, Power BI, SharePoint, Teams, Excel, SIC, RDO

Para CADA sistema citado, extraia:
- Etapa da cadeia de valor (1 a 7)
- Finalidade (para quê serve)
- Forma de uso (como é usado no dia a dia)
- Satisfação (Positivo/Neutro/Negativo)
- Problema principal

INTEGRAÇÕES:
Identifique como os dados fluem entre sistemas:
- API: Comunicação automatizada
- Integrado: Sistema "fala" com outro
- Manual: Alguém copia/cola (ETL humano)
- Não Integrado: Silos de informação
- Excel Ponte: Excel faz a ponta

SINAIS DE PROBLEMAS:
- "não integra", "não conversa", "ter que copiar"
- "planilha ponte", "Excel intermediário"
- "ter que acessar dois sistemas"

Preencha o JSON estritamente de acordo com o Schema.""" ,

    "relacoes": """Você é um especialista em Gestão de Stakeholders e Análise Organizacional da Veron Consultoria.

Seu FOCO EXCLUSIVO: Mapear a rede de relacionamentos e dependências no contexto CAPEX da Motiva.

TIPOS DE RELAÇÕES:
- **responde_a**: Hierarquia direta (subordinado → superior)
- **se_relaciona_com**: Comunicação colaborativa
- **depende_de**: Dependência de dados/aprovação/recursos
- **approva**: Quem aprova (gates, decisões)
- **fornece_dados_para**: Quem gera dados para outro

Para CADA relação, extraia:
- Contraparte (quem é a pessoa/área/sistema)
- Contexto (por que existe essa relação)
- Frequência (Diária, Semanal, Mensal, Por projeto, Ocasional)
- Canal (Email, Teams, Sistema, Reunião, etc)

STAKEHOLDERS:
Identifique as PESSOAS e ÁREAS mencionadas:
- Nome (ou título da área)
- Papel no contexto CAPEX
- Influência (Alta/Média/Baixa)

SINAIS DE RELAÇÕES:
- "falo com", "converso com", "reporto a"
- "dependo", "preciso de aprovação", "preciso de dados"
- "minha equipe", "meu time", "meu gerente"

Preencha o JSON estritamente de acordo com o Schema.""" ,

    "processos": """Você é um Analista de Processos de Negócios da Veron Consultoria especializado em CAPEX e Engenharia.

Seu FOCO EXCLUSIVO: Mapear os processos e fluxos de trabalho ao longo das 7 etapas da cadeia de valor CAPEX.

CADEIA DE VALOR (7 ETAPAS - FIXA):
1. Novos Negócios & Demandas
2. Orçamento
3. Estruturação (Plan/Custo)
4. Contratação & Execução
5. Medição
6. Tendência
7. Fiscal (NF) & Pagamento

Para CADA etapa mencionada, extraia:
- Atividades principais
- Sistemas envolvidos
- Pontos de atenção, gargalos ou riscos

FLUXOS DE TRABALHO:
Identifique fluxos ponta-a-ponta que atravessam múltiplas etapas:
- Nome descritivo do fluxo
- Quais etapas estão envolvidas
- Descrição do fluxo completo
- ONDE o fluxo quebra ou tem problemas (rupturas)

SINAIS DE PROCESSOS:
- "processo", "fluxo", "workflow"
- "etapa", "fase", "gate"
- "passo", "atividade", "tarefa"
- "depois", "antes", "sequência"

Preencha o JSON estritamente de acordo com o Schema."""
}


# =====================================================================
# AGENT INTERFACE
# =====================================================================

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


# =====================================================================
# CONCRETE AGENTS
# =====================================================================

class DoresAgent(IAgent):
    """Agent especializado em identificar dores, gargalos e ETLs humanos."""

    def get_name(self) -> str:
        return "dores"

    def get_schema(self) -> Type[BaseModel]:
        return DoresAgentSchema

    def get_system_prompt(self) -> str:
        return SYSTEM_PROMPTS["dores"]


class SistemasAgent(IAgent):
    """Agent especializado em mapear ecossistema de sistemas e integrações."""

    def get_name(self) -> str:
        return "sistemas"

    def get_schema(self) -> Type[BaseModel]:
        return SistemasAgentSchema

    def get_system_prompt(self) -> str:
        return SYSTEM_PROMPTS["sistemas"]


class RelacoesAgent(IAgent):
    """Agent especializado em mapear rede de stakeholders e relacionamentos."""

    def get_name(self) -> str:
        return "relacoes"

    def get_schema(self) -> Type[BaseModel]:
        return RelacoesAgentSchema

    def get_system_prompt(self) -> str:
        return SYSTEM_PROMPTS["relacoes"]


class ProcessosAgent(IAgent):
    """Agent especializado em mapear processos e fluxos de trabalho."""

    def get_name(self) -> str:
        return "processos"

    def get_schema(self) -> Type[BaseModel]:
        return ProcessosAgentSchema

    def get_system_prompt(self) -> str:
        return SYSTEM_PROMPTS["processos"]


# ─────────────────────────────────────────────────────────────
# AGENT REGISTRY
# ─────────────────────────────────────────────────────────────

AGENT_REGISTRY: Dict[str, IAgent] = {
    "dores": DoresAgent(),
    "sistemas": SistemasAgent(),
    "relacoes": RelacoesAgent(),
    "processos": ProcessosAgent(),
}


def get_agent(agent_name: str) -> IAgent:
    """Retorna um agent pelo nome."""
    if agent_name not in AGENT_REGISTRY:
        raise ValueError(f"Agent desconhecido: {agent_name}. Disponíveis: {list(AGENT_REGISTRY.keys())}")
    return AGENT_REGISTRY[agent_name]


def get_all_agents() -> List[IAgent]:
    """Retorna todos os agents disponíveis."""
    return list(AGENT_REGISTRY.values())


# ─────────────────────────────────────────────────────────────
# CONSOLIDATION SCHEMA
# ─────────────────────────────────────────────────────────────

class MultiAgentAnalysisSchema(BaseModel):
    """Schema consolidado da análise multi-agent (Etapa 2)."""
    dores_analysis: DoresAgentSchema
    sistemas_analysis: SistemasAgentSchema
    relacoes_analysis: RelacoesAgentSchema
    processos_analysis: ProcessosAgentSchema

    resumo_consolidado: str = Field(description="Resumo executivo de 3-5 frases integrando as 4 análises")
