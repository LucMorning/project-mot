# Ficha de Diagnóstico As-Is: Rodrigo Correa de Souza

## 👤 Perfil Organizacional
- **Cargo**: Consultor Engenharia
- **Área**: Engenharia de Implantação / Qualidade
- **Diretoria**: VP Trilhos
- **Nível**: Operacional

## 🖥️ Ecossistema de Sistemas e Workarounds
- **Prisma** 🟡 *(Uso: Gerenciamento e estruturação de projetos (PEP/EAP). Utilizado para definir a estrutura analítica de projetos e a estrutura de custos.)*
  - ⚠️ **Workaround / ETL Humano:** Potencial falta de integração com sistemas de execução e controle de custos.
- **SAP FI/CO** 🟡 *(Uso: Gestão financeira e contábil, controle de custos de projetos. Registro de transações financeiras, controle orçamentário e contabilidade de custos.)*
  - ⚠️ **Workaround / ETL Humano:** Dificuldade em correlacionar dados de custo com qualidade e manutenção, falta de mão de obra para análise aprofundada.
- **SAP PS** 🟡 *(Uso: Gerenciamento de projetos, planejamento, execução e controle de custos. Criação de estruturas de projeto, alocação de recursos, acompanhamento de progresso físico e financeiro, registro de medições.)*
  - ⚠️ **Workaround / ETL Humano:** Dificuldade em integrar dados de execução e qualidade de obra para uma visão completa do projeto.
- **Compor 90** 🟡 *(Uso: Orçamentação de obras, composição de custos e planejamento. Elaboração de orçamentos detalhados para projetos de engenharia.)*
  - ⚠️ **Workaround / ETL Humano:** Potencial desconsideração de custos de ciclo de vida na fase de orçamentação, focando apenas no custo inicial.
- **Excel** 🔴 *(Uso: Análise de dados, controle auxiliar, 'ponte' entre sistemas, estruturação inicial. Criação de planilhas para estruturação, acompanhamento, cálculos e consolidação de informações.)*
  - ⚠️ **Workaround / ETL Humano:** Uso excessivo como ferramenta de integração manual e para preencher lacunas de sistemas, gerando inconsistências e retrabalho.
- **Project** 🟡 *(Uso: Planejamento e cronogramas de projetos. Criação e gestão de cronogramas, alocação de tarefas e recursos.)*
  - ⚠️ **Workaround / ETL Humano:** Dificuldade em gerenciar prazos apertados e integrar o planejamento com a execução real e os custos.
- **DocuSign** 🟢 *(Uso: Assinatura eletrônica de documentos. Formalização de contratos e outros documentos relacionados à contratação.)*
- **Coupa** 🟡 *(Uso: Gestão de compras e suprimentos (Procure-to-Pay). Processamento de requisições, ordens de compra, gestão de fornecedores.)*
  - ⚠️ **Workaround / ETL Humano:** Potencial foco excessivo no custo inicial na seleção de fornecedores, levando a problemas de qualidade e manutenção futura.
- **SAP MM/SRM** 🟡 *(Uso: Gestão de materiais e serviços, compras e suprimentos. Registro de fornecedores, gestão de contratos, processamento de pedidos de compra.)*
  - ⚠️ **Workaround / ETL Humano:** Dificuldade em integrar critérios de qualidade e custo de ciclo de vida na seleção de fornecedores, além de problemas com a homologação de pequenos fornecedores.
- **Teams** 🟢 *(Uso: Comunicação, colaboração, gestão de reuniões, compartilhamento de documentos e ideias. Reuniões online, chats, compartilhamento de arquivos, gestão de equipes de projeto.)*
- **Netlex** 🟡 *(Uso: Gestão de contratos e documentos jurídicos. Armazenamento e gestão de contratos, controle de cláusulas e prazos.)*
  - ⚠️ **Workaround / ETL Humano:** Potencial falta de integração com sistemas de execução e pagamento, dificultando o acompanhamento do cumprimento contratual.
- **Flexchain** 🟡 *(Uso: Gestão da cadeia de suprimentos, rastreabilidade. Acompanhamento de fornecedores e materiais na cadeia de suprimentos.)*
  - ⚠️ **Workaround / ETL Humano:** Dificuldade em garantir a qualidade dos materiais e serviços de pequenos fornecedores, mesmo com ferramentas de rastreabilidade.
- **Kartado** 🟡 *(Uso: Gestão de obras e equipes em campo. Acompanhamento de atividades em campo, registro de ocorrências, gestão de equipes.)*
  - ⚠️ **Workaround / ETL Humano:** Potencial falta de integração dos dados de campo com sistemas de planejamento e controle financeiro.
- **Power Apps** 🟡 *(Uso: Desenvolvimento de aplicações personalizadas para processos específicos. Criação de apps para coleta de dados, automação de fluxos de trabalho em campo ou escritório.)*
  - ⚠️ **Workaround / ETL Humano:** Risco de criar silos de informação se os apps não forem bem integrados aos sistemas corporativos.
- **SharePoint** 🟢 *(Uso: Gestão de documentos, colaboração, portais de equipe. Armazenamento e compartilhamento de documentos de projeto, gestão de versões.)*
- **Conecta** 🟡 *(Uso: Plataforma de comunicação e gestão de projetos. Colaboração entre equipes, compartilhamento de informações de projeto.)*
  - ⚠️ **Workaround / ETL Humano:** Potencial de ser mais uma ferramenta de comunicação sem integração profunda com dados de execução e controle.
- **Fulcrum** 🟡 *(Uso: Coleta de dados em campo, inspeções, medições. Realização de inspeções e medições em obras, registro de dados via dispositivos móveis.)*
  - ⚠️ **Workaround / ETL Humano:** Dificuldade em integrar os dados de medição e inspeção com sistemas de controle de custos e qualidade para análise de desempenho.
- **Archer** 🟡 *(Uso: Gestão de riscos, conformidade e auditoria (GRC). Identificação, avaliação e monitoramento de riscos de projetos e operações.)*
  - ⚠️ **Workaround / ETL Humano:** Dificuldade em correlacionar riscos identificados com dados de execução e custos reais, devido à falta de integração.
- **SAP BW/BPC** 🔴 *(Uso: Business Warehouse (Data Warehousing) e Business Planning and Consolidation (Planejamento e Consolidação). Consolidação de dados para relatórios e análises, planejamento orçamentário e financeiro.)*
  - ⚠️ **Workaround / ETL Humano:** Falta de mão de obra para análise de dados, dificuldade em correlacionar dados de diferentes fontes para uma visão completa de custo-benefício.
- **Power BI** 🔴 *(Uso: Visualização e análise de dados, criação de dashboards. Criação de painéis para monitoramento de KPIs e desempenho de projetos.)*
  - ⚠️ **Workaround / ETL Humano:** Dificuldade em consolidar dados de diversas fontes para criar dashboards que reflitam a real eficiência e os custos de ciclo de vida.
- **Atlas** 🟡 *(Uso: Gestão fiscal e de notas fiscais. Processamento e armazenamento de notas fiscais, cumprimento de obrigações fiscais.)*
  - ⚠️ **Workaround / ETL Humano:** Potencial falta de integração com sistemas de pagamento e controle de projetos, gerando inconsistências.
- **V360** 🟡 *(Uso: Gestão de documentos ou processos fiscais. Suporte a processos fiscais e de conformidade.)*
  - ⚠️ **Workaround / ETL Humano:** Potencial falta de integração com outros sistemas, exigindo acesso a múltiplas plataformas.
- **Forms** 🟡 *(Uso: Coleta de dados estruturados, formulários digitais. Criação de formulários para coleta de informações fiscais ou de processo.)*
  - ⚠️ **Workaround / ETL Humano:** Risco de criar silos de dados se as informações coletadas não forem integradas automaticamente aos sistemas principais.
- **Painel de Chamados** 🟡 *(Uso: Gestão de solicitações e chamados, incluindo os relacionados a pagamentos. Registro e acompanhamento de solicitações de pagamento ou problemas relacionados.)*
  - ⚠️ **Workaround / ETL Humano:** Potencial de atrasos ou inconsistências se não houver integração direta com o sistema de pagamento (SAP FI/AP).
