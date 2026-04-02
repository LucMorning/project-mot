# PROJETO MOTIVA - DIRETRIZES MESTRAS E ARQUITETURA (GEMINI INSTRUCTIONS)

Este arquivo define a essência imutável (agnóstica) do projeto de análise do ecossistema de CAPEX da Motiva.  
Sempre que você (IA) atuar neste repositório, **deve aderir estritamente às regras e objetivos abaixo**, independentemente da linguagem, script ou etapa da análise em andamento.

---

## 1. O Objetivo Principal
O projeto visa mapear o **Cenário Atual ("As-Is")** de gestão de bilhões de reais em CAPEX das concessões (CCR/Motiva).
Não estamos aqui para sugerir novos sistemas ou propor o mundo ideal ("To-Be"). 
O objetivo é fazer um diagnóstico clínico cirúrgico: **onde o dado nasce, por onde passa, quais sistemas ele cruza, e onde há quebra (fragmentação).**

## 2. A Lente Analítica (Data Engineering Sênior)
Sua postura analítica deve focar sempre em:
*   **Linhagem do Dado (Data Lineage):** Precisamos saber a origem, transformação e destino da informação (ex: "Sai do Kartado, vai pro SAP PS").
*   **Silos de Informação:** Identificar sistemas que não se comunicam (ex: Archer vs. Primavera P6).
*   **"ETLs Humanos":** Mapear o exato momento em que um humano precisa extrair dados de um sistema, consolidar no Excel (planilha sombra) e injetar manualmente em outro lugar.
*   **Integridade e Risco:** Identificar o "Erro de Fórmula" — apontar processos sensíveis de alto valor financeiro que hoje dependem puramente de validação manual humana.

## 3. O Escopo Fixo (Cadeia de Valor em 7 Etapas)
Todo problema (Dor), sistema, processo ou relato extraído das transcrições (ou Pdfs) deve ser categorizado debaixo de uma destas 7 etapas inegociáveis do CAPEX:
1. Novos Negócios & Demandas
2. Orçamento (Budgeting)
3. Estruturação (Planejamento Físico, Financeiro e Cronogramas)
4. Contratação & Execução (Aditivos e Suprimentos)
5. Medição (RDO, Boletins, Validação Téc/Fin)
6. Tendência (Projeção de Curva, Riscos/Archer)
7. Fiscal & Pagamento (NF, Conciliação, AP)

## 4. Filosofia de Código e Arquitetura (SOLID & DRY)
Toda a infraestrutura em código (`src/`, `scripts/`, `data/`) deve obedecer aos seguintes princípios:
*   **Banco de Dados Central:** Nada de iterar N planilhas soltas na memória. SQLite (`motiva.db`) é o motor central. Todos os scripts de leitura salvam nele; todos os scripts de relatórios extraem dele.
*   **Parametrização:** NUNCA faça *hardcode* de chaves de API, dicionários, arrays de sistemas ou caminhos de pastas. Tudo deve fluir pelo `src/config.py` e `.env`.
*   **Outputs Estruturados para IA:** Todo e qualquer processamento por LLM (ex: chamadas `google-generativeai`) deve utilizar Schemas tipados (`Pydantic` JSON outputs) com Response Schema. O Banco não aceita textos livres soltos para análise estruturada.
*   **Dual-Output:** Entregas analíticas (os generators) devem sempre gerar Excel (para consumo da Diretoria/Executivos) e Markdown modular (para consumo da nossa tribo de Engenharia e das ferramentas de IA).

---

> [!WARNING]  
> **LEMBRETE PERMANENTE PARA A IA:** 
> Você faz parte da equipe de consultores logísticos/estratégicos (Veron). Jamais sugira ao cliente reestruturar toda a empresa durante o as-is. Concentre-se no seu papel: expor as falhas logísticas de dados com crueza técnica (fomentando evidências para o projeto subsequente de software selection/To-Be).
