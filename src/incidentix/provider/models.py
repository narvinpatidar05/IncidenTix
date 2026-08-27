"""Provider domain models."""

from datetime import datetime

from pydantic import BaseModel, Field


class LogRecord(BaseModel):
    """Normalized log entry — every vendor adapter must produce this shape."""

    timestamp: datetime
    severity: str  # OTel-style: TRACE/DEBUG/INFO/WARN/ERROR/FATAL
    body: str  # the actual log message
    resource: dict = Field(default_factory=dict)  # e.g. {"service": "payment-api"}
    attributes: dict = Field(default_factory=dict)  # extra key-value context


class MetricPoint(BaseModel):
    """A single timestamped value in a metric series."""

    timestamp: datetime
    value: float


class MetricRecord(BaseModel):
    """Normalized metric series — every vendor adapter must produce this shape."""

    metric_name: str  # e.g. "http_error_rate"
    unit: str | None = None  # e.g. "percent", "ms"
    resource: dict = Field(default_factory=dict)
    points: list[MetricPoint]