- **Prisma** 🟡 *(Uso: Estruturação de projetos, WBS (EAP) e Project Systems (PEP). Criação e gestão da estrutura de projetos.)*
- **SAP FI/CO** 🟡 *(Uso: Gestão financeira e contábil, controle de custos. Registro de transações financeiras, alocação de custos a projetos.)*
- **SAP PS** 🟡 *(Uso: Gerenciamento de projetos, controle de custos e prazos de projetos. Criação de estruturas de projeto (PEP/WBS), acompanhamento financeiro de projetos.)*
- **Compor 90** 🟡 *(Uso: Orçamentação de obras, composição de custos unitários. Elaboração de orçamentos detalhados para projetos de engenharia.)*
- **Excel** 🔴 *(Uso: Ferramenta de apoio para cálculos, análises e gestão de listas não integradas. Criação de planilhas para estruturação, controle de homologação de fornecedores técnicos, análises ad-hoc e como 'ponte' de dados.)*
  - ⚠️ **Workaround / ETL Humano:** Usado como 'ponte' para dados não integrados, falta de formalização de processos e silos de informação (ex: lista de homologação técnica).
- **Project** 🟡 *(Uso: Planejamento e acompanhamento de cronogramas de projetos. Criação de cronogramas, alocação de recursos, monitoramento de progresso.)*
- **DocuSign** 🟢 *(Uso: Assinatura eletrônica de documentos e contratos. Formalização digital de contratos com fornecedores e parceiros.)*
- **Coupa** 🔴 *(Uso: Gestão de compras e suprimentos, e-procurement. Processos de cotação, pedidos de compra, gestão de fornecedores.)*
  - ⚠️ **Workaround / ETL Humano:** Processo de homologação contratual não se integra com a homologação técnica de fornecedores, gerando silos de informação.
- **SAP** 🟡 *(Uso: Sistema ERP central para diversas funções empresariais. Base para processos de contratação, finanças, projetos e suprimentos.)*
  - ⚠️ **Workaround / ETL Humano:** Complexidade e desafios de integração com processos específicos, como a homologação técnica de fornecedores.
- **Teams** 🟢 *(Uso: Comunicação e colaboração interna. Reuniões, compartilhamento de documentos, comunicação entre equipes.)*
- **Netlex** 🟡 *(Uso: Gestão de contratos jurídicos. Armazenamento e acompanhamento de contratos.)*
- **Flexchain** 🟡 *(Uso: Gestão da cadeia de suprimentos, visibilidade de fornecedores. Monitoramento de fornecedores e processos de suprimentos.)*
- **Kartado** 🟡 *(Uso: Gestão de obras e equipes em campo. Acompanhamento de atividades, registro de ocorrências em canteiro.)*
- **Power Apps** 🟢 *(Uso: Desenvolvimento de aplicações customizadas para processos específicos. Criação de apps para coleta de dados ou automação de tarefas.)*
- **SharePoint** 🟢 *(Uso: Compartilhamento de documentos e gestão de conteúdo. Repositório de documentos de projetos, colaboração em arquivos.)*
- **Conecta** 🟡 *(Uso: Plataforma de comunicação e gestão de informações de projetos. Centralização de informações e comunicação entre stakeholders.)*
- **Fulcrum** 🟡 *(Uso: Coleta de dados em campo para medições e inspeções. Registro de medições de progresso físico de obras.)*
- **SAP PS/FI** 🟡 *(Uso: Registro e controle financeiro das medições de obras. Lançamento de medições para faturamento e controle de custos.)*
- **Archer** 🟡 *(Uso: Gestão de riscos corporativos e compliance. Registro e acompanhamento de riscos e tendências.)*
- **SAP BW/BPC** 🟡 *(Uso: Business Warehouse (data warehousing) e Business Planning and Consolidation (planejamento e consolidação). Análise de dados históricos e projeções financeiras para identificar tendências.)*
- **BI (Power BI)** 🟢 *(Uso: Visualização e análise de dados para tomada de decisão. Criação de dashboards e relatórios para monitorar tendências e performance.)*
- **Teams Idea** 🟢 *(Uso: Brainstorming e gestão de ideias para inovação e melhoria. Plataforma para colaboração na geração e avaliação de ideias.)*
- **Atlas** 🟡 *(Uso: Gestão fiscal e emissão de notas fiscais. Processamento de documentos fiscais.)*
- **V360** 🟡 *(Uso: Gestão de documentos e processos fiscais. Controle e organização de informações fiscais.)*
- **SAP FI** 🟡 *(Uso: Contabilidade financeira, gestão de contas a pagar/receber. Registro de transações fiscais e financeiras.)*
- **Forms** 🟢 *(Uso: Coleta de dados e informações através de formulários. Criação de formulários para coleta de dados fiscais ou internos.)*
- **Painel de Chamados** 🟡 *(Uso: Gestão de solicitações e acompanhamento de pagamentos. Registro e monitoramento de chamados relacionados a pagamentos.)*
- **SAP FI/AP** 🟡 *(Uso: Gestão de contas a pagar. Processamento e controle de pagamentos a fornecedores.)*
- **Prisma** 🟡 *(Uso: Ferramenta para estruturação de projetos, incluindo Project Execution Plan (PEP) e Estrutura Analítica do Projeto (EAP). Utilizado para definir a estrutura e o escopo inicial dos projetos.)*
- **Fli/CO** 🟡 *(Uso: Gestão financeira e de custos, alocação orçamentária e controle de despesas para projetos. Definição de centros de custo, elementos de custo e acompanhamento financeiro inicial do projeto.)*
- **SAP PS** 🟡 *(Uso: Gerenciamento de projetos no ambiente SAP, incluindo estruturação de PEP e EAP, planejamento de recursos e cronogramas. Criação e gestão da estrutura do projeto, alocação de recursos e acompanhamento de fases.)*
- **Compor 90** 🟡 *(Uso: Elaboração de orçamentos detalhados e composição de custos para obras e projetos. Utilizado para calcular e detalhar os custos de cada componente do projeto.)*
- **Excel** 🔴 *(Uso: Apoio em cálculos, simulações, análises ad-hoc e como ferramenta intermediária para troca de dados. Criação de planilhas para complementar informações, realizar análises e transferir dados entre sistemas.)*
  - ⚠️ **Workaround / ETL Humano:** Atua como "ponte" ou "intermediário" entre sistemas, indicando lacunas de integração e processos manuais.
