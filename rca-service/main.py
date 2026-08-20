from fastapi import FastAPI

app = FastAPI(
    title="incidenTix",
    description="AI-powered incident root-cause-analysis (RCA) service",
    version="0.1.0",
)


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "incidenTix", "status": "ok"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}
