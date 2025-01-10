import asyncio
import os

import daemon
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
        "scraper.main:create_app", port=5000, log_level="info", reload=False, host="0.0.0.0"
    )
    server = uvicorn.Server(config)

    if asyncio.get_event_loop().is_running():
        asyncio.create_task(server.serve())
    else:
        asyncio.run(server.serve())


def run_as_daemon():
    with daemon.DaemonContext(
        working_directory=os.getcwd(),  # Ensure it runs in the project directory
        stdout=open("/tmp/app_stdout.log", "a"),  # Redirect standard output
        stderr=open("/tmp/app_stderr.log", "a"),  # Redirect standard error
    ):
        server()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "daemon":
        run_as_daemon()
    else:
        server()
