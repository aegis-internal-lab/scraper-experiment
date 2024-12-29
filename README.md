# Scraper Experiment

## Gettin Started

This repo is made using [`poetry`](https://python-poetry.org), all you have to do is run `poetry install` and then `poetry run server` to activate the endpoints assuming that you already set the necessary `.env`.

### ENV File Content
In order to run the server, you have to add the necessary `.env` at the **project root**

```env
# GNEWS CONFIG
INTERVAL_TIME="5" // default 5
MAX_RESULTS="3" // default 3

# PROMPT CONFIG
GEMINI_API_KEY="" // get it by following this guide https://ai.google.dev/gemini-api/docs/api-key

RC_ANALYSIS_PROMPT="" // example: "Give me a 5w1h analysis using the following url:"
SENTIMENT_ANALYSIS_PROMPT="" // example: "Give me a sentiment analysis using the following url:"
PROMINENT_ANALYSIS_PROMPT="" // example: "Give me a prominent feature analysis using the following url:"
HTTPS_PROXY="" // use proxy server for safety reasons

# APP CONFIG
LOG_LEVEL="INFO" // default INFO
DB_URL="sqlite:///app.db" // your database URL
```
