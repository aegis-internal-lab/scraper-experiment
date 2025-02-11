import os

from dotenv import load_dotenv

load_dotenv(override=True)

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://db.sqlite3")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOGGER_FILE_NAME = os.getenv("LOGGER_FILE_NAME", "news_scraper.log")

# Scraper
INTERVAL_TIME = int(os.getenv("INTERVAL_TIME", 5))
MAX_RESULTS = int(os.getenv("MAX_RESULTS", 3))
NEWS_PERIOD = os.getenv("NEWS_PERIOD", "7d")
HTTPS_PROXY = os.getenv("HTTPS_PROXY")

# Analysis
AI_MODEL = os.getenv("AI_MODEL", "gemini-2.0-flash")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
RC_ANALYSIS_PROMPT = os.getenv("RC_ANALYSIS_PROMPT")
SENTIMENT_ANALYSIS_PROMPT = os.getenv("SENTIMENT_ANALYSIS_PROMPT")
PROMINENT_ANALYSIS_PROMPT = os.getenv("PROMINENT_ANALYSIS_PROMPT")
EXTRACTING_PROMPT = os.getenv("EXTRACTING_PROMPT")
