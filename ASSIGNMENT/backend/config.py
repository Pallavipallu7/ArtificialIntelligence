import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = os.getenv("SECRET_KEY", "campus_ai_helpdesk_secret_key_2026_academic")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/campus_helpdesk.db")

MODEL_DIR = BASE_DIR / "models_artifacts"
DATA_DIR = BASE_DIR / "data"

MODEL_DIR.mkdir(exist_ok=True, parents=True)
DATA_DIR.mkdir(exist_ok=True, parents=True)

ESCALATION_RISK_THRESHOLD = 0.65
Q_LEARNING_EPISODES = 500