- **Project** 🟡 *(Uso: Planejamento e gestão de cronogramas de projetos, alocação de tarefas e recursos. Criação, acompanhamento e atualização de cronogramas detalhados dos projetos.)*
- **DocuSign** 🟢 *(Uso: Assinatura eletrônica de documentos e contratos, agilizando o processo de formalização. Envio de documentos para assinatura digital e gestão do fluxo de aprovação.)*
- **Coupia** 🟡 *(Uso: Gestão de compras, sourcing, gestão de fornecedores e automação do ciclo Procure-to-Pay. Processamento de requisições de compra, cotações, pedidos e gestão de contratos com fornecedores.)*
- **SAP** 🟡 *(Uso: Gestão de suprimentos, contratos e pedidos de compra dentro do ecossistema SAP. Registro e acompanhamento de contratos, pedidos e recebimento de materiais/serviços.)*
- **Teams** 🟢 *(Uso: Comunicação, colaboração e compartilhamento de informações entre as equipes envolvidas no processo de contratação. Reuniões online, chats, compartilhamento de documentos e organização de fluxos de trabalho.)*
- **Netflex** 🟡 *(Uso: Gestão do ciclo de vida de contratos, automação de documentos jurídicos e conformidade. Criação, revisão, aprovação e armazenamento de contratos.)*
- **Flexchain** 🟡 *(Uso: Gestão da cadeia de suprimentos, rastreamento e otimização de processos logísticos. Monitoramento de fornecedores, entregas e gestão de inventário.)*
- **PM** 🟡 *(Uso: Gerenciamento e acompanhamento de projetos, tarefas e marcos. Registro de atividades, prazos, recursos e monitoramento do progresso da execução.)*
- **Kartado** 🟡 *(Uso: Gestão de obras em campo, diário de obras digital, controle de equipes e equipamentos. Registro de informações diárias da obra, fotos, ocorrências e medições preliminares.)*
- **Power Apps** 🟡 *(Uso: Desenvolvimento de aplicativos personalizados para otimizar processos específicos de planejamento e execução. Criação e utilização de apps para coleta de dados, automação de fluxos de trabalho e relatórios.)*
- **SharePoint** 🟢 *(Uso: Compartilhamento de documentos, gestão de conteúdo e colaboração em projetos. Armazenamento centralizado de documentos, controle de versões e espaços de trabalho para equipes.)*
- **Conecta** 🟡 *(Uso: Plataforma de comunicação e colaboração para equipes de projeto. Troca de informações, gestão de tarefas e acompanhamento de atividades.)*
- **Fulcrum** 🟡 *(Uso: Coleta de dados em campo, inspeções e medições de progresso físico das obras. Aplicativo móvel para registro de informações georreferenciadas e evidências fotográficas.)*
- **SAP PS/FI** 🟡 *(Uso: Registro e controle financeiro das medições de projetos, faturamento e acompanhamento de custos reais. Lançamento das medições aprovadas para processamento financeiro e contábil.)*
- **Archer** 🟡 *(Uso: Gestão de riscos corporativos, conformidade, auditoria e gestão de desempenho. Registro, monitoramento e avaliação de riscos e controles internos.)*
- **SAP BW/BPC** 🟡 *(Uso: Business Warehouse (BW) para relatórios e análises de dados, e Business Planning and Consolidation (BPC) para planejamento, orçamento e consolidação financeira. Geração de relatórios gerenciais, análise de tendências e suporte à tomada de decisão.)*
- **BI** 🟢 *(Uso: Análise de dados, criação de dashboards e relatórios para visualização de indicadores de desempenho e tendências. Consumo de informações gerenciais e operacionais para monitoramento e análise.)*
- **Teams Idea** 🟡 *(Uso: Ferramenta de colaboração para geração e gestão de ideias, inovações e tendências. Espaço para discussões, registro de insights e acompanhamento de iniciativas.)*
- **Atlas** 🟡 *(Uso: Gestão fiscal, emissão e recebimento de notas fiscais e conformidade tributária. Processamento e controle de documentos fiscais.)*
- **V360** 🟡 *(Uso: Gestão fiscal e conformidade, controle de informações tributárias. Validação e controle de dados fiscais.)*
- **SAP FI** 🟡 *(Uso: Contabilidade financeira, registro de transações fiscais e gestão de impostos. Lançamento e controle de notas fiscais, apuração de impostos e geração de obrigações fiscais.)*
- **Forms** 🟡 *(Uso: Coleta de informações e dados através de formulários digitais para processos fiscais. Criação e preenchimento de formulários para entrada de dados.)*
- **Painel de Chamados** 🟡 *(Uso: Gestão de solicitações e chamados relacionados a processos de pagamento. Abertura, acompanhamento e resolução de tickets de pagamento.)*
- **SAP FI/AP** 🟡 *(Uso: Processamento e controle de contas a pagar, execução de pagamentos a fornecedores. Lançamento de faturas, aprovação e efetivação de pagamentos.)*
- **Prisma** 🟡 *(Uso: Ferramenta para estruturação de projetos (PEP e EAP). Utilizado para definir a estrutura analítica de projetos e elementos PEP.)*
- **Fli/CO** 🟡 *(Uso: Suporte à estruturação de projetos e controle financeiro/contábil. Utilizado para definir a estrutura analítica de projetos e gerenciar custos e receitas.)*
- **SAP PS** 🟡 *(Uso: Gerenciamento de projetos (Project Systems), incluindo estruturação e planejamento. Criação de estruturas de projeto, acompanhamento de progresso e registro de medições.)*
- **Compor 90** 🟡 *(Uso: Apoio na estruturação de projetos, possivelmente para orçamentação e composição de custos. Utilizado para auxiliar na definição da estrutura e custos dos projetos.)*
- **Excel** 🟡 *(Uso: Ferramenta de apoio para estruturação de projetos, cálculos, análises e como ponte de dados. Criação de planilhas para estruturação, cálculos e como intermediário para troca de dados.)*
  - ⚠️ **Workaround / ETL Humano:** Potencialmente usado como 'ponte' ou para compensar falta de integração entre sistemas.
- **Project** 🟡 *(Uso: Planejamento e gerenciamento de cronogramas de projetos. Criação e acompanhamento de cronogramas, tarefas e recursos.)*
- **DocuSign** 🟡 *(Uso: Assinatura eletrônica de documentos, especialmente contratos. Envio e recebimento de documentos para assinatura digital, agilizando o processo de contratação.)*
- **Coupia** 🟡 *(Uso: Gestão de compras e suprimentos, incluindo processos de contratação e gestão de fornecedores. Gerenciamento de fornecedores, cotações e contratos.)*
- **SAP** 🟡 *(Uso: Suporte a processos de contratação, como registro de fornecedores e pedidos. Utilizado para formalizar e registrar etapas da contratação, como pedidos de compra e contratos.)*
- **Teams** 🟡 *(Uso: Comunicação e colaboração entre equipes durante o processo de contratação. Reuniões, compartilhamento de documentos e comunicação instantânea.)*
- **Netflex** 🟡 *(Uso: Gestão de contratos e documentos jurídicos. Armazenamento, controle de versões e gerenciamento de contratos.)*
- **Flexchain** 🟡 *(Uso: Gestão da cadeia de suprimentos, possivelmente para homologação e qualificação de fornecedores. Gerenciamento de fornecedores e processos de homologação.)*
- **PM** 🟡 *(Uso: Suporte ao planejamento e execução de projetos. Acompanhamento de atividades, recursos e prazos.)*
- **Kartado** 🟡 *(Uso: Gestão de obras e equipes em campo, registro de atividades. Registro de atividades, ocorrências e progresso em campo.)*
- **Power Apps** 🟡 *(Uso: Desenvolvimento de aplicativos personalizados para otimizar processos e coleta de dados. Criação de ferramentas para coleta de dados ou automação de tarefas específicas de projeto.)*
- **SharePoint** 🟡 *(Uso: Compartilhamento de documentos, gestão de conteúdo e colaboração em projetos. Armazenamento de arquivos, gestão de versões e comunicação entre equipes.)*
- **Conecta** 🟡 *(Uso: Plataforma de comunicação e colaboração para equipes de projeto. Interação entre equipes e compartilhamento de informações.)*
- **Fulcrum** 🟡 *(Uso: Coleta de dados em campo para medição e inspeção. Registro de informações de medição e inspeção no local da obra, via dispositivos móveis.)*
- **SAP PS/FI** 🟡 *(Uso: Registro e processamento de medições financeiras e de progresso de projetos. Lançamento de medições para faturamento, controle de custos e acompanhamento do progresso físico-financeiro.)*
- **Archer** 🟡 *(Uso: Gestão de riscos, conformidade e auditoria. Monitoramento de riscos, registro de não conformidades e análise de tendências.)*
- **SAP BW/BPC** 🟡 *(Uso: Business Warehouse (BW) para relatórios e Business Planning and Consolidation (BPC) para planejamento, orçamento e consolidação. Análise de dados históricos e projeções para identificar tendências de desempenho e financeiras.)*
- **BI** 🟡 *(Uso: Visualização e análise de dados para identificar tendências e apoiar a tomada de decisões. Criação de dashboards e relatórios interativos para monitoramento de indicadores.)*
- **Teams Idea** 🟡 *(Uso: Coleta e gestão de ideias para inovação e melhoria contínua. Plataforma para submissão, avaliação e acompanhamento de ideias.)*
- **Atlas** 🟡 *(Uso: Gestão fiscal e de notas fiscais. Processamento, armazenamento e validação de documentos fiscais.)*
- **V360** 🟡 *(Uso: Gestão fiscal e de conformidade. Verificação e validação de informações fiscais e tributárias.)*
- **SAP FI** 🟡 *(Uso: Contabilidade financeira, incluindo processamento fiscal. Registro de transações financeiras e emissão de relatórios fiscais.)*
- **Forms** 🟡 *(Uso: Coleta de dados e informações, possivelmente para processos fiscais ou internos. Criação de formulários para coleta de dados e feedback.)*
- **Painel de Chamados** 🟡 *(Uso: Gestão de solicitações e aprovações relacionadas a pagamentos. Registro e acompanhamento de chamados para processamento de pagamentos.)*
- **SAP FI/AP** 🟡 *(Uso: Gestão de contas a pagar e processamento de pagamentos a fornecedores. Registro de faturas, aprovação e execução de pagamentos a fornecedores.)*
- **SAP PS** 🟡 *(Uso: Gestão de projetos, controle de custos e prazos, medição de progresso físico-financeiro. Estruturação de projetos, acompanhamento financeiro e físico de empreendimentos.)*
- **SAP FI** 🟡 *(Uso: Contabilidade financeira, gestão de pagamentos, controle fiscal e registro de transações. Registro de transações financeiras, processamento de pagamentos, emissão de notas fiscais e relatórios contábeis.)*
- **SAP BW** 🟡 *(Uso: Data warehousing e relatórios analíticos para suporte à decisão. Consolidação de dados de diversas fontes para análises e geração de relatórios gerenciais.)*
- **SAP BPC** 🟡 *(Uso: Planejamento financeiro, orçamentação, previsão e consolidação. Elaboração de orçamentos, projeções financeiras e consolidação de resultados.)*
- **SAP MM** 🟡 *(Uso: Gestão de suprimentos, compras, estoque e serviços. Processos de aquisição de materiais e serviços, gestão de pedidos e fornecedores.)*
- **Prisma** 🟡 *(Uso: Estruturação de projetos (PEP - Project Execution Plan e EAP - Estrutura Analítica do Projeto). Ferramenta para planejamento inicial e detalhamento da estrutura de projetos.)*
- **Project** 🟡 *(Uso: Planejamento e gerenciamento de cronogramas de projetos. Criação, acompanhamento e atualização de cronogramas e recursos de projetos.)*
- **P6** 🟡 *(Uso: Planejamento e controle avançado de projetos, cronogramas e recursos. Gestão de grandes projetos, cronogramas complexos e análise de caminho crítico.)*
- **Primavera** 🟡 *(Uso: Planejamento e controle de projetos, gestão de cronogramas e recursos. Gestão de cronogramas, recursos e custos de projetos.)*
- **Compor 90** 🟡 *(Uso: Orçamentação e composição de custos de obras e serviços de engenharia. Elaboração de orçamentos detalhados, com base em composições de custos.)*
- **Coupa** 🟡 *(Uso: Gestão de compras, despesas e automação de processos de procurement. Processos de aquisição, gestão de fornecedores e controle de gastos.)*
- **Netlex** 🟡 *(Uso: Gestão do ciclo de vida de contratos, desde a criação até o encerramento. Armazenamento, acompanhamento e controle de contratos.)*
- **Flexchain** 🟡 *(Uso: Gestão da cadeia de suprimentos e logística. Otimização de processos logísticos, gestão de fornecedores e transporte.)*
- **Docusign** 🟡 *(Uso: Assinatura eletrônica de documentos de forma segura e legalmente válida. Agilizar o processo de assinatura de contratos, aditivos e outros documentos.)*
- **Kartado** 🟡 *(Uso: Gestão de obras e equipes em campo, coleta de dados e acompanhamento. Acompanhamento de atividades, recursos e progresso em canteiros de obra.)*
- **Conecta** 🟡 *(Uso: Comunicação e colaboração entre equipes de projeto. Plataforma para interação, compartilhamento de informações e gestão de tarefas.)*
- **Fulcrum** 🟡 *(Uso: Coleta de dados em campo para medição e inspeções. Ferramenta móvel para registro de medições, fotos e informações de campo.)*
- **Archer** 🟡 *(Uso: Gestão de riscos corporativos, conformidade e auditoria. Identificação, avaliação, monitoramento e mitigação de riscos.)*
- **V360** 🟡 *(Uso: Gestão fiscal e de notas fiscais eletrônicas. Processamento, validação e controle de documentos fiscais.)*
- **Atlas** 🟡 *(Uso: Gestão fiscal e de notas fiscais. Processamento e controle de documentos fiscais.)*
- **Power BI** 🟢 *(Uso: Visualização de dados, criação de dashboards e indicadores de desempenho. Recebe dados compilados (manualmente do Excel) para gerar relatórios e apresentações gerenciais.)*
  - ⚠️ **Workaround / ETL Humano:** Dependência de dados manuais e não integrados de outras fontes.
