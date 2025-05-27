from blacksheep import json

from scraper.configs.openapidocs import docs
from scraper.routes.routers import base


@docs(
    responses={200: "Health check successful"},
    description="Health check endpoint to verify the service is running",
    tags=["Health"],
)
@base.get("/health")
async def health_check():
    """Health check endpoint"""
    return json({"status": "healthy", "message": "Scraper service is running"}, status=200)


@docs(
    responses={200: "Service information"},
    description="Get service information",
    tags=["Info"],
)
@base.get("/info")
async def service_info():
    """Get service information"""
    return json(
        {
            "name": "News Scraper API",
            "version": "0.1.0",
            "description": "A service for scraping news and performing AI analysis",
        },
        status=200,
    )
