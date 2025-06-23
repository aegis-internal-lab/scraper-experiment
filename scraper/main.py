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


def is_daemon_mode():
    """Check if running in daemon mode"""
    return os.getenv('DAEMON_MODE') == '1'


def setup_logging(log_file="news_scraper.log"):
    """Setup application logging"""
    # Clear any existing handlers
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # Always add file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Add console handler only if not in daemon mode
    if not is_daemon_mode():
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    root_logger.setLevel(logging.INFO)


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
        access_log=not is_daemon_mode(),  # Disable access log in daemon mode
    )
    server = uvicorn.Server(config)
    
    # Setup signal handlers for graceful shutdown
    shutdown_event = asyncio.Event()
    
    def signal_handler():
        logging.info("Received shutdown signal, stopping server...")
        shutdown_event.set()
        server.should_exit = True
    
    # Register signal handlers only if not in daemon mode (daemon handles its own signals)
    if not is_daemon_mode():
        for sig in (signal.SIGTERM, signal.SIGINT):
            signal.signal(sig, lambda s, f: signal_handler())
    
    try:
        # Start the server
        server_task = asyncio.create_task(server.serve())
        
        # Wait for shutdown signal or server completion
        done, pending = await asyncio.wait(
            [server_task, asyncio.create_task(shutdown_event.wait())],
            return_when=asyncio.FIRST_COMPLETED
        )
        
        # Cancel any remaining tasks
        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
                
        logging.info("Server shutdown complete")
        
    except asyncio.CancelledError:
        logging.info("Server cancelled")
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
    # Setup daemon-specific logging before daemonization
    os.environ['DAEMON_MODE'] = '1'
    
    # Open log files that will persist after daemonization
    log_file = open(DAEMON_LOG_FILE, 'a')
    
    # Create daemon context with proper file handling
    daemon_context = daemon.DaemonContext(
        working_directory=DAEMON_WORKING_DIR,
        pidfile=pidfile.TimeoutPIDLockFile(DAEMON_PID_FILE),
        stdin=open('/dev/null', 'r'),
        stdout=log_file,
        stderr=log_file,
        files_preserve=[log_file],  # Keep log file open
        detach_process=True,
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
            # Setup logging again after daemonization
            setup_logging(DAEMON_LOG_FILE)
            logging.info("Daemon started successfully")
            
            # Run the server with proper asyncio handling for daemon
            daemon_run_server()
    except Exception as e:
        logging.error(f"Daemon error: {e}")
        raise


def daemon_run_server():
    """Run server specifically for daemon mode with proper asyncio handling"""
    try:
        # Create a new event loop for the daemon process
        if hasattr(asyncio, 'set_event_loop_policy'):
            # Use a different event loop policy that works better with daemons
            asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(async_server())
        finally:
            # Clean shutdown
            pending = asyncio.all_tasks(loop)
            if pending:
                logging.info(f"Cancelling {len(pending)} pending tasks")
                for task in pending:
                    task.cancel()
                
                # Wait for all tasks to complete cancellation
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            
            loop.close()
            
    except KeyboardInterrupt:
        logging.info("Daemon shutdown requested")
    except Exception as e:
        logging.error(f"Daemon server error: {e}")
        raise


def stop_daemon():
    """Stop the daemon process"""
    is_running, pid = is_daemon_running()
    
    if not is_running:
        print("Daemon is not running")
        return False
    
    try:
        # Send SIGTERM to gracefully shutdown
        if pid is None:
            print("No valid PID found for daemon process.")
            return False
        print(f"Stopping daemon (PID: {pid})...")
        os.kill(pid, signal.SIGTERM)
        
        # Wait a bit and check if it's gone
        import time
        for i in range(30):  # Wait up to 30 seconds
            time.sleep(1)
            if not is_daemon_running()[0]:
                print("Daemon stopped successfully")
                return True
            if i % 5 == 0:  # Print progress every 5 seconds
                print(f"Waiting for daemon to stop... ({i+1}s)")
        
        # If still running, force kill
        if is_daemon_running()[0]:
            print("Daemon didn't stop gracefully, force killing...")
            if pid is not None:
                os.kill(pid, signal.SIGKILL)
                time.sleep(2)
            
            if is_daemon_running()[0]:
                print("Failed to stop daemon")
                return False
            else:
                print("Daemon force stopped")
                return True
        
        return True
        
    except (PermissionError, ProcessLookupError) as e:
        print(f"Error stopping daemon: {e}")
        return False


def is_daemon_running():
    """Check if daemon is currently running"""
    pid_file_path = Path(DAEMON_PID_FILE)
    
    if not pid_file_path.exists():
        return False, None
    
    try:
        with open(pid_file_path, 'r') as f:
            pid = int(f.read().strip())
        
        try:
            os.kill(pid, 0)  # Check if process exists
            return True, pid
        except OSError:
            # Process doesn't exist, remove stale PID file
            pid_file_path.unlink(missing_ok=True)
            return False, None
            
    except (ValueError, FileNotFoundError) as e:
        logging.error(f"Error reading PID file: {e}")
        return False, None


def daemon_status():
    """Check daemon status"""
    is_running, pid = is_daemon_running()
    
    if is_running:
        print(f"Daemon is running (PID: {pid})")
        return True
    else:
        print("Daemon is not running")
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


# For docker/module execution
def main():
    """Main entry point for module execution"""
    server()