- **SharePoint** 🟡 *(Uso: Compartilhamento de documentos, gestão de conteúdo e colaboração. Armazenamento e acesso a documentos de projeto, gestão de versões.)*
- **Teams** 🟡 *(Uso: Comunicação unificada, colaboração em equipe, reuniões online. Reuniões, chats, compartilhamento de arquivos e colaboração em documentos.)*
- **Excel** 🔴 *(Uso: Estruturação de projetos, registro de não conformidades e desvios, compilação de dados, criação de indicadores. Preenchimento manual de planilhas para controle de qualidade, consolidação de dados para análise e geração de indicadores.)*
  - ⚠️ **Workaround / ETL Humano:** Processos manuais, burocracia, exige compilação manual, atua como 'planilha ponte' entre sistemas.
- **SIC** 🟡 *(Uso: Controle e análise de custos de projetos e empreendimentos. Monitoramento de despesas, orçamentos e variações de custos.)*
- **RDO** 🟡 *(Uso: Registro de atividades diárias da obra, ocorrências e progresso. Preenchimento de relatórios diários de obra para acompanhamento.)*
- **Word** 🔴 *(Uso: Elaboração de formulários padrão de não conformidade e relatórios. Preenchimento manual de documentos para registro de não conformidades, incluindo análise de causa raiz.)*
  - ⚠️ **Workaround / ETL Humano:** Manual, burocrático, não é um sistema integrado, dificuldade de compilação de dados.
- **Autodesk Docs** 🟡 *(Uso: Armazenamento e gestão de documentos de projeto. Tentativa de migração de documentos e formulários, mas com dificuldades.)*
  - ⚠️ **Workaround / ETL Humano:** Dificuldade com templates, 'visivelmente, estava muito ruim'.
- **Autodesk Build** 🟢 *(Uso: Realização de inspeções de qualidade, registro de desvios apontados e corrigidos. Utilizado para registrar inspeções e desvios no campo, facilitando o controle de qualidade.)*
- **SGQ (Sistema de Gestão da Qualidade)** 🟢 *(Uso: Definir e monitorar indicadores de qualidade (inspeções, rastreabilidade de documentos, não conformidades). Estrutura para desenvolvimento de novos indicadores e monitoramento da qualidade, buscando antecipar problemas.)*
- **Forms** 🟡 *(Uso: Coleta de informações e dados diversos. Criação de formulários para coleta de dados específicos.)*
- **Painel de Chamados** 🟡 *(Uso: Gestão de solicitações e chamados relacionados a processos de pagamento. Abertura e acompanhamento de chamados para resolução de questões de pagamento.)*
- **SAP FI/AP** 🟡 *(Uso: Processamento de contas a pagar, gestão de faturas de fornecedores. Gestão de faturas de fornecedores, aprovações e execução de pagamentos.)*
- **Teams Idea** 🟡 *(Uso: Geração e gestão de ideias, inovação e melhoria contínua. Plataforma para colaboração na criação e desenvolvimento de novas ideias.)*

## 🔥 Dores, Gargalos e Diagnósticos
### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** Desde a concepção do empreendimento, passando pela especificação de requisitos de materiais e metodologias executivas, até a contratação e execução, buscando otimizar o custo total de propriedade (CAPEX + OPEX) ao longo do ciclo de vida do ativo.

**Sistemas Envolvidos:** ``

> *"Rupturas: Falta de integração e colaboração entre as equipes de Implantação (CAPEX) e Operação e Manutenção (OPEX) para avaliar o custo total de propriedade, Prazos curtos e apertados que levam a decisões focadas no CAPEX inicial em detrimento do OPEX futuro, Foco no mínimo aceitável do contrato em vez da qualidade que reduz a manutenção"*

### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** Processo de seleção, homologação e gestão de fornecedores, acompanhamento da qualidade dos materiais e serviços durante a execução da obra, e quantificação de não conformidades e retrabalhos para aprendizado e melhoria contínua.

**Sistemas Envolvidos:** ``

