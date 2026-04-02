# Ficha de Diagnóstico As-Is: Paulo Henrique de Almeida Aredes

## 👤 Perfil Organizacional
- **Cargo**: Consultor Contratos Implantação (L4)
- **Área**: Contratos e Riscos
- **Diretoria**: VP Trilhos
- **Nível**: Operacional

## 🖥️ Ecossistema de Sistemas e Workarounds
- **SAP PS** 🔴 *(Uso: Estruturação de PEP (Plano de Execução do Projeto) e EAP (Estrutura Analítica do Projeto), gestão de projetos e registro de medições. Utilizado para definir a estrutura do projeto e registrar o avanço físico/financeiro, sendo parte do processo de medição.)*
  - ⚠️ **Workaround / ETL Humano:** Morosidade no processo de pagamento devido à necessidade de re-entrada manual de dados de campo e burocracia interna.
- **SAP FI** 🔴 *(Uso: Estruturação de PEP e EAP (financeira), gestão fiscal e controle financeiro geral. Usado para gerenciar aspectos financeiros e fiscais, incluindo o registro de notas fiscais e gestão de aditivos.)*
  - ⚠️ **Workaround / ETL Humano:** Morosidade na gestão de aditivos e processos financeiros devido à governança e burocracia.
- **SAP BW** 🟡 *(Uso: Business Warehouse para relatórios e análise de dados. Utilizado para extrair e consolidar dados de diversas fontes para relatórios gerenciais e acompanhamento de tendências.)*
- **SAP BPC** 🟡 *(Uso: Business Planning and Consolidation para planejamento e orçamento. Utilizado para planejamento financeiro, orçamentário e consolidação de dados.)*
- **SAP MM** 🟡 *(Uso: Gestão de materiais, serviços e contratos de suprimentos. Utilizado para gerenciar o ciclo de compras e contratos com fornecedores.)*
- **Prisma** 🟡 *(Uso: Estruturação de PEP e EAP. Ferramenta para definir a estrutura do projeto.)*
- **Project** 🟡 *(Uso: Estruturação de PEP e EAP, planejamento e acompanhamento de cronogramas. Ferramenta para gestão de cronogramas e tarefas do projeto.)*
- **Primavera** 🟡 *(Uso: Planejamento e controle avançado de projetos, cronogramas e recursos (P6). Utilizado para gerenciar cronogramas complexos e recursos de grandes projetos.)*
- **Compor 90** 🟡 *(Uso: Composição de custos e orçamentos de obras. Ferramenta para detalhar e estruturar orçamentos de projetos.)*
- **Coupa** 🟡 *(Uso: Gestão de suprimentos, compras e contratos. Plataforma para gerenciar o ciclo de vida de compras e contratos.)*
- **Netlex** 🟡 *(Uso: Gestão jurídica de contratos. Utilizado para gerenciar o ciclo de vida legal dos contratos.)*
- **Flexchain** 🟡 *(Uso: Gestão da cadeia de suprimentos e contratos. Ferramenta para gerenciar aspectos da cadeia de suprimentos.)*
- **Docusign** 🟢 *(Uso: Assinatura eletrônica de contratos e documentos. Utilizado para formalizar contratos de forma digital e segura.)*
- **Kartado** 🟡 *(Uso: Gestão de campo, diário de obra e acompanhamento da execução. Utilizado para gerenciar atividades e coletar dados de campo.)*
- **Conecta** 🟡 *(Uso: Colaboração e comunicação em projetos. Ferramenta de conexão ou gestão de informações para equipes de projeto.)*
- **Fulcrum** 🟡 *(Uso: Coleta de dados de campo para medição do avanço físico. Utilizado pela engenharia de campo para registrar o avanço e medições.)*
  - ⚠️ **Workaround / ETL Humano:** Dados coletados precisam ser re-inseridos ou processados manualmente antes de entrar no SAP, contribuindo para a morosidade.
- **Archer** 🟡 *(Uso: Gestão de riscos corporativos e tendências. Ferramenta para monitorar e analisar riscos do projeto e da companhia.)*
- **V360** 🟡 *(Uso: Gestão fiscal e de notas fiscais. Utilizado para processar e gerenciar documentos fiscais.)*
- **Atlas** 🟡 *(Uso: Gestão fiscal e de notas fiscais. Utilizado para processar e gerenciar documentos fiscais.)*
- **Power BI** 🟢 *(Uso: Geração de dashboards e relatórios de desempenho e tendências. Ferramenta para visualização e análise de dados de diversas fontes.)*
- **SharePoint** 🟡 *(Uso: Gestão documental, colaboração e armazenamento de informações de projeto. Utilizado para armazenamento e compartilhamento de documentos de projeto.)*
- **Teams** 🟢 *(Uso: Colaboração, comunicação, reuniões e gestão de ideias (Teams Idea). Plataforma de comunicação e colaboração para equipes e gestão de informações.)*
- **Excel** 🟡 *(Uso: Estruturação de PEP e EAP, análises ad-hoc, consolidação de dados e 'ponte' entre sistemas. Utilizado para estruturar projetos e como ferramenta auxiliar em diversas etapas, frequentemente para consolidar dados ou preencher lacunas de integração.)*
  - ⚠️ **Workaround / ETL Humano:** Frequentemente usado como 'ponte' ou para preencher lacunas de integração, gerando retrabalho e morosidade.
- **SIC** 🟡 *(Uso: Sistema de Informações Gerenciais para acompanhamento de projetos. Utilizado para acessar informações e relatórios gerenciais.)*
- **RDO** 🟡 *(Uso: Registro Diário de Obras. Utilizado para registrar o andamento diário das atividades da obra.)*
- **Power Apps** 🟡 *(Uso: Desenvolvimento de aplicações personalizadas para processos de campo. Criação de apps para otimizar processos de campo ou coleta de dados.)*
- **Microsoft Forms** 🟡 *(Uso: Coleta de dados e informações, possivelmente para processos fiscais ou de NF. Criação de formulários para coleta de informações de forma estruturada.)*
- **Painel de Chamados** 🟡 *(Uso: Gestão de chamados e solicitações relacionadas a pagamentos. Utilizado para registrar e acompanhar solicitações de pagamento e outras demandas financeiras.)*
- **SAP FI/AP** 🔴 *(Uso: Contas a Pagar, operacionalização e processamento de pagamentos a fornecedores. Módulo do SAP para gerenciar e executar pagamentos a fornecedores, recebendo dados de medição.)*
  - ⚠️ **Workaround / ETL Humano:** Morosidade no processo de pagamento devido à governança e burocracia, exigindo re-entrada de dados e aprovações demoradas.
- **SAP PS** 🟡 *(Uso: Gestão de projetos, controle de custos e prazos, medição de progresso físico e financeiro. Registro e acompanhamento da estrutura analítica de projetos (PEP e EAP), alocação de custos e medições.)*
- **SAP FI** 🟡 *(Uso: Contabilidade financeira, gestão fiscal, processamento de pagamentos e controle de custos. Registro de transações financeiras, emissão de notas fiscais, processamento de contas a pagar e a receber.)*
- **SAP BW** 🟡 *(Uso: Business Warehouse para relatórios e análises de dados corporativos. Geração de relatórios gerenciais e análises de desempenho baseadas em dados de diversas fontes SAP.)*
- **SAP BPC** 🟡 *(Uso: Planejamento, Orçamento e Consolidação de dados financeiros. Elaboração de orçamentos, previsões financeiras e consolidação de resultados.)*
- **SAP MM** 🟡 *(Uso: Gestão de materiais e suprimentos, incluindo compras e estoque. Processamento de requisições de compra, pedidos, recebimento de materiais e gestão de inventário.)*
- **Prisma** 🟡 *(Uso: Estruturação de projetos, especialmente PEP (Plano de Execução de Projeto) e EAP (Estrutura Analítica de Projeto). Criação e manutenção da estrutura detalhada dos projetos, definindo escopo e entregas.)*
- **Project** 🟡 *(Uso: Planejamento e acompanhamento de cronogramas de projetos. Criação, gestão e monitoramento de cronogramas, tarefas e recursos de projetos.)*
- **P6** 🟡 *(Uso: Planejamento e controle avançado de projetos e portfólios. Gestão de grandes projetos, recursos e cronogramas complexos, com análise de caminho crítico.)*
- **Primavera** 🟡 *(Uso: Planejamento e controle avançado de projetos e portfólios. Gestão de grandes projetos, recursos e cronogramas complexos, com análise de caminho crítico.)*
- **Compor 90** 🟡 *(Uso: Composição de custos e orçamentos de obras e serviços de engenharia. Elaboração de orçamentos detalhados, com base em composições de preços unitários.)*
- **Coupa** 🟡 *(Uso: Gestão de compras e suprimentos (e-procurement), incluindo cotações e pedidos. Processos de cotação, aprovação de pedidos, gestão de fornecedores e contratos de compra.)*
- **Netlex** 🟡 *(Uso: Gestão do ciclo de vida de contratos. Armazenamento, acompanhamento e gestão de cláusulas e aditivos contratuais.)*
- **Flexchain** 🟡 *(Uso: Gestão da cadeia de suprimentos e logística. Otimização de processos logísticos, rastreamento de materiais e gestão de fornecedores.)*
- **Docusign** 🟡 *(Uso: Assinatura eletrônica de documentos e contratos. Formalização digital de contratos, aditivos e outros documentos que requerem assinatura.)*
- **Kartado** 🟡 *(Uso: Gestão de obras e equipes em campo, com foco em produtividade e controle. Acompanhamento de atividades em canteiro, registro de ocorrências e medição de progresso.)*
- **Conecta** 🟡 *(Uso: Plataforma de colaboração e comunicação para equipes de projeto. Compartilhamento de informações, documentos e comunicação entre os membros da equipe.)*
- **Fulcrum** 🟡 *(Uso: Coleta de dados em campo para medição e inspeção. Registro de dados de medição, fotos e informações relevantes diretamente no local da obra.)*
- **Archer** 🟡 *(Uso: Gestão de riscos e conformidade (GRC). Monitoramento, avaliação e mitigação de riscos, além de garantir a conformidade com regulamentações.)*
- **V360** 🟡 *(Uso: Gestão fiscal e tributária, com foco na conformidade e processamento de documentos. Processamento, validação e armazenamento de documentos fiscais, garantindo a conformidade tributária.)*
- **Atlas** 🟡 *(Uso: Gestão fiscal e tributária, com foco na conformidade e processamento de documentos. Processamento, validação e armazenamento de documentos fiscais, garantindo a conformidade tributária.)*
- **Power BI** 🟡 *(Uso: Análise e visualização de dados para insights de negócios. Criação de dashboards interativos e relatórios para monitorar o desempenho e identificar tendências.)*
- **SharePoint** 🟡 *(Uso: Gestão documental, colaboração e intranet corporativa. Armazenamento, compartilhamento e controle de versão de documentos de projeto, além de sites de equipe.)*
- **Teams** 🟡 *(Uso: Comunicação unificada e colaboração em equipe. Reuniões online, chats, compartilhamento de arquivos e organização de equipes de projeto.)*
- **Excel** 🟡 *(Uso: Cálculos, controle de cronogramas, planilhas de linha de base e suporte a processos. Criação e manutenção do 'cronograma de linha de base' com cálculos automáticos de produtividade e prazos. Utilizado como ferramenta intermediária para ajustes contratuais.)*
  - ⚠️ **Workaround / ETL Humano:** Atua como 'planilha ponte' para formalização de ajustes contratuais em contratos não FIDC, exigindo ajustes e formalizações manuais em outros sistemas.
