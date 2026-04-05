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
from .pain_points import PainPointsAgent, PainPointsAgentSchema
from .systems import SystemsAgent, SystemsAgentSchema
from .relations import RelationsAgent, RelationsAgentSchema
from .processes import ProcessesAgent, ProcessesAgentSchema


# ─────────────────────────────────────────────────────────────
# AGENT REGISTRY
# ─────────────────────────────────────────────────────────────

AGENT_REGISTRY: Dict[str, IAgent] = {
    "pain_points": PainPointsAgent(),
    "systems": SystemsAgent(),
    "relations": RelationsAgent(),
    "processes": ProcessesAgent(),
}


def get_agent(agent_name: str) -> IAgent:
    """Retorna um agent pelo nome."""
    if agent_name not in AGENT_REGISTRY:
        available = list(AGENT_REGISTRY.keys())
        raise ValueError(f"Agent desconhecido: {agent_name}. Disponíveis: {available}")
    return AGENT_REGISTRY[agent_name]


def get_all_agents() -> List[IAgent]:
    """Retorna todos os agents disponíveis."""
    return list(AGENT_REGISTRY.values())


# Alias para compatibilidade
ACTIVE_AGENTS = AGENT_REGISTRY

__all__ = [
    'IAgent',
    'PainPointsAgent', 'PainPointsAgentSchema',
    'SystemsAgent', 'SystemsAgentSchema',
    'RelationsAgent', 'RelationsAgentSchema',
    'ProcessesAgent', 'ProcessesAgentSchema',
    'AGENT_REGISTRY',
    'ACTIVE_AGENTS',
    'get_agent',
    'get_all_agents',
]
