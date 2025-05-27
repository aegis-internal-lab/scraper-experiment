from email.utils import parsedate_to_datetime

from gnews import GNews # type: ignore
from googlenewsdecoder import new_decoderv1 # type: ignore

from scraper.configs.constants import (
    GNEWS_COUNTRY,
    GNEWS_EXCLUDE_WEBSITES,
    GNEWS_LANGUAGE,
    INTERVAL_TIME,
    MAX_RESULTS,
    NEWS_PERIOD,
)
from scraper.configs.models import ResponseJSON, Site, Status
from scraper.libs.logger import logger
from scraper.libs.rotation_utils import proxy_rotator, rate_limiter, user_agent_rotator
from scraper.services.interfaces import NewsServiceInterface


class NewsService(NewsServiceInterface):
    """Service for handling news scraping operations with advanced anti-detection features"""

    def __init__(self):
        # Create instance without storing it to allow fresh configs per request
        pass

    def _create_gnews_instance(self):
        """Create GNews instance with proxy rotation and advanced configurations"""
        config = {
            "max_results": MAX_RESULTS,
            "period": NEWS_PERIOD,
            "language": GNEWS_LANGUAGE,
            "country": GNEWS_COUNTRY,
        }
        
        # Add proxy configuration using rotation
        proxy_config = proxy_rotator.get_next_proxy()
        if proxy_config:
            config["proxy"] = proxy_config
            logger.info(f"Using proxy configuration: {list(proxy_config.keys())}")
        
        # Add exclude websites if configured
        if GNEWS_EXCLUDE_WEBSITES:
            exclude_list = [site.strip() for site in GNEWS_EXCLUDE_WEBSITES.split(",") if site.strip()]
            if exclude_list:
                config["exclude_websites"] = exclude_list
                logger.info(f"Excluding websites: {exclude_list}")
        
        return GNews(**config)

    async def get_news_by_keyword(self, keyword: str, use_rca: bool) -> ResponseJSON:
        """Fetch news by keyword and optionally perform RCA with advanced anti-detection"""
        # Lazy import to avoid circular imports
        from scraper.services.analysis_service import AnalysisService
        
        try:
            analysis_service = AnalysisService()
            logger.info("Initializing news scraping with rotation features...")
            
            # Create fresh GNews instance with rotated proxy for each request
            current_news_scraper = self._create_gnews_instance()
            logger.info("News scraper initialized with advanced configurations")

            logger.info("Fetching news articles...")
            latest_news = current_news_scraper.get_news(keyword)
            news_count = len(latest_news) if latest_news else 0
            logger.info(f"{news_count} news articles retrieved")

            if latest_news:
                for index, news in enumerate(latest_news):
                    await self._process_news_item(news, use_rca, keyword, analysis_service, index)

            return ResponseJSON(
                status=Status.SUCCESS, message=f"{news_count} news articles fetched successfully"
            )
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return ResponseJSON(status=Status.ERROR, message=str(e))

    async def _process_news_item(self, news: dict, use_rca: bool, keyword: str, analysis_service, request_count: int = 0) -> None:
        """Process individual news item with enhanced rate limiting"""
        truncated_url = news["url"][:30] + "..." if len(news["url"]) > 30 else news["url"]
        logger.info(f"Processing news item: {truncated_url}")

        try:
            # Use enhanced rate limiting with jitter
            await rate_limiter.adaptive_wait(request_count)
            
            # Decode the masked Google News URL
            decoder = new_decoderv1(news["url"], interval=INTERVAL_TIME)
            real_url = decoder["decoded_url"]
            logger.info("Real URL retrieved")

            # Extract content from the real URL using AnalysisService
            site_content = await analysis_service.extract_content_site(real_url)
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

            # Perform RCA if requested using AnalysisService
            if use_rca:
                await analysis_service.generate_root_cause_analysis(real_url)
                logger.info("Root cause analysis completed")

        except Exception as e:
            logger.error(f"Error processing news item {truncated_url}: {e}")
            # Continue processing other items instead of failing completely
