from scraper.configs.models import Site


async def get_current_data(url: str):
    return await Site.filter(url=url).first()
