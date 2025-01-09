from blacksheep import json

from scraper.configs.models import Status
from scraper.configs.openapidocs import docs
from scraper.libs.get_news import get_news_list
from scraper.routes.routers import base


@docs(
    responses={200: "News fetched successfully", 500: "Internal Server Error with error message"},
    description="This endpoint will fetch news from Google News based on the keywords provided",
    tags=["News"],
)
@base.get("/get-news/")
async def get_news(keyword: str, use_rca: bool):
    """
    Getting news list from Google News

    @param keyword: The keywords to search
    @param use_rca: Use Root Cause Analysis
    """
    result = await get_news_list(keyword, use_rca)
    if result.status == Status.ERROR:
        return json({"message": result.message}, status=500)
    return json({"message": f"news-result: {result.message}"}, status=200)
