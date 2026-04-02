"""
Agents Package - Multi-agent system para análise CAPEX.

4 Agents especializados por domínio:
- PainPointsAgent: ETL humano, silos, gargalos
- SystemsAgent: Uso de ferramentas, integração
- RelationsAgent: Stakeholders, relacionamentos
- ProcessesAgent: Fluxos de trabalho, cadeia de valor
"""
from typing import List, Dict
from .base import IAgent
from .dores import DoresAgent, DoresAgentSchema
from .sistemas import SystemsAgent, SistemasAgentSchema
from .relacoes import RelationsAgent, RelacoesAgentSchema
from .processos import ProcessesAgent, ProcessesAgentSchema


# ─────────────────────────────────────────────────────────────
# AGENT REGISTRY
# ─────────────────────────────────────────────────────────────

AGENT_REGISTRY: Dict[str, IAgent] = {
    "dores": DoresAgent(),
    "sistemas": SystemsAgent(),
    "relacoes": RelationsAgent(),
    "processos": ProcessesAgent(),
}


def get_agent(agent_name: str) -> IAgent:
    """Retorna um agent pelo nome."""
    if agent_name not in AGENT_REGISTRY:
        available = list(ACTIVE_AGENTS.keys())
        raise ValueError(f"Agent desconhecido: {agent_name}. Disponíveis: {available}")
    return AGENT_REGISTRY[agent_name]


def get_all_agents() -> List[IAgent]:
    """Retorna todos os agents disponíveis."""
    return list(ACTIVE_AGENTS.values())


# Alias para compatibilidade
ACTIVE_AGENTS = AGENT_REGISTRY

__all__ = [
    'IAgent',
    'DoresAgent', 'DoresAgentSchema',
    'SystemsAgent', 'SistemasAgentSchema',
    'RelationsAgent', 'RelationsAgentSchema',
    'ProcessesAgent', 'ProcessesAgentSchema',
    'AGENT_REGISTRY',
    'ACTIVE_AGENTS',
    'get_agent',
    'get_all_agents',
]
