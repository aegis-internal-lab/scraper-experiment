from gnews import GNews
from googlenewsdecoder import new_decoderv1

from scraper.configs.constants import INTERVAL_TIME, MAX_RESULTS, NEWS_PERIOD
from scraper.configs.models import ResponseJSON, Site, Status
from scraper.libs.generate_reports import extract_content_site, rc_analysis
from scraper.libs.logger import logger

news_scraper = GNews(max_results=MAX_RESULTS, period=NEWS_PERIOD)


async def _get_news_real_url_and_content(news: dict[str, str], use_rca: bool) -> None:
    truncated_string = news["url"][:30] + "..." if len(news["url"]) > 30 else news["url"]
    logger.info(f"Getting Real URL from {truncated_string}")
    decoder = new_decoderv1(news["url"], interval=INTERVAL_TIME)
    print(decoder)
    result = decoder["decoded_url"]
    logger.info("Real URL Retrieved")
    site = await extract_content_site(result)
    logger.info("Saving Masked URL and Real URL to Database...")
    await Site.create(masked_url=news["url"], url=result, title=site.title, content=site.content)
    logger.info("Masked URL and Real URL Saved to Database")
    if use_rca:
        await rc_analysis(result)


async def get_news_list(keyword: str, use_rca: bool) -> ResponseJSON:
    try:
        logger.info("Initializing Scraper...")
        logger.info("Scraper Initialized")

        logger.info("Getting News...")
        latest_news = news_scraper.get_news(keyword)

        news_count = len(latest_news) if latest_news else 0
        logger.info(f"{news_count} News Retrieved")

        if latest_news is not None:
            for news in latest_news:
                await _get_news_real_url_and_content(news, use_rca)
        return ResponseJSON(
            status=Status.SUCCESS, message=f"{news_count} News fetched successfully"
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        return ResponseJSON(status=Status.ERROR, message=str(e))
