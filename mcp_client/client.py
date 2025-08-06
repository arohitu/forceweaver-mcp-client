#!/usr/bin/env python3
"""
ForceWeaver MCP Client
Professional MCP client for ForceWeaver Revenue Cloud health checking service.
"""
import asyncio
import logging
import os
import sys
import time
import aiohttp
from typing import Optional, List, Dict, Any
from mcp.server.fastmcp import FastMCP

from .exceptions import ForceWeaverError, AuthenticationError, ConnectionError

# Version info
VERSION = "1.1.0"
API_BASE_URL = os.environ.get("FORCEWEAVER_API_URL", "https://mcp.forceweaver.com")

# Configure logging to stderr (MCP best practice)
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("ForceWeaver MCP Client")

class ForceWeaverMCPClient:
    """Enhanced client for ForceWeaver cloud services with proper error handling"""
    
    def __init__(self, api_base_url: str = API_BASE_URL):
        self.api_base_url = api_base_url.rstrip('/')
        self.session = None
        self.timeout = aiohttp.ClientTimeout(total=120)
    
    async def _get_session(self):
        """Get or create HTTP session with proper SSL handling"""
        if not self.session or self.session.closed:
            import ssl
            import certifi
            
            # Proper SSL context as per security best practices
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            connector = aiohttp.TCPConnector(
                ssl=ssl_context,
                limit=10, 
                ttl_dns_cache=300,
                use_dns_cache=True
            )
            
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=self.timeout,
                headers={'User-Agent': f'ForceWeaver-MCP-Client/{VERSION}'}
            )
        return self.session
    
    async def call_mcp_api(self, endpoint: str, method: str = "POST", **params) -> str:
        """Call ForceWeaver API with comprehensive error handling"""
        session = await self._get_session()
        
        # Extract API key for authorization
        api_key = params.get('forceweaver_api_key')
        if not api_key:
            logger.error("Missing API key in request")
            raise AuthenticationError("ForceWeaver API key is required")
        
        # Remove API key from params (it goes in header)
        request_params = {k: v for k, v in params.items() if k != 'forceweaver_api_key'}
        
        try:
            # Add MCP format parameter for AI-friendly responses
            url = f"{self.api_base_url}/api/v1.0/{endpoint}?format=mcp"
            headers = {"Authorization": f"Bearer {api_key}"}
            
            logger.info(f"Calling ForceWeaver API: {endpoint}")
            start_time = time.time()
            
            # Call appropriate HTTP method
            if method.upper() == "GET":
                async with session.get(url, headers=headers) as response:
                    return await self._process_response(response, start_time, endpoint)
            else:
                async with session.post(url, json=request_params, headers=headers) as response:
                    return await self._process_response(response, start_time, endpoint)
        
        except asyncio.TimeoutError:
            logger.error(f"Timeout calling {endpoint}")
            raise ConnectionError("Request timeout - the health check took too long to complete")
        
        except aiohttp.ClientError as e:
            logger.error(f"Connection error calling {endpoint}: {e}")
            raise ConnectionError(f"Connection error: {str(e)}")
        
        except (AuthenticationError, ConnectionError, ForceWeaverError):
            # Re-raise our own exceptions as-is
            raise
        
        except Exception as e:
            logger.error(f"Unexpected error calling {endpoint}: {e}")
            raise ForceWeaverError(f"Unexpected error: {str(e)}")
    
    async def _process_response(self, response, start_time, endpoint):
        """Process API response with detailed error handling"""
        execution_time = int((time.time() - start_time) * 1000)
        logger.info(f"API call to {endpoint} completed in {execution_time}ms (HTTP {response.status})")
        
        if response.status == 200:
            result = await response.json()
            
            # Return formatted output if available
            if "formatted_output" in result:
                return result["formatted_output"]
            elif "success" in result and result["success"]:
                return str(result.get("data", result))
            else:
                raise ForceWeaverError(f"API Error: {result.get('message', 'Unknown error')}")
        
        elif response.status == 401:
            raise AuthenticationError(
                "❌ Authentication Failed\n\n" +
                "Your ForceWeaver API key is invalid or expired.\n" +
                "Please check your key at: https://mcp.forceweaver.com/dashboard/keys"
            )
        
        elif response.status == 403:
            raise AuthenticationError(
                "❌ Access Denied\n\n" +
                "Your subscription doesn't include this feature.\n" +
                "Upgrade at: https://mcp.forceweaver.com/dashboard/billing"
            )
        
        elif response.status == 429:
            raise ForceWeaverError(
                "❌ Rate Limited\n\n" +
                "You've exceeded your usage limits.\n" +
                "Check your usage at: https://mcp.forceweaver.com/dashboard/usage"
            )
        
        elif response.status == 404:
            raise ForceWeaverError(
                "❌ Salesforce Org Not Found\n\n" +
                "The specified Salesforce org was not found in your account.\n" +
                "Add it at: https://mcp.forceweaver.com/dashboard/orgs"
            )
        
        else:
            error_text = await response.text()
            raise ForceWeaverError(
                f"❌ Service Error (HTTP {response.status})\n\n" +
                f"{error_text}\n\nContact support: https://mcp.forceweaver.com/support"
            )
    
    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()

