from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    project_name: str = Field(default="Collabrix API")
    database_url: str = Field(
        default="postgresql+psycopg2://collabrix:collabrix@localhost:5432/collabrix",
        validation_alias="DATABASE_URL",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()