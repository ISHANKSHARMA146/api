import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables
    """
    # API Configuration
    API_TITLE: str = "Job Description Extraction & Enhancement API"
    API_DESCRIPTION: str = "API for extracting and enhancing job descriptions from various file formats"
    API_VERSION: str = "1.0.0"
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GPT_MODEL: str = os.getenv("GPT_MODEL", "gpt-4o")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # CORS Settings
    CORS_ORIGINS: list = ["*"]
    
    # Settings configuration (pydantic v2 style)
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )

@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached instance of settings
    """
    return Settings() 