import asyncio

from scraper.configs.openapidocs import docs
from scraper.libs.generate_reports import prominent_analysis, rc_analysis, sentiment_analysis
from scraper.libs.utils import get_current_data
from scraper.routes.routers import base


@docs(
    responses={200: "Analysis Done Successfully", 500: "Internal Server Error with error message"},
    description="This endpoint will perform Root Cause Analysis (5W1H), Sentiment Analysis, and Prominent Analysis using Google's GEMINI API ",
    tags=["Analysis"],
)
@base.route("/gen-all-analysis")
async def gen_all_analysis(url: str):
    """
    Getting analysis from all analysis functions available.

    @param url: The URL that will be used for analysis.
    """
    await asyncio.to_thread(rc_analysis, url)
    await asyncio.to_thread(sentiment_analysis, url)
    await asyncio.to_thread(prominent_analysis, url)
    current_data = await get_current_data(url)
    if current_data is not None:
        return {
            url: current_data.url,
            "masked-url": current_data.masked_url,
            "rc-analysis": current_data.rc_analysis,
            "sentiment-analysis": current_data.sentiment_analysis,
            "prominent_analysis": current_data.prominent_analysis,
        }


@docs(
    responses={200: "Analysis Done Successfully", 500: "Internal Server Error with error message"},
    description="This endpoint will perform Root Cause Analysis (5W1H) using Google's GEMINI API ",
    tags=["Analysis"],
)
@base.route("/gen-rc-analysis")
async def gen_rc_analysis(url: str):
    """
    Getting Root Cause Analysis.

    @param url: The URL that will be used for analysis.
    """
    await asyncio.to_thread(rc_analysis, url)
    current_data = await get_current_data(url)
    if current_data is not None:
        return {
            url: current_data.url,
            "masked-url": current_data.masked_url,
            "rc-analysis": current_data.rc_analysis,
        }
