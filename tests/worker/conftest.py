"""Worker test setup. API key must exist before worker.config is imported."""

import os

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
