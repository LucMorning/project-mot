# Dicionário de Dados: MOTIVA CAPEX (SQLite)

Este documento descreve as tabelas utilizadas no `motiva.db`. **Importante:** Cada tabela possui campos de tracking para permitir consultas sobre o progresso e o status da análise.

## 1. `entrevistados`
Armazena a visão macro da lista de entrevistas (planilha `lista_entrevistas.xlsx`).
* `id`: Chave primária.
* `nome`: Nome do entrevistado.
* `cargo`, `diretoria`, `plataforma`, `area`, `nivel`: Dados organizacionais originais.
* `data_entrevista`, `tipo_entrevista`: Data e contexto ("Coleta de Dados", "Aprofundamento").
* `arquivo_transcricao`: Nome do arquivo Word (em snake_case, ex: `entrevista_as_is_flavio.docx`).
* `arquivo_cargo_pdf`: Link pro documento de especificação de cargo se existir.
* **Tracking Fields**:
  * `status_revisao`: 'pendente', 'em_progresso', 'concluida', 'erro'. Útil pra IA saber quem falta analisar.
  * `notas_revisor`: Anotações ou logs de erro durante processamento.
  * `data_revisao`: Timestamp de quando a análise via IA foi efetuada.

## 2. `transcricoes`
Armazena o texto bruto processado do MS Word (`.docx`).
* `id`, `entrevistado_id` (FK)
* `texto_completo`: Transcript full.
* `num_paragrafos`, `num_caracteres`: Metadados extraídos pra fins de volume.

## 3. `cargos`
Armazena informações dos arquivos PDF com descrições de cargo oficiais das áreas.
* `id`: PK.
* `titulo_cargo`, `arquivo_pdf`: Arquivo origem.
* `texto_extraido`: O conteúdo OCR/textual do PDF.
* **Insights**: `responsabilidades`, `competencias`, `area_atuacao`.

## 4. `insights_ia`
Tabela fundamental contendo todos os achados da IA.
* `id`, `entrevistado_id` (FK).
* `etapa_cadeia_valor`: Etapa (das 7) impactada. Ex: "5. Medição".
* `categoria`: "Dor", "Processo", "Risco", "ETL Humano", "Insight Entrelinhas".
* `subcategoria`: Detalhamento. 
* `descricao`: Descrição detalhada via IA.
* `citacao_direta`: Quote da entrevista confirmando a descrição.
* `sistemas_envolvidos`: Array JSON dos sistemas (SAP, Archer, etc).
* `severidade`: 'Alta', 'Média', 'Baixa'.
* `confianca`, `modelo_ia`: Metadados da chamada LLM.

## 5. `relacoes`
Para construir o grafo hierárquico e de informação.
* `id`, `entrevistado_id` (FK).
* `tipo`: "responde_a", "se_relaciona_com", "depende_de".
* `pessoa_ou_area`: Nome do stakeholder.
* `contexto`: Descrição rápida.

## 6. `sistemas_uso`
Tabela 1:N entre o entrevistado e o ecossistema tecnológico.
* `id`, `entrevistado_id` (FK).
* `sistema`: Nom de (ex: "SAP PS").
* `como_usa`: Fluxo.
* `etapa_cadeia`: Vinculado a uma daquelas 7 etapas do CAPEX.
* `satisfacao`: 'Positivo', 'Neutro', 'Negativo'.
* `workaround`: Existe processo paralelo? (A "sombra").

## Como extrair o progresso via IA:
Pode usar a seguinte query local:
```sql
SELECT status_revisao, count(*) as total 
FROM entrevistados 
GROUP BY status_revisao;
```
