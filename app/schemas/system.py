from pydantic import BaseModel, Field


class ServiceInfoResponse(BaseModel):
    service: str
    status: str = Field(examples=["ok"])
    environment: str
    version: str
    api_v1_prefix: str
