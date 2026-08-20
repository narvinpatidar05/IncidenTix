# incidenTix

AI-powered incident root-cause-analysis (RCA) agent — investigates production alerts using an agentic tool-use loop (logs, metrics, deploy history) and produces structured root-cause findings.

This project is in early development. The current focus is an RCA-service-first approach: data ingestion, webhooks, and multi-tenant onboarding come later.

## Run the RCA service

```bash
cd rca-service
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

- API: http://127.0.0.1:8000
- Health: http://127.0.0.1:8000/health
- Docs: http://127.0.0.1:8000/docs