- **SIC** 🟡 *(Uso: Sistema de Informação ao Cidadão (geralmente para transparência pública). Não especificado no contexto de CAPEX da Motiva.)*
- **RDO** 🟡 *(Uso: Registro Diário de Obras. Documentação diária de atividades, recursos utilizados, ocorrências e progresso da obra.)*
- **Power Apps** 🟡 *(Uso: Desenvolvimento de aplicativos de negócios personalizados para otimização de processos. Criação de ferramentas específicas para coleta de dados, aprovações ou gestão de tarefas em projetos.)*
- **Forms** 🟡 *(Uso: Coleta de dados via formulários digitais. Criação e distribuição de formulários para coleta de informações fiscais ou outras necessidades de dados.)*
- **Painel de Chamados** 🟡 *(Uso: Gestão de solicitações e acompanhamento de processos internos, incluindo pagamentos. Abertura e acompanhamento de chamados para processamento de pagamentos após aprovação de medições.)*
- **SAP PS** 🟡 *(Uso: Gerenciamento de projetos, controle de custos e medição de progresso físico-financeiro. Criação e gestão de estruturas de projeto (PEP/EAP), registro de medições de obras e acompanhamento do avanço.)*
  - ⚠️ **Workaround / ETL Humano:** Potencial complexidade na integração com ferramentas de engenharia e na agilidade para processar pleitos contratuais.
- **SAP FI** 🟡 *(Uso: Contabilidade financeira, gestão de custos, fiscal, faturamento e pagamentos. Registro de transações financeiras, controle de pagamentos a fornecedores, gestão de impostos e emissão de notas fiscais.)*
  - ⚠️ **Workaround / ETL Humano:** Necessidade de inputs manuais ou conciliações de dados provenientes de sistemas externos, gerando retrabalho.
- **SAP BW/BPC** 🟡 *(Uso: Business Warehouse para relatórios e análises, e Business Planning and Consolidation para planejamento e orçamento. Geração de relatórios gerenciais de performance, suporte à tomada de decisão estratégica e planejamento financeiro.)*
  - ⚠️ **Workaround / ETL Humano:** Complexidade na extração e consolidação de dados de múltiplas fontes, impactando a agilidade das análises.
- **Prisma** 🟡 *(Uso: Estruturação de projetos, planejamento e controle de escopo. Definição de estruturas analíticas de projeto (EAP) e elementos PEP, alinhamento com o escopo da obra.)*
  - ⚠️ **Workaround / ETL Humano:** Potencial desalinhamento ou retrabalho na transição de dados para sistemas de execução e financeiro como o SAP PS.
- **Project** 🟡 *(Uso: Gerenciamento de cronogramas, tarefas e recursos de projeto. Criação e acompanhamento de planos de projeto detalhados, gestão de prazos e dependências.)*
  - ⚠️ **Workaround / ETL Humano:** Dificuldade de integração automática com sistemas financeiros e de controle de custos, exigindo atualizações manuais.
- **Compor 90** 🟡 *(Uso: Composição de custos e orçamentos de obras. Elaboração de orçamentos detalhados, análise de preços unitários e composições para pleitos contratuais.)*
  - ⚠️ **Workaround / ETL Humano:** Necessidade de exportação/importação manual de dados para outros sistemas de gestão, como o SAP.
- **Coupa** 🟡 *(Uso: Gestão de compras e suprimentos, e-procurement. Condução de processos de cotação, emissão de pedidos de compra e gestão de fornecedores.)*
  - ⚠️ **Workaround / ETL Humano:** Potencial para desintegração com sistemas de gestão de contratos e financeiro, exigindo conciliações.
- **Netlex** 🟡 *(Uso: Gestão do ciclo de vida dos contratos. Armazenamento, acompanhamento e gestão de cláusulas contratuais, aditivos e pleitos.)*
  - ⚠️ **Workaround / ETL Humano:** Dificuldade em integrar automaticamente dados de pleitos ou aditivos com sistemas financeiros e de planejamento.
- **Flexchain** 🟡 *(Uso: Gestão da cadeia de suprimentos e logística. Rastreamento de materiais, gestão de fornecedores e otimização de fluxos logísticos.)*
  - ⚠️ **Workaround / ETL Humano:** Desconexão com o processo de contratação e execução de obras, gerando silos de informação.
- **Docusign** 🟢 *(Uso: Assinatura eletrônica de documentos. Formalização digital de contratos, aditivos e outros documentos legais, agilizando o processo.)*
  - ⚠️ **Workaround / ETL Humano:** Necessidade de integração com sistemas de gestão de contratos para arquivamento automático e rastreabilidade.
- **Teams** 🟢 *(Uso: Comunicação e colaboração interna. Reuniões online, chats, compartilhamento de documentos e gestão de ideias para projetos.)*
  - ⚠️ **Workaround / ETL Humano:** Dificuldade em rastrear decisões e informações críticas de projeto de forma estruturada e auditável.
- **PM** 🟡 *(Uso: Gerenciamento de projetos (genérico). Planejamento, execução e controle de atividades de projeto.)*
  - ⚠️ **Workaround / ETL Humano:** Potencial para duplicação de esforços ou inconsistências com outras ferramentas de planejamento e controle.
- **Kartado** 🟡 *(Uso: Gestão de obras e equipes em campo. Acompanhamento de atividades, registro de ocorrências e gestão de recursos em canteiros de obra.)*
  - ⚠️ **Workaround / ETL Humano:** Dificuldade em sincronizar dados de progresso em tempo real com o planejamento mestre e sistemas financeiros.
- **Power Apps** 🟡 *(Uso: Desenvolvimento de aplicações personalizadas para otimização de processos. Criação de ferramentas para coleta de dados, automação de fluxos de trabalho ou gestão de informações específicas.)*
  - ⚠️ **Workaround / ETL Humano:** Manutenção e integração com sistemas legados, além da necessidade de expertise para desenvolvimento.
- **SharePoint** 🟡 *(Uso: Compartilhamento de documentos e colaboração. Armazenamento de arquivos de projeto, gestão de versões e criação de portais de equipe.)*
  - ⚠️ **Workaround / ETL Humano:** Dificuldade em manter a governança e evitar a dispersão de informações se não houver uma estrutura bem definida.
- **Conecta** 🟡 *(Uso: Colaboração e comunicação em projetos. Compartilhamento de informações, comunicação entre equipes e gestão de tarefas colaborativas.)*
  - ⚠️ **Workaround / ETL Humano:** Pode gerar informações dispersas e dificultar a rastreabilidade de decisões importantes.
- **Fulcrum** 🟡 *(Uso: Coleta de dados em campo para medição de progresso de obras. Registro de medições físicas, inspeções e coleta de evidências fotográficas diretamente no canteiro.)*
  - ⚠️ **Workaround / ETL Humano:** Necessidade de integração manual ou semi-automática com sistemas de faturamento (SAP FI/PS) para processamento.
- **Archer** 🟡 *(Uso: Gestão de riscos corporativos, conformidade e auditoria. Registro e acompanhamento de riscos, gestão de políticas e controles internos.)*
  - ⚠️ **Workaround / ETL Humano:** Desconexão com os riscos operacionais e de projeto específicos do CAPEX, exigindo adaptações.
- **BI** 🟢 *(Uso: Análise de dados e visualização de indicadores de performance. Criação de dashboards e relatórios para monitoramento de performance de projetos e tendências.)*
  - ⚠️ **Workaround / ETL Humano:** Dependência da qualidade e integração dos dados de origem, que podem estar em silos.
- **Atlas** 🟡 *(Uso: Gestão fiscal e de notas fiscais. Processamento, validação e armazenamento de documentos fiscais.)*
  - ⚠️ **Workaround / ETL Humano:** Necessidade de conciliação manual com o SAP FI, gerando retrabalho e potencial para erros.
