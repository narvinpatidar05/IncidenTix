"""Tests for provider/models.py domain models."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from incidentix.provider.models import LogRecord, MetricPoint, MetricRecord

# ---------- LogRecord ----------


def test_log_record_valid_minimal():
    """Should create with only required fields; dict fields default to empty."""
    log = LogRecord(
        timestamp=datetime.now(UTC),
        severity="ERROR",
        body="Payment gateway timeout",
    )
    assert log.severity == "ERROR"
    assert log.body == "Payment gateway timeout"
    assert log.resource == {}
    assert log.attributes == {}


def test_log_record_valid_full():
    """Should accept resource and attributes dicts."""
    log = LogRecord(
        timestamp=datetime.now(UTC),
        severity="WARN",
        body="High latency detected",
        resource={"service": "payment-api"},
        attributes={"request_id": "abc-123"},
    )
    assert log.resource == {"service": "payment-api"}
    assert log.attributes == {"request_id": "abc-123"}


@pytest.mark.parametrize("missing_field", ["timestamp", "severity", "body"])
def test_log_record_missing_required_field_raises(missing_field):
    """Should raise ValidationError when a required field is missing."""
    data = {
        "timestamp": datetime.now(UTC),
        "severity": "INFO",
        "body": "test message",
    }
    data.pop(missing_field)
    with pytest.raises(ValidationError):
        LogRecord(**data)


def test_log_record_invalid_timestamp_type_raises():
    """Should raise ValidationError for a non-parseable timestamp."""
    with pytest.raises(ValidationError):
        LogRecord(timestamp="not-a-date", severity="INFO", body="test")


# ---------- MetricPoint ----------


def test_metric_point_valid():
    point = MetricPoint(timestamp=datetime.now(UTC), value=42.5)
    assert point.value == 42.5


def test_metric_point_value_must_be_float_coercible():
    """Pydantic coerces numeric strings; non-numeric should fail."""
    with pytest.raises(ValidationError):
        MetricPoint(timestamp=datetime.now(UTC), value="not-a-number")


# ---------- MetricRecord ----------


def test_metric_record_valid_minimal():
    """unit and resource should default when omitted."""
    record = MetricRecord(
        metric_name="http_error_rate",
        points=[MetricPoint(timestamp=datetime.now(UTC), value=1.0)],
    )
    assert record.unit is None
    assert record.resource == {}
    assert len(record.points) == 1


def test_metric_record_valid_full():
    ts = datetime.now(UTC)
    record = MetricRecord(
        metric_name="http_error_rate",
        unit="percent",
        resource={"service": "payment-api"},
        points=[
            MetricPoint(timestamp=ts, value=1.0),
            MetricPoint(timestamp=ts, value=2.5),
        ],
    )
    assert record.unit == "percent"
    assert len(record.points) == 2
    assert record.points[1].value == 2.5


def test_metric_record_accepts_raw_dict_points():
    """MetricRecord should coerce list[dict] into list[MetricPoint]."""
    record = MetricRecord(
        metric_name="cpu_usage",
        points=[{"timestamp": datetime.now(UTC), "value": 88.2}],
    )
    assert isinstance(record.points[0], MetricPoint)
    assert record.points[0].value == 88.2


def test_metric_record_missing_metric_name_raises():
    with pytest.raises(ValidationError):
        MetricRecord(points=[])


def test_metric_record_invalid_point_in_list_raises():
    """A malformed point dict inside points should fail validation."""
    with pytest.raises(ValidationError):
        MetricRecord(
            metric_name="cpu_usage",
            points=[{"timestamp": datetime.now(UTC)}],  # missing 'value'
        )
