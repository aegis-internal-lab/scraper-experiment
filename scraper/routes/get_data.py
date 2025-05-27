from blacksheep import HTTPException, json

from scraper.configs.openapidocs import docs
from scraper.routes.routers import base
from scraper.services.data_service import DataService


@docs(
    responses={
        200: "Data fetched successfully",
        404: "No items found",
        500: "Internal Server Error with error message",
    },
    description="Fetch all data from the database.",
    tags=["Data"],
)
@base.get("/get-data/")
async def get_data():
    """
    Get All Data from the database
    """
    try:
        data_service = DataService()
        sites = await data_service.get_all_sites()

        if not sites:
            raise HTTPException(status=404, message="No items found")

        return json(sites, status=200)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status=500, message=f"Error fetching data: {str(e)}")


@docs(
    responses={
        200: "Site data fetched successfully",
        404: "Site not found",
        400: "Bad request - URL is required",
        500: "Internal Server Error",
    },
    description="Get a specific site by URL from the database.",
    tags=["Data"],
)
@base.get("/get-data/by-url")
async def get_site_by_url(url: str):
    """
    Get a specific site by URL

    @param url: The URL of the site to retrieve
    """
    try:
        if not url or len(url.strip()) == 0:
            raise HTTPException(status=400, message="URL parameter is required")

        data_service = DataService()
        site = await data_service.get_site_by_url(url.strip())

        if not site:
            raise HTTPException(status=404, message="Site not found")

        # Convert site to dictionary manually
        site_data = {
            "id": site.id,
            "title": site.title,
            "published_date": site.published_date.isoformat() if site.published_date else None,
            "keyword": site.keyword,
            "content": site.content,
            "masked_url": site.masked_url,
            "url": site.url,
            "is_extracted": site.is_extracted,
            "has_rc_analysis": site.has_rc_analysis,
            "rc_analysis": site.rc_analysis,
            "has_sentiment_analysis": site.has_sentiment_analysis,
            "sentiment_analysis": site.sentiment_analysis,
            "has_prominent_analysis": site.has_prominent_analysis,
            "prominent_analysis": site.prominent_analysis,
            "created_at": site.created_at.isoformat() if site.created_at else None,
            "updated_at": site.updated_at.isoformat() if site.updated_at else None,
        }

        return json(site_data, status=200)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status=500, message=f"Error fetching site data: {str(e)}")


@docs(
    responses={
        200: "Sites fetched successfully",
        404: "No sites found for the keyword",
        400: "Bad request - keyword is required",
        500: "Internal Server Error",
    },
    description="Get all sites that match a specific keyword.",
    tags=["Data"],
)
@base.get("/get-data/by-keyword")
async def get_sites_by_keyword(keyword: str):
    """
    Get all sites that match a specific keyword

    @param keyword: The keyword to search for
    """
    try:
        if not keyword or len(keyword.strip()) == 0:
            raise HTTPException(status=400, message="Keyword parameter is required")

        data_service = DataService()
        sites = await data_service.get_sites_by_keyword(keyword.strip())

        if not sites:
            raise HTTPException(status=404, message=f"No sites found for keyword: {keyword}")

        # Convert sites to dictionaries
        sites_data = [
            {
                "id": site.id,
                "title": site.title,
                "published_date": site.published_date.isoformat() if site.published_date else None,
                "keyword": site.keyword,
                "content": site.content,
                "masked_url": site.masked_url,
                "url": site.url,
                "is_extracted": site.is_extracted,
                "has_rc_analysis": site.has_rc_analysis,
                "rc_analysis": site.rc_analysis,
                "has_sentiment_analysis": site.has_sentiment_analysis,
                "sentiment_analysis": site.sentiment_analysis,
                "has_prominent_analysis": site.has_prominent_analysis,
                "prominent_analysis": site.prominent_analysis,
                "created_at": site.created_at.isoformat() if site.created_at else None,
                "updated_at": site.updated_at.isoformat() if site.updated_at else None,
            }
            for site in sites
        ]

        return json(sites_data, status=200)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status=500, message=f"Error fetching sites by keyword: {str(e)}")


@docs(
    responses={
        200: "Sites count fetched successfully",
        500: "Internal Server Error",
    },
    description="Get the total count of sites in the database.",
    tags=["Data"],
)
@base.get("/get-data/count")
async def get_sites_count():
    """
    Get the total count of sites in the database
    """
    try:
        data_service = DataService()
        count = await data_service.get_sites_count()

        return json({"total_sites": count}, status=200)

    except Exception as e:
        raise HTTPException(status=500, message=f"Error fetching sites count: {str(e)}")