- **V360** 🟡 *(Uso: Gestão fiscal e de notas fiscais. Processamento e validação de documentos fiscais, suporte à conformidade.)*
  - ⚠️ **Workaround / ETL Humano:** Similar ao Atlas, potencial para retrabalho ou inconsistências na integração com o SAP FI.
- **Forms** 🟡 *(Uso: Coleta de informações e dados estruturados. Criação de formulários para entrada de dados fiscais, de processo ou de feedback.)*
  - ⚠️ **Workaround / ETL Humano:** Necessidade de processamento manual dos dados coletados e integração com outros sistemas.
- **Painel de Chamados** 🟡 *(Uso: Gestão de solicitações e acompanhamento de pagamentos. Registro e acompanhamento de chamados relacionados a pagamentos, dúvidas ou problemas.)*
  - ⚠️ **Workaround / ETL Humano:** Desconexão com o fluxo de aprovação de pagamentos no SAP FI/AP, podendo atrasar processos.
- **Excel** 🔴 *(Uso: Cálculos, análises ad-hoc, 'planilha ponte' para integração de dados. Suporte a decisões, cálculos de pleitos, como intermediário entre sistemas não integrados.)*
  - ⚠️ **Workaround / ETL Humano:** Falta de integração, suscetibilidade a erros manuais, retrabalho e falta de rastreabilidade das informações.
- **Fli/CO** 🟡 *(Uso: Contabilidade financeira e controle de custos. Registro de custos, acompanhamento orçamentário e análise de despesas.)*
  - ⚠️ **Workaround / ETL Humano:** Complexidade na integração com sistemas de planejamento de engenharia e na consolidação de dados.
- **SAP** 🟡 *(Uso: Sistema de gestão empresarial para diversas funções, incluindo contratação. Registro e gestão de informações relacionadas a contratos e fornecedores.)*
  - ⚠️ **Workaround / ETL Humano:** Generalista, pode exigir módulos específicos ou integrações para atender plenamente às necessidades de contratação.
- **SAP FI/AP** 🟡 *(Uso: Gestão de contas a pagar. Processamento e liberação de pagamentos a fornecedores, registro contábil das obrigações.)*
  - ⚠️ **Workaround / ETL Humano:** Dependência de inputs de outros sistemas para iniciar o processo de pagamento, gerando gargalos.
- **SAP PS** 🟡 *(Uso: Lançamento e registro de medições de obras e criação de folhas de registro. A área de Gestão Administrativa de Contratos (GACNE) lança as medições e cria as folhas de registro no sistema após as análises e validações externas.)*
  - ⚠️ **Workaround / ETL Humano:** Parte de um processo moroso e com múltiplos pontos de validação externa, contribuindo para o gargalo de prazo.
- **SAP FI** 🟡 *(Uso: Programação de pagamentos a fornecedores e gestão financeira. Recebe as aprovações da diretoria para programar os pagamentos após o lançamento das medições no SAP PS e o encaminhamento das notas fiscais.)*
  - ⚠️ **Workaround / ETL Humano:** Nenhum problema sistêmico direto, mas o fluxo de aprovação e validação que o antecede é complexo e demorado.
- **Primavera** 🔴 *(Uso: Elaboração e acompanhamento do planejamento físico das obras. Utilizado para criar e gerenciar o cronograma e o avanço físico dos projetos.)*
  - ⚠️ **Workaround / ETL Humano:** Não há integração sistêmica com o financeiro (SAP) nem com a gestão contratual, gerando silos de informação e a necessidade de acompanhamento manual.
- **Project** 🔴 *(Uso: Elaboração e acompanhamento do planejamento físico das obras. Utilizado para criar e gerenciar o cronograma e o avanço físico dos projetos.)*
  - ⚠️ **Workaround / ETL Humano:** Não há integração sistêmica com o financeiro (SAP) nem com a gestão contratual, gerando silos de informação e a necessidade de acompanhamento manual.
- **Prisma** 🟡 *(Uso: Definição e gestão da Estrutura Analítica de Projeto (EAP) e Elementos PEP. Utilizado para criar e organizar a hierarquia de projetos e suas atividades.)*
- **Fli/CO** 🟡 *(Uso: Gestão de contabilidade financeira e controle de custos de projetos. Suporte à estruturação financeira dos projetos e acompanhamento de custos.)*
- **SAP PS** 🟡 *(Uso: Gestão de projetos, controle de custos e acompanhamento físico-financeiro. Criação de projetos, alocação de recursos, registro de medições e controle de progresso.)*
- **SAP FI** 🟡 *(Uso: Contabilidade financeira, gestão de ativos, controle de pagamentos e recebimentos. Lançamento de despesas, gestão de faturas, processamento de pagamentos e controle fiscal.)*
- **Compor 90** 🟡 *(Uso: Composição de custos e orçamentação detalhada de projetos de engenharia. Elaboração de orçamentos e planilhas de custo para obras e serviços.)*
- **Excel** 🟡 *(Uso: Análises ad-hoc, controle paralelo, e como ferramenta de 'ponte' para dados. Criação de planilhas para cálculos, listas e como intermediário para troca de dados.)*
  - ⚠️ **Workaround / ETL Humano:** Potencial uso como 'ponte' para dados não integrados
- **Project** 🟡 *(Uso: Planejamento e acompanhamento de cronogramas de projetos. Criação de cronogramas, alocação de tarefas e monitoramento do progresso físico.)*
- **DocuSign** 🟡 *(Uso: Assinatura eletrônica de documentos e contratos. Envio e recebimento de documentos para coleta de assinaturas digitais de forma segura.)*
- **Coupia** 🟡 *(Uso: Gestão de compras, sourcing e gestão de fornecedores. Processamento de requisições de compra, cotações e ordens de compra.)*
- **SAP** 🟡 *(Uso: Suporte a processos de contratação, como registro de fornecedores e ordens de compra. Utilizado para etapas financeiras e de registro relacionadas à contratação.)*
- **Teams** 🟡 *(Uso: Colaboração, comunicação, reuniões e compartilhamento de documentos. Comunicação interna, reuniões de projeto e gestão de equipes de contratação.)*
- **Netlex** 🟡 *(Uso: Gestão de contratos jurídicos e documentos legais. Armazenamento, acompanhamento e controle de contratos e aditivos.)*
- **Flexchain** 🟡 *(Uso: Gestão da cadeia de suprimentos e contratos. Monitoramento de contratos e fornecedores ao longo da cadeia de suprimentos.)*
- **PM** 🟡 *(Uso: Ferramenta genérica de gestão de projetos para planejamento e acompanhamento. Utilizado para gerenciar tarefas, recursos e prazos durante a execução dos projetos.)*
- **Kartado** 🟡 *(Uso: Gestão de obras em campo, diário de obras e medição de serviços. Registro de atividades diárias, fotos e medições de campo para acompanhamento da execução.)*
- **Power Apps** 🟡 *(Uso: Desenvolvimento de aplicações personalizadas para processos específicos de projeto. Criação de apps para coleta de dados, workflows e automação de tarefas no campo.)*
- **SharePoint** 🟡 *(Uso: Gestão de documentos, portais de equipe e colaboração. Armazenamento e compartilhamento de documentos de projeto, relatórios e informações.)*
- **Conecta** 🟡 *(Uso: Plataforma de colaboração e gestão de projetos. Compartilhamento de informações, acompanhamento de tarefas e comunicação entre equipes.)*
- **Fulcrum** 🟡 *(Uso: Coleta de dados em campo para medições e inspeções. Registro de informações de medição no local da obra, com dados georreferenciados.)*
- **Archer** 🟡 *(Uso: Gestão de riscos, compliance e auditoria. Monitoramento de riscos de projetos, controles internos e conformidade regulatória.)*
- **SAP BW** 🟡 *(Uso: Data warehousing para relatórios e análises gerenciais. Extração e consolidação de dados de diversas fontes para suporte à tomada de decisão.)*
- **SAP BPC** 🟡 *(Uso: Planejamento, orçamento, previsão e consolidação financeira. Elaboração de orçamentos, projeções financeiras e análise de cenários.)*
- **BI** 🟡 *(Uso: Visualização de dados, criação de dashboards e relatórios para análise de performance. Acompanhamento de indicadores de projeto, financeiros e operacionais.)*
- **Teams Idea** 🟡 *(Uso: Gestão de ideias e inovação dentro do ambiente Microsoft Teams. Coleta, organização e avaliação de sugestões e projetos de melhoria.)*
- **Atlas** 🟡 *(Uso: Gestão de documentos fiscais e notas fiscais. Processamento, armazenamento e consulta de notas fiscais eletrônicas.)*
- **V360** 🟡 *(Uso: Gestão fiscal e tributária, com foco em conformidade. Cálculo e apuração de impostos, garantindo a conformidade com a legislação fiscal.)*
- **Forms** 🟡 *(Uso: Coleta de dados através de formulários digitais. Criação e distribuição de formulários para diversas finalidades, incluindo coleta de informações fiscais.)*
- **Painel de Chamados** 🟡 *(Uso: Gerenciamento de solicitações e tickets relacionados a pagamentos. Abertura, acompanhamento e fechamento de chamados para processamento de pagamentos.)*
- **Prisma** 🟡 *(Uso: Estruturação de projetos (PEP e EAP). Utilizado para definir a estrutura analítica e de projetos.)*
- **SAP PS** 🟡 *(Uso: Gerenciamento de projetos (Project Systems), controle de custos e medição. Usado para estruturar projetos e registrar medições e custos.)*
- **SAP FI** 🟡 *(Uso: Contabilidade financeira, registro de medições, fiscal e pagamentos. Utilizado para registrar transações financeiras, medições, notas fiscais e processar pagamentos.)*
- **SAP BW/BPC** 🟡 *(Uso: Business Warehouse (BW) para relatórios e Business Planning and Consolidation (BPC) para planejamento e orçamento. Usado para análise de dados, planejamento financeiro e consolidação de informações de custos e progresso.)*
- **SAP MM** 🟡 *(Uso: Gestão de materiais e suprimentos, incluindo processos de compra. Utilizado para gerenciar pedidos de compra e contratos de suprimentos.)*
- **Compor 90** 🟡 *(Uso: Composição de custos e orçamentos de obras. Usado para detalhar e compor os custos de projetos de engenharia.)*
- **Excel** 🔴 *(Uso: Ferramenta de apoio para estruturação, análise de dados, relatórios e "ponte" entre sistemas. Criação e análise de relatórios, consolidação de dados, cálculos e como intermediário para troca de informações.)*
  - ⚠️ **Workaround / ETL Humano:** Usado como "ponte" ou para "trabalho braçal" devido à falta de integração ou automação entre sistemas.
