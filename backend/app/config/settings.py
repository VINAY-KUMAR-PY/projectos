from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_SECRET_KEY = "change-this-secret-key-later"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "ProjectOS"
    app_version: str = "0.1.0"
    environment: str = "development"

    database_url: str = "sqlite:///./projectos.db"
    auto_create_tables: bool = True

    ai_provider: str = "mock"
    ai_model: str = "mock-model"
    ai_allowed_providers: str = "mock,ollama,gemini,openai"
    ai_monthly_budget_inr: int = 2000
    ai_max_request_cost_inr: int = 20
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-1.5-flash"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"

    max_upload_size_mb: int = 25
    secret_key: str = DEFAULT_SECRET_KEY
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    @model_validator(mode="after")
    def validate_production_settings(self):
        if self.environment == "production":
            self.auto_create_tables = False
            if self.secret_key == DEFAULT_SECRET_KEY:
                raise ValueError("SECRET_KEY must be changed in production")
        return self


settings = Settings()
