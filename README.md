# incidenTix

AI-powered incident root-cause-analysis (RCA) agent — investigates production alerts using an agentic tool-use loop (logs, metrics, deploy history) and produces structured root-cause findings.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Health: http://127.0.0.1:8000/health
- Versioned health: http://127.0.0.1:8000/api/v1/health
- Docs: http://127.0.0.1:8000/docs

```bash
pytest
```

## Layout

Request flow: **route → controller → service → repository**.

```
app/
├── main.py                 # FastAPI app factory
├── api/v1/
│   ├── routes/             # HTTP paths only
│   └── controllers/        # request/response mapping
├── services/               # business logic
├── repositories/           # data access (DB/queue later)
├── models/                 # domain objects
├── schemas/                # Pydantic API contracts
├── core/                   # config, constants, logging, errors
└── utils/
tests/
```