# Global client instance
client = ForceWeaverMCPClient()

@mcp.tool()
async def revenue_cloud_health_check(
    forceweaver_api_key: str,
    salesforce_org_id: str,
    check_types: Optional[List[str]] = None,
    api_version: Optional[str] = None
) -> str:
    """
    Perform comprehensive Salesforce Revenue Cloud health check and analysis.
    
    Performs advanced analysis of your Salesforce org including:
    - Organization setup and configuration validation  
    - Sharing model analysis for PCM objects
    - Bundle hierarchy and dependency analysis
    - Attribute picklist integrity validation
    
    Args:
        forceweaver_api_key: Your ForceWeaver API key from https://mcp.forceweaver.com/dashboard/keys
        salesforce_org_id: Your Salesforce org identifier (from connected orgs)
        check_types: Optional list of specific checks to run (default: all basic checks)
        api_version: Optional Salesforce API version (default: v64.0)
    
    Returns:
        Comprehensive health report with scores, findings, and recommendations
    """
    logger.info(f"Starting health check for org: {salesforce_org_id}")
    
    return await client.call_mcp_api(
        "health/check",
        method="POST",
        forceweaver_api_key=forceweaver_api_key,
        salesforce_org_id=salesforce_org_id,
        check_types=check_types or ["basic_org_info", "sharing_model", "bundle_analysis"],
        api_version=api_version or "v64.0"
    )

@mcp.tool()
async def get_detailed_bundle_analysis(
    forceweaver_api_key: str,
    salesforce_org_id: str,
    api_version: Optional[str] = None
) -> str:
    """
    Get detailed Revenue Cloud bundle hierarchy analysis with comprehensive statistics.
    
    Provides in-depth analysis including:
    - Number of bundle products analyzed
    - Component count statistics across all bundles
    - Bundle hierarchy depth analysis  
    - Circular dependency detection with resolution paths
    - Bundle complexity metrics and performance impact analysis
    
    Args:
        forceweaver_api_key: Your ForceWeaver API key
        salesforce_org_id: Your Salesforce org identifier
        api_version: Optional Salesforce API version (default: v64.0)
    
    Returns:
        Detailed bundle analysis report with comprehensive statistics
    """
    logger.info(f"Starting detailed bundle analysis for org: {salesforce_org_id}")
    
    return await client.call_mcp_api(
        "health/check",
        method="POST",
        forceweaver_api_key=forceweaver_api_key,
        salesforce_org_id=salesforce_org_id,
        check_types=["bundle_analysis"],
        api_version=api_version or "v64.0"
    )

@mcp.tool()
async def list_available_orgs(forceweaver_api_key: str) -> str:
    """
    List all Salesforce organizations connected to your ForceWeaver account.
    
    Args:
        forceweaver_api_key: Your ForceWeaver API key
    
    Returns:
        List of connected Salesforce organizations
    """
    logger.info("Listing available orgs")
    
    return await client.call_mcp_api(
        "orgs/list",
        method="GET",
        forceweaver_api_key=forceweaver_api_key
    )

@mcp.tool()
async def get_usage_summary(forceweaver_api_key: str) -> str:
    """
    Get current usage statistics and subscription status.
    
    Args:
        forceweaver_api_key: Your ForceWeaver API key
    
    Returns:
        Usage summary and subscription status
    """
    logger.info("Getting usage summary")
    
    return await client.call_mcp_api(
        "usage/summary",
        method="GET",
        forceweaver_api_key=forceweaver_api_key
    )

# Cleanup on shutdown
async def cleanup():
    """Cleanup resources on shutdown"""
    logger.info("Shutting down ForceWeaver MCP Client")
    await client.close()

def main():
    """Main entry point supporting both STDIO and HTTP transports"""
    logger.info(f"Starting ForceWeaver MCP Client v{VERSION}")
    logger.info("Connecting to ForceWeaver cloud services...")
    logger.info("Get your API key at: https://mcp.forceweaver.com/dashboard/keys")
    
    # Determine transport from command line args or environment
    transport = "stdio"  # Default
    if len(sys.argv) > 1:
        if "--http" in sys.argv:
            transport = "http"
        elif "--stdio" in sys.argv:
            transport = "stdio"
    
    # Override from environment
    transport = os.environ.get("MCP_TRANSPORT", transport)
    
    logger.info(f"Using {transport} transport")
    
    try:
        if transport == "http":
            # HTTP transport for remote server hosting
            port = int(os.environ.get("MCP_PORT", "8000"))
            logger.info(f"Starting HTTP server on port {port}")
            mcp.run(transport="http", port=port)
        else:
            # STDIO transport for local clients
            mcp.run(transport="stdio")
            
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Server error: {e}")
    finally:
        asyncio.run(cleanup())

if __name__ == "__main__":
    main()