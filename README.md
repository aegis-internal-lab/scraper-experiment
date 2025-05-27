# Scraper Experiment

A modern news scraping and AI analysis service built with BlackSheep, Tortoise ORM, and Google's Gemini AI.

## Features

- 🔍 **News Scraping**: Fetch news from Google News using keywords
- 🤖 **AI Analysis**: Root cause analysis, sentiment analysis, and prominent analysis using Google's Gemini AI
- 🔄 **Anti-Detection**: Advanced proxy rotation, user agent rotation, and enhanced rate limiting with jitter
- 🌐 **Proxy Support**: Multiple proxy configuration with automatic rotation
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

# ====================
# ENHANCED RATE LIMITING
# ====================
# Jitter range for random delays (in seconds)
JITTER_MIN=1.0
JITTER_MAX=3.0

# ====================
# PROXY CONFIGURATION
# ====================
# Single proxy configuration (basic)
# HTTP_PROXY=http://your-proxy-server:port
# HTTPS_PROXY=https://your-proxy-server:port

# Multiple proxy configuration for rotation
# Format: "proxy1:port,proxy2:port,proxy3:port"
# PROXY_LIST=proxy1.example.com:8080,proxy2.example.com:8080,proxy3.example.com:8080

# Enable proxy rotation (requires PROXY_LIST or multiple proxies)
USE_PROXY_ROTATION=false

# ====================
# USER AGENT ROTATION
# ====================
# Enable user agent rotation for anti-detection
USE_USER_AGENT_ROTATION=true

# ====================
# PROXY CONFIGURATION (Optional)
# ====================
# HTTP_PROXY=http://your-proxy-server:port
# HTTPS_PROXY=https://your-proxy-server:port

# ====================
# GNEWS CONFIGURATION (Optional)
# ====================
GNEWS_LANGUAGE=en
GNEWS_COUNTRY=US
# GNEWS_EXCLUDE_WEBSITES=yahoo.com,cnn.com

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

### Anti-Detection Features

The scraper includes sophisticated anti-detection features to avoid getting banned:

#### **🔄 Proxy Rotation**
- **Multiple Proxies**: Configure multiple proxies for automatic rotation
- **Round Robin**: Proxies are cycled automatically for each request
- **Fallback**: Falls back to single proxy if rotation is disabled

#### **🕵️ User Agent Rotation**
- **Diverse Browsers**: Rotates between Chrome, Firefox, Safari, Edge user agents
- **Multiple Platforms**: Windows, macOS, and Linux user agent strings
- **Realistic Headers**: Complete HTTP headers that mimic real browsers

#### **⏱️ Enhanced Rate Limiting**
- **Jitter**: Random delays between requests to avoid patterns
- **Adaptive**: Delays increase based on request count
- **Configurable**: Adjustable base interval and jitter range

#### **🎯 Smart Distribution**
- **Session Management**: Fresh proxy/user-agent combination per session
- **Request Spreading**: Distributes load across multiple endpoints
- **Error Handling**: Graceful handling of proxy failures

### Configuration Examples

#### Basic Proxy Setup
```env
HTTP_PROXY=http://proxy.company.com:8080
HTTPS_PROXY=https://proxy.company.com:8080
```

#### Advanced Proxy Rotation
```env
PROXY_LIST=proxy1.example.com:8080,proxy2.example.com:8080,proxy3.example.com:8080
USE_PROXY_ROTATION=true
```

#### Rate Limiting Configuration
```env
INTERVAL_TIME=5        # Base delay between requests
JITTER_MIN=1.0        # Minimum random jitter
JITTER_MAX=3.0        # Maximum random jitter
```

#### User Agent Rotation
```env
USE_USER_AGENT_ROTATION=true   # Enable user agent rotation
```

#### GNews Configuration

Customize the news scraping behavior:

- **GNEWS_LANGUAGE**: Language code (e.g., 'en', 'es', 'fr', 'de')
- **GNEWS_COUNTRY**: Country code (e.g., 'US', 'GB', 'CA', 'AU')
- **GNEWS_EXCLUDE_WEBSITES**: Comma-separated list of websites to exclude

Example:
```env
GNEWS_LANGUAGE=en
GNEWS_COUNTRY=US
GNEWS_EXCLUDE_WEBSITES=yahoo.com,cnn.com,foxnews.com
```

## API Endpoints

### Health Check
- `GET /health` - Service health check
- `GET /info` - Service information

### Status & Monitoring
- `GET /status/rotation` - View rotation and anti-detection status
- `GET /status/proxy` - Validate proxy configuration

### News
- `GET /get-news/?keyword=<keyword>&use_rca=<boolean>` - Fetch news by keyword

### Data
- `GET /get-data/` - Get all scraped data
- `GET /get-data/by-url?url=<url>` - Get a specific site by URL
- `GET /get-data/by-keyword?keyword=<keyword>` - Get sites by keyword
- `GET /get-data/count` - Get total count of sites in database

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

## Management Commands

The project includes a comprehensive management script for testing and debugging the rotation features:

### Testing Anti-Detection Features
```bash
# Test all rotation features
python manage.py all

# Test specific components
python manage.py status          # View rotation status
python manage.py proxy           # Test proxy configuration  
python manage.py user-agent      # Test user agent rotation
python manage.py proxy-rotation  # Test proxy rotation
python manage.py news            # Test news fetching with rotation
```

### Available Commands
- **status**: Display current rotation and anti-detection configuration
- **proxy**: Validate proxy configuration and test connectivity
- **user-agent**: Test user agent rotation functionality
- **proxy-rotation**: Test proxy rotation if configured
- **news**: Test news fetching with all rotation features enabled
- **all**: Run comprehensive test suite covering all features

### Management Script Features
- **🔍 Comprehensive Testing**: Tests all rotation and anti-detection features
- **📊 Detailed Status**: Shows configuration and performance metrics
- **✅ Validation**: Verifies proxy connectivity and rotation functionality
- **💡 Recommendations**: Provides optimization suggestions
- **🎯 Targeted Testing**: Individual component testing for debugging

## Running the Application