- **Project** 🟡 *(Uso: Planejamento e acompanhamento de cronogramas de projetos. Usado para criar e gerenciar cronogramas de obras e atividades.)*
- **P6** 🟡 *(Uso: Planejamento e controle avançado de projetos, cronogramas e recursos. Utilizado para planejamento detalhado de projetos de grande porte e acompanhamento de progresso.)*
- **Primavera** 🟡 *(Uso: Planejamento e controle avançado de projetos, cronogramas e recursos. Utilizado para planejamento detalhado de projetos de grande porte e acompanhamento de progresso.)*
- **DocuSign** 🟢 *(Uso: Assinatura eletrônica de documentos. Usado para formalizar a assinatura de contratos e outros documentos legais.)*
- **Coupa** 🟡 *(Uso: Gestão de compras e despesas (Procure-to-Pay). Utilizado para gerenciar o processo de contratação de fornecedores e aquisições.)*
- **Netlex** 🟡 *(Uso: Gestão de contratos e documentos jurídicos. Usado para gerenciar o ciclo de vida dos contratos, cláusulas e documentos relacionados.)*
- **Flexchain** 🟡 *(Uso: Gestão da cadeia de suprimentos e logística. Utilizado para gerenciar aspectos da cadeia de suprimentos relacionados aos contratos e projetos.)*
- **Kartado** 🟡 *(Uso: Gestão de obras e equipes em campo. Usado para acompanhar o progresso das obras e atividades em campo, gerando relatórios de execução.)*
- **Conecta** 🟡 *(Uso: Plataforma de colaboração e comunicação. Utilizado para facilitar a comunicação e o compartilhamento de informações entre as equipes de projeto.)*
- **Fulcrum** 🟡 *(Uso: Coleta de dados em campo para medição e inspeção. Usado para registrar dados de medição diretamente da obra.)*
- **Archer** 🟡 *(Uso: Gestão de riscos e conformidade. Utilizado para identificar, avaliar e monitorar riscos de projetos e conformidade regulatória.)*
- **V360** 🟡 *(Uso: Gestão de documentos fiscais e notas fiscais. Usado para processar e armazenar documentos fiscais e notas fiscais.)*
- **Atlas** 🟡 *(Uso: Gestão de documentos fiscais e notas fiscais. Usado para processar e armazenar documentos fiscais e notas fiscais.)*
- **Power BI** 🟢 *(Uso: Análise de dados e criação de dashboards para visualização de indicadores. Usado para criar painéis de controle e relatórios gerenciais sobre avanço, custos e status de contratos.)*
- **SharePoint** 🟡 *(Uso: Compartilhamento e gestão de documentos. Usado para armazenar e compartilhar documentos de projeto, como RDOs, atas e cartas.)*
- **Teams** 🟢 *(Uso: Comunicação e colaboração. Usado para reuniões semanais, chats e colaboração em documentos entre equipes internas e externas.)*
- **SIC** 🟡 *(Uso: Sistema de Informação e Controle. Utilizado para registro e consulta de informações gerais.)*
- **RDO** 🟡 *(Uso: Registro diário das atividades, ocorrências e progresso da obra. Documento gerado pela empreiteira e analisado pela equipe interna da Motiva.)*
  - ⚠️ **Workaround / ETL Humano:** Pode ser manual ou semi-automatizado, exigindo conferência e análise manual.
- **CI do poder concedente** 🟡 *(Uso: Canal formal de comunicação e protocolo de documentos com o poder concedente. Usado para protocolar cartas e comunicações oficiais, após elaboração manual das minutas.)*
  - ⚠️ **Workaround / ETL Humano:** Processo manual de elaboração de minutas e protocolo, gerando "trabalho braçal".
- **Forms** 🟡 *(Uso: Coleta de dados e formulários. Utilizado para coletar informações fiscais ou de processo.)*
- **Painel de Chamados** 🟡 *(Uso: Gestão de solicitações e chamados, possivelmente para pagamentos. Usado para registrar e acompanhar solicitações de pagamento ou outras demandas.)*
- **SAP FI/AP** 🟡 *(Uso: Contas a Pagar no SAP FI. Utilizado para processar e gerenciar pagamentos a fornecedores.)*
- **Power Apps** 🟡 *(Uso: Criação de aplicativos personalizados para otimizar processos. Pode ser usado para digitalizar formulários ou processos específicos da obra.)*
- **Teams Idea** 🟢 *(Uso: Colaboração e brainstorming para novas ideias e tendências. Usado para discussões e compartilhamento de insights sobre tendências e inovações.)*

## 🔥 Dores, Gargalos e Diagnósticos
### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** O fluxo inicia com a engenharia em campo acompanhando e analisando a execução dos serviços para fins de medição. Após a validação inicial, a responsabilidade é transferida para outra área que operacionaliza a medição no sistema SAP, culminando no processamento do pagamento ao fornecedor.

**Sistemas Envolvidos:** ``

> *"Rupturas: A transição entre a análise de campo/engenharia e a operacionalização da medição no SAP é lenta e ineficiente, gerando morosidade e atrasos significativos no processo de pagamento."*

### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** Qualquer alteração ou aditivo a um contrato existente requer a adesão a uma governança interna rigorosa, que envolve múltiplas etapas de aprovação e validação.

**Sistemas Envolvidos:** ``

> *"Rupturas: A governança interna é percebida como excessivamente burocrática e demorada, resultando em atrasos na formalização de aditivos., Os atrasos nos aditivos prejudicam o andamento da obra e a capacidade de adaptação com os fornecedores."*

### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** O contrato FIDC possui uma planilha de cronograma de linha de base que define a produtividade e o previsto para cada trecho. Mensalmente, se a empreiteira encontra condições diferentes do previsto (ex: tipo de solo), sua produtividade é impactada. A planilha calcula automaticamente o ajuste no prazo. Como é uma prerrogativa do contrato FIDC, este ajuste não requer aditivo mensal.

**Sistemas Envolvidos:** ``

> *"Rupturas: Embora o ajuste seja automático e previsto, a prática da execução e o aprendizado com situações novas podem gerar desafios operacionais."*

### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** Durante a execução, a construtora realiza a medição. Itens dentro do 'B de line' são medidos automaticamente, enquanto itens fora geram um pleito. O engenheiro da Motiva valida a medição e o relatório de impacto. Em seguida, a documentação é enviada à certificadora (consórcio que atua para o poder concedente) para análise técnica. Após a validação da certificadora, o poder concedente emite o termo de aceite. Somente com este aceite, um chamado interno é aberto para o processo de pagamento, anexando toda a documentação aprovada.

**Sistemas Envolvidos:** ``

> *"Rupturas: Atraso significativo no processo devido à necessidade de validação externa (certificadora e poder concedente)., Burocracia adicional para justificar pleitos e alterações ao poder concedente, aumentando o tempo de ciclo., Potencial atrito ou divergência entre a análise do engenheiro da Motiva e a certificadora/poder concedente."*

### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** Alterações contratuais, take-offs e pleitos são identificados durante a medição e execução. Para contratos FIDC (Linha 4), ajustes de produtividade e prazo podem ser automáticos via planilha de linha de base. Outros contratos da companhia exigem ajuste e formalização via aditivo. Qualquer alteração significativa ou aditivo requer justificação da causa raiz, não apenas para a Motiva, mas também para o poder concedente (para Linha 4). O objetivo é ter rastreabilidade dessas alterações e suas causas raiz para entender o desempenho do contrato.

**Sistemas Envolvidos:** ``

> *"Rupturas: Falta de rastreabilidade consolidada dos principais aditivos e suas causas raiz para o contrato novo (ainda em fase inicial)., O processo de formalização de aditivos para contratos não-FIDC pode ser demorado e burocrático., A necessidade de justificar detalhadamente para o poder concedente adiciona complexidade e tempo ao processo de gestão de alterações."*

### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** O fluxo inicia com a identificação de um fato gerador e a apresentação do pleito pelo fornecedor. Segue para a análise de mérito, quantidades e preços pela engenharia da concessionária, validação interna e consenso de valor. A formalização do aditivo é então iniciada, e para pleitos relacionados, a aprovação do Poder Concedente é buscada, culminando no processamento do pagamento ou na recusa.

**Sistemas Envolvidos:** ``

> *"Rupturas: Pleitos evitáveis devido a planejamento inicial inadequado ou pressa, Perda de mérito do pleito por atraso na apresentação pelo fornecedor (após 28 dias), Não aprovação do pleito pelo Poder Concedente, mesmo após validação interna, resultando em não pagamento, Falta de um sistema informatizado mais prático para gerenciar o processo"*

### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** Este fluxo abrange a execução de obras sob contratos que combinam preço global e preço unitário. Para as partes de preço unitário, envolve a medição física do executado em campo (take-off) e a subsequente validação dessas medições para fins de faturamento e controle contratual.

