from abc import ABC, abstractmethod
from typing import List, Optional

from scraper.configs.models import ResponseJSON, ResponseContent, Site


class NewsServiceInterface(ABC):
    """Interface for news scraping service"""

    @abstractmethod
    async def get_news_by_keyword(self, keyword: str, use_rca: bool) -> ResponseJSON:
        """Fetch news by keyword"""
        pass


class AnalysisServiceInterface(ABC):
    """Interface for AI analysis service"""

    @abstractmethod
    async def generate_root_cause_analysis(self, url: str) -> None:
        """Generate root cause analysis for given URL"""
        pass

    @abstractmethod
    async def generate_sentiment_analysis(self, url: str) -> None:
        """Generate sentiment analysis for given URL"""
        pass

    @abstractmethod
    async def generate_prominent_analysis(self, url: str) -> None:
        """Generate prominent analysis for given URL"""
        pass

    @abstractmethod
    async def generate_all_analysis(self, url: str) -> Optional[dict]:
        """Generate all types of analysis for given URL"""
        pass

    @abstractmethod
    async def extract_content_site(self, url: str) -> ResponseContent:
        """Extract content from a website URL"""
        pass


class DataServiceInterface(ABC):
    """Interface for data management service"""

    @abstractmethod
    async def get_all_sites(self) -> List[dict]:
        """Get all sites from database"""
        pass

    @abstractmethod
    async def get_site_by_url(self, url: str) -> Optional[Site]:
        """Get site by URL"""
        pass