> *"Rupturas: Contratação de fornecedores baseada apenas no menor preço, resultando em baixa qualidade, Pulverização de obras e subcontratação descontrolada, dificultando o controle de qualidade, Falta de mão de obra para quantificar e monetizar não conformidades, retrabalhos e atrasos, impedindo a análise de tendências e a tomada de decisões baseadas em dados"*

### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** Este fluxo abrange a estruturação do Sistema de Gestão da Qualidade (SGQ) para a engenharia de implantação, buscando padronização e diretrizes. Em paralelo, ocorre a homologação de parceiros, onde Suprimentos foca na avaliação contratual das contratadas, enquanto a equipe de Qualidade realiza a homologação técnica, principalmente de subcontratadas. A Qualidade também atua na execução, participando de liberações de serviço, kick-offs e gerenciando RNCs.

**Sistemas Envolvidos:** ``

> *"Rupturas: Falta de diretrizes claras e estrutura de SGQ na holding, dificultando a padronização e a busca por referências internas, Desalinhamento e falta de integração entre os processos de homologação de Suprimentos (contratual) e Qualidade (técnica), gerando burocracia e lentidão, A homologação técnica da Qualidade não é um gate formal obrigatório, permitindo que decisões de contratação ignorem as recomendações técnicas, Suprimentos não avalia tecnicamente as subcontratadas, criando um risco de qualidade que precisa ser mitigado pela equipe de engenharia, A equipe de Qualidade atua de forma reativa ou como "backup" na decisão de contratação, em vez de ser um ator proativo e decisivo, Falta de equipe dedicada para levantamentos detalhados (ex: OHH), impactando a precisão do planejamento e custo"*

### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** O fluxo inicia com a estruturação de uma equipe de qualidade para fiscalizar a obra, garantindo o cumprimento dos requisitos contratuais e normativos durante a execução. As atividades de fiscalização e controle de implantação de obra alimentam a verificação do progresso físico para fins de medição.

**Sistemas Envolvidos:** ``

> *"Rupturas: A 'gestão com silo' e o 'pessoal trabalhando bem separado' impedem a fluidez e a integração entre as etapas de execução e medição, podendo gerar desalinhamentos e dificuldades na comunicação e no controle., Falta de um núcleo central para fazer a ligação entre os processos, resultando em descontinuidade e retrabalho."*

### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** A contratada especifica a subcontratada. A equipe de engenharia realiza uma avaliação técnica da subcontratada para homologação. Existe um banco de dados de empresas homologadas que pode ser consultado. A diretriz é não efetivar o contrato principal antes da homologação da subcontratada para evitar burocracia e atrasos.

**Sistemas Envolvidos:** ``

> *"Rupturas: Efetivação do contrato antes da homologação da subcontratada, resultando em burocracia e atrasos no cronograma, Problemas com subcontratadas muito pequenas e não homologadas"*

### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** Inicia-se com a definição de diretrizes e especificações técnicas de serviços no contrato, incluindo planos de inspeção e testes (PITs) para atividades civis e estruturas metálicas. Durante a execução, equipes de inspetores especializados realizam inspeções conforme os PITs, verificando critérios normativos, frequência de amostragem e registrando documentos. Há um esforço para estruturar um SGQ, realizar auditorias internas e buscar certificação. A inspeção de sistemas é intrínseca aos especialistas de sistemas, com um processo mais maduro, mas busca-se padronização e integração com a equipe de civil/metálica.

**Sistemas Envolvidos:** ``

> *"Rupturas: Falta de padronização na inspeção de sistemas (ponto de melhoria), Necessidade de melhor interface entre a equipe de qualidade de obras (civil/metálica) e a equipe de implantação de sistemas, Proposta de SGQ e certificação ainda não validada"*

### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** O fluxo inicia com a definição de planos de ensaio e a entrega do Plano de Garantia da Qualidade (PGQ) pelo construtor. Durante a execução, o time de qualidade realiza inspeções, registrando 'desvios' para problemas corrigíveis no local e 'não conformidades' para questões críticas. Desvios são corrigidos e acompanhados, enquanto não conformidades exigem análise de causa raiz e planos de ação do construtor. Os dados são compilados mensalmente para identificar tendências, reincidências e gerar indicadores de qualidade, que são usados para ações preventivas e relatórios gerenciais.

**Sistemas Envolvidos:** ``

> *"Rupturas: Processo inicial imaturo e sem sistema de gestão de qualidade, Problemas com fornecedores pequenos e sem certificação, Pressão por prazos e metas que podem levar a verificações superficiais, Compilação manual de dados de não conformidades no Excel, Dificuldade na migração de templates para o Autodesk Docs, Risco de reincidência de não conformidades devido a análises de causa raiz ineficazes"*

### 🟦 [Dor] ETL Humano (Etapa: Planejamento e Execução)
**Descrição:** A empresa não possui um manual formalizado e atualizado para procedimentos executivos e de inspeção. Em vez disso, utiliza uma "planilha" como seu principal guia, o que pode levar a inconsistências, erros manuais e dificuldades de rastreabilidade e atualização de informações críticas.

**Sistemas Envolvidos:** `Excel`

> *"Rodrigo, no final do dia, vocês não tem um manual manual, mas vocês tem uma planilha que basicamente fala o que o manual fala. Rodrigo Correa de Souza É exato o manual. Ele é. Ele é o nosso manual."*

### 🟦 [Dor] Gargalo (Etapa: Planejamento e Execução)
**Descrição:** A equipe não possui recursos humanos suficientes para elaborar e manter procedimentos executivos internos, nem para realizar as inspeções de qualidade necessárias. Isso força a delegação da responsabilidade de criação de procedimentos para as construtoras, o que pode gerar inconsistências e dependência externa.

**Sistemas Envolvidos:** ``

> *"A gente não dispunha de gente suficiente para poder é elaborar a documentação e realizar as inspeções."*

### 🟦 [Dor] Erro Manual (Etapa: Contratação & Execução)
**Descrição:** Construtoras frequentemente falham em incluir no orçamento e realizar ensaios obrigatórios e caros (como provas de carga em fundações), mesmo quando especificados em projeto e referenciados por normas. Isso resulta em prejuízos financeiros para a Motiva e gera conflitos e discussões recorrentes, indicando uma falha na comunicação, fiscalização ou na aderência aos requisitos contratuais.

**Sistemas Envolvidos:** ``

> *"Aconteceu muito com fundação, por exemplo. Quando a gente vai fazer alguma estaca... É um ensaio que é caro... se ele não compôs no custo dele, é prejuízo. Então, esse foi um problema que a gente teve, mesmo especificando no projeto a referência da norma de fundações... Foi algo que foi uma Barreira que deu muita briga. Vez ou outra ainda aparece"*

### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** O fluxo envolve a identificação de falhas técnicas ou não conformidades durante a execução do contrato. Em grandes empreendimentos, o gestor recebe a medição da construtora e a encaminha para as áreas de qualidade, implantação e meio ambiente, que sinalizam itens passíveis de retenção ou não medição. Esses itens são então retidos do valor a ser pago. Em empreendimentos menores, o processo é menos formalizado e mais propenso a falhas.

> *"Rupturas: Ausência de valores categorizados para multas e retenções por falhas de qualidade, A sinalização de problemas para retenção é manual (e-mail), não sistêmica, gerando falta de controle, Dificuldade em aplicar retenções em empreendimentos pequenos, com risco de inviabilizar o fornecedor e a obra, A qualidade não está formalmente integrada ao boletim de medição como um item de valor, O foco está na punição tardia, em vez de prevenção ou remediação antecipada"*

### 🟦 [Dor] Silo de Informação (Etapa: Concepção e Estruturação)
**Descrição:** Falta de colaboração e visão integrada entre as diretorias de Implantação e Operação e Manutenção, impedindo a equalização de objetivos e a otimização do custo total de propriedade dos ativos. Decisões de especificação de materiais e metodologias executivas são tomadas sem considerar o impacto a longo prazo na manutenção.

**Sistemas Envolvidos:** `Implantação (Diretoria), Operação e Manutenção (Diretoria)`

> *"a gente não, a gente não chegou a fazer um trabalho. Com o time de operação e manutenção, porque que é o certo nesse caso, a gente ir lá com o time de operação e manutenção, verificar quais são os principais pontos de atuação deles. É se tem esse tipo de problema. [...] a gente não está tendo essa visão das 2 coisas. Sob a mesma perspetiva, a gente pode não estar vendo um ponto muito bom"*