**Sistemas Envolvidos:** ``

> *"Rupturas: Imprecisão na medição do executado, Dificuldade na gestão e diferenciação entre as parcelas de preço global e unitário do contrato"*

### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** A empreiteira apresenta a medição, que é analisada por um engenheiro independente. A concessionária recebe a análise, encaminha para certificador e poder concedente para validação. Após aprovação, a área GACNE lança a medição no SAP, cria folha de registro e envia o BM para assinatura do fornecedor. Com o BM assinado, o fornecedor encaminha as notas fiscais, que são aprovadas pela diretoria. Antes do pagamento, é necessária a objeção/termo de aceite do poder concedente. Finalmente, o processo segue para o financeiro para programação de pagamento.

**Sistemas Envolvidos:** ``

> *"Rupturas: Processo moroso devido a múltiplas validações e comunicação via carta/protocolo, Prazo contratual de 56 dias para pagamento é um gargalo, exigindo cobrança constante dos envolvidos, Engenheiro e empreiteira não têm visibilidade direta do certificador e poder concedente, exigindo que a concessionária faça o 'meio de campo', Possibilidade de divergências que precisam ser tratadas em medições futuras, impactando o fluxo"*

### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** Após a entrada dos custos e o acompanhamento do planejamento (Primavera/Project) e custos (SAP), o time de PMO reporta a tendência mensal do empreendimento, analisando a variação do orçamento original versus o realizado. Qualquer divergência do orçado deve ser justificada internamente e também para o poder concedente, com a montagem de reports de avanço e corporativos.

**Sistemas Envolvidos:** ``

> *"Rupturas: A falta de uma plataforma unificada para gestão contratual, planejamento e financeiro dificulta a integração dos dados para a análise de tendência e a geração de relatórios consolidados, A necessidade de justificar divergências para o poder concedente adiciona uma camada de complexidade e tempo ao processo"*

### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** Este fluxo abrange a administração dos contratos com as empreiteiras, incluindo a definição de responsabilidades e o acompanhamento de marcos. Ele é fortemente influenciado pela necessidade de aprovações do poder concedente para diversas etapas e decisões do projeto.

**Sistemas Envolvidos:** ``

> *"Rupturas: O principal ponto de ruptura é a dependência excessiva e o tempo de resposta do poder concedente, que pode atrasar o andamento da obra e forçar a equipe a tomar decisões de risco para evitar multas contratuais."*

### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** Este fluxo detalha as atividades de coleta, revisão e validação dos dados de medição. É um processo com procedimentos bem definidos e envolve a fiscalização de diversas partes para garantir a acurácia e a transparência das informações.

**Sistemas Envolvidos:** ``

> *"Rupturas: O texto não aponta rupturas explícitas, mas a natureza 'delicada' do processo e a necessidade de 'muita gente olhando' indicam que a falta de rigor na validação ou a inconsistência de dados poderiam ser problemas potenciais, embora mitigados pela supervisão atual."*

### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** O fluxo inicia com o recebimento e análise de relatórios mensais da empreiteira (planejamento, riscos, progresso). A equipe interna (Engenharia e Contratos) realiza reuniões semanais, analisa documentações e verifica a aderência às cláusulas contratuais. Pleitos da empreiteira são discutidos internamente e, se aprovados pela Engenharia, são formalizados e apresentados ao certificador e poder concedente. Documentos como RDOs, atas e cartas são gerados e protocolados. A medição e o pagamento dependem da análise e aprovação dos pleitos, com um prazo acordado para resposta do poder concedente.

**Sistemas Envolvidos:** ``

> *"Rupturas: Falta de 'sentimento de dono' da Engenharia em alguns aspectos do processo, exigindo maior intervenção do time de contratos., Divergências internas entre Engenharia e Contratos/Jurídico podem atrasar a tomada de decisão sobre pleitos., Risco de ter que pagar a empreiteira por pleitos que o poder concedente pode não aceitar, para evitar a paralisação da obra., O alto volume de comunicações formais via cartas pode tornar o processo lento e burocrático."*

### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** A empreiteira apresenta um pleito (ex: alteração tributária). O time interno (Engenharia, Consultor Contratos Implantação, Jurídico) discute e analisa o pleito. Se a Engenharia aprovar, o pleito é formalizado e levado ao certificador e poder concedente para análise e aprovação, com a expectativa de resposta antes do pagamento. Se a Engenharia não aprovar, o pleito não avança para o poder concedente, e o empreiteiro pode recorrer ao David (resolução de conflitos).

**Sistemas Envolvidos:** ``

> *"Rupturas: Divergência interna entre Engenharia e time de Contratos/Jurídico, atrasando a decisão sobre o pleito., A não aprovação do pleito pela Engenharia pode escalar para um processo de resolução de conflitos (David)., O prazo de 30 dias para análise de pleitos pode ser insuficiente, impactando o prazo de pagamento de 56 dias., Risco de pagar o empreiteiro por um pleito que o poder concedente não aprove, caso a obra não possa ser paralisada."*

### 🟨 [Processo] Fluxo (Etapa: None)
**Descrição:** Todas as comunicações formais com a empreiteira são realizadas via cartas/avisos, exigindo alta formalização. Similarmente, toda comunicação com o certificador e poder concedente é feita via cartas, com cópia para o poder concedente. O time de administração contratual elabora as minutas das cartas, que são revisadas pelo pessoal de contrato de concessão (com foco no contrato de concessão e aditivos) e protocoladas via CI do poder concedente.

**Sistemas Envolvidos:** ``

> *"Rupturas: O grande volume de cartas (ex: 114 recebidas em 4 meses) indica um processo pesado e potencialmente lento para formalização e resposta., A necessidade de múltiplas análises (time de contratos, pessoal de contrato de concessão) pode atrasar a comunicação formal."*

### 🟦 [Dor] Gargalo (Etapa: Planejamento e Execução)
**Descrição:** A governança interna da Motiva, embora robusta, é percebida como burocrática, introduzindo lentidão e travando processos essenciais para a eficiência dos projetos.

**Sistemas Envolvidos:** ``

> *"como toda empresa grande, a gente tem uma governança muito forte. Acho que acho que junto com governança, a gente não vou falar burocracia, mas a gente tem certas burocracias também que travam um pouco um pouco o processo."*

### 🟦 [Dor] Gargalo (Etapa: Medição)
**Descrição:** O processo de medição das contratadas sofre com a morosidade devido a um handoff manual entre a equipe de engenharia de campo (que analisa) e outra área responsável por operacionalizar a medição no SAP, atrasando o processo de pagamento.

**Sistemas Envolvidos:** `SAP`

> *"A parte de campo, a parte de engenharia que acompanha, faz todo o processo ali, analisa. E a partir disso tem. A gente passa para outro, outra pessoa, outro, outra área que faz a quem que de fato operacionaliza lá no SAP para fazer a medição. [...] tudo isso no processo como um todo isso isso acaba causando uma morosidade ali no no processo de pagamento."*

### 🟦 [Dor] Gargalo (Etapa: Contratação)
**Descrição:** A governança para aprovação de aditivos contratuais é demorada, resultando em atrasos que podem prejudicar o andamento das obras e a relação com fornecedores, especialmente os de menor porte.

**Sistemas Envolvidos:** ``

> *"a gente até para um aditivo hoje por exemplo a gente tem que seguir nossa governança que demora alguns dias né algunsInclusive, se for o caso, isso prejudica olhando para a obra, especificamente para a obra, prejudica, inclusive, o andamento da obra. [...] quanto mais de Moraes para fazer os pagamentos para eles receberem maisMais prejudicado."*

### 🟦 [Dor] ETL Humano (Etapa: Planejamento e Execução)
**Descrição:** Utilização de uma planilha Excel para o 'cronograma de linha de base' que calcula automaticamente ajustes de produtividade e prazo em contratos FIDC. Embora 'automático' dentro da planilha, representa um sistema paralelo e propenso a erros manuais ou falta de integração com sistemas oficiais.

**Sistemas Envolvidos:** `Excel`

> *"a gente tem hoje no contrato uma planilha que chama cronograma de linha de base, trazendo em português, que regra a produtividade e o que ele que ele eventualmente vai encontrar ali em cada trecho e ela já comer que ela tem uma fórmula, ela calcula automático"*

### 🟦 [Dor] Gargalo (Etapa: Contratação)
**Descrição:** Em contratos da companhia que não possuem a prerrogativa do contrato FIDC, os ajustes contratuais precisam ser formalizados manualmente, gerando burocracia e lentidão no processo de atualização e registro.

**Sistemas Envolvidos:** `Processos Manuais/Documentais, SAP`

> *"em outros contatos da companhia da motiva, isso. Precisa ser ajustado. Sim, tá. Então é, a gente tem essa particularidade, que é um contrato Frederico, que tem essa prerrogativa, mas em os contratos que eu já participei, que também a gente precisa ir ajustando e formalizando isso no contrato."*

### 🟦 [Dor] Gargalo (Etapa: Contratação)
**Descrição:** A Linha 4, por ser um contrato com financiamento externo (Poder Concedente), exige múltiplas etapas de anuência e validação (Motiva, Certificadora, Poder Concedente) para emissão de ordens de serviço e medições, resultando em processos mais lentos e burocráticos.

**Sistemas Envolvidos:** `Processos Manuais/Documentais, Teams`

> *"tudo que vem da quatro a gente como é um contrato que poder consciente está pagando a gente precisa ter anuência deles né então se a gente pegar para emissão de uma ordem de serviço né a gente9 ordem de serviço hoje previsto no contrato. Antes de qualquer emissão, a gente precisa ir lá pedindo a objeção do poder concedente. É para o próprio processo de medição. Então o engenheiro valida a medição, a gente valida, precisa ir para a certificadora, que é um braço do poder concedente. Para validar também. E a partir daí, o poder concedente emitir o termo de aceite."*

