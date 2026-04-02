# Scripts - Utilitários para Desenvolvedor

Scripts de suporte para desenvolvimento, manutenção e operações one-shot.

## Arquivos

### Limpeza e Manutenção

| Script | Descrição |
|--------|-----------|
| `clean_transcripts.py` | Limpeza e normalização de transcrições |
| `rename_files.py` | Renomeação em lote de arquivos de transcrição |
| `move_old_files.py` | Move arquivos antigos para estrutura atualizada |

### Mapeamento e QA

| Script | Descrição |
|--------|-----------|
| `map_sistemas_ti.py` | Mapeamento manual de sistemas de TI |
| `qa_integrity_check.py` | Verificação de integridade dos dados |

## Convenções

- Scripts aqui são **one-shot** ou utilitários de desenvolvimento
- Não fazem parte do pipeline ETL principal (veja `src/pipelines/`)
- Podem ser executados diretamente: `python scripts/<script>.py`

## Scripts Removidos (Legado)

Os seguintes scripts foram removidos pois usavam abordagem antiga de chunking no banco:
- `chunk_transcripts.py` - Substituído por `src/utils/chunking.py`
- `process_ia_chunks.py` - Substituído por `src/pipelines/run_ai_diagnostic.py`
