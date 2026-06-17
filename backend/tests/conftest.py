import os

# Set dummy env vars before any app module is imported.
# This prevents pydantic-settings from raising ValidationError
# when OPENROUTER_API_KEY is absent in the local environment.
os.environ.setdefault("OPENROUTER_API_KEY", "test-key-not-used")
os.environ.setdefault("OPENROUTER_MODEL", "google/gemma-3-27b-it:free")
