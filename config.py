import os
from pathlib import Path

# Base directory for the project
BASE_DIR = Path(__file__).resolve().parent

# Database configuration (with safe dev defaults)
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = os.environ.get("DB_PORT", "3307")
DB_NAME = os.environ.get("DB_NAME", "economic_dashboard")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")

# World Bank API Configuration
WORLD_BANK_API_URL = "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json&per_page=20000"

# NewsAPI Configuration
# On Streamlit Cloud: set NEWS_API_KEY in App Settings > Secrets
# Locally: set the NEWS_API_KEY environment variable or use a .env file
def _get_news_api_key() -> str:
    """Read the NewsAPI key from Streamlit secrets (Cloud) or env vars (local)."""
    # Try Streamlit secrets first (works on Streamlit Cloud)
    try:
        import streamlit as st
        key = st.secrets.get("NEWS_API_KEY", "")
        if key:
            return key
    except Exception:
        pass
    # Fall back to environment variable (works locally)
    return os.environ.get("NEWS_API_KEY", "")

NEWS_API_KEY = _get_news_api_key()

# Directories to auto-create
DIRECTORIES = [
    BASE_DIR / "data" / "raw",
    BASE_DIR / "data" / "processed",
    BASE_DIR / "reports" / "charts",
    BASE_DIR / "models",
]

for directory in DIRECTORIES:
    directory.mkdir(parents=True, exist_ok=True)

# Model configuration
MODEL_PATH = BASE_DIR / "models" / "gdp_forecast.pkl"
FEATURES = ["Year", "Previous_GDP", "GDP_Difference", "GDP_Growth_Rate"]
TARGET = "GDP_USD"
