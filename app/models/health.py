from dataclasses import dataclass


@dataclass(frozen=True)
class HealthCheck:
    status: str
    service: str
    environment: str
    version: str
