# Tests - Suíte de Testes

Testes unitários e de integração para validar componentes do pipeline.

## Arquivos

### Testes Unitários

| Teste | Descrição |
|-------|-----------|
| `test_schemas.py` | Valida todos os Pydantic schemas |
| `test_chunking.py` | Testa divisão de transcrições longas |
| `test_etapa1.py` | Testa análise macro (Etapa 1) local |
| `test_db_service.py` | Testa salvamento no banco |
| `test_integracao.py` | Teste completo end-to-end do pipeline |

### Testes de API

| Teste | Descrição |
|-------|-----------|
| `test_gemini_api.py` | Testa conexão e structured output da API Gemini |

## Como Executar

```bash
# Teste individual
python tests/test_schemas.py

# Teste completo (valida pipeline funcionando)
python tests/test_integracao.py
```

## Dados de Teste

- `trans_teste_grande.txt` - Transcrição grande (354k chars) para testar chunking

## Convenções

- Testes usam ID `999` para dados de teste (limpo após execução)
- Sempre removem dados de teste do banco após conclusão
- Nomeclatura: `test_<modulo>.py` ou `test_<funcionalidade>.py`
