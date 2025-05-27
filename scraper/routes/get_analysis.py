from blacksheep import HTTPException, json

from scraper.configs.openapidocs import docs
from scraper.routes.routers import base
from scraper.services.analysis_service import AnalysisService
from scraper.services.data_service import DataService


@docs(
    responses={
        200: "Analysis Done Successfully",
        404: "URL not found",
        500: "Internal Server Error",
    },
    description=(
        "This endpoint will perform Root Cause Analysis (5W1H), "
        "Sentiment Analysis, and Prominent Analysis using Google's GEMINI API"
    ),
    tags=["Analysis"],
)
@base.get("/gen-all-analysis")
async def gen_all_analysis(url: str):
    """
    Getting analysis from all analysis functions available.

    @param url: The URL that will be used for analysis.
    """
    try:
        if not url or len(url.strip()) == 0:
            raise HTTPException(status=400, message="URL cannot be empty")

        # Check if URL exists in database
        data_service = DataService()
        if not await data_service.site_exists(url):
            raise HTTPException(status=404, message="URL not found in database")

        # Perform analysis
        analysis_service = AnalysisService()
        result = await analysis_service.generate_all_analysis(url)

        if result is None:
            raise HTTPException(status=404, message="No data found for the provided URL")

        return json(result, status=200)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status=500, message=f"Error performing analysis: {str(e)}")


@docs(
    responses={
        200: "Analysis Done Successfully",
        404: "URL not found",
        500: "Internal Server Error",
    },
    description="This endpoint will perform Root Cause Analysis (5W1H) using Google's GEMINI API ",
    tags=["Analysis"],
)
@base.get("/gen-rc-analysis")
async def gen_rc_analysis(url: str):
    """
    Getting Root Cause Analysis.

    @param url: The URL that will be used for analysis.
    """
    try:
        if not url or len(url.strip()) == 0:
            raise HTTPException(status=400, message="URL cannot be empty")

        # Check if URL exists in database
        data_service = DataService()
        site = await data_service.get_site_by_url(url)
        if not site:
            raise HTTPException(status=404, message="URL not found in database")

        # Perform RC analysis
        analysis_service = AnalysisService()
        await analysis_service.generate_root_cause_analysis(url)

        # Get updated data
        updated_site = await data_service.get_site_by_url(url)
        if not updated_site:
            raise HTTPException(status=404, message="Site data not found after analysis")

        return json(
            {
                "url": updated_site.url,
                "masked_url": updated_site.masked_url,
                "rc_analysis": updated_site.rc_analysis,
            },
            status=200,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status=500, message=f"Error performing RC analysis: {str(e)}")
