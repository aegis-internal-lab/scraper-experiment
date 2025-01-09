from gnews import GNews
from googlenewsdecoder import new_decoderv1

from scraper.configs.constants import INTERVAL_TIME
from scraper.configs.models import ResponseJSON, Site, Status
from scraper.libs.logger import logger


async def _get_news_real_url(news: dict[str, str]) -> None:
    logger.info("Getting Real URL...")
    result = new_decoderv1(news["url"], interval=INTERVAL_TIME)["decoded_url"]
    logger.info("Real URL Retrieved")
    logger.info("Saving Masked URL and Real URL to Database...")
    await Site.create(masked_url=news["url"], url=result)
    logger.info("Masked URL and Real URL Saved to Database")


async def get_news_list(keyword: str) -> ResponseJSON:
    try:
        logger.info("Initializing Scraper...")
        news_scraper = GNews(max_results=2, period="2d")
        logger.info("Scraper Initialized")

        logger.info("Getting News...")
        latest_news = news_scraper.get_news(keyword)

        news_count = len(latest_news) if latest_news else 0
        logger.info(f"{news_count} News Retrieved")

        if latest_news is not None:
            for news in latest_news:
                await _get_news_real_url(news)
        return ResponseJSON(status=Status.SUCCESS, message="News fetched successfully")
    except Exception as e:
        logger.error(f"Error: {e}")
        return ResponseJSON(status=Status.ERROR, message=str(e))
