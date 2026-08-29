"""Registry for choosing the right adapter per tenant."""

from .base import LogProvider, MetricProvider
from .mock import MockLogProvider, MockMetricProvider

LOG_PROVIDERS: dict[str, type] = {
    "mock": MockLogProvider,
}

METRIC_PROVIDERS: dict[str, type] = {
    "mock": MockMetricProvider,
    # "prometheus": PrometheusMetricProvider,  (future)
}


def get_log_provider(provider_name: str, **config) -> LogProvider:
    """Instantiate the registered LogProvider matching provider_name."""
    provider_cls = LOG_PROVIDERS.get(provider_name)
    if not provider_cls:
        raise ValueError(f"Unknown log provider: {provider_name}")
    return provider_cls(**config)


def get_metric_provider(provider_name: str, **config) -> MetricProvider:
    """Instantiate the registered MetricProvider matching provider_name."""
    provider_cls = METRIC_PROVIDERS.get(provider_name)
    if not provider_cls:
        raise ValueError(f"Unknown metric provider: {provider_name}")
    return provider_cls(**config)