### 🟦 [Dor] Gargalo (Etapa: Contratação)
**Descrição:** Processo de contratação de fornecedores que prioriza o menor valor, resultando em 'barato que sai caro' devido à baixa qualidade dos materiais e serviços, exigindo manutenções precoces e gerando retrabalhos. Embora um processo de homologação técnica tenha sido iniciado, a cultura de priorizar o custo inicial persiste.

**Sistemas Envolvidos:** `Coupia, SAP`

> *"olham muito para o. Para o valor, acaba contratando mais barato, só que esse barato sai caro."*

### 🟦 [Dor] Erro Manual (Etapa: Execução)
**Descrição:** Deficiência na quantificação dos custos reais associados a não conformidades, retrabalhos, atrasos de entregas e multas geradas por fornecedores. A falta de mão de obra e/ou processos sistemáticos impede a correlação desses problemas com o desempenho dos fornecedores e o custo total do empreendimento, dificultando a tomada de decisões estratégicas.

**Sistemas Envolvidos:** `PM, Kartado, Power Apps, Atlas, V360, SAP FI, Forms, Painel de Chamados, SAP FI/AP`

> *"a gente não tem mão de obra suficiente para poder quantificar o quanto que esse cara efetivamente é. Fazer um levantamento de todas as não conformidades, de retrabalho, quantificarHH material confrontar é atraso de entregas que geraram multas."*

### 🟦 [Dor] ETL Humano (Etapa: Estruturação PEP e EAP)
**Descrição:** A equipe precisa dedicar recursos significativos para levantar manualmente as horas-homem (OHH) detalhadas para cada função em projetos, como concreto armado, o que indica um processo manual e demorado para coleta de dados de planejamento.

**Sistemas Envolvidos:** ``

> *"realmente tem que ter uma parte da equipe dedicada para poder levantar isso no detalhe para poder. É trazer OHH ali de cada de cada função."*

### 🟦 [Dor] Erro Manual (Etapa: Planejamento e Execução)
**Descrição:** O processo de registro, acompanhamento e cobrança de Não Conformidades (RNCs) é manual e burocrático, gerando um 'favor de gestão' que poderia ser evitado com um processo mais estruturado e automatizado.

**Sistemas Envolvidos:** ``

> *"de você ter que registrar essas RNC, acompanhar, cobrar e aí tudo isso já tem inclusive um favor de gestão que poderia ser evitado se tivesse uma empresa mais estruturada"*

### 🟦 [Dor] Silo de Informação (Etapa: Planejamento e Execução)
**Descrição:** Há uma dificuldade em encontrar diretrizes e estruturas padronizadas na holding para a implementação do Sistema de Gestão da Qualidade (SGQ) na Engenharia de Implantação, forçando a equipe a buscar referências do zero ou de forma informal.

**Sistemas Envolvidos:** ``

> *"Eu sinto muita falta de ter uma estrutura montada na holding já, onde eu pudesse seguir as diretrizes em relação a isso. Eu estou com uma dificuldade de achar a pessoa que eu consiga falar 'Vem cá, onde que eu posso copiar algo pelo menos.'"*

### 🟦 [Dor] Silo de Informação (Etapa: Contratação)
**Descrição:** Os processos de homologação de fornecedores entre Suprimentos (foco contratual) e Qualidade (foco técnico) são distintos e não integrados, gerando burocracia, entraves e impedindo decisões rápidas. A tentativa de unificar falhou.

**Sistemas Envolvidos:** `SAP, Excel`

> *"o processo de homologação deles é um pouco diferente, porque eles estão eles estão mais preocupados com homologação do ponto de vista. Contratual, não homologação técnica. [...] não foi para frente, estava com muito entrave. É essas burocracias que a gente acaba se perdendo um pouco, porque a gente precisa tomar uma decisão rápida e não consegue."*

### 🟦 [Dor] ETL Humano (Etapa: Contratação)
**Descrição:** A homologação técnica de fornecedores é gerenciada por uma 'planilha padrão' mantida pela equipe de qualidade, que não é um processo formal e mandatório. Isso permite que tomadores de decisão contratem empresas não homologadas tecnicamente, aumentando o risco de qualidade.

**Sistemas Envolvidos:** `Excel`

> *"a gente tem uma planilha padrão que a gente especifica quais são os fornecedores homologados, os que não estão homologados, com a justificativa e tal" e "se o tomador de decisão quiser, por exemplo, ele pode falar assim, não, eu vou. Tem uma empresa que não é homologada e mesmo assim eu vou fechar com ela. Porque isso hoje não é um processo formal de assim, tem que estar homologado para fechar."*

### 🟦 [Dor] Silo de Informação (Etapa: Contratação)
**Descrição:** O departamento de Suprimentos foca na homologação de contratadas principais, mas não estende esse olhar para as subcontratadas, que são cruciais para a qualidade técnica das obras. A equipe de qualidade precisa atuar separadamente para cobrir essa lacuna.

**Sistemas Envolvidos:** `SAP, Excel`

> *"o suprimentos, ele olha para a contratada, ele não olha para a sub. Por mais que deveria, eles passam por um é. [...] para a gente como qualidade, o que importa, que é o técnico, ele não é visto. Então por isso que a gente atacou a subcontratadas."*

### 🟦 [Dor] Silo de Informação e Falta de Integração (Etapa: Planejamento e Execução)
**Descrição:** Existe uma cultura de trabalho em silos, onde diferentes núcleos e gerências operam de forma isolada, resultando em informações fragmentadas e falta de comunicação entre os processos. Isso impede uma visão holística e integrada da gestão de projetos CAPEX.

**Sistemas Envolvidos:** `Sistemas das diferentes gerências/núcleos`

> *"gestão com silo. Aconteceu muito aqui, o pessoal trabalhando. É bem separado, então agora que a gente vai buscar linkar todos esses processos."*

### 🟦 [Dor] Gargalo na Definição de Processos (Etapa: Planejamento e Execução)
**Descrição:** A tentativa de elaborar uma matriz RACI para definir papéis e responsabilidades resultou em um documento excessivamente complexo e 'poluído', que perdeu sua clareza e propósito original. Isso indica uma dificuldade em estabelecer e comunicar de forma eficaz as responsabilidades dentro dos processos, o que pode levar a gargalos na execução e tomada de decisão.

**Sistemas Envolvidos:** `Ferramentas de Gestão de Processos (ex: RACI)`

> *"É, ficou um tanto quanto poluído, porque perdeu um pouco do sentido da matriz raça e colocaram muita coisa."*

### 🟦 [Dor] Gargalo (Etapa: Contratação)
**Descrição:** Atrasos e burocracia na efetivação de contratos devido à falta de homologação prévia de subcontratadas, o que levava a problemas com empresas de pequeno porte e não qualificadas. Embora mitigado por um banco de dados atual, a diretriz ainda é necessária para evitar a recorrência do problema.

**Sistemas Envolvidos:** `DocuSign, Coupia, SAP`

> *"a gente orienta para não efetivar o contrato antes de ter a homologação, porque se não traz uma burocracia e aí já começa a atrasar cronograma. Se ela já já segue com a contratação da Silva antes de homologar, porque no começo a gente pegou uma série de de subcontratadas. Empresas muito pequenas mesmo."*

### 🟦 [Dor] Silo de Informação (Etapa: Planejamento e Execução)
**Descrição:** Existe uma lacuna na interface e padronização dos processos de inspeção de qualidade entre as equipes de obras civis/estruturas metálicas e as equipes de implantação de sistemas, sendo esta última uma área nova para a equipe de qualidade de obras.

**Sistemas Envolvidos:** `Implantação e Sistemas, Projetos de Sistemas`

> *"O que a gente está melhorando agora que eu estou puxando para o SGQ também é a interface com sistemas. Então porque eu falo por mim e pela minha equipe, a nossa especialidade são obras civis. [...] Dali para frente entrava a equipe sistemas então é algo novo para mim e para minha equipe então agora a gente está começando a ter mais interface com o pessoal de implantação e sistemas com o pessoal de projetos de sistemas também [...] agora que a gente vai começar A estreitar. E aí é o mundo que eu estou conhecendo Vitor."*

