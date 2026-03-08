from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / "backend"
DATA_DIR = BASE_DIR / "data"

DB_PATH = BACKEND_DIR / "business_intelligence.db"
CSV_PATH = DATA_DIR / "sales.csv"

API_KEY = ""
GEMINI_MODEL = "gemini-1.5-flash"

LOG_LEVEL = "INFO"
MAX_ROWS = 1000
