"""
Test suite for ForceWeaver MCP Client
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from forceweaver_mcp_client import ForceWeaverMCPClient
from forceweaver_mcp_client.exceptions import (
    ForceWeaverError,
    AuthenticationError,
    ConnectionError
)

class TestForceWeaverMCPClient:
    """Test cases for ForceWeaver MCP Client"""
    
    @pytest.fixture
    def client(self):
        """Create a test client instance"""
        return ForceWeaverMCPClient()
    
    @pytest.fixture
    def mock_session_response(self):
        """Create a mock HTTP response"""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "success": True,
            "formatted_output": "Test health check output"
        })
        return mock_response
    
    @pytest.mark.asyncio
    async def test_client_initialization(self, client):
        """Test client initialization"""
        assert client.api_base_url == "https://mcp.forceweaver.com"
        assert client.session is None
        assert client.timeout.total == 120
    
    @pytest.mark.asyncio
    async def test_session_creation(self, client):
        """Test HTTP session creation"""
        session = await client._get_session()
        assert session is not None
        assert client.session is not None
        await client.close()
    
    @pytest.mark.asyncio
    async def test_missing_api_key_error(self, client):
        """Test error when API key is missing"""
        with pytest.raises(AuthenticationError) as exc_info:
            await client.call_mcp_api("health/check")
        
        assert "ForceWeaver API key is required" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_successful_api_call(self, client, mock_session_response):
        """Test successful API call"""
        with patch.object(client, '_get_session') as mock_get_session:
            mock_session = AsyncMock()
            mock_session.post.return_value.__aenter__.return_value = mock_session_response
            mock_get_session.return_value = mock_session
            
            result = await client.call_mcp_api(
                "health/check",
                forceweaver_api_key="fk_test_key",
                org_id="test_org"
            )
            
            assert result == "Test health check output"
            mock_session.post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_authentication_error_response(self, client):
        """Test authentication error handling"""
        mock_response = AsyncMock()
        mock_response.status = 401
        mock_response.text = AsyncMock(return_value="Unauthorized")
        
        with patch.object(client, '_get_session') as mock_get_session:
            mock_session = AsyncMock()
            mock_session.post.return_value.__aenter__.return_value = mock_response
            mock_get_session.return_value = mock_session
            
            with pytest.raises(AuthenticationError) as exc_info:
                await client.call_mcp_api(
                    "health/check",
                    forceweaver_api_key="fk_invalid_key"
                )
            
            assert "Authentication Failed" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_rate_limit_error_response(self, client):
        """Test rate limit error handling"""
        mock_response = AsyncMock()
        mock_response.status = 429
        mock_response.text = AsyncMock(return_value="Rate Limited")
        
        with patch.object(client, '_get_session') as mock_get_session:
            mock_session = AsyncMock()
            mock_session.post.return_value.__aenter__.return_value = mock_response
            mock_get_session.return_value = mock_session
            
            with pytest.raises(ForceWeaverError) as exc_info:
                await client.call_mcp_api(
                    "health/check",
                    forceweaver_api_key="fk_test_key"
                )
            
            assert "Rate Limited" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_connection_timeout(self, client):
        """Test connection timeout handling"""
        with patch.object(client, '_get_session') as mock_get_session:
            mock_session = AsyncMock()
            mock_session.post.side_effect = asyncio.TimeoutError()
            mock_get_session.return_value = mock_session
            
            with pytest.raises(ConnectionError) as exc_info:
                await client.call_mcp_api(
                    "health/check",
                    forceweaver_api_key="fk_test_key"
                )
            
            assert "Request timeout" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_client_cleanup(self, client):
        """Test client cleanup"""
        # Create session
        await client._get_session()
        assert client.session is not None
        
        # Close client
        await client.close()
        
        # Session should be closed
        assert client.session.closed

class TestMCPTools:
    """Test cases for MCP tools"""
    
    @pytest.mark.asyncio
    async def test_revenue_cloud_health_check_tool(self):
        """Test revenue cloud health check tool"""
        from forceweaver_mcp_client.client import revenue_cloud_health_check
        
        with patch('forceweaver_mcp_client.client.client') as mock_client:
            mock_client.call_mcp_api = AsyncMock(return_value="Health check result")
            
            result = await revenue_cloud_health_check(
                forceweaver_api_key="fk_test_key",
                salesforce_org_id="test_org"
            )
            
            assert result == "Health check result"
            mock_client.call_mcp_api.assert_called_once_with(
                "health/check",
                method="POST",
                forceweaver_api_key="fk_test_key",
                org_id="test_org",
                check_types=["basic_org_info", "sharing_model", "bundle_analysis"],
                api_version="v64.0"
            )
    
    @pytest.mark.asyncio
    async def test_bundle_analysis_tool(self):
        """Test detailed bundle analysis tool"""
        from forceweaver_mcp_client.client import get_detailed_bundle_analysis
        
        with patch('forceweaver_mcp_client.client.client') as mock_client:
            mock_client.call_mcp_api = AsyncMock(return_value="Bundle analysis result")
            
            result = await get_detailed_bundle_analysis(
                forceweaver_api_key="fk_test_key",
                salesforce_org_id="test_org"
            )
            
            assert result == "Bundle analysis result"
            mock_client.call_mcp_api.assert_called_once_with(
                "health/check",
                method="POST",
                forceweaver_api_key="fk_test_key",
                org_id="test_org",
                check_types=["bundle_analysis"],
                api_version="v64.0"
            )
    
    @pytest.mark.asyncio
    async def test_list_orgs_tool(self):
        """Test list organizations tool"""
        from forceweaver_mcp_client.client import list_available_orgs
        
        with patch('forceweaver_mcp_client.client.client') as mock_client:
            mock_client.call_mcp_api = AsyncMock(return_value="Organizations list")
            
            result = await list_available_orgs(
                forceweaver_api_key="fk_test_key",
                username="test@example.com"
            )
            
            assert result == "Organizations list"
            mock_client.call_mcp_api.assert_called_once_with(
                "orgs/list",
                method="POST",
                forceweaver_api_key="fk_test_key",
                username="test@example.com"
            )
    
    @pytest.mark.asyncio
    async def test_usage_summary_tool(self):
        """Test usage summary tool"""
        from forceweaver_mcp_client.client import get_usage_summary
        
        with patch('forceweaver_mcp_client.client.client') as mock_client:
            mock_client.call_mcp_api = AsyncMock(return_value="Usage summary")
            
            result = await get_usage_summary(
                forceweaver_api_key="fk_test_key"
            )
            
            assert result == "Usage summary"
            mock_client.call_mcp_api.assert_called_once_with(
                "usage",
                method="GET",
                forceweaver_api_key="fk_test_key"
            )