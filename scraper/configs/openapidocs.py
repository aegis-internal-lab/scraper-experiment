from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Contact, Info # type: ignore

# OpenAPI handler for route decorations - this creates the /docs and /openapi.json endpoints
docs = OpenAPIHandler(
    info=Info(title="Scraper REST API", version="0.6.1", contact=Contact(name="Dev Team")),
    ui_path="/docs",
    json_spec_path="/openapi.json"
)
