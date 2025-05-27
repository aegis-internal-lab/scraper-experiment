from typing import Callable

from blacksheep import Request, Response, json
from blacksheep.server.application import Application

from scraper.libs.logger import setup_logger

logger = setup_logger(__name__)


async def error_handler_middleware(request: Request, handler: Callable) -> Response:
    """Global error handling middleware"""
    try:
        return await handler(request)
    except Exception as e:
        logger.error(f"Unhandled error in request {request.url}: {e}")
        return json(
            {
                "error": "Internal Server Error",
                "message": "An unexpected error occurred",
                "status_code": 500,
            },
            status=500,
        )


async def logging_middleware(request: Request, handler: Callable) -> Response:
    """Request logging middleware"""
    logger.info(f"Request: {request.method} {request.url}")
    response = await handler(request)
    logger.info(f"Response: {response.status}")
    return response


def setup_middleware(app: Application):
    """Setup application middleware"""
    app.middlewares.append(logging_middleware)
    app.middlewares.append(error_handler_middleware)
