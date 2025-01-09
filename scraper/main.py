import asyncio

import uvicorn
from blacksheep import Application
from tortoise.contrib.blacksheep import register_tortoise

from scraper.configs.constants import DATABASE_URL
from scraper.configs.openapidocs import docs
from scraper.routes.routers import base


def create_app():
    app = Application(router=base)

    docs.bind_app(app)

    register_tortoise(
        app,
        db_url=DATABASE_URL,
        modules={"models": ["scraper.configs.models"]},
        generate_schemas=True,
    )
    return app


def server():
    config = uvicorn.Config(
        "scraper.main:create_app", port=5000, log_level="info", reload=True, host="0.0.0.0"
    )
    server = uvicorn.Server(config)

    if asyncio.get_event_loop().is_running():
        # If an event loop is already running, serve the application
        asyncio.create_task(server.serve())
    else:
        # Otherwise, run normally
        asyncio.run(server.serve())


if __name__ == "__main__":
    server()
