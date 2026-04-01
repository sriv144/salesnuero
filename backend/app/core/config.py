from typing import List
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "SalesNeuro API"
    VERSION: str = "0.1.0"

    # API Keys (loaded from .env)
    TAVILY_API_KEY: str = ""
    NVIDIA_API_KEY: str = ""

    # ChromaDB Configuration
    CHROMA_PERSIST_DIRECTORY: str = "../../data/chroma_db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
