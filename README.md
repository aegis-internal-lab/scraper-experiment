# Scraper Experiment

A modern news scraping and AI analysis service built with BlackSheep, Tortoise ORM, and Google's Gemini AI.

## Features

- 🔍 **News Scraping**: Fetch news from Google News using keywords
- 🤖 **AI Analysis**: Root cause analysis, sentiment analysis, and prominent analysis using Google's Gemini AI
- 📊 **Data Management**: Store and retrieve scraped news data
- 🚀 **REST API**: Well-documented RESTful endpoints
- 🐳 **Docker Support**: Ready for containerized deployment
- 🧪 **Testing**: Comprehensive test suite with coverage
- 📝 **Logging**: Structured logging for monitoring and debugging

## Architecture

The project follows a clean architecture pattern with:

- **Services Layer**: Business logic separated into service classes
- **Routes Layer**: HTTP endpoint handlers
- **Models Layer**: Database models and schemas
- **Core Layer**: Configuration, exceptions, and utilities
- **Dependency Injection**: Proper service management

## Getting Started

### Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org) for dependency management

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd scraper-experiment
```

2. Install dependencies:
```bash
make dev-install
# or
poetry install
```

3. Create your `.env` file (see [Environment Configuration](#environment-configuration) below)

4. Run the server:
```bash
make run
# or
poetry run server
```

### Development

Run in development mode with auto-reload:
```bash
make dev
```

Run tests:
```bash
make test
```

Run tests with coverage:
```bash
make test-cov
```

Format code:
```bash
make format
```

Run linting:
```bash
make lint
```

Run all checks:
```bash
make check
```

## Environment Configuration

Create a `.env` file in the project root with the following variables:

```env
# ====================
# DATABASE CONFIGURATION
# ====================
DATABASE_URL=sqlite://db.sqlite3

# ====================
# LOGGING CONFIGURATION
# ====================
LOG_LEVEL=INFO
LOGGER_FILE_NAME=news_scraper.log

# ====================
# SERVER CONFIGURATION
# ====================
SERVER_HOST=0.0.0.0
SERVER_PORT=5000
SERVER_RELOAD=false
SERVER_LOG_LEVEL=info

# ====================
# SCRAPER CONFIGURATION
# ====================
INTERVAL_TIME=5
MAX_RESULTS=3
NEWS_PERIOD=7d
HTTPS_PROXY=

# ====================
# AI CONFIGURATION
# ====================
AI_MODEL=gemini-2.0-flash
GEMINI_API_KEY=your_gemini_api_key_here

# Analysis prompts (optional - defaults will be used if not provided)
RC_ANALYSIS_PROMPT=Perform a detailed 5W1H analysis...
SENTIMENT_ANALYSIS_PROMPT=Analyze the sentiment...
PROMINENT_ANALYSIS_PROMPT=Identify the most prominent...
EXTRACTING_PROMPT=Extract the title and content...
```

## API Endpoints

### Health Check
- `GET /health` - Service health check
- `GET /info` - Service information

### News
- `GET /get-news/?keyword=<keyword>&use_rca=<boolean>` - Fetch news by keyword

### Data
- `GET /get-data/` - Get all scraped data

### Analysis
- `GET /gen-all-analysis?url=<url>` - Generate all types of analysis
- `GET /gen-rc-analysis?url=<url>` - Generate root cause analysis

### Documentation
- Visit `/docs` for interactive API documentation

## Docker Deployment

Build and run with Docker:
```bash
make docker-build
make docker-run
```

Or use docker-compose directly:
```bash
docker-compose up -d
```

## Project Structure

```
scraper/
├── configs/          # Configuration and models
├── core/            # Core utilities, exceptions, DI container
├── libs/            # Utility libraries and legacy code
├── routes/          # HTTP route handlers
├── schemas/         # Pydantic schemas for validation
└── services/        # Business logic services
```

## Development Guidelines

- Follow PEP 8 style guidelines
- Write tests for new functionality
- Use type hints
- Document your code
- Follow the service pattern for business logic

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the MIT License.
