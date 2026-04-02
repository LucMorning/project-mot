"""
Workflows - Orquestradores de pipelines em estágios.

Exporta:
- run_ingestion: Workflow de ingestão de dados
- run_ai_analysis: Workflow de análise com IA
- run_reports: Workflow de geração de relatórios
"""

from .ingestion import run_ingestion
from .ai_analysis import run_ai_analysis
from .reports import run_reports

__all__ = ['run_ingestion', 'run_ai_analysis', 'run_reports']
