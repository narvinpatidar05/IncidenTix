from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(examples=["healthy"])
    service: str
    environment: str
    version: str
