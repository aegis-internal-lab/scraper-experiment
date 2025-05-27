import asyncio
import logging
import os
import signal

import daemon # type: ignore
import uvicorn
from blacksheep import Application
from tortoise.contrib.blacksheep import register_tortoise

from scraper.configs.constants import DATABASE_URL
from scraper.configs.openapidocs import docs
from scraper.routes.routers import base

# Global app instance - created only once
_app_instance = None


def setup_logging():
    """Setup application logging"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("news_scraper.log"), logging.StreamHandler()],
    )


def create_app():
    """Create and configure the BlackSheep application"""
    global _app_instance
    
    # Return existing app if already created
    if _app_instance is not None:
        return _app_instance
    
    setup_logging()

    app = Application(router=base)
    
    # Configure OpenAPI documentation
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

    # Store the app instance
    _app_instance = app
    return app


# Create app instance for ASGI server - only once at module level
app = create_app()


async def async_server():
    """Start the server with proper signal handling"""
    config = uvicorn.Config(
        "scraper.main:app",
        port=5000,
        log_level="info",
        reload=False,
        host="0.0.0.0",
        factory=False,
    )
    server = uvicorn.Server(config)
    
    # Setup signal handlers for graceful shutdown
    def signal_handler():
        logging.info("Received shutdown signal, stopping server...")
        server.should_exit = True
    
    # Register signal handlers
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda s, f: signal_handler())
    
    try:
        await server.serve()
    except asyncio.CancelledError:
        logging.info("Server shutdown complete")
    except Exception as e:
        logging.error(f"Server error: {e}")
        raise


def server():
    """Start the server with graceful shutdown handling"""
    try:
        asyncio.run(async_server())
    except KeyboardInterrupt:
        logging.info("Server shutdown requested by user")
    except Exception as e:
        logging.error(f"Server error: {e}")
        raise


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
