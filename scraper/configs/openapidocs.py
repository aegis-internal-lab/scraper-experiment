from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Contact, Info

docs = OpenAPIHandler(
    info=Info(title="Scraper REST API", version="0.0.1", contact=Contact(name="Dev Team"))
)
