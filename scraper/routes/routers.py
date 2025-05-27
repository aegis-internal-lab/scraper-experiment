from blacksheep import Router

# Create the main router
base = Router()

# Import route modules to register them with the router
from scraper.routes import get_analysis, get_data, get_news  # noqa: F401, E402
from scraper.routes import health  # noqa: F401, E402
from scraper.routes import lyrics  # noqa: F401, E402
from scraper.routes import status  # noqa: F401, E402
