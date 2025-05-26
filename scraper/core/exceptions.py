class ScraperException(Exception):
    """Base exception for scraper application"""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NewsScrapingError(ScraperException):
    """Exception raised when news scraping fails"""

    def __init__(self, message: str = "Failed to scrape news"):
        super().__init__(message, 500)


class AnalysisError(ScraperException):
    """Exception raised when AI analysis fails"""

    def __init__(self, message: str = "Failed to perform analysis"):
        super().__init__(message, 500)


class DataNotFoundError(ScraperException):
    """Exception raised when requested data is not found"""

    def __init__(self, message: str = "Data not found"):
        super().__init__(message, 404)


class ValidationError(ScraperException):
    """Exception raised when validation fails"""

    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, 400)


class ConfigurationError(ScraperException):
    """Exception raised when configuration is invalid"""

    def __init__(self, message: str = "Invalid configuration"):
        super().__init__(message, 500)
