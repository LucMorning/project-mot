# Contexto de Continuação (Handoff) - Projeto MOTIVA

> **LEIA ISSO PRIMEIRO NO NOVO CHAT:** Este documento consolida o estado da arte do projeto de Diagnóstico Estratégico "As-Is" do núcleo de CAPEX da Motiva. Leia este arquivo na íntegra para absorver todo o contexto.

---

## 1. O Problema e o Contexto de Negócio
A **Veron** (consultoria estratégica da qual fazemos parte) está diagnosticando o núcleo de **CAPEX** da **Motiva/CCR** (projetos de bilhões de reais como Serra das Araras e concessões de pedágio/trilhos). O diagnóstico atual é focado **100% no "As-Is"** (como as coisas funcionam hoje, suas deficiências e processos atuais, *sem propor o "To-Be"* ainda).

Nossa lente é de **Data Engineering Sênior**: queremos rastrear a **Linhagem do Dado (Data Lineage)**, medir a **Fragmentação de Sistemas** (SAP, Archer, P6, Kartado, etc.) e mapear a fundo os chamados **"ETLs Humanos"** (pessoas extraindo relatórios de um sistema X, colando em planilhas Excel "sombra" e subindo em outro sistema Y porque eles não se falam). Toda a análise macro obedece a **Cadeia de Valor do CAPEX (7 etapas: Demandas, Orçamento, Estruturação, Contratação, Medição, Tendência e Fiscal/Pagamento)**.

## 2. A Arquitetura do Repositório (O que construímos)
Nós herdamos diversos arquivos brutos soltos e reestruturamos o projeto inteiro aplicando **SOLID, DRY** e transformando-o num verdadeiro *pipeline* escalável focado em IA e Analytics. Hoje a árvore de diretórios oficial é:

```
MOTIVA/
├── venv/                       # Ambiente virtual (libs: pdfplumber, pydantic, google-generativeai, etc)
├── data/
│   ├── raw/                    # Planilha mestre: lista_entrevistas.xlsx
│   ├── transcricoes/           # 68 transcrições originais docx limpas e renomeadas em snake_case
│   ├── cargos/                 # 63 KPIs/Descrições oficiais de Cargo em PDF copiados da holding
│   └── output/                 
│       └── motiva.db           # Banco de dados SQLite contendo todo o state e raw data
├── src/
│   ├── config.py               # Todos os paths absolutos, strings, regras base e 25+ sistemas
│   ├── utils/                  # matching.py, file_readers.py, etc
│   ├── database/               # schema.py estruturado com types
│   ├── pipelines/              # Os executáveis que engolem docs brutos e enviam pra IA
│   └── generators/             # (Pendente) Scripts que lerão o BD para cuspir os reports finais
└── scripts/
    ├── rename_files.py         # Arquivo que padronizou a bagunça antiga
    └── move_old_files.py       # (Pendente) Script p/ mandar o legacy para _old/ ao fim
```

## 3. Estrutura do Banco de Dados (`motiva.db`)
Fugindo de scripts lentos que iteram Excel, tudo está centralizado no `motiva.db`. Tabelas e relacionamentos principais:
1. `entrevistados`: A lista dos 69 indivíduos (Controles/Tracking de status da IA em cada).
2. `transcricoes`: Onde fizemos OCR/Parse dos arquivos .docx originais de cada um.
3. `cargos`: Aqui os PDFs de cargos já viraram longtext e metadados.
4. `insights_ia`: Schema JSON Pydantic gerado nativamente pelo Gemini (a IA grava a dor encontrada, cita a etapa do funil do CAPEX, nomeia o problema, lista `sistemas_envolvidos` e captura uma `citacao_direta` das aspas originais atestando aquilo).
5. `sistemas_uso`: Cadastro de quais ferramentas o sujeito declarou usar + nível de satisfação.
6. `relacoes`: Mapa de quem responde estruturalmente acima/abaixo dele para gráfico de stakeholder.

## 4. Onde paramos cronologicamente (O seu "Continue Daqui")
Já rodamos os extratores burros e os parsers:
- **`ingest_metadata_from_excel.py`** ✅ (Carregou Planilha pro BD)
- **`extract_docx_transcripts.py`** ✅ (Parseou DOCXs)
- **`extract_pdf_roles.py`** ✅ (Extraiu PDF Plumber)

Já escrevemos O Pipeline de Inteligência:
- **`run_ai_diagnostic.py`** ⏳ *(Pronto, mas não foi disparado o PLAY)*
O Script `run_ai_diagnostic.py` implementa `google-generativeai` (Gemini SDK) puro, injetando Schema JSON (Structured Output). Ele junta o "texto extraído do cargo do PDF" com a "transcrição do jeito que fulano fala" num só prompt pra forçar a inteligência de analisar desvios de função. O script processa de 5 em 5 para evitar rate limit.

## 5. Excesso Próximos Passos Inegociáveis (A sua Missão)

1. **Ativar o Cérebro AI (`run_ai_diagnostic.py`):** 
   Crie um `.env` na raiz colocando a `GEMINI_API_KEY`. Rode `python src/pipelines/run_ai_diagnostic.py`. Veja os metadados fluírem para o BD mágico. Certifique-se que as "aspas diretas" das dores e os "ETLs Humanos" mapeados fazem sentido nas tabelas. 

2. **Implementar o "Bloco 6" (Relatórios Ouro):**
   Com o BD repleto de inteligência analítica de 68 humanos de alto nível, os próximos códigos devem extrair respostas prontas e visuais:
   - `src/generators/xlsx_report.py`: Pivot tables geradas mapeando todas as dores classificadas contra todos os 25 sistemas da infraestrutura da CCR/Motiva + Resumo Executivo. A Diretoria pediu esse arquivo.
   - `src/generators/md_context.py`: Loop SQL exportando uma documentação `.md` individual "Ficha Técnica do Fulano", bonitão (pra consumo das IAs internas e nosso alinhamento humano).
   - `src/generators/pptx_builder.py`: Refazer a "Cadeia de Valor do As-Is" nos 7 slides originais do projeto de forma programática.

3. **Arquivamento Final:** 
   Confirmada a saúde das tabelas e reports gerados, chame `scripts/move_old_files.py` para defenestrar as planilhas da raiz para a lixeira rica `_old/`.
