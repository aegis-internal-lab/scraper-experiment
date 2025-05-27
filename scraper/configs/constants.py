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
JITTER_MIN = float(os.getenv("JITTER_MIN", 1.0))
JITTER_MAX = float(os.getenv("JITTER_MAX", 3.0))
MAX_RESULTS = int(os.getenv("MAX_RESULTS", 3))
NEWS_PERIOD = os.getenv("NEWS_PERIOD", "7d")

# Proxy Configuration
HTTP_PROXY = os.getenv("HTTP_PROXY")
HTTPS_PROXY = os.getenv("HTTPS_PROXY")
# Support for multiple proxies (comma-separated)
PROXY_LIST = os.getenv("PROXY_LIST", "")  # Format: "proxy1:port,proxy2:port,proxy3:port"
USE_PROXY_ROTATION = os.getenv("USE_PROXY_ROTATION", "false").lower() == "true"

# User Agent Configuration
USE_USER_AGENT_ROTATION = os.getenv("USE_USER_AGENT_ROTATION", "true").lower() == "true"

# GNews Configuration
GNEWS_LANGUAGE = os.getenv("GNEWS_LANGUAGE", "en")
GNEWS_COUNTRY = os.getenv("GNEWS_COUNTRY", "US")
GNEWS_EXCLUDE_WEBSITES = os.getenv("GNEWS_EXCLUDE_WEBSITES", "")

# Analysis
AI_MODEL = os.getenv("AI_MODEL", "gemini-2.0-flash")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
RC_ANALYSIS_PROMPT = os.getenv("RC_ANALYSIS_PROMPT")
SENTIMENT_ANALYSIS_PROMPT = os.getenv("SENTIMENT_ANALYSIS_PROMPT")
PROMINENT_ANALYSIS_PROMPT = os.getenv("PROMINENT_ANALYSIS_PROMPT")
EXTRACTING_PROMPT = os.getenv("EXTRACTING_PROMPT", "Extract the main title and content from this webpage. Return only the title and content in a clear, readable format.")
