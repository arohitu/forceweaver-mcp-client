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
            
            # DEBUG: Log what we actually receive
            logger.info(f"API Response keys: {list(result.keys())}")
            logger.info(f"Has formatted_output: {'formatted_output' in result}")
            if "formatted_output" in result:
                logger.info(f"formatted_output length: {len(result['formatted_output'])}")
            
            # Return formatted output if available (MCP format)
            if "formatted_output" in result:
                logger.info("Using formatted_output from backend")
                return result["formatted_output"]
            elif "success" in result and result["success"]:
                logger.info("Using custom formatting for raw JSON")
                # Format the raw JSON response for better display
                return self._format_health_check_response(result)
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
    
    def _format_health_check_response(self, result):
        """Format health check response for better display in chat"""
        lines = []
        
        # Header
        lines.append("🔍 **ForceWeaver Revenue Cloud Health Check Report**")
        lines.append("=" * 60)
        
        # Basic info
        if "org_id" in result:
            lines.append(f"📊 Organization: {result.get('org_name', result['org_id'])}")
        
        # Summary
        if "summary" in result:
            summary = result["summary"]
            lines.append(f"⏱️ Execution Time: {summary.get('execution_time_ms', 0)}ms")
            lines.append(f"📅 Generated: {result.get('timestamp', 'N/A')}")
            lines.append("")
            lines.append(f"🎯 **Overall Health Score: {summary.get('overall_score', 0)}%** (Grade: {self._get_grade(summary.get('overall_score', 0))})")
            lines.append("")
        
        # Results section
        if "results" in result and "results" in result["results"]:
            lines.append("### Results")
            lines.append("")
            
            for check_type, check_result in result["results"]["results"].items():
                lines.append(f"**{check_type.replace('_', ' ').title()}**")
                lines.append(f"Status: {check_result.get('status', 'unknown').upper()}")
                lines.append(f"Score: {check_result.get('score', 0)}%")
                
                if "details" in check_result:
                    lines.append("Details:")
                    for detail in check_result["details"]:
                        lines.append(f"  • {detail}")
                lines.append("")
        
        # Footer
        lines.append("---")
        if "summary" in result:
            lines.append(f"💰 Cost: {result['summary'].get('cost_cents', 0)}¢")
            lines.append(f"✅ Checks Performed: {result['summary'].get('checks_performed', 0)}")
        
        lines.append("")
        lines.append("For more detailed analysis or specific recommendations, please let me know!")
        
        return "\n".join(lines)
    
    def _get_grade(self, score):
        """Convert numeric score to letter grade"""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
        else:
            return "F"
    
    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()

# Global client instance
client = ForceWeaverMCPClient()

