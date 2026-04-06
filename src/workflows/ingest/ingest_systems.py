"""
Sistemas TI Ingest - Mapeia relatório de sistemas TI para o banco.

Usa tabelas dim_sistemas e dim_processos criadas pelo schema.py.
"""
import sqlite3
import sys
sys.path.insert(0, '.')
from src.config import DB_PATH


def map_sistemas_ti_to_db():
    """Mapeia os dados do Relatório de Sistemas TI para o banco de dados."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Dados do Slide 2 - Visão Macro de Sistemas (25 sistemas em 7 etapas)
    sistemas_data = [
        # Etapa 1: Estruturação PEP e EAP
        ('Prisma', 'Estruturação PEP e EAP', None),
        ('Fli/CO', 'Estruturação PEP e EAP', None),
        ('SAP PS', 'Estruturação PEP e EAP', None),
        ('Compor 90', 'Estruturação PEP e EAP', None),
        ('Excel', 'Estruturação PEP e EAP', None),
        ('Project', 'Estruturação PEP e EAP', None),

        # Etapa 2: Contratação
        ('DocuSign', 'Contratação', None),
        ('Coupia', 'Contratação', None),
        ('SAP', 'Contratação', None),
        ('Teams', 'Contratação', None),
        ('Netflex', 'Contratação', None),
        ('Flexchain', 'Contratação', None),

        # Etapa 3: Planejamento e Execução
        ('PM', 'Planejamento e Execução', None),
        ('Kartado', 'Planejamento e Execução', None),
        ('Power Apps', 'Planejamento e Execução', None),
        ('SharePoint', 'Planejamento e Execução', None),
        ('Conecta', 'Planejamento e Execução', None),

        # Etapa 4: Medição
        ('Fulcrum', 'Medição', None),
        ('SAP PS/FI', 'Medição', None),

        # Etapa 5: Tendência
        ('Archer', 'Tendência', None),
        ('SAP BW/BPC', 'Tendência', None),
        ('BI', 'Tendência', None),
        ('Teams Idea', 'Tendência', None),

        # Etapa 6: Fiscal e NF
        ('Atlas', 'Fiscal e NF', None),
        ('V360', 'Fiscal e NF', None),
        ('SAP FI', 'Fiscal e NF', None),
        ('Forms', 'Fiscal e NF', None),

        # Etapa 7: Pagamento
        ('Painel de Chamados', 'Pagamento', None),
        ('SAP FI/AP', 'Pagamento', None),
    ]

    # Dados dos Slides 3, 4, 5 - Processos por Área
    processos_data = [
        # Slide 3 - Outras Áreas (Corporativo)
        ('Gestão do Capex', 'Núcleo Capex', None),
        ('Atualização Curva Iso Risco', 'Núcleo Capex', None),
        ('Reunião quinzenal de Gestão de Risco', 'Núcleo Capex', None),
        ('Definição de Orçamento', 'Núcleo Capex', None),
        ('Orçamento, Negociação e Contratação', 'Suprimentos', None),
        ('Criação de Contrato e Pedido de Compra', 'Suprimentos', None),
        ('Aditivo contratual', 'Suprimentos', None),
        ('Estruturação do PEP', 'Frotas', None),
        ('Medição produto', 'Frotas', None),
        ('Medição Serviços', 'Frotas', None),
        ('Compra sob demanda', 'Frotas', None),
        ('Compra Nova Concessão', 'Frotas', None),
        ('Medição - Serviço', 'TI', None),
        ('Medição - Materiais', 'TI', None),
        ('Remanejamento de PEPs', 'TI', None),
        ('Criação de Elemento PEP', 'PMO TI', None),
        ('Criação de Elemento PEP Filho', 'PMO TI', None),
        ('Carga de orçamento no PEP', 'PMO TI', None),
        ('Criação de PEP e Contratação', 'PMO TI', None),
        ('Recebimento (Material)', 'Facilities', None),
        ('Integração', 'Facilities', None),
        ('Medição (Serviço)', 'Facilities', None),
        ('Contratação de Serviços de Manutenção', 'Tendência', None),
        ('Medição do Serviço Prestado', 'Segurança', None),
        ('Medição de Serviços (CSC e Tecnologia)', 'Central de Medição', None),
        ('Medição de Serviços Jurídico', 'Central de Medição', None),
        ('Processo de Liquidação da Conta 8', 'Central de Medição', None),
        ('Entrada NF e Folha de Registro', 'Central de Medição', None),
        ('Recebimento Integrado Entrada NF', 'Central de Medição', None),
        ('Pagamentos', 'Pagamentos', None),

        # Slide 4 - Trilhos
        ('Trilhos - Eng. Custos - Orçamento', 'Eng. Custos', 'Trilhos'),
        ('Trilhos - Qualidade', 'Qualidade', 'Trilhos'),
        ('Administração Contratual - Trilhos', 'Adm Contratual', 'Trilhos'),
        ('Criação PEP', 'PMO Financeiro', 'Trilhos'),
        ('Camadas Folha de Medição', 'PMO Financeiro', 'Trilhos'),
        ('Antecipação de Pagamento', 'PMO Financeiro', 'Trilhos'),
        ('Bloqueio de Pagamento', 'PMO Financeiro', 'Trilhos'),
        ('Desbloqueio de Pagamento', 'PMO Financeiro', 'Trilhos'),
        ('Lançamentos Urgentes', 'PMO Financeiro', 'Trilhos'),
        ('Adiantamento de Pagamento', 'PMO Financeiro', 'Trilhos'),
        ('Estorno de Pagamento - 19', 'PMO Financeiro', 'Trilhos'),
        ('Regularização', 'PMO Financeiro', 'Trilhos'),
        ('Contratos - Remanejamento', 'PMO Financeiro', 'Trilhos'),
        ('Contratos - Encerramento', 'PMO Financeiro', 'Trilhos'),
        ('Contratos - Reajuste', 'PMO Financeiro', 'Trilhos'),
        ('Tendência', 'PMO Financeiro', 'Trilhos'),
        ('Projeto de Engenharia e Centro de Expertise', 'Projetos de Engenharia', 'Trilhos'),
        ('Gestão Adm de contratos', 'GAC', 'Trilhos'),
        ('IFRS', 'PMO Financeiro', 'Trilhos'),
        ('Planejamento', 'PMO Planejamento', 'Trilhos'),
        ('Gestão de Aditivos e Mudanças Contratuais', 'PMO Planejamento', 'Trilhos'),
        ('Desenvolvimento de Projetos', 'PMO Engenharia', 'Trilhos'),
        ('Distribuição de Chamados', 'PMO Financeiro', 'Trilhos'),

        # Slide 5 - Rodovias
        ('Orçamentação Obras - Criação Requisição de Compras', 'Engenharia Custo', 'Rodovias'),
        ('Revisão da Requisição de Compras', 'Engenharia Custo', 'Rodovias'),
        ('Criação de Requisição de Compras por Aditivo', 'Engenharia Custo', 'Rodovias'),
        ('Planejamento de Medição e qualidade', 'Engenharia Custo', 'Rodovias'),
        ('Qualidade e Inspeção', 'Qualidade', 'Rodovias'),
        ('Fluxo de Não Conformidade', 'Qualidade', 'Rodovias'),
        ('Gestão de Não Conformidade', 'Qualidade', 'Rodovias'),
        ('Data Book', 'Qualidade', 'Rodovias'),
        ('Estruturação do Capex', 'PMO Unidades', 'Rodovias'),
        ('Gestão do Capex e Atualização de Tendência', 'PMO Unidades', 'Rodovias'),
        ('Medição', 'PMO Unidades', 'Rodovias'),
        ('Antecipação Financeira', 'PMO Unidades', 'Rodovias'),
        ('Adiantamento', 'PMO Unidades', 'Rodovias'),
        ('Caução', 'PMO Unidades', 'Rodovias'),
        ('Aditivo', 'PMO Unidades', 'Rodovias'),
        ('Faturamento Direto', 'PMO Unidades', 'Rodovias'),
        ('Faturamento Direto - Ressarcimento', 'PMO Unidades', 'Rodovias'),
        ('Criação de Elemento PEP (PQQ)', 'PMO Consolidador', 'Rodovias'),
        ('Revisão PEPs criados (PQQ)', 'PMO Consolidador', 'Rodovias'),
        ('Provisão de Manutenção (PQQ)', 'PMO Consolidador', 'Rodovias'),
        ('Monitoramento de Tendência Econômico', 'PMO Consolidador', 'Rodovias'),
        ('Monitoramento de Tendência Físico', 'PMO Consolidador', 'Rodovias'),
        ('Construção do Orçamento (Rodovias)', 'PMO Consolidador', 'Rodovias'),
        ('Monitoramento de Tendência Financeiro', 'PMO Consolidador', 'Rodovias'),
        ('Implantação', 'Engenharia', 'Rodovias'),
        ('Planejamento de Medição', 'Obras Via Oeste', 'Rodovias'),
        ('Execução da Obra e Lançamento da Medição', 'Obras Via Oeste', 'Rodovias'),
        ('Medições com/sem aprovação qualidade', 'Obras Via Oeste', 'Rodovias'),
        ('Planejamento prévio da medição', 'Conservação', 'Rodovias'),
        ('Gestão da Medição', 'Conservação', 'Rodovias'),
        ('Troca de NF', 'Conservação', 'Rodovias'),
        ('Criação da RC conforme Contrato', 'Conservação', 'Rodovias'),
        ('Não Conformidade', 'Obra Serra das Araras', 'Rodovias'),
        ('Planejamento e Controle da Operação', 'Operação PCO', 'Rodovias'),
        ('Emergencial ou Descentralizado até 10 mil', 'Operação PCO', 'Rodovias'),
        ('Equipamentos e sistemas - Preventiva', 'Manutenção', 'Rodovias'),
        ('Equipamentos e sistemas - Sob Demanda', 'Manutenção', 'Rodovias'),
        ('Pré-Obra', 'Pré-Obra', 'Rodovias'),
    ]

    # Inserir sistemas
    for sistema in sistemas_data:
        cursor.execute('''
            INSERT OR REPLACE INTO dim_sistemas (nome, etapa_processo, area_responsavel)
            VALUES (?, ?, ?)
        ''', sistema)

    # Inserir processos
    for processo in processos_data:
        cursor.execute('''
            INSERT OR REPLACE INTO dim_processos (nome, area_responsavel, unidade_negocio)
            VALUES (?, ?, ?)
        ''', processo)

    conn.commit()

    # Contar registros
    cursor.execute('SELECT COUNT(*) FROM dim_sistemas')
    sistemas_count = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM dim_processos')
    processos_count = cursor.fetchone()[0]

    conn.close()

    print(f'[MAPEAMENTO] Sistemas TI inseridos: {sistemas_count}')
    print(f'[MAPEAMENTO] Processos inseridos: {processos_count}')
    print(f'[MAPEAMENTO] Mapeamento concluído com sucesso!')


if __name__ == "__main__":
    map_sistemas_ti_to_db()
