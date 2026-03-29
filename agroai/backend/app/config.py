"""
Application configuration via environment variables.
Version: 1.0.2 (Triggered reload for Gemini Key)
Location: backend/app/config.py
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./agroai.db"

    # Auth
    jwt_secret: str = "dev-secret-change-in-production"
    jwt_expire_days: int = 7
    otp_expire_seconds: int = 300  # 5 minutes

    # LLM
    llm_api_key: str = ""
    llm_model: str = "gemini-2.0-flash"
    llm_max_tokens: int = 512

    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Environment
    environment: str = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# Diagnostic startup log
print(f"--- AGROAI RUNTIME INITIALIZED ---")
print(f"Provider: {'Google Gemini' if 'gemini' in settings.llm_model.lower() else 'OpenAI'}")
print(f"Active Model: {settings.llm_model}")
print(f"API Key Configured: {'YES' if settings.llm_api_key else 'NO'}")
print(f"----------------------------------")