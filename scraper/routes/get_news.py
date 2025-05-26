from blacksheep import HTTPException, json

from scraper.configs.models import Status
from scraper.configs.openapidocs import docs
from scraper.routes.routers import base
from scraper.services.news_service import NewsService


@docs(
    responses={
        200: "News fetched successfully",
        400: "Bad request - invalid parameters",
        500: "Internal Server Error",
    },
    description="This endpoint will fetch news from Google News based on the keywords provided",
    tags=["News"],
)
@base.get("/get-news/")
async def get_news(keyword: str, use_rca: bool = False):
    """
    Getting news list from Google News

    @param keyword: The keywords to search
    @param use_rca: Use Root Cause Analysis
    """
    try:
        # Validate input
        if not keyword or len(keyword.strip()) == 0:
            raise HTTPException(status=400, message="Keyword cannot be empty")

        # Get service and fetch news
        news_service = NewsService()
        result = await news_service.get_news_by_keyword(keyword.strip(), use_rca)

        if result.status == Status.ERROR:
            raise HTTPException(status=500, message=result.message)

        return json({"message": result.message, "status": result.status.value}, status=200)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status=500, message=f"Unexpected error: {str(e)}")
