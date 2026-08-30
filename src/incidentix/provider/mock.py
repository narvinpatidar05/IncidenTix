"""Mock log and metric providers returning realistic sample data for testing."""

from datetime import datetime, timedelta

from .models import LogRecord, MetricPoint, MetricRecord


class MockLogProvider:
    """Fake provider — no real vendor call, returns realistic sample data."""

    def fetch_logs(
        self, service: str, query: str, minutes_back: int
    ) -> list[LogRecord]:
        """Return two hardcoded ERROR log records for the given service."""
        now = datetime.now()
        return [
            LogRecord(
                timestamp=now - timedelta(minutes=5),
                severity="ERROR",
                body=f"Connection timeout to {service}",
                resource={"service": service},
                attributes={"request_id": "abc123"},
            ),
            LogRecord(
                timestamp=now - timedelta(minutes=3),
                severity="ERROR",
                body=f"DB pool exhausted for {service}",
                resource={"service": service},
                attributes={"request_id": "def456"},
            ),
        ]


class MockMetricProvider:
    """Fake provider for metrics — returns a series with a visible spike."""

    def fetch_metrics(self, query: str, minutes_back: int) -> MetricRecord:
        """Return a hardcoded metric series with a visible spike on the last point."""
        now = datetime.now()
        return MetricRecord(
            metric_name=query,
            unit="percent",
            resource={},
            points=[
                MetricPoint(timestamp=now - timedelta(minutes=10), value=2.0),
                MetricPoint(timestamp=now - timedelta(minutes=5), value=3.0),
                MetricPoint(timestamp=now - timedelta(minutes=1), value=45.0),  # spike
            ],
        )