@mcp.tool()
async def revenue_cloud_health_check(
    forceweaver_api_key: Optional[str] = None,
    salesforce_org_id: Optional[str] = None,
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
        forceweaver_api_key: Your ForceWeaver API key (optional if set via environment)
        salesforce_org_id: Your Salesforce org identifier (optional if set via environment)
        check_types: Optional list of specific checks to run (default: all basic checks)
        api_version: Optional Salesforce API version (default: v64.0)
    
    Returns:
        Comprehensive health report with scores, findings, and recommendations
    """
    # Use environment variables as fallback
    api_key = forceweaver_api_key or os.environ.get("FORCEWEAVER_API_KEY")
    org_id = salesforce_org_id or os.environ.get("SALESFORCE_ORG_ID")
    
    # Enhanced debugging for credential issues
    logger.info(f"Revenue Cloud Health Check - API key provided as param: {bool(forceweaver_api_key)}")
    logger.info(f"Revenue Cloud Health Check - API key from env: {bool(os.environ.get('FORCEWEAVER_API_KEY'))}")
    logger.info(f"Revenue Cloud Health Check - Org ID provided as param: {bool(salesforce_org_id)}")
    logger.info(f"Revenue Cloud Health Check - Org ID from env: {bool(os.environ.get('SALESFORCE_ORG_ID'))}")
    logger.info(f"Revenue Cloud Health Check - Final API key available: {bool(api_key)}")
    logger.info(f"Revenue Cloud Health Check - Final org ID available: {bool(org_id)}")
    if api_key:
        logger.info(f"API key starts with: {api_key[:10]}...")
    
    if not api_key:
        logger.error("❌ API key missing in revenue_cloud_health_check")
        raise AuthenticationError("I cannot analyze your Revenue Cloud bundle structure because your ForceWeaver API key is missing, invalid, or expired. Please update your API key in the prompt or environment and try again. If you need help updating the key, let me know!")
    
    if not org_id:
        logger.error("❌ Org ID missing in revenue_cloud_health_check")  
        raise AuthenticationError("To analyze your Revenue Cloud bundle structure, I need your Salesforce org ID. Please provide your Salesforce org identifier so I can proceed with the analysis.")
    
    logger.info(f"Starting health check for org: {org_id}")
    
    return await client.call_mcp_api(
        "health/check",
        method="POST",
        forceweaver_api_key=api_key,
        org_id=org_id,  # Backend expects 'org_id', not 'salesforce_org_id'
        check_types=check_types or ["basic_org_info", "sharing_model", "bundle_analysis"],
        api_version=api_version or "v64.0"
    )

@mcp.tool()
async def get_detailed_bundle_analysis(
    forceweaver_api_key: Optional[str] = None,
    salesforce_org_id: Optional[str] = None,
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
        forceweaver_api_key: Your ForceWeaver API key (optional if set via environment)
        salesforce_org_id: Your Salesforce org identifier (optional if set via environment)
        api_version: Optional Salesforce API version (default: v64.0)
    
    Returns:
        Detailed bundle analysis report with comprehensive statistics
    """
    # Use environment variables as fallback
    api_key = forceweaver_api_key or os.environ.get("FORCEWEAVER_API_KEY")
    org_id = salesforce_org_id or os.environ.get("SALESFORCE_ORG_ID")
    
    if not api_key:
        raise AuthenticationError("ForceWeaver API key is required. Provide it as parameter or set FORCEWEAVER_API_KEY environment variable.")
    
    if not org_id:
        raise AuthenticationError("Salesforce Org ID is required. Provide it as parameter or set SALESFORCE_ORG_ID environment variable.")
    
    logger.info(f"Starting detailed bundle analysis for org: {org_id}")
    
    return await client.call_mcp_api(
        "health/check",
        method="POST",
        forceweaver_api_key=api_key,
        org_id=org_id,
        check_types=["bundle_analysis"],
        api_version=api_version or "v64.0"
    )

@mcp.tool()
async def list_available_orgs(forceweaver_api_key: Optional[str] = None) -> str:
    """
    List all Salesforce organizations connected to your ForceWeaver account.
    
    Args:
        forceweaver_api_key: Your ForceWeaver API key (optional if set via environment)
    
    Returns:
        List of connected Salesforce organizations
    """
    # Use environment variable as fallback
    api_key = forceweaver_api_key or os.environ.get("FORCEWEAVER_API_KEY")
    
    if not api_key:
        raise AuthenticationError("ForceWeaver API key is required. Provide it as parameter or set FORCEWEAVER_API_KEY environment variable.")
    
    logger.info("Listing available orgs")
    
    return await client.call_mcp_api(
        "orgs/list",
        method="GET",
        forceweaver_api_key=api_key
    )

@mcp.tool()
async def get_usage_summary(forceweaver_api_key: Optional[str] = None) -> str:
    """
    Get current usage statistics and subscription status.
    
    Args:
        forceweaver_api_key: Your ForceWeaver API key (optional if set via environment)
    
    Returns:
        Usage summary and subscription status
    """
    # Use environment variable as fallback
    api_key = forceweaver_api_key or os.environ.get("FORCEWEAVER_API_KEY")
    
    if not api_key:
        raise AuthenticationError("ForceWeaver API key is required. Provide it as parameter or set FORCEWEAVER_API_KEY environment variable.")
    
    logger.info("Getting usage summary")
    
    return await client.call_mcp_api(
        "usage/summary",
        method="GET",
        forceweaver_api_key=api_key
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