### 🟦 [Dor] Silo de Informação (Etapa: Planejamento e Execução)
**Descrição:** Falta de rastreabilidade e mapeamento das causas raiz de aditivos e alterações contratuais em contratos recentes, como o da Linha 4, que está em fase inicial. Isso dificulta a gestão proativa e a validação junto ao poder concedente.

**Sistemas Envolvidos:** `Nenhum sistema dedicado`

> *"hoje hoje a gente não tem uma piada porque tá no começo né mas é o objetivo né A ideia que a gente né tenha a gente precisa ter tudo isso uma piada até para validar junto ao poder concedente"*

### 🟦 [Dor] ETL Humano (Etapa: Pagamento)
**Descrição:** Após a aprovação da medição pelo poder concedente, é necessário abrir um chamado interno manualmente, anexando o boletim de medição e todas as evidências de validação, o que pode gerar atrasos e risco de erros na transferência de informações.

**Sistemas Envolvidos:** `Painel de Chamados, SAP FI/AP`

> *"o poder concedente aprovando, a gente tem que abrir um chamado interno e com todo, com a medição aprovada, com os com um boletim de medição e as evidências de validações por todos, inclusive o poder concedente."*

### 🟦 [Dor] Gargalo (Etapa: Planejamento e Execução)
**Descrição:** A pressa na tomada de decisões e a ausência de um sistema informatizado para apoiar o planejamento prévio resultam em caminhos subótimos e pleitos que poderiam ser evitados, impactando a eficiência e os custos dos projetos.

**Sistemas Envolvidos:** `Processos Manuais`

> *"Acho que a pressa, em alguns momentos, acaba fazendo a gente tomar decisões ou seguir por caminhos ali. Não vou falar que é culpa de um ou outro, mas era a decisão que era ser tomada na hora. Então isso acontece sim, acho que. Pode ser que talvez trazendo para o lado de um de um sistema informatizado, algo que seja mais prático, aí acho que ajudaria também."*

### 🟦 [Dor] Gargalo (Etapa: Contratação)
**Descrição:** A análise de mérito, técnica e financeira dos pleitos contratuais é altamente dependente da 'mão de obra' do engenheiro, tornando o processo lento, propenso a erros humanos e ineficiente.

**Sistemas Envolvidos:** `Processos Manuais`

> *"A gente usa meio que a mão de obra do dinheiro para fazer essa análise"*

### 🟦 [Dor] Erro Manual (Etapa: Contratação)
**Descrição:** A validação de preços unitários e a análise das composições apresentadas pelos fornecedores para pleitos é um processo manual, o que pode gerar atrasos, inconsistências e aumentar o risco de erros na precificação.

**Sistemas Envolvidos:** `Processos Manuais`

> *"E os preços unitários, se são preços que já temos hoje no contrato, se são preços novos, eles precisam apresentar as composições para que a gente continue com a análise."*

### 🟦 [Dor] Gargalo (Etapa: Contratação)
**Descrição:** O processo de formalização de aditivos contratuais, após a validação interna e consenso de valores, é descrito como um 'processo interno' que pode ser um ponto de espera e burocracia, atrasando a efetivação das alterações contratuais.

**Sistemas Envolvidos:** `DocuSign, Coupia, SAP`

> *"a gente inicia o processo interno mesmo para formalizar esse aditivo no contrato"*

### 🟦 [Dor] Gargalo (Etapa: Contratação)
**Descrição:** A aprovação final de pleitos relacionados depende da validação do Poder Concedente, adicionando uma etapa externa e burocrática que pode atrasar significativamente o processo e a resposta aos fornecedores.

**Sistemas Envolvidos:** `Processos Manuais`

> *"a gente precisa após a nossa validação na junto com o engenheiro pegar na objeção Priscila Galindo Yan. Paulo Henrique de Almeida Aredes poder concedente para que ele que ele valide Esse preço também então todos os pleitos hoje praticamente todos eles são pretos relacionados né então a gente só só válida né só a prova se o poder concedente aprovar"*

### 🟦 [Dor] Gargalo (Etapa: Contratação)
**Descrição:** Existe o risco de que pleitos aprovados internamente pela Motiva sejam rejeitados pelo Poder Concedente, resultando em retrabalho, perda de tempo e recursos, e impactando a relação com os fornecedores.

**Sistemas Envolvidos:** `Processos Manuais`

> *"Existe a possibilidade do engenheiro e agente aprovar o mérito do pleito, construir todo o pleito e chegar no poder concedente. E ele fala, não, eu não aceito, não concordo com isso."*

### 🟦 [Dor] Gargalo (Etapa: Contratação)
**Descrição:** A gestão dos múltiplos e complexos prazos contratuais para apresentação, análise e aprovação de pleitos é um desafio, com risco de perda de validade dos pleitos se não houver um controle rigoroso e automatizado.

**Sistemas Envolvidos:** `Processos Manuais`

> *"Temos um tempo, vamos olhando o nosso contrato com a empreiteira hoje, então eles, o contrato da FIDC, ele regra muito bem os prazos, então eles têm até 28 Dias do conhecimento do fato que gerou o pleito para apresentar o pleito para a gente."*

### 🟦 [Dor] Gargalo (Etapa: Medição, Pagamento)
**Descrição:** O processo de medição e pagamento é excessivamente moroso, com um prazo contratual de 56 dias para a construtora que é constantemente desafiado pela necessidade de múltiplas análises e aprovações de diversos stakeholders (engenheiro, certificador, poder concedente, diretoria). A equipe precisa realizar um esforço manual de 'cobrança' para garantir o cumprimento dos prazos.

**Sistemas Envolvidos:** `SAP, DocuSign`

> *"Eu acho que o principal gargalo é o prazo que a gente contratualmente para pagar a construtora. A gente tem 56 dias a partir do ano que ela apresenta a medição para gente... A gente tem prazos regrados com todos, mas a gente tem que ficar ali. No sentido cobrando todo mundo para que não fuja do prazo."*

### 🟦 [Dor] Gargalo, Erro Manual (Etapa: Medição)
**Descrição:** A comunicação e o envio de relatórios de análise da medição entre a empreiteira, o engenheiro contratado e a concessionária (Motiva) são realizados 'via carta' e 'protocolado', introduzindo burocracia, lentidão e risco de extravio ou atraso. O engenheiro tem um prazo de 15 dias para sua análise, contribuindo significativamente para o gargalo geral do processo.

**Sistemas Envolvidos:** ``

> *"hoje o maior prazo é do engenheiro que faz análise no detalhe de tudo e emitir um relatório para gente aí tem 15 dias para analisar a partir disso a gente né o tudo via carta né tudo isso é protocolado para ficar formalmente registrado"*

### 🟦 [Dor] ETL Humano, Gargalo (Etapa: Medição, Contratação)
**Descrição:** A Motiva desempenha um papel de intermediário ('meio de campo') entre o engenheiro/empreiteira e o certificador/poder concedente, uma vez que essas partes não se comunicam diretamente. Isso implica em receber análises e repassá-las manualmente, adicionando uma etapa de coordenação que é propensa a atrasos e potenciais erros de comunicação.

**Sistemas Envolvidos:** ``

> *"É o engenheiro e a e a empreiteira é contratualmente. Eles não enxergam o certificador e poder concedente. Então a gente a gente faz esse meio de campo também entre Engenharia e Empreiteira com o certificador e poder concedente. Então a gente recebe a análise da medição do engenheiro e passa para o certificador e poder concedente."*

### 🟦 [Dor] Silo de Informação, Falta Integração (Etapa: Planejamento e Execução, Contratação, Medição)
**Descrição:** Não existe uma plataforma unificada que integre a gestão de contratos, planejamento e finanças. O planejamento é realizado no Primavera, o financeiro no SAP, e a gestão contratual carece de um sistema específico, dependendo de uma pessoa dedicada para acompanhar o contrato de concessão. Essa fragmentação impede uma visão integrada e unificada do projeto.

**Sistemas Envolvidos:** `Primavera, SAP`

> *"Sistemicamente não né então olhando o contato de obra hoje a gente tem um planejamento que é feito no Primavera né o contrato hoje é toda a parte financeira é físico Primavera o financeiro é SAP né é e a gente não tem uma especificamente para gestão contratual a gente não tem uma plataforma que que unifique esses esses dois então hoje e aí para conversar com contrato concedente a gente tem uma pessoa também que é do contrato de concessão que fica é dedicada também para o projetoMas não é algo. Não existe 11 local unificado que a gente consiga fazer tudo isso."*

### 🟦 [Dor] ETL Humano (Etapa: Planejamento e Execução, Contratação, Tendência)
**Descrição:** Uma pessoa dedicada aos contratos de concessão é responsável por acompanhar o planejamento (realizado em sistemas como Primavera/Project) e os custos (registrados no SAP) para, então, montar um relatório sobre o avanço do projeto. Isso implica em uma consolidação manual de dados provenientes de sistemas distintos, aumentando o tempo e o risco de erros.

**Sistemas Envolvidos:** `Primavera, Project, SAP`

> *"Essa pessoa de contratos, ela é contrato de concessão, então ela olha especificamente o nosso contrato de concessão... ela vai, faz o acompanhamento do planejamento e do custo e aí basicamente monta um report para entender como é que tá o avanço disso tudo."*

### 🟦 [Dor] Gargalo (Etapa: Planejamento e Execução)
**Descrição:** A necessidade de aprovação do poder concedente para todas as etapas do projeto gera atrasos significativos, impactando o cronograma da obra e podendo levar a multas contratuais. A equipe é forçada a tomar decisões de risco para evitar paralisações, mesmo sem a aprovação formal.

