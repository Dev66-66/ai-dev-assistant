from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    llm_provider: str = "openrouter"  # "openrouter" or "ollama"

    openrouter_api_key: str = ""
    openrouter_model: str = "google/gemma-3-27b-it:free"

    ollama_base_url: str = "http://host.docker.internal:11434/v1"
    ollama_model: str = "qwen2.5-coder:7b"
    ollama_completion_model: str = "qwen2.5-coder:1.5b"

    backend_host: str = "0.0.0.0"  # nosec B104 — intentional: container must bind all interfaces
    backend_port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
