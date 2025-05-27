from email.utils import parsedate_to_datetime  # Parses RFC 2822 dates

from gnews import GNews
from googlenewsdecoder import new_decoderv1

from scraper.configs.constants import (
    GNEWS_COUNTRY,
    GNEWS_EXCLUDE_WEBSITES,
    GNEWS_LANGUAGE,
    INTERVAL_TIME,
    MAX_RESULTS,
    NEWS_PERIOD,
)
from scraper.configs.models import ResponseJSON, Site, Status
from scraper.libs.generate_reports import extract_content_site, rc_analysis
from scraper.libs.logger import logger
from scraper.libs.rotation_utils import proxy_rotator, rate_limiter, user_agent_rotator

# Initialize GNews with configuration
def _create_gnews_instance():
    """Create GNews instance with proxy and other configurations"""
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


async def _get_news_real_url_and_content(news: dict[str, str], use_rca: bool, keyword: str, request_count: int = 0) -> None:
    truncated_string = news["url"][:30] + "..." if len(news["url"]) > 30 else news["url"]
    logger.info(f"Getting Real URL from {truncated_string}")
    
    # Use enhanced rate limiting with jitter
    await rate_limiter.adaptive_wait(request_count)
    
    decoder = new_decoderv1(news["url"], interval=INTERVAL_TIME)
    result = decoder["decoded_url"]
    logger.info("Real URL Retrieved")
    site = await extract_content_site(result)
    logger.info("Saving Masked URL and Real URL to Database...")
    await Site.create(
        masked_url=news["url"],
        url=result,
        title=site.title,
        content=site.content,
        keyword=keyword,
        published_date=parsedate_to_datetime(news["published date"]),
    )
    logger.info("Masked URL and Real URL Saved to Database")
    if use_rca:
        await rc_analysis(result)


async def get_news_list(keyword: str, use_rca: bool) -> ResponseJSON:
    try:
        logger.info("Initializing Scraper...")
        
        # Create fresh GNews instance with rotated proxy for each request
        current_news_scraper = _create_gnews_instance()
        logger.info("Scraper Initialized")

        logger.info("Getting News...")
        latest_news = current_news_scraper.get_news(keyword)

        news_count = len(latest_news) if latest_news else 0
        logger.info(f"{news_count} News Retrieved")

        if latest_news is not None:
            for index, news in enumerate(latest_news):
                await _get_news_real_url_and_content(news, use_rca, keyword, index)
        return ResponseJSON(
            status=Status.SUCCESS, message=f"{news_count} News fetched successfully"
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        return ResponseJSON(status=Status.ERROR, message=str(e))
