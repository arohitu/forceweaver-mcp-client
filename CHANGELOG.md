# Changelog

All notable changes to the ForceWeaver MCP Client will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-01-05

### Added
- **MCP Security Best Practices compliance** - Full implementation of official MCP security guidelines
- **Dual transport support** - Both STDIO (local) and HTTP (remote) transport protocols
- **Enhanced error handling** - Comprehensive error messages with user guidance
- **SSL/TLS security** - Proper certificate validation using certifi
- **Connection pooling** - Optimized HTTP client performance
- **Security logging** - All logging directed to stderr for MCP compliance
- **Custom exceptions** - Structured error handling with specific exception types
- **Professional packaging** - Proper Python package structure for PyPI distribution

### Changed
- **Improved API error messages** - More user-friendly error responses
- **Enhanced logging** - Better structured logging with security compliance
- **Updated dependencies** - Latest versions of MCP and HTTP client libraries
- **Refined tool descriptions** - More detailed and helpful tool documentation

### Security
- **Token validation** - Ensures tokens are issued TO the MCP server
- **Input sanitization** - Comprehensive parameter validation
- **Session security** - Secure session management with user binding
- **OAuth security** - Protected against confused deputy attacks

## [1.0.0] - 2024-12-15

### Added
- Initial release of ForceWeaver MCP Client
- Basic health check functionality
- VS Code and Claude Desktop integration
- Simple API key authentication
- Bundle analysis capabilities
- Organization listing
- Usage statistics

### Features
- **Revenue Cloud Health Checks** - Comprehensive Salesforce org analysis
- **Bundle Analysis** - Detailed bundle hierarchy and dependency analysis
- **Organization Management** - List and manage connected Salesforce orgs
- **Usage Tracking** - Monitor API usage and subscription status
- **MCP Protocol Support** - Full Model Context Protocol implementation
- **Multi-platform Support** - Works with VS Code, Claude Desktop, and other MCP clients