**Sistemas Envolvidos:** ``

> *"Acho que talvez o maior gargalo de todos é essa interação com o poder concedente, voltando nesse assunto que tudo precisa passar por ele, então."*

### 🟦 [Dor] Silo de Informação (Etapa: Planejamento e Execução)
**Descrição:** Documentos cruciais como fluxos de processo, matrizes de responsabilidade e fluxos de medição são gerenciados e compartilhados manualmente via e-mail, o que pode levar a versões desatualizadas, dificuldade de acesso e falta de uma fonte única da verdade para informações essenciais do projeto.

**Sistemas Envolvidos:** `Email`

> *"Tá eu vou compartilhar com vocês o fluxo, a matriz de responsabilidade que a gente fez e esse fluxo das medições também acho que é legal. ... Mas eu peço, só que você compartilhe por e-mail, porque esse chat aqui eu vou. Eu vou fechar ele justamente para essa, para esse probleminha que está dando de convites, tá. Se você puder compartilhar por e-mail."*

### 🟦 [Dor] ETL Humano (Etapa: Planejamento e Execução)
**Descrição:** A equipe de Contratos de Implantação recebe relatórios mensais de avanço, planejamento e riscos da Engenharia (empreiteira), que são compilados e re-reportados manualmente para análise interna e para o poder concedente. Este processo é propenso a erros e atrasos devido à manipulação manual de dados.

**Sistemas Envolvidos:** `Excel, Sistemas da Empreiteira, BI`

> *"vocês recebem um relatório e vocês provavelmente só pega esse relatório e reporta depois para o poder concedente, o que você, o que vocês estão estão recebendo ali de reporte."*

### 🟦 [Dor] ETL Humano (Etapa: Contratação)
**Descrição:** A comunicação formal entre a Motiva, a empreiteira e o poder concedente é realizada predominantemente via cartas e avisos. Este processo é altamente manual, envolvendo a elaboração de minutas, reunião de informações e protocolo, resultando em um volume expressivo de documentos (centenas em poucos meses) e um 'trabalho braçal'.

**Sistemas Envolvidos:** `DocuSign, CI do poder concedente, Teams, SharePoint`

> *"Hoje a gente tem um número grande de cartas que já que estão para lá e para cá e por conta dessa formalidade do tipo de contrato também. [...] a gente elabora as minutas, faz todo. É esse trabalho braçal. Podemos falar assim, reúne aí tudo e passa para o pessoal de contrato de concessão."*

### 🟦 [Dor] Gargalo (Etapa: Contratação)
**Descrição:** O processo de aprovação de pleitos (ex: alteração tributária) é um gargalo, pois envolve discussões internas entre diferentes áreas da Motiva (Engenharia e Jurídico) que podem ter posicionamentos divergentes. A decisão final só é levada ao poder concedente após consenso interno e aprovação da Engenharia, o que pode gerar atrasos significativos.

**Sistemas Envolvidos:** `Teams, SharePoint`

> *"juridicamente, o nosso escritório tem um posicionamento e o Engenharia não tem outro. A gente tá num numa discussão aí pra pra chegar nesse consenso final."*

### 🟦 [Dor] Erro Manual (Etapa: Planejamento e Execução)
**Descrição:** A equipe de Contratos de Implantação precisa realizar uma validação manual extensiva da análise e documentação fornecida pela Engenharia, verificando a conformidade com o contrato e a execução. Essa necessidade surge, em parte, pela percepção de falta de 'sentimento de dono' da Engenharia em alguns pontos do processo, aumentando o risco de erros e retrabalho.

**Sistemas Envolvidos:** `Excel, Sistemas da Empreiteira, SharePoint`

> *"pedir algumas documentações até para fazer a conferência, se está correto, o que ele está mencionando e tudo mais."*

## 🤝 Mapa de Relações e Stakeholders
- **responde_a**: Paulo Henrique de Almeida Aredes | **Área:** Gerência Executiva de Contratos e Riscos 
  - *Contexto:* Hierarquia direta, Paulo Henrique é alocado ao projeto da Linha 4, mas faz parte da gerência executiva de Emílio.
- **se_relaciona_com**: Paulo Henrique de Almeida Aredes | **Área:** Não citada 
  - *Contexto:* Faz o meio de campo entre o Engenheiro (gestor da obra) e a empreiteira, acompanhando tratativas e reuniões com olhar contratual.
- **se_relaciona_com**: Paulo Henrique de Almeida Aredes | **Área:** Não citada 
  - *Contexto:* Faz o meio de campo entre o Engenheiro (gestor da obra) e a empreiteira, acompanhando tratativas e reuniões com olhar contratual.
- **se_relaciona_com**: Paulo Henrique de Almeida Aredes | **Área:** Artesp 
  - *Contexto:* Atua na tratativa junto ao poder concedente, participando de reuniões para atualização do status da obra.
- **approva**: Não citada | **Área:** Não citada 
  - *Contexto:* O Engenheiro (Consórcio OA...) atua de forma independente, avaliando pleitos e com poder de decisão no contrato FIDIC.
- **fornece_dados_para**: Não citada | **Área:** Área de Engenharia (campo) 
  - *Contexto:* A parte de campo da engenharia faz a análise e o processo de medição das contratadas, fornecendo os dados para a operacionalização no SAP.
- **depende_de**: Não citada | **Área:** Área de Medição/Pagamento (SAP) 
  - *Contexto:* Para operacionalizar a medição e o pagamento no SAP, a área depende dos dados e análises fornecidos pela engenharia de campo.
- **depende_de**: Não citada | **Área:** Não citada 
  - *Contexto:* A governança interna da Motiva, com suas burocracias, causa morosidade nos processos de pagamento e aditivos, impactando o andamento da obra.
- **se_relaciona_com**: Não citada | **Área:** Não citada 
  - *Contexto:* A Motiva se relaciona com fornecedores para a execução de obras, e a morosidade nos pagamentos pode prejudicá-los.
- **se_relaciona_com**: Paulo Henrique de Almeida Aredes | **Área:** Gerência Executiva de Contratos e Riscos 
  - *Contexto:* Paulo Henrique atua na gestão de riscos da construtora, sendo parte integrante da Gerência Executiva de Contratos e Riscos.
- **depende_de**: Não citada | **Área:** Poder Concedente 
  - *Contexto:* Reequilíbrio de condições contratuais (B de line, subsolo) e aprovação de pleitos.
- **se_relaciona_com**: Não citada | **Área:** Construtora 
  - *Contexto:* Pagamento por serviços e ajustes contratuais.
- **se_relaciona_com**: Paulo Henrique de Almeida Aredes | **Área:** Construtora 
  - *Contexto:* Ajuste automático de produtividade e prazo em contrato FIDC.
- **se_relaciona_com**: Paulo Henrique de Almeida Aredes | **Área:** Não citada 
  - *Contexto:* Ajuste e formalização de contratos da Motiva que não são FIDC.
- **depende_de**: Não citada | **Área:** Poder Concedente 
  - *Contexto:* Anuência para emissão de ordem de serviço.
- **fornece_dados_para**: Não citada | **Área:** Engenharia (Motiva) 
  - *Contexto:* Validação inicial da medição da construtora.
- **se_relaciona_com**: Não citada | **Área:** Certificadora 
  - *Contexto:* Envio de medição para validação.
- **depende_de**: Não citada | **Área:** Certificadora 
  - *Contexto:* Validação da medição antes do aceite do Poder Concedente.
- **approva**: Não citada | **Área:** Poder Concedente 
  - *Contexto:* Emissão do termo de aceite da medição.
- **depende_de**: Não citada | **Área:** Certificadora 
  - *Contexto:* Análise técnica das medições e pleitos para o Poder Concedente.
- **fornece_dados_para**: Não citada | **Área:** Engenharia (Motiva) 
  - *Contexto:* Relatório de análise de impacto (prazo/custo) para o certificador.
- **se_relaciona_com**: Não citada | **Área:** Poder Concedente 
  - *Contexto:* Justificativa de causa raiz para aditivos/registros.
- **se_relaciona_com**: Não citada | **Área:** Área de Pagamento/Financeiro (Motiva) 
  - *Contexto:* Abertura de chamado interno para processar pagamento após aprovação do Poder Concedente.
- **depende_de**: Paulo Henrique de Almeida Aredes | **Área:** Engenharia 
  - *Contexto:* Paulo depende da análise técnica e financeira da Engenharia para pleitos contratuais.
- **fornece_dados_para**: Não citada | **Área:** Não citada 
  - *Contexto:* Fornecedores apresentam pleitos detalhados para análise da Engenharia.
- **se_relaciona_com**: Não citada | **Área:** Engenharia 
  - *Contexto:* Engenharia comunica o recebimento e o parecer final dos pleitos aos fornecedores.
- **depende_de**: Não citada | **Área:** Concessionária 
  - *Contexto:* A Concessionária depende da aprovação do Poder Concedente para formalizar aditivos de pleitos relacionados.
- **approva**: Não citada | **Área:** Poder Concedente 
  - *Contexto:* O Poder Concedente aprova os preços e mérito dos pleitos relacionados apresentados pela Concessionária.
- **fornece_dados_para**: Não citada | **Área:** Não citada 
  - *Contexto:* Fornecedores apresentam pleitos iniciais ao Time de Implantação para análise de mérito.
- **fornece_dados_para**: Não citada | **Área:** Implantação 
  - *Contexto:* O Time de Implantação faz a análise inicial de mérito e a repassa para a Engenharia para continuar a análise.
