"""
Test suite for ForceWeaver MCP Client
"""
import os
import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from aioresponses import aioresponses
from src import ForceWeaverMCPClient
from src.exceptions import (
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
    async def test_successful_api_call(self, client):
        """Test successful API call"""
        with aioresponses() as m:
            m.post(
                'https://mcp.forceweaver.com/api/v1.0/health/check?format=mcp',
                payload={'formatted_output': 'Test health check output'}
            )
            
            result = await client.call_mcp_api(
                "health/check",
                forceweaver_api_key="fk_test_key",
                salesforce_org_id="test_org"
            )
            
            assert result == "Test health check output"
    
    @pytest.mark.asyncio
    async def test_authentication_error_response(self, client):
        """Test authentication error handling"""
        with aioresponses() as m:
            m.post(
                'https://mcp.forceweaver.com/api/v1.0/health/check?format=mcp',
                status=401,
                payload={'error': 'Unauthorized'}
            )
            
            with pytest.raises(AuthenticationError) as exc_info:
                await client.call_mcp_api(
                    "health/check",
                    forceweaver_api_key="fk_invalid_key"
                )
            
            assert "Authentication Failed" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_rate_limit_error_response(self, client):
        """Test rate limit error handling"""
        with aioresponses() as m:
            m.post(
                'https://mcp.forceweaver.com/api/v1.0/health/check?format=mcp',
                status=429,
                payload={'error': 'Rate Limited'}
            )
            
            with pytest.raises(ForceWeaverError) as exc_info:
                await client.call_mcp_api(
                    "health/check",
                    forceweaver_api_key="fk_test_key"
                )
            
            assert "Rate Limited" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_connection_timeout(self, client):
        """Test connection timeout handling"""
        with aioresponses() as m:
            m.post(
                'https://mcp.forceweaver.com/api/v1.0/health/check?format=mcp',
                exception=asyncio.TimeoutError()
            )
            
            with pytest.raises(ConnectionError) as exc_info:
                await client.call_mcp_api(
                    "health/check",
                    forceweaver_api_key="fk_test_key"
                )
            
            assert "Request timeout" in str(exc_info.value)
    
    
    @pytest.mark.asyncio
    async def test_access_denied_error_response(self, client):
        """Test access denied error handling"""
        with aioresponses() as m:
            m.post(
                'https://mcp.forceweaver.com/api/v1.0/health/check?format=mcp',
                status=403,
                payload={'error': 'Access Denied'}
            )
            
            with pytest.raises(AuthenticationError) as exc_info:
                await client.call_mcp_api(
                    "health/check",
                    forceweaver_api_key="fk_test_key"
                )
            
            assert "Access Denied" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_not_found_error_response(self, client):
        """Test not found error handling"""
        with aioresponses() as m:
            m.post(
                'https://mcp.forceweaver.com/api/v1.0/health/check?format=mcp',
                status=404,
                payload={'error': 'Not Found'}
            )
            
            with pytest.raises(ForceWeaverError) as exc_info:
                await client.call_mcp_api(
                    "health/check",
                    forceweaver_api_key="fk_test_key"
                )
            
            assert "Salesforce Org Not Found" in str(exc_info.value)
            
    @pytest.mark.asyncio
    async def test_server_error_response(self, client):
        """Test server error handling"""
        with aioresponses() as m:
            m.post(
                'https://mcp.forceweaver.com/api/v1.0/health/check?format=mcp',
                status=500,
                payload={'error': 'Internal Server Error'}
            )
            
            with pytest.raises(ForceWeaverError) as exc_info:
                await client.call_mcp_api(
                    "health/check",
                    forceweaver_api_key="fk_test_key"
                )
            
            assert "Service Error (HTTP 500)" in str(exc_info.value)
            
    @pytest.mark.asyncio
    async def test_successful_api_call_with_custom_formatting(self, client):
        """Test successful API call with custom formatting"""
        with aioresponses() as m:
            m.post(
                'https://mcp.forceweaver.com/api/v1.0/health/check?format=mcp',
                payload={
                    "success": True, 
                    "results": {"results": {}}, 
                    "summary": {"overall_score": 95}
                }
            )
            
            result = await client.call_mcp_api(
                "health/check",
                forceweaver_api_key="fk_test_key",
                salesforce_org_id="test_org"
            )
            
            assert "Overall Health Score: 95%" in result

    def test_get_grade(self, client):
        """Test grade calculation"""
        assert client._get_grade(95) == "A+"
        assert client._get_grade(85) == "A"
        assert client._get_grade(75) == "B"
        assert client._get_grade(65) == "C"
        assert client._get_grade(55) == "D"
        assert client._get_grade(45) == "F"

    def test_format_health_check_response(self, client):
        """Test health check response formatting"""
        sample_response = {
            "org_id": "test_org",
            "summary": {
                "overall_score": 88,
                "execution_time_ms": 1200,
                "cost_cents": 2,
                "checks_performed": 1
            },
            "results": {
                "results": {
                    "bundle_analysis": {
                        "status": "healthy",
                        "score": 100,
                        "details": ["No issues found"]
                    }
                }
            }
        }
        
        formatted_string = client._format_health_check_response(sample_response)
        
        assert "Overall Health Score: 88%" in formatted_string
        assert "Bundle Analysis" in formatted_string
        assert "No issues found" in formatted_string
    
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

    @pytest.mark.asyncio
    @patch.dict(os.environ, {"FORCEWEAVER_API_KEY": "fk_env_key", "SALESFORCE_ORG_ID": "env_org"})
    async def test_revenue_cloud_health_check_tool_with_env_vars(self):
        """Test health check tool with environment variables"""
        from src.server import revenue_cloud_health_check
        
        with patch('src.server.client') as mock_client:
            mock_client.call_mcp_api = AsyncMock(return_value="Health check result")
            
            await revenue_cloud_health_check()
            
            mock_client.call_mcp_api.assert_called_once_with(
                "health/check",
                method="POST",
                forceweaver_api_key="fk_env_key",
                org_id="env_org",
                check_types=["basic_org_info", "sharing_model", "bundle_analysis"],
                api_version="v64.0"
            )
            
    @pytest.mark.asyncio
    async def test_revenue_cloud_health_check_tool_missing_credentials(self):
        """Test health check tool with missing credentials"""
        from src.server import revenue_cloud_health_check
        
        with pytest.raises(AuthenticationError) as exc_info:
            await revenue_cloud_health_check()
            
        assert "API key is missing" in str(exc_info.value)
        
    @pytest.mark.asyncio
    async def test_bundle_analysis_tool_missing_credentials(self):
        """Test bundle analysis tool with missing credentials"""
        from src.server import get_detailed_bundle_analysis
        
        with pytest.raises(AuthenticationError) as exc_info:
            await get_detailed_bundle_analysis()
            
        assert "API key is required" in str(exc_info.value)
        
    @pytest.mark.asyncio
    async def test_list_orgs_tool_missing_credentials(self):
        """Test list orgs tool with missing credentials"""
        from src.server import list_available_orgs
        
        with pytest.raises(AuthenticationError) as exc_info:
            await list_available_orgs()
            
        assert "API key is required" in str(exc_info.value)
        
    @pytest.mark.asyncio
    async def test_usage_summary_tool_missing_credentials(self):
        """Test usage summary tool with missing credentials"""
        from src.server import get_usage_summary
        
        with pytest.raises(AuthenticationError) as exc_info:
            await get_usage_summary()
            
        assert "API key is required" in str(exc_info.value)

class TestMain:
    """Test cases for main entry point"""
    
    @patch('src.server.mcp')
    @patch('src.server.sys.argv', ['server.py'])
    def test_main_stdio(self, mock_mcp):
        """Test main with stdio transport"""
        from src.server import main
        main()
        mock_mcp.run.assert_called_once_with(transport="stdio")
        
    @patch('src.server.mcp')
    @patch('src.server.sys.argv', ['server.py', '--http'])
    def test_main_http(self, mock_mcp):
        """Test main with http transport"""
        from src.server import main
        main()
        mock_mcp.run.assert_called_once_with(transport="http", port=8000)
        
    @patch('src.server.mcp')
    @patch.dict(os.environ, {"MCP_TRANSPORT": "http", "MCP_PORT": "9000"})
    @patch('src.server.sys.argv', ['server.py'])
    def test_main_http_with_env(self, mock_mcp):
        """Test main with http transport from environment variables"""
        from src.server import main
        main()
        mock_mcp.run.assert_called_once_with(transport="http", port=9000)

    """Test cases for MCP tools"""
    
    @pytest.mark.asyncio
    async def test_revenue_cloud_health_check_tool(self):
        """Test revenue cloud health check tool"""
        from src.server import revenue_cloud_health_check
        
        with patch('src.server.client') as mock_client:
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
        from src.server import get_detailed_bundle_analysis
        
        with patch('src.server.client') as mock_client:
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
        from src.server import list_available_orgs
        
        with patch('src.server.client') as mock_client:
            mock_client.call_mcp_api = AsyncMock(return_value="Organizations list")
            
            result = await list_available_orgs(
                forceweaver_api_key="fk_test_key"
            )
            
            assert result == "Organizations list"
            mock_client.call_mcp_api.assert_called_once_with(
                "orgs/list",
                method="GET",
                forceweaver_api_key="fk_test_key"
            )
    
    @pytest.mark.asyncio
    async def test_usage_summary_tool(self):
        """Test usage summary tool"""
        from src.server import get_usage_summary
        
        with patch('src.server.client') as mock_client:
            mock_client.call_mcp_api = AsyncMock(return_value="Usage summary")
            
            result = await get_usage_summary(
                forceweaver_api_key="fk_test_key"
            )
            
            assert result == "Usage summary"
            mock_client.call_mcp_api.assert_called_once_with(
                "usage/summary",
                method="GET",
                forceweaver_api_key="fk_test_key"
            )