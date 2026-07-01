from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_SECRET_KEY = "change-this-secret-key-later"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "ProjectOS"
    app_version: str = "1.0.0"
    environment: str = "development"

    database_url: str = "sqlite:///./projectos.db"
    redis_url: str = "redis://localhost:6379"
    auto_create_tables: bool = True

    ai_provider: str = "mock"
    ai_model: str = "mock-model"
    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-sonnet-4-6"
    ai_allowed_providers: str = "mock,anthropic,ollama,gemini,openai"
    ai_monthly_budget_inr: int = 2000
    ai_max_request_cost_inr: int = 20
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-1.5-flash"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"
    chroma_persist_dir: str = "./chroma_db"
    upload_dir: str = "./uploads"
    stripe_secret_key: str | None = None
    stripe_webhook_secret: str | None = None
    razorpay_key_id: str | None = None
    razorpay_key_secret: str | None = None
    github_client_id: str | None = None
    github_client_secret: str | None = None
    google_client_id: str | None = None
    google_client_secret: str | None = None
    cloudinary_url: str | None = None
    cors_origins: list[str] = ["http://localhost:3000"]

    max_upload_size_mb: int = 50
    secret_key: str = DEFAULT_SECRET_KEY
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value):
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @model_validator(mode="after")
    def validate_production_settings(self):
        if self.environment == "production":
            self.auto_create_tables = False
            if self.secret_key == DEFAULT_SECRET_KEY:
                raise ValueError("SECRET_KEY must be changed in production")
        return self


settings = Settings()
