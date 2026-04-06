# MOTIVA - CAPEX Analysis Pipeline

Automated diagnostic report generation using AI agents for MOTIVA CAPEX analysis.

## Installation

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Enter the virtual environment
poetry shell
```

## Available Scripts

### Ingestion (Stage 1)

```bash
# Complete ingestion workflow (all 6 steps)
poetry run ingest

# Individual steps
poetry run ingest-metadata      # Excel → stg_entrevistados
poetry run extract-roles         # PDFs → stg_cargos
poetry run extract-transcripts   # DOCX → stg_transcricoes
poetry run create-chunks         # Transcriptions → stg_chunks
poetry run ingest-systems        # Catalog → dim_sistemas
poetry run link-roles            # Link cargo ↔ pessoa
poetry run deduplicate           # Remove duplicate interviewees
```

### AI Analysis (Stage 2)

```bash
# Run AI analysis (default: batch mode)
poetry run analyze

# Staged mode (3 stages: macro → multi-agent → cross-validation)
poetry run analyze --mode staged

# Batch mode with max rounds limit
poetry run analyze --mode batch --max-rounds 10

# Direct batch execution
poetry run analyze-batch

# Direct staged execution
poetry run analyze-staged
```

### Reports (Stage 3)

```bash
# Generate markdown reports
poetry run reports

# Generate markdown reports (explicit)
poetry run reports --format markdown

# Generate PowerPoint reports (coming soon)
poetry run reports --format pptx

# Direct markdown generation
poetry run generate-markdown
```

## Project Structure

```
motiva/
├── src/
│   ├── agents/           # AI agents for analysis
│   ├── config.py         # Central configuration
│   ├── database/         # Database schema & repositories
│   ├── pipelines/        # Analysis pipelines
│   ├── providers/        # LLM providers (Gemini, OpenAI, etc)
│   ├── utils/            # Utilities (chunking, parsing, etc)
│   └── workflows/        # Main workflows
│       ├── ingest/       # Ingestion pipelines
│       ├── analyze/      # AI analysis pipelines
│       └── generate/     # Report generation
├── data/
│   ├── raw/              # Input files (Excel, PDFs, DOCX)
│   └── output/           # Database and generated reports
├── pyproject.toml        # Poetry configuration
└── README.md
```

## Environment Variables

Create a `.env` file in the project root:

```env
# Gemini API (required for AI analysis)
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.0-flash-exp

# Pipeline settings (optional)
BATCH_SIZE=3
BATCH_INTERVIEWEES=5
BATCH_SLEEP=10
BATCH_ERROR_THRESHOLD=5
```

## Development

```bash
# Run tests
poetry run pytest

# Code formatting
poetry run black .
poetry run ruff check .

# Type checking
poetry run mypy src/
```

## License

MIT
