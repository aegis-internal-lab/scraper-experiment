from blacksheep import json

from scraper.configs.openapidocs import docs
from scraper.libs.rotation_utils import get_rotation_status
from scraper.routes.routers import base


@docs(
    responses={200: "Rotation status information"},
    description="Get current rotation and anti-detection configuration status",
    tags=["Status"],
)
@base.get("/status/rotation")
async def rotation_status():
    """Get rotation and anti-detection status"""
    try:
        status = get_rotation_status()
        return json(status, status=200)
    except Exception as e:
        return json({"error": f"Failed to get rotation status: {str(e)}"}, status=500)


@docs(
    responses={200: "Proxy validation results"},
    description="Validate proxy configuration and test connectivity",
    tags=["Status"],
)
@base.get("/status/proxy")
async def proxy_validation():
    """Validate proxy configuration"""
    try:
        from scraper.libs.proxy_utils import validate_proxy_configuration
        
        is_valid, status = validate_proxy_configuration()
        return json({
            "valid": is_valid,
            "details": status
        }, status=200)
    except Exception as e:
        return json({"error": f"Failed to validate proxy: {str(e)}"}, status=500)
