from typing import List, Optional

from scraper.configs.models import Site
from scraper.services.interfaces import DataServiceInterface


class DataService(DataServiceInterface):
    """Service for handling data operations"""

    async def get_all_sites(self) -> List[dict]:
        """Get all sites from database"""
        sites = await Site.all()
        return [
            {
                "id": site.id,
                "title": site.title,
                "published_date": site.published_date.isoformat() if site.published_date else None,
                "keyword": site.keyword,
                "content": site.content,
                "masked_url": site.masked_url,
                "url": site.url,
                "is_extracted": site.is_extracted,
                "has_rc_analysis": site.has_rc_analysis,
                "rc_analysis": site.rc_analysis,
                "has_sentiment_analysis": site.has_sentiment_analysis,
                "sentiment_analysis": site.sentiment_analysis,
                "has_prominent_analysis": site.has_prominent_analysis,
                "prominent_analysis": site.prominent_analysis,
                "created_at": site.created_at.isoformat() if site.created_at else None,
                "updated_at": site.updated_at.isoformat() if site.updated_at else None,
            }
            for site in sites
        ]

    async def get_site_by_url(self, url: str) -> Optional[Site]:
        """Get site by URL"""
        return await Site.filter(url=url).first()

    async def site_exists(self, url: str) -> bool:
        """Check if site exists in database"""
        return await Site.filter(url=url).exists()

    async def get_sites_by_keyword(self, keyword: str) -> List[Site]:
        """Get sites by keyword"""
        return await Site.filter(keyword=keyword).all()

    async def get_sites_count(self) -> int:
        """Get total count of sites"""
        return await Site.all().count()
