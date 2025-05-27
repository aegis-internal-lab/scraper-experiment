from email.utils import parsedate_to_datetime

from gnews import GNews # type: ignore
from googlenewsdecoder import new_decoderv1 # type: ignore

from scraper.configs.constants import INTERVAL_TIME, MAX_RESULTS, NEWS_PERIOD
from scraper.configs.models import ResponseJSON, Site, Status
from scraper.libs.generate_reports import extract_content_site, rc_analysis
from scraper.libs.logger import logger
from scraper.services.interfaces import NewsServiceInterface


class NewsService(NewsServiceInterface):
    """Service for handling news scraping operations"""

    def __init__(self):
        self.news_scraper = GNews(max_results=MAX_RESULTS, period=NEWS_PERIOD)

    async def get_news_by_keyword(self, keyword: str, use_rca: bool) -> ResponseJSON:
        """Fetch news by keyword and optionally perform RCA"""
        try:
            logger.info("Initializing news scraping...")
            latest_news = self.news_scraper.get_news(keyword)
            news_count = len(latest_news) if latest_news else 0
            logger.info(f"{news_count} news articles retrieved")

            if latest_news:
                for news in latest_news:
                    await self._process_news_item(news, use_rca, keyword)

            return ResponseJSON(
                status=Status.SUCCESS, message=f"{news_count} news articles fetched successfully"
            )
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return ResponseJSON(status=Status.ERROR, message=str(e))

    async def _process_news_item(self, news: dict, use_rca: bool, keyword: str) -> None:
        """Process individual news item"""
        truncated_url = news["url"][:30] + "..." if len(news["url"]) > 30 else news["url"]
        logger.info(f"Processing news item: {truncated_url}")

        try:
            # Decode the masked Google News URL
            decoder = new_decoderv1(news["url"], interval=INTERVAL_TIME)
            real_url = decoder["decoded_url"]
            logger.info("Real URL retrieved")

            # Extract content from the real URL
            site_content = await extract_content_site(real_url)
            logger.info("Content extracted")

            # Save to database
            await Site.create(
                masked_url=news["url"],
                url=real_url,
                title=site_content.title,
                content=site_content.content,
                keyword=keyword,
                published_date=parsedate_to_datetime(news["published date"]),
            )
            logger.info("Site data saved to database")

            # Perform RCA if requested
            if use_rca:
                await rc_analysis(real_url)
                logger.info("Root cause analysis completed")

        except Exception as e:
            logger.error(f"Error processing news item {truncated_url}: {e}")
            # Continue processing other items instead of failing completely
