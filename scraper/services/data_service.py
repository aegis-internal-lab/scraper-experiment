from typing import List, Optional

from tortoise.contrib.pydantic import pydantic_model_creator

from scraper.configs.models import Site
from scraper.services.interfaces import DataServiceInterface


class DataService(DataServiceInterface):
    """Service for handling data operations"""

    async def get_all_sites(self) -> List[dict]:
        """Get all sites from database"""
        SitePydantic = pydantic_model_creator(Site, name="site_db")
        sites = Site.all()  # This returns a QuerySet
        pydantic_sites = await SitePydantic.from_queryset(sites)
        return [site.model_dump() for site in pydantic_sites]

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
