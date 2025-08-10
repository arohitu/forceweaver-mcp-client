"""
ForceWeaver MCP Client Exceptions
Custom exception classes for the ForceWeaver MCP client.
"""


class ForceWeaverError(Exception):
    """Base exception for ForceWeaver client errors"""

    pass


class AuthenticationError(ForceWeaverError):
    """Raised when authentication fails"""

    pass


class ConnectionError(ForceWeaverError):
    """Raised when connection to ForceWeaver service fails"""

    pass


class ValidationError(ForceWeaverError):
    """Raised when input validation fails"""

    pass


class RateLimitError(ForceWeaverError):
    """Raised when rate limits are exceeded"""

    pass


class ServiceUnavailableError(ForceWeaverError):
    """Raised when ForceWeaver service is unavailable"""

    pass
