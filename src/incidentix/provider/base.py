"""Provider protocol interfaces for log and metric vendor adapters."""

from typing import Protocol

from .models import LogRecord, MetricRecord


class LogProvider(Protocol):
    """Contract every log-vendor adapter must implement.

    Examples: Loki, Datadog, CloudWatch.
    """

    def fetch_logs(
        self, service: str, query: str, minutes_back: int
    ) -> list[LogRecord]:
        """Fetch log records for a service matching a query within a time window."""
        ...


class MetricProvider(Protocol):
    """Contract every metric-vendor adapter must implement.

    Examples: Prometheus, Datadog.
    """

    def fetch_metrics(self, query: str, minutes_back: int) -> MetricRecord:
        """Fetch a metric record matching a query within a time window."""
        ...