- **approva**: Não citada | **Área:** Concessionária 
  - *Contexto:* A Concessionária (Engenharia e Paulo) aprova o mérito e o valor final dos pleitos antes de submeter ao Poder Concedente ou formalizar.
- **depende_de**: Não citada | **Área:** GACNE (Gestão Administrativa de Contratos) 
  - *Contexto:* Operacionalização de medições e registros no SAP para o processo de pagamento.
- **se_relaciona_com**: Não citada | **Área:** GACNE (Gestão Administrativa de Contratos) 
  - *Contexto:* Obtenção de assinatura do fornecedor no Boletim de Medição (BM).
- **fornece_dados_para**: Não citada | **Área:** Não citada 
  - *Contexto:* Envio de notas fiscais para aprovação da diretoria.
- **approva**: Adriana | **Área:** Diretoria 
  - *Contexto:* Aprovação das notas fiscais encaminhadas pelo fornecedor.
- **se_relaciona_com**: Não citada | **Área:** Financeiro 
  - *Contexto:* Encaminhamento da aprovação para programação de pagamentos.
- **fornece_dados_para**: Não citada | **Área:** PMO (Time de PMO) 
  - *Contexto:* Reporte mensal de tendências e desvios do empreendimento para a equipe de contratos.
- **se_relaciona_com**: Kizzy | **Área:** PMO 
  - *Contexto:* Discussão e análise de tendências versus realizado no contexto CAPEX.
- **se_relaciona_com**: Jean | **Área:** PMO 
  - *Contexto:* Discussão e análise de tendências versus realizado no contexto CAPEX.
- **fornece_dados_para**: Não citada | **Área:** Poder Concedente 
  - *Contexto:* Apresentação de justificativas de divergências do orçado para segunda validação.
- **approva**: Não citada | **Área:** Poder Concedente 
  - *Contexto:* Aprovação do termo de aceite para que a concessionária possa efetuar o pagamento da obra.
- **fornece_dados_para**: Não citada | **Área:** Sistra/Geribelo/GeoCompany 
  - *Contexto:* Análise detalhada e emissão de relatório sobre a medição da empreiteira para a concessionária.
- **fornece_dados_para**: Não citada | **Área:** Não citada 
  - *Contexto:* Apresentação da medição para análise do engenheiro contratado.
- **fornece_dados_para**: Não citada | **Área:** Sistra/Geribelo/GeoCompany 
  - *Contexto:* Encaminhamento da análise da medição com o valor aprovado para a concessionária.
- **fornece_dados_para**: Não citada | **Área:** Certificador 
  - *Contexto:* Encaminhamento da análise da medição para validação do certificador.
- **fornece_dados_para**: Não citada | **Área:** Poder Concedente 
  - *Contexto:* Encaminhamento da análise da medição para validação do poder concedente.
- **depende_de**: Não citada | **Área:** Certificador 
  - *Contexto:* Recebimento da análise da medição da concessionária para revisão e validação.
- **depende_de**: Não citada | **Área:** Poder Concedente 
  - *Contexto:* Recebimento da análise da medição da concessionária para revisão e validação.
- **se_relaciona_com**: Não citada | **Área:** Certificador 
  - *Contexto:* Análise conjunta e discussão de divergências sobre a medição com o Poder Concedente.
- **se_relaciona_com**: Não citada | **Área:** Não citada 
  - *Contexto:* Acompanhamento e discussão de aspectos do contrato de concessão com a equipe de contratos.
- **fornece_dados_para**: Kizzy | **Área:** PMO/Planejamento 
  - *Contexto:* Elaboração e envio de reportes corporativos sobre o projeto CAPEX.
- **fornece_dados_para**: Não citada | **Área:** Sistra/Geribelo/GeoCompany 
  - *Contexto:* Análise de pleitos, identificação de pontos e elaboração de reportes sobre execução, planejamento e custo para a concessionária.
- **se_relaciona_com**: Paulo Henrique de Almeida Aredes | **Área:** Engenharia 
  - *Contexto:* Criação de matriz de responsabilidade para o contrato, junto com o engenheiro.
- **se_relaciona_com**: Paulo Henrique de Almeida Aredes | **Área:** Empreiteira 
  - *Contexto:* Criação de matriz de responsabilidade para o contrato, junto com a empreiteira.
- **depende_de**: Paulo Henrique de Almeida Aredes | **Área:** Poder Concedente 
  - *Contexto:* Todas as decisões e aprovações precisam passar pelo Poder Concedente, gerando gargalos e impactando o andamento da obra.
- **approva**: Não citada | **Área:** Poder Concedente 
  - *Contexto:* Aprova decisões e ações relacionadas ao contrato, com impacto em prazos e multas.
- **se_relaciona_com**: Paulo Henrique de Almeida Aredes | **Área:** Poder Concedente 
  - *Contexto:* Interação para tomada de decisões conjuntas e gestão de riscos relacionados a prazos e multas contratuais.
- **se_relaciona_com**: Paulo Henrique de Almeida Aredes | **Área:** Empreiteira 
  - *Contexto:* Gestão de marcos de penalidade e acompanhamento do contrato.
- **fornece_dados_para**: Não citada | **Área:** Medição 
  - *Contexto:* Geração de dados de medição que são acompanhados por diversas áreas.
- **fornece_dados_para**: Paulo Henrique de Almeida Aredes | **Área:** PMO 
  - *Contexto:* Compartilhamento de fluxos, matriz de responsabilidade e fluxo das medições com a equipe de consultoria.
- **fornece_dados_para**: Não citada | **Área:** Empreiteira 
  - *Contexto:* Geração de relatórios de avanço, custos e status do contrato de obra para a Área de Contratos.
- **se_relaciona_com**: Paulo Henrique de Almeida Aredes | **Área:** Empreiteira 
  - *Contexto:* Agendas semanais e reuniões de gestão para controle de temas contratuais, planejamento e riscos.
- **fornece_dados_para**: Paulo Henrique de Almeida Aredes | **Área:** Poder Concedente 
  - *Contexto:* Reportar informações e relatórios do contrato de obra para o Poder Concedente.
- **depende_de**: Paulo Henrique de Almeida Aredes | **Área:** Engenharia 
  - *Contexto:* Análise do processo contratual, onde a Engenharia faz grande parte do trabalho e fornece informações.
- **depende_de**: Paulo Henrique de Almeida Aredes | **Área:** Engenharia 
  - *Contexto:* Solicitação de documentação para conferência e validação de informações fornecidas pela Engenharia.
- **se_relaciona_com**: Paulo Henrique de Almeida Aredes | **Área:** Engenharia (Consultor de Contratos) 
  - *Contexto:* Apoio na análise de contratos e validação de informações.
- **se_relaciona_com**: Paulo Henrique de Almeida Aredes | **Área:** Engenharia 
  - *Contexto:* Participação ativa nas reuniões de gestão contratual com a empreiteira para identificar e validar análises.
- **se_relaciona_com**: Paulo Henrique de Almeida Aredes | **Área:** Engenharia 
  - *Contexto:* Discussão e busca de consenso sobre pleitos (ex: alteração tributária) e posicionamentos contratuais.
- **depende_de**: Não citada | **Área:** Escritório Jurídico 
  - *Contexto:* Obtenção de posicionamento jurídico para análise e discussão de pleitos.
- **approva**: Não citada | **Área:** Engenharia 
  - *Contexto:* Aprovação interna de pleitos antes de serem apresentados ao Certificador e Poder Concedente.
- **fornece_dados_para**: Paulo Henrique de Almeida Aredes | **Área:** Certificador 
  - *Contexto:* Apresentação de pleitos aprovados e pacotes de documentação.
- **fornece_dados_para**: Paulo Henrique de Almeida Aredes | **Área:** Poder Concedente 
  - *Contexto:* Apresentação de pleitos aprovados e pacotes de documentação.
- **se_relaciona_com**: Não citada | **Área:** David 
  - *Contexto:* Resolução de conflitos em caso de discordância entre Engenharia e Empreiteira sobre pleitos.
- **se_relaciona_com**: Não citada | **Área:** Empreiteira 
  - *Contexto:* Troca formal de documentação como RDO, atas de reunião, não conformidades e cartas.
- **se_relaciona_com**: Não citada | **Área:** Engenharia 
  - *Contexto:* Troca formal de avisos e notificações via cartas.
- **fornece_dados_para**: Paulo Henrique de Almeida Aredes | **Área:** Certificador 
  - *Contexto:* Comunicação formal e envio de cópias de cartas para o Certificador.
- **fornece_dados_para**: Paulo Henrique de Almeida Aredes | **Área:** Poder Concedente 
  - *Contexto:* Comunicação formal e envio de cópias de cartas para o Poder Concedente.
- **fornece_dados_para**: Paulo Henrique de Almeida Aredes | **Área:** Pessoal de Contrato de Concessão 
  - *Contexto:* Elaboração de minutas e documentação para análise e protocolo relacionados ao contrato de concessão.
- **se_relaciona_com**: Não citada | **Área:** Engenharia 
  - *Contexto:* Colaboração na definição do fluxo de análise e resposta de pleitos antes do pagamento.
- **se_relaciona_com**: Não citada | **Área:** Certificador 
  - *Contexto:* Colaboração na definição do fluxo de análise e resposta de pleitos antes do pagamento.
- **se_relaciona_com**: Não citada | **Área:** Poder Concedente 
  - *Contexto:* Colaboração na definição do fluxo de análise e resposta de pleitos antes do pagamento.
- **se_relaciona_com**: Não citada | **Área:** Equipe de Planejamento (Motiva) 
  - *Contexto:* Agendas semanais recorrentes para tratar temas de planejamento e controle.

---
*Relatório gerado pelo Pipeline Sênior MOTIVA | Veron Consultoria.*
