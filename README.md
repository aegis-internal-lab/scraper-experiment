# Scraper Experiment

## Gettin Started

This repo is made using [`poetry`](https://python-poetry.org) so install poetry first. After that, all you have to do is run `poetry install` and then `poetry run server` to activate the endpoints assuming that you already set the necessary `.env`.

### ENV File Content
In order to run the server, you have to add the necessary `.env` at the **project root**

```env
# ====================
# DATABASE CONFIGURATION
# ====================
# The URL for the database connection. 
# Default is SQLite for local development. Replace with your database URL for production.
DATABASE_URL=sqlite://db.sqlite3

# ====================
# LOGGING CONFIGURATION
# ====================
# The logging level for the application.
# Options: DEBUG, INFO, WARNING, ERROR, CRITICAL. Default is INFO.
LOG_LEVEL=INFO

# The name of the file where logs will be stored.
LOGGER_FILE_NAME=news_scraper.log

# ====================
# SCRAPER CONFIGURATION
# ====================
# Time interval (in seconds) between each scraping job.
# Default is 5 seconds.
INTERVAL_TIME=5

# The maximum number of results to return per scraping job.
# Default is 3 results.
MAX_RESULTS=3

# The period for news articles to be scraped.
# Format: "Nd" (e.g., "7d" for 7 days). Default is 7 days.
NEWS_PERIOD=7d

# HTTPS proxy to route scraper traffic through (optional).
# Leave blank if no proxy is needed.
HTTPS_PROXY=

# ====================
# ANALYSIS CONFIGURATION
# ====================
# The AI model to be used for analysis. 
# Default is "gemini-2.0-flash-exp". Replace with your desired model.
AI_MODEL=gemini-2.0-flash-exp

# The API key for the AI model. Required for authentication. get it from https://ai.google.dev/gemini-api/docs/api-key
GEMINI_API_KEY=

# Prompts for various types of analyses.
# Add your custom prompt text or leave blank for default behavior.

# For analyzing Root Cause Analysis or 5W1H Analysis.
RC_ANALYSIS_PROMPT=Perform a detailed 5W1H analysis of the provided content. Break down the information explicitly into the following categories:\n1. Who: Identify the key individuals, groups, or entities involved.\n2. What: Define the main event, action, or subject matter.\n3. When: Specify the time frame or timeline of relevance.\n4. Where: Determine the location(s) or setting of the events.\n5. Why: Explain the reasons, motivations, or context behind the events.\n6. How: Describe the methods, processes, or means by which the events occurred.\nEnsure the output is concise, structured, and relevant to the content, with no additional commentary or irrelevant information. the provided content url is

# For analyzing sentiment (positive, negative, neutral).
SENTIMENT_ANALYSIS_PROMPT=

# For analyzing prominent details in the scraped data.
PROMINENT_ANALYSIS_PROMPT=

# For extracting specific information from the scraped data.
EXTRACTING_PROMPT=Extract the data and return it as a *single-line* JSON string, with *no* surrounding backticks, markdown, or other commentary. The JSON should have the following format: "{"title": "title of the url", "content": "content of the url article"}" . The output must contain *only* the single-line, valid JSON string. The provided content url is
```
