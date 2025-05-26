import asyncio
from typing import Optional

from scraper.configs.models import Site
from scraper.libs.generate_reports import prominent_analysis, rc_analysis, sentiment_analysis
from scraper.services.interfaces import AnalysisServiceInterface


class AnalysisService(AnalysisServiceInterface):
    """Service for handling AI analysis operations"""

    async def generate_root_cause_analysis(self, url: str) -> None:
        """Generate root cause analysis for given URL"""
        await rc_analysis(url)

    async def generate_sentiment_analysis(self, url: str) -> None:
        """Generate sentiment analysis for given URL"""
        await sentiment_analysis(url)

    async def generate_prominent_analysis(self, url: str) -> None:
        """Generate prominent analysis for given URL"""
        await prominent_analysis(url)

    async def generate_all_analysis(self, url: str) -> Optional[dict]:
        """Generate all types of analysis for given URL"""
        # Run all analysis in parallel for better performance
        await asyncio.gather(
            self.generate_root_cause_analysis(url),
            self.generate_sentiment_analysis(url),
            self.generate_prominent_analysis(url),
        )

        # Get the updated data
        current_data = await Site.filter(url=url).first()
        if current_data:
            return {
                "url": current_data.url,
                "masked_url": current_data.masked_url,
                "rc_analysis": current_data.rc_analysis,
                "sentiment_analysis": current_data.sentiment_analysis,
                "prominent_analysis": current_data.prominent_analysis,
            }
        return None