### 🟦 [Dor] Falta de Padronização (Etapa: Planejamento e Execução)
**Descrição:** A inspeção de qualidade em sistemas não possui uma estrutura específica e formalizada como a de obras civis, sendo a responsabilidade embutida nos especialistas e analistas, o que gera a necessidade de padronização e uma equipe dedicada para essa função.

**Sistemas Envolvidos:** `Implantação de Sistemas`

> *"Não específica que nem a nossa de civil, mas está embutido na responsabilidade dos especialistas e analistas. Eles desenvolvem até aqui. É tem um processo bem implantado, mas é o que a gente está trazendo agora para padronização. [...] o pessoal de implantação, não o pessoal de projetos, mas o pessoal de implantação é sempre comentou sobre a necessidade de ter uma equipe de implantação de sistemas com olhar de qualidade. Então, assim, é um é um ponto de melhoria."*

### 🟦 [Dor] Gargalo (Etapa: Planejamento e Execução)
**Descrição:** O processo de gestão de qualidade é considerado imaturo, sem um sistema formalizado, e há desafios com fornecedores menores que não possuem certificação, o que exige adaptações e controles manuais.

**Sistemas Envolvidos:** ``

> *"a gente percebeu que a gente estava é num processo muito imaturo, ainda sem sistema de gestão de qualidade, com esse problema de fornecedores. Pequenos, é sem certificação"*

### 🟦 [Dor] Erro Manual (Etapa: Planejamento e Execução)
**Descrição:** A identificação e correção de desvios em frentes de serviço são registradas manualmente em 'fichas de verificação', dependendo da especificação do inspetor, o que pode levar a inconsistências e dificuldades na consolidação.

**Sistemas Envolvidos:** ``

> *"na nossa ficha,De verificação, tem lá desvio apontado, aí o instrutor, o inspetor, ele especifica o que foi apontado"*

### 🟦 [Dor] Silo de Informação (Etapa: Planejamento e Execução)
**Descrição:** As não conformidades são gerenciadas em documentos Word, sem um sistema dedicado, o que dificulta a rastreabilidade e a análise de causa raiz. Há uma tentativa de migrar para o Autodesk Docs, mas com dificuldades de template.

**Sistemas Envolvidos:** `Word, Excel, Autodesk Docs`

> *"Mas hoje é hoje é tudo Excel. Rodrigo Correa de Souza É, tudo externo Word, não é nenhum sistema. A gente está querendo migrar agora para o Autodesk Docs, a gente está tentando levar o máximo de documentos para o Autodesk Docs, mas a Lima estava com uma dificuldade de template"*

### 🟦 [Dor] ETL Humano (Etapa: Medição)
**Descrição:** A tabulação das informações de desvios e não conformidades para a criação de indicadores de qualidade é realizada manualmente no Excel antes de ser enviada para o BI, introduzindo riscos de erro e atrasos.

**Sistemas Envolvidos:** `Excel, BI`

> *"a compilação disso tudo. Ela é feita manualmente no Excel. Ali você cria os indicadores. Rodrigo Correa de Souza Um indicador, isso é que leva. A gente leva para OBI"*

### 🟦 [Dor] Silo de Informação (Etapa: Planejamento e Execução)
**Descrição:** As inspeções e desvios são gerenciados no Autodesk Build, enquanto as não conformidades são tratadas separadamente no Word, criando um silo de informação e dificultando uma visão unificada da qualidade.

**Sistemas Envolvidos:** `Autodesk Build, Word`

> *"A gente que as inspeções, esses desvios apontados e corrigidos, a gente faz faz tudo no build... Mas anão conformidade... a gente acabou optando por fazer no... No Word mesmo."*

## 🤝 Mapa de Relações e Stakeholders
- **se_relaciona_com**: Rodrigo Correa de Souza | **Área:** Não citada 
  - *Contexto:* Discussão sobre o trabalho de Rodrigo, mapeamento de processos e SGQ
- **se_relaciona_com**: Vitor Pryzbeuka | **Área:** Não citada 
  - *Contexto:* Discussão sobre o trabalho de Rodrigo, mapeamento de processos e SGQ
- **se_relaciona_com**: Priscila Galindo Alexandre | **Área:** Não citada 
  - *Contexto:* Discussão sobre o trabalho de Rodrigo, mapeamento de processos e SGQ
- **se_relaciona_com**: Sander | **Área:** Não citada 
  - *Contexto:* Discussão sobre o trabalho de Rodrigo, mapeamento de processos e SGQ
- **se_relaciona_com**: Não citada | **Área:** Diretoria de Operação e Manutenção 
  - *Contexto:* Equalizar objetivos para especificação de requisitos mínimos de entrega e durabilidade de materiais
- **depende_de**: Não citada | **Área:** Diretoria de Operação e Manutenção 
  - *Contexto:* Verificar pontos de atuação, problemas de manutenção e onde o dinheiro está sendo gasto, a fim de evitar problemas desde a concepção do empreendimento
- **se_relaciona_com**: Não citada | **Área:** Diretoria de Implantação 
  - *Contexto:* Tomada de decisões conjuntas para otimizar investimentos, considerando o trade-off entre custo de implantação e manutenção
- **se_relaciona_com**: Não citada | **Área:** Diretoria de Operação e Manutenção 
  - *Contexto:* Tomada de decisões conjuntas para otimizar investimentos, considerando o trade-off entre custo de implantação e manutenção
- **se_relaciona_com**: Não citada | **Área:** Construtoras 
  - *Contexto:* Execução de obras, gestão de qualidade, segurança e meio ambiente
- **depende_de**: Não citada | **Área:** Pequenos Fornecedores 
  - *Contexto:* Subcontratação de serviços específicos por construtoras
- **depende_de**: Não citada | **Área:** Poder Concedente (TESP) 
  - *Contexto:* Atendimento a requisitos de contrato e padrões de exigência
- **se_relaciona_com**: Não citada | **Área:** Área de Suprimentos 
  - *Contexto:* Processo de homologação técnica de fornecedores para melhorar a qualidade e reduzir custos a longo prazo
- **se_relaciona_com**: Vitor Pryzbeuka | **Área:** Engenharia 
  - *Contexto:* Discussão sobre processos internos que guiam decisões de investimento vs. manutenção
- **se_relaciona_com**: Rodrigo Correa de Souza | **Área:** Engenharia de Implantação da Motiva Trilhos 
  - *Contexto:* Comunicação colaborativa e suporte para garantir a padronização e performance
- **se_relaciona_com**: Não citada | **Área:** Equipe de Qualidade 
  - *Contexto:* Comunicação colaborativa e suporte para garantir a padronização e performance
- **depende_de**: Não citada | **Área:** Holding 
  - *Contexto:* Busca por estrutura e diretrizes para a implantação do SGQ da Engenharia de Implantação
- **se_relaciona_com**: Não citada | **Área:** Suprimentos 
  - *Contexto:* Tentativa de estreitar a relação para unificar o processo de homologação de fornecedores (técnica vs. contratual)
- **approva**: Não citada | **Área:** Suprimentos 
  - *Contexto:* Homologação de contratadas do ponto de vista contratual
- **approva**: Não citada | **Área:** Equipe de Qualidade 
  - *Contexto:* Homologação técnica de subcontratadas (estruturas metálicas, pré-moldados, usina de concreto, usina de asfalto, laboratório)
- **fornece_dados_para**: Não citada | **Área:** Equipe de Qualidade 
  - *Contexto:* Fornecimento de lista de fornecedores homologados para apoiar a decisão dos tomadores de decisão
- **approva**: Andre Teixeira | **Área:** Gerência Executiva da vertical 
  - *Contexto:* Tomada de decisão sobre subcontratações após a figura do GP não existir mais
- **approva**: Priscila Galindo | **Área:** Gerência Executiva da vertical 
  - *Contexto:* Tomada de decisão sobre subcontratações após a figura do GP não existir mais
- **approva**: Minha Moura | **Área:** Gerência Executiva da vertical 
  - *Contexto:* Tomada de decisão sobre subcontratações após a figura do GP não existir mais
- **approva**: Não citada | **Área:** Diretoria 
  - *Contexto:* Exposição e treinamento de diretrizes para padronização
- **approva**: Não citada | **Área:** Gerentes Executivos 
  - *Contexto:* Exposição e treinamento de diretrizes para padronização
