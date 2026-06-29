from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ProjectOS"
    app_version: str = "0.1.0"
    environment: str = "development"

    database_url: str = "sqlite:///./projectos.db"

    ai_provider: str = "mock"
    ai_model: str = "mock-model"

    max_upload_size_mb: int = 25

    class Config:
        env_file = ".env"


settings = Settings()