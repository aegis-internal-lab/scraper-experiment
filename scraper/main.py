import asyncio
import logging
import signal
import sys
import os
from pathlib import Path

import uvicorn
from blacksheep import Application
from tortoise.contrib.blacksheep import register_tortoise
import daemon
from daemon import pidfile

from scraper.configs.constants import DATABASE_URL
from scraper.configs.openapidocs import docs
from scraper.routes.routers import base

# Global app instance - created only once
_app_instance = None

# Daemon configuration
DAEMON_PID_FILE = "/tmp/scraper_daemon.pid"
DAEMON_LOG_FILE = "scraper_daemon.log"
DAEMON_WORKING_DIR = os.getcwd()


def setup_logging(log_file="news_scraper.log"):
    """Setup application logging"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler() if not os.getenv('DAEMON_MODE') else logging.NullHandler()
        ],
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


def daemon_server():
    """Run the server as a daemon process"""
    # Setup daemon-specific logging
    os.environ['DAEMON_MODE'] = '1'
    setup_logging(DAEMON_LOG_FILE)
    
    # Create daemon context
    daemon_context = daemon.DaemonContext(
        working_directory=DAEMON_WORKING_DIR,
        pidfile=pidfile.TimeoutPIDLockFile(DAEMON_PID_FILE),
        stdout=open(DAEMON_LOG_FILE, 'a'),
        stderr=open(DAEMON_LOG_FILE, 'a'),
    )
    
    # Setup signal handlers for daemon
    def terminate_handler(signum, frame):
        logging.info(f"Daemon received signal {signum}, shutting down...")
        sys.exit(0)
    
    daemon_context.signal_map = {
        signal.SIGTERM: terminate_handler,
        signal.SIGINT: terminate_handler,
    }
    
    try:
        logging.info("Starting daemon...")
        with daemon_context:
            logging.info("Daemon started successfully")
            server()
    except Exception as e:
        logging.error(f"Daemon error: {e}")
        raise


def stop_daemon():
    """Stop the daemon process"""
    pid_file_path = Path(DAEMON_PID_FILE)
    
    if not pid_file_path.exists():
        print("Daemon is not running (no PID file found)")
        return False
    
    try:
        with open(pid_file_path, 'r') as f:
            pid = int(f.read().strip())
        
        # Check if process is actually running
        try:
            os.kill(pid, 0)  # This doesn't kill, just checks if process exists
        except OSError:
            print(f"Process {pid} not found, removing stale PID file")
            pid_file_path.unlink()
            return False
        
        # Send SIGTERM to gracefully shutdown
        print(f"Stopping daemon (PID: {pid})...")
        os.kill(pid, signal.SIGTERM)
        
        # Wait a bit and check if it's gone
        import time
        for _ in range(10):  # Wait up to 10 seconds
            try:
                os.kill(pid, 0)
                time.sleep(1)
            except OSError:
                print("Daemon stopped successfully")
                return True
        
        # If still running, force kill
        print("Daemon didn't stop gracefully, force killing...")
        os.kill(pid, signal.SIGKILL)
        print("Daemon force stopped")
        return True
        
    except (ValueError, FileNotFoundError, PermissionError) as e:
        print(f"Error stopping daemon: {e}")
        return False


def daemon_status():
    """Check daemon status"""
    pid_file_path = Path(DAEMON_PID_FILE)
    
    if not pid_file_path.exists():
        print("Daemon is not running (no PID file)")
        return False
    
    try:
        with open(pid_file_path, 'r') as f:
            pid = int(f.read().strip())
        
        try:
            os.kill(pid, 0)  # Check if process exists
            print(f"Daemon is running (PID: {pid})")
            return True
        except OSError:
            print(f"Daemon PID file exists but process {pid} is not running")
            print("Removing stale PID file...")
            pid_file_path.unlink()
            return False
            
    except (ValueError, FileNotFoundError) as e:
        print(f"Error checking daemon status: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "daemon":
            daemon_server()
        elif command == "stop":
            stop_daemon()
        elif command == "status":
            daemon_status()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: daemon, stop, status")
    else:
        server()