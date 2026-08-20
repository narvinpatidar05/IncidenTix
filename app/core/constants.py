SERVICE_NAME = "incidenTix"
SERVICE_SLUG = "incidentix-rca"

API_V1_PREFIX = "/api/v1"

ROOT_PATH = "/"
HEALTH_PATH = "/health"


class HealthStatus:
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class AppEnv:
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
