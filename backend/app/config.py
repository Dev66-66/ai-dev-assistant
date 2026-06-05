from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openrouter_api_key: str
    openrouter_model: str = "google/gemma-4-31b-it:free"
    backend_host: str = "0.0.0.0"  # nosec B104 — intentional: container must bind all interfaces
    backend_port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