- **se_relaciona_com**: Não citada | **Área:** Teixeira Duarte 
  - *Contexto:* Empresa contratada que expõe falhas nos processos internos da Motiva, gerando oportunidades de melhoria
- **responde_a**: Rodrigo Correa de Souza | **Área:** Gerência de Acompanhamento de Projetos 
  - *Contexto:* Rodrigo responde a Michel, seu gerente na Gerência de Acompanhamento de Projetos.
- **se_relaciona_com**: Rodrigo Correa de Souza | **Área:** Time de PMO 
  - *Contexto:* Rodrigo colabora com o Time de PMO em atividades de acompanhamento de projetos CAPEX e OPEX.
- **se_relaciona_com**: Rodrigo Correa de Souza | **Área:** Não citada 
  - *Contexto:* Rodrigo se aproximou de Alexandre para discutir problemas e apresentações.
- **fornece_dados_para**: Rodrigo Correa de Souza | **Área:** Não citada 
  - *Contexto:* Rodrigo e sua equipe elaboraram e filtraram a matriz RACI para ser apresentada a Adriana.
- **se_relaciona_com**: Rodrigo Correa de Souza | **Área:** Líderes e Donos de Processos 
  - *Contexto:* Rodrigo realizou entrevistas e repassou a matriz RACI para os líderes e donos de processos para a implantação do SGQ.
- **approva**: Não citada | **Área:** Comitê Consultivo da Motiva 
  - *Contexto:* O Comitê Consultivo da Motiva é responsável por validar as hipóteses levantadas pela consultoria.
- **se_relaciona_com**: Não citada | **Área:** Comitê Consultivo da Motiva 
  - *Contexto:* O Comitê Consultivo envolve pessoas das plataformas e do corporativo para validações.
- **se_relaciona_com**: Vitor Pryzbeuka | **Área:** Não citada 
  - *Contexto:* Vitor Pryzbeuka, da Veron Consultoria, realiza entrevistas com Rodrigo Correa de Souza para o diagnóstico de processos CAPEX.
- **se_relaciona_com**: Priscila Galindo | **Área:** Não citada 
  - *Contexto:* Priscila Galindo, da Veron Consultoria, apoia nas entrevistas com Rodrigo Correa de Souza para o diagnóstico de processos CAPEX.
- **depende_de**: Não citada | **Área:** Engenharia de Implantação 
  - *Contexto:* A Engenharia de Implantação depende da colaboração e integração dos diversos núcleos da Motiva para a implantação do Sistema de Gestão da Qualidade (SGQ), superando a gestão em silos.
- **fornece_dados_para**: Rodrigo Correa de Souza | **Área:** Engenharia de Implantação 
  - *Contexto:* A equipe de qualidade, sob a coordenação de Rodrigo (anteriormente), fornecia dados de fiscalização de obra para garantir o cumprimento de requisitos contratuais e normativos na Engenharia de Implantação.
- **fornece_dados_para**: Não citada | **Área:** Motiva 
  - *Contexto:* A Boston Consulting Group (BCG) forneceu um modelo padrão de matriz RACI para a Motiva, utilizado na estruturação de processos.
- **se_relaciona_com**: Rodrigo Correa de Souza | **Área:** Contratadas/Subcontratadas 
  - *Contexto:* Homologação técnica de subcontratadas e disponibilização de banco de dados de empresas homologadas.
- **depende_de**: Rodrigo Correa de Souza | **Área:** Contratadas 
  - *Contexto:* A contratada especifica a subcontratada para homologação.
- **se_relaciona_com**: Rodrigo Correa de Souza | **Área:** Compliance 
  - *Contexto:* Esbarrou em critérios de compliance ao tentar fazer pesquisa de mercado para subcontratadas.
- **responde_a**: Rodrigo Correa de Souza | **Área:** Não citada 
  - *Contexto:* Michel, seu gerente executivo, valida a proposta de estruturação do SGQ.
- **se_relaciona_com**: Rodrigo Correa de Souza | **Área:** Qualidade de Obras 
  - *Contexto:* Inspeção de obras civis e estruturas metálicas, com equipe de inspetores especialistas.
- **se_relaciona_com**: Rodrigo Correa de Souza | **Área:** Implantação e Sistemas 
  - *Contexto:* Melhoria da interface com sistemas para o SGQ e padronização de processos.
- **se_relaciona_com**: Rodrigo Correa de Souza | **Área:** Projetos de Sistemas 
  - *Contexto:* Melhoria da interface com sistemas para o SGQ e padronização de processos.
- **se_relaciona_com**: Rodrigo Correa de Souza | **Área:** Engenharia de Projetos Central de Integração e Interface 
  - *Contexto:* Processos correlatos ao SGQ, gestão de requisitos técnicos, interface e operação.
- **responde_a**: Fabiana | **Área:** Central de Expertise 
  - *Contexto:* Fabiana tem responsabilidades de integração, interface, projetos e sistemas sob a gerência executiva de Jackie.
- **responde_a**: Alessandra | **Área:** Demais Empreendimentos (Linha 8 e 9) 
  - *Contexto:* Alessandra é gerente de implantação de sistemas sob a gerência executiva de André Teixeira.
- **se_relaciona_com**: Não citada | **Área:** Implantação de Sistemas 
  - *Contexto:* Especialistas e analistas de implantação de sistemas desenvolvem processos e têm responsabilidade de qualidade embutida.
- **se_relaciona_com**: Rodrigo Correa de Souza | **Área:** Implantação de Sistemas 
  - *Contexto:* Discussões sobre a necessidade de uma equipe de implantação de sistemas com olhar de qualidade.
- **depende_de**: Não citada | **Área:** Construtora 
  - *Contexto:* Coleta e envio de amostras de material para laboratório para double check de qualidade.
- **depende_de**: Não citada | **Área:** Construtora 
  - *Contexto:* Necessidade de certificado do fabricante e ensaio de laboratório para validação de material.
- **se_relaciona_com**: Não citada | **Área:** Time de Qualidade (Motiva) 
  - *Contexto:* Realização de verificações de serviço (checklist) em estruturas de concreto armado.
- **fornece_dados_para**: Não citada | **Área:** Time de Qualidade (Motiva) 
  - *Contexto:* Apontamento de desvios em fichas de verificação pelo inspetor.
- **se_relaciona_com**: Não citada | **Área:** Time de Qualidade (Motiva) 
  - *Contexto:* Orientação para correção de desvios identificados na frente de serviço, chamando o encarregado ou engenheiro da construtora.
- **fornece_dados_para**: Não citada | **Área:** Time de Qualidade (Motiva) 
  - *Contexto:* Registro de desvios corrigidos na ficha de verificação.
- **fornece_dados_para**: Não citada | **Área:** Time de Qualidade (Motiva) 
  - *Contexto:* Tabulação mensal de informações sobre desvios para gerar indicadores.
- **fornece_dados_para**: Não citada | **Área:** OBI (Business Intelligence) 
  - *Contexto:* Envio de dados de desvios e não conformidades para OBI para tratamento e geração de dashboards.
- **se_relaciona_com**: Não citada | **Área:** Construtora 
  - *Contexto:* Solicitação de análise de causa raiz para não conformidades pela Motiva.
- **se_relaciona_com**: Não citada | **Área:** Não citada 
  - *Contexto:* Migração de documentos para Autodesk Docs pelo Time de Qualidade.
- **fornece_dados_para**: Não citada | **Área:** Não citada 
  - *Contexto:* Registro de inspeções e desvios apontados e corrigidos no Autodesk Build.
- **fornece_dados_para**: Não citada | **Área:** Não citada 
  - *Contexto:* Registro de não conformidades e investigações de causa raiz em documento Word.
- **approva**: Michel | **Área:** Não citada 
  - *Contexto:* Validação de um novo indicador de qualidade elaborado pelo Time de Qualidade.
- **fornece_dados_para**: Não citada | **Área:** Construtora 
  - *Contexto:* Entrega de documentos (Plano de Garantia da Qualidade, relatórios mensais, data book) para o controle de qualidade da Motiva.
- **depende_de**: Não citada | **Área:** Construtora 
  - *Contexto:* Correção de não conformidades e penalização por reincidência, monitorado pela Motiva.

---
*Relatório gerado pelo Pipeline Sênior MOTIVA | Veron Consultoria.*
