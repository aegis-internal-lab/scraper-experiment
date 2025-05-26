from typing import Optional

from scraper.configs.models import Site


async def get_current_data(url: str) -> Optional[Site]:
    """
    Get site data by URL

    @deprecated: Use DataService.get_site_by_url() instead
    """
    return await Site.filter(url=url).first()


def validate_url(url: Optional[str]) -> bool:
    """Validate if URL format is correct"""
    if not url:  # Handle None, empty string, and other falsy values
        return False
    return url.startswith(("http://", "https://")) and len(url.strip()) > 0


def truncate_string(text: str, max_length: int = 30) -> str:
    """Truncate string with ellipsis if too long"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
