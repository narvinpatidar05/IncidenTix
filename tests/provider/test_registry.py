"""Tests for the provider registry and its factory functions."""

import pytest

from incidentix.provider.mock import MockLogProvider, MockMetricProvider
from incidentix.provider.registry import get_log_provider, get_metric_provider


class TestGetLogProvider:
    def test_returns_mock_log_provider_instance(self):
        provider = get_log_provider("mock")

        assert isinstance(provider, MockLogProvider)

    def test_raises_value_error_for_unknown_provider(self):
        with pytest.raises(ValueError, match="Unknown log provider: bogus"):
            get_log_provider("bogus")

    def test_forwards_config_kwargs_to_constructor(self, monkeypatch):
        received_kwargs = {}

        class FakeConfigurableProvider:
            def __init__(self, **kwargs):
                received_kwargs.update(kwargs)

        monkeypatch.setitem(
            __import__(
                "incidentix.provider.registry", fromlist=["LOG_PROVIDERS"]
            ).LOG_PROVIDERS,
            "fake",
            FakeConfigurableProvider,
        )

        get_log_provider("fake", region="us-east-1", timeout=30)

        assert received_kwargs == {"region": "us-east-1", "timeout": 30}


class TestGetMetricProvider:
    def test_returns_mock_metric_provider_instance(self):
        provider = get_metric_provider("mock")

        assert isinstance(provider, MockMetricProvider)

    def test_raises_value_error_for_unknown_provider(self):
        with pytest.raises(ValueError, match="Unknown metric provider: bogus"):
            get_metric_provider("bogus")

    def test_forwards_config_kwargs_to_constructor(self, monkeypatch):
        received_kwargs = {}

        class FakeConfigurableProvider:
            def __init__(self, **kwargs):
                received_kwargs.update(kwargs)

        monkeypatch.setitem(
            __import__(
                "incidentix.provider.registry", fromlist=["METRIC_PROVIDERS"]
            ).METRIC_PROVIDERS,
            "fake",
            FakeConfigurableProvider,
        )

        get_metric_provider("fake", region="us-east-1", timeout=30)

        assert received_kwargs == {"region": "us-east-1", "timeout": 30}
