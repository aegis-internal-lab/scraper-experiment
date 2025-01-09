import json
from blacksheep import  HTTPException, ok
from scraper.configs.models import Site
from scraper.configs.openapidocs import docs
from scraper.routes.routers import base
from tortoise.contrib.pydantic import pydantic_model_creator

@docs(
    responses={200: "Data fetched successfully", 404: "No items found", 500: "Internal Server Error with error message"},
    description="Fetch all data from the database.",
    tags=["Data"],
)
@base.get("/get-data/")
async def get_data():
    """
    Get All Data from the database
    """
    SitePydantic = pydantic_model_creator(Site, name="site_db")

    items = Site.all()
    if not await items:
        raise HTTPException(status=404, message="No items found")
    
    return ok(await SitePydantic.from_queryset(items))  