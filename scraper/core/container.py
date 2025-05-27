from functools import lru_cache

from scraper.services.analysis_service import AnalysisService
from scraper.services.data_service import DataService
from scraper.services.news_service import NewsService


class Container:
    """Dependency injection container"""

    def __init__(self):
        self._news_service = None
        self._analysis_service = None
        self._data_service = None

    @property
    def news_service(self) -> NewsService:
        if self._news_service is None:
            self._news_service = NewsService()
        return self._news_service

    @property
    def analysis_service(self) -> AnalysisService:
        if self._analysis_service is None:
            self._analysis_service = AnalysisService()
        return self._analysis_service

    @property
    def data_service(self) -> DataService:
        if self._data_service is None:
            self._data_service = DataService()
        return self._data_service


@lru_cache()
def get_container() -> Container:
    """Get the application container"""
    return Container()
