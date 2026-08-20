from dataclasses import dataclass


@dataclass(frozen=True)
class ServiceInfo:
    service: str
    status: str
    environment: str
    version: str
    api_v1_prefix: str
