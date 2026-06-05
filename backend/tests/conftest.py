import os

# Set dummy env vars before any app module is imported.
# This prevents pydantic-settings from raising ValidationError
# when OPENROUTER_API_KEY is absent in the local environment.
os.environ.setdefault("OPENROUTER_API_KEY", "test-key-not-used")
os.environ.setdefault("OPENROUTER_MODEL", "google/gemini-2.0-flash")
