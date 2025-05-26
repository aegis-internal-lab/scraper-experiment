import asyncio
import logging
import os

import daemon
import uvicorn
from blacksheep import Application
from tortoise.contrib.blacksheep import register_tortoise

from scraper.configs.constants import DATABASE_URL
from scraper.configs.openapidocs import docs
from scraper.routes.routers import base


def setup_logging():
    """Setup application logging"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("news_scraper.log"), logging.StreamHandler()],
    )


def create_app():
    """Create and configure the BlackSheep application"""
    setup_logging()

    app = Application(router=base)
    docs.bind_app(app)

    register_tortoise(
        app,
        db_url=DATABASE_URL,
        modules={"models": ["scraper.configs.models"]},
        generate_schemas=True,
    )

    # Add error handlers
    @app.exception_handler(404)
    async def not_found_handler(app, request, exception):
        from blacksheep import json
        return json({"error": "Not Found", "message": str(exception), "status_code": 404}, status=404)

    @app.exception_handler(500)
    async def server_error_handler(app, request, exception):
        from blacksheep import json
        logging.error(f"Server error: {exception}")
        return json({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "status_code": 500,
        }, status=500)

    return app


# Create app instance for ASGI server
app = create_app()


def server():
    """Start the server"""
    config = uvicorn.Config(
        "scraper.main:create_app",
        port=5000,
        log_level="info",
        reload=False,
        host="0.0.0.0",
        factory=True,
    )
    server = uvicorn.Server(config)

    if asyncio.get_event_loop().is_running():
        asyncio.create_task(server.serve())
    else:
        asyncio.run(server.serve())


def run_as_daemon():
    """Run the server as a daemon"""
    with daemon.DaemonContext(
        working_directory=os.getcwd(),
        stdout=open("/tmp/app_stdout.log", "a"),
        stderr=open("/tmp/app_stderr.log", "a"),
    ):
        server()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "daemon":
        run_as_daemon()
    else:
        server()
