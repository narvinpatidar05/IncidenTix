"""FastAPI application entrypoint."""

from fastapi import FastAPI

app = FastAPI(
    title="IncidenTix",
    description="AI-powered incident investigation and RCA agent",
)


@app.get("/health")
async def health():
    """Return the health status of the application."""
    return {"status": "ok"}
