# app/config.py

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from a .env file if present
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = "ShopLens"
    DB_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/shoplens_db")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "supersecretkey")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

settings = Settings()
