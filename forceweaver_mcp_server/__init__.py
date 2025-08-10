"""
ForceWeaver MCP Server
Professional Salesforce Revenue Cloud health checking for AI agents

This package provides a lightweight MCP server that connects to the ForceWeaver
cloud service for comprehensive Salesforce health checks.

Website: https://mcp.forceweaver.com
Documentation: https://github.com/forceweaver/forceweaver-mcp-server
Support: https://mcp.forceweaver.com/support
"""

__version__ = "1.1.0"
__author__ = "ForceWeaver Team"
__email__ = "support@forceweaver.com"
__license__ = "MIT"

from .exceptions import AuthenticationError, ConnectionError, ForceWeaverError
from .server import ForceWeaverMCPClient

__all__ = [
    "ForceWeaverMCPClient",
    "ForceWeaverError",
    "AuthenticationError",
    "ConnectionError",
]
