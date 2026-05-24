import os
from pathlib import Path

# Load .env only if it exists (local dev); on Render, env vars come from dashboard
_dotenv_path = Path(__file__).parent.parent / ".env"
if _dotenv_path.exists():
    from dotenv import load_dotenv
    load_dotenv(_dotenv_path)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./emotion_diary.db",
)

JWT_SECRET = os.getenv("JWT_SECRET", "change-me-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60 * 24  # 24 hours
