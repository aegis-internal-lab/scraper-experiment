import pytest
from unittest.mock import Mock, patch, AsyncMock

from scraper.services.data_service import DataService
from scraper.configs.models import Site


class TestDataService:
    """Test cases for DataService"""

    @pytest.mark.asyncio
    async def test_get_site_by_url_existing(self):
        """Test getting an existing site by URL"""
        # Mock the Site.filter method
        with patch.object(Site, 'filter') as mock_filter:
            mock_site = Mock()
            mock_site.url = "https://example.com"
            mock_query = Mock()
            mock_query.first = AsyncMock(return_value=mock_site)
            mock_filter.return_value = mock_query
            
            service = DataService()
            result = await service.get_site_by_url("https://example.com")
            
            assert result == mock_site
            mock_filter.assert_called_once_with(url="https://example.com")

    @pytest.mark.asyncio
    async def test_get_site_by_url_not_found(self):
        """Test getting a non-existing site by URL"""
        with patch.object(Site, 'filter') as mock_filter:
            mock_query = Mock()
            mock_query.first = AsyncMock(return_value=None)
            mock_filter.return_value = mock_query
            
            service = DataService()
            result = await service.get_site_by_url("https://nonexistent.com")
            
            assert result is None

    @pytest.mark.asyncio
    async def test_site_exists_true(self):
        """Test checking if site exists when it does"""
        with patch.object(Site, 'filter') as mock_filter:
            mock_query = Mock()
            mock_query.exists = AsyncMock(return_value=True)
            mock_filter.return_value = mock_query
            
            service = DataService()
            result = await service.site_exists("https://example.com")
            
            assert result is True

    @pytest.mark.asyncio
    async def test_site_exists_false(self):
        """Test checking if site exists when it doesn't"""
        with patch.object(Site, 'filter') as mock_filter:
            mock_query = Mock()
            mock_query.exists = AsyncMock(return_value=False)
            mock_filter.return_value = mock_query
            
            service = DataService()
            result = await service.site_exists("https://nonexistent.com")
            
            assert result is False
