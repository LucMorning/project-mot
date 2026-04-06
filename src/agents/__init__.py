"""
Agents Package - Multi-agent system para análise CAPEX.

4 Agents especializados por domínio:
- PainPointsAgent: ETL humano, silos, gargalos
- SystemsAgent: Uso de ferramentas, integração
- RelationsAgent: Stakeholders, relacionamentos
- ProcessesAgent: Fluxos de trabalho, cadeia de valor

WHITELIST: O SystemsAgent usa apenas sistemas do catálogo oficial.
"""
from typing import List, Dict, Optional
from .base import IAgent
from .pain_points import PainPointsAgent, PainPointsAgentSchema
from .systems import SystemsAgent, SystemsAgentSchema
from .relations import RelationsAgent, RelationsAgentSchema
from .processes import ProcessesAgent, ProcessesAgentSchema


# ─────────────────────────────────────────────────────────────
# AGENT REGISTRY
# ─────────────────────────────────────────────────────────────

# Agentes base (sem configuração especial)
_AGENT_FACTORIES = {
    "pain_points": lambda: PainPointsAgent(),
    "systems": lambda sistemas=None: SystemsAgent(sistemas),
    "relations": lambda: RelationsAgent(),
    "processes": lambda: ProcessesAgent(),
}

# Registry instanciado (pode ser reconfigurado)
AGENT_REGISTRY: Dict[str, IAgent] = {
    "pain_points": _AGENT_FACTORIES["pain_points"](),
    "systems": _AGENT_FACTORIES["systems"](),
    "relations": _AGENT_FACTORIES["relations"](),
    "processes": _AGENT_FACTORIES["processes"](),
}


def configure_systems_agent(sistemas_oficiais: List[str]) -> None:
    """
    Reconfigura o SystemsAgent com whitelist de sistemas oficiais.

    Args:
        sistemas_oficiais: Lista de nomes do catálogo dim_sistemas (fonte='relatorio_ti')
    """
    AGENT_REGISTRY["systems"] = SystemsAgent(sistemas_oficiais)


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
    'configure_systems_agent',
]
