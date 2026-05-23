import os
import pytest

# Set dummy env vars before any app module is imported.
# This prevents pydantic-settings from raising ValidationError
# when GEMINI_API_KEY is absent in the local environment.
os.environ.setdefault("GEMINI_API_KEY", "test-key-not-used")
os.environ.setdefault("GEMINI_MODEL", "gemini-2.0-flash")
