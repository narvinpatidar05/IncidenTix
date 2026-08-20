from fastapi import FastAPI

from app.api.investigations import router as investigations_router

app = FastAPI(
    title="incidenTix",
    description="AI-powered incident root-cause-analysis (RCA) agent",
    version="0.1.0",
)

app.include_router(investigations_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
