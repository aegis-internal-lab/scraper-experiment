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
