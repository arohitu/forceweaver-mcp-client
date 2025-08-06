# 🤖 **Cursor AI Handoff: ForceWeaver MCP Client Repository**

**Context for AI Assistant working on the `forceweaver-mcp-client` repository**

---

## 📋 **Project Background**

### **What is ForceWeaver?**
ForceWeaver is a **Salesforce Revenue Cloud health checking platform** that provides comprehensive analysis and optimization recommendations for Salesforce orgs. It performs various health checks including:
- Organization setup validation
- Bundle hierarchy analysis  
- Sharing model configuration
- Attribute picklist integrity
- Circular dependency detection

### **What is MCP?**
**Model Context Protocol (MCP)** is a standardized protocol that allows AI agents (like GitHub Copilot, Claude Desktop, Claude Web) to interact with external services and tools. It uses JSON-RPC 2.0 for communication.

### **The Architecture Decision**
The original ForceWeaver project contained both:
1. **Backend Logic** - Proprietary Salesforce analysis algorithms, Flask web app, database
2. **MCP Server** - Direct integration for AI agents

**Problem**: Distributing the MCP server would expose proprietary backend code, preventing monetization.

**Solution**: Split into two repositories:
- **Private Backend** (`forceweaver-mcp`): Heroku-hosted SaaS with API endpoints
- **Public Client** (`forceweaver-mcp-client`): Lightweight MCP client that proxies to backend APIs

---

## 🎯 **Your Mission: Public MCP Client Repository**

### **Repository Purpose**
Create a **professional, open-source Python package** that:
1. **Acts as MCP server** for AI agents (VS Code, Claude Desktop, Claude Web)
2. **Proxies requests** to the private ForceWeaver backend APIs
3. **Handles authentication** using ForceWeaver API keys
4. **Provides security compliance** following MCP best practices
5. **Enables easy distribution** via PyPI and GitHub

### **Target Users**
- **Salesforce developers** using AI coding assistants
- **Revenue Cloud consultants** needing health check automation
- **DevOps teams** integrating Salesforce analysis into workflows
- **AI agent enthusiasts** exploring MCP integrations

---

## 🏗️ **Technical Requirements**

### **Core Functionality**
The client must provide these MCP tools:

1. **`revenue_cloud_health_check`**
   - Parameters: `forceweaver_api_key`, `salesforce_org_id`, `check_types`, `api_version`
   - Calls: `POST https://mcp.forceweaver.com/api/v1.0/health/check?format=mcp`
   - Returns: Formatted health report with scores, recommendations

2. **`get_detailed_bundle_analysis`**
   - Parameters: `forceweaver_api_key`, `salesforce_org_id`, `api_version`
   - Calls: `POST https://mcp.forceweaver.com/api/v1.0/health/check?format=mcp` (bundle_analysis only)
   - Returns: Detailed bundle statistics without AI summarization

3. **`list_available_orgs`**
   - Parameters: `forceweaver_api_key`
   - Calls: `GET https://mcp.forceweaver.com/api/v1.0/orgs/list?format=mcp`
   - Returns: List of connected Salesforce orgs

4. **`get_usage_summary`**
   - Parameters: `forceweaver_api_key`
   - Calls: `GET https://mcp.forceweaver.com/api/v1.0/usage/summary?format=mcp`
   - Returns: API usage statistics and billing info

### **Security Requirements**
- **Token validation**: Verify API keys with backend
- **SSL/TLS**: All HTTPS communications with certificate validation
- **Input sanitization**: Validate and sanitize all user inputs
- **Error handling**: Graceful failure with helpful error messages
- **Rate limiting**: Respect backend rate limits
- **Logging**: Log to stderr (MCP requirement), not stdout

### **Platform Support**
- **VS Code + GitHub Copilot**: STDIO transport via `.vscode/mcp.json`
- **Claude Desktop**: STDIO transport via config file
- **Claude Web**: HTTP transport via Custom Connectors (future)

---

## 📦 **Package Structure Requirements**

### **Python Package Structure**
```
forceweaver-mcp-client/
├── forceweaver_mcp_client/          # Main package
│   ├── __init__.py                  # Package initialization
│   ├── __main__.py                  # Module entry point
│   ├── client.py                    # Core MCP client logic
│   └── exceptions.py                # Custom exceptions
├── tests/                           # Test suite
├── examples/                        # Configuration examples
├── docs/                           # Documentation
├── .github/workflows/              # CI/CD
├── setup.py                        # Legacy packaging
├── pyproject.toml                  # Modern packaging
├── requirements.txt                # Dependencies
└── README.md                       # Main documentation
```

### **Entry Points**
- **Module**: `python -m forceweaver_mcp_client`
- **Console script**: `forceweaver-mcp` (after pip install)
- **Import**: `import forceweaver_mcp_client`

### **Dependencies (Minimal)**
- `mcp>=1.12.0` - MCP framework
- `aiohttp>=3.8.0` - Async HTTP client
- `certifi` - SSL certificate bundle

---

## 🔧 **Implementation Details**

### **Backend API Integration**
The client calls existing ForceWeaver APIs with `?format=mcp` parameter:

```python
# Health check example
response = await session.post(
    "https://mcp.forceweaver.com/api/v1.0/health/check?format=mcp",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "salesforce_org_id": org_id,
        "check_types": check_types,
        "api_version": api_version
    }
)
```

### **MCP Server Implementation**
Use FastMCP framework:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ForceWeaver")

@mcp.tool()
async def revenue_cloud_health_check(
    forceweaver_api_key: str,
    salesforce_org_id: str,
    check_types: Optional[List[str]] = None,
    api_version: Optional[str] = None
) -> str:
    """Run comprehensive health check on Salesforce Revenue Cloud setup."""
    # Implementation here
```

### **Error Handling**
- **API Key Invalid**: Clear message with dashboard link
- **Org Not Found**: List available orgs
- **Rate Limited**: Explain limits and retry timing
- **Network Issues**: Suggest connectivity checks
- **SSL Errors**: Provide certificate troubleshooting

---

## 🚀 **Distribution Strategy**

### **PyPI Publishing**
- **Package name**: `forceweaver-mcp-client`
- **Version**: Start at 1.0.0, follow semantic versioning
- **Classifiers**: Include MCP, Salesforce, AI agent tags
- **GitHub Actions**: Automated testing and publishing

### **Documentation Requirements**
- **README.md**: Installation, configuration, usage examples
- **SETUP.md**: Detailed setup for each AI agent platform
- **API documentation**: All MCP tools with parameters
- **Troubleshooting guide**: Common issues and solutions

### **Configuration Examples**
Provide working examples for:
- VS Code `.vscode/mcp.json`
- Claude Desktop config
- Environment variable setup
- API key management

---

## 🎯 **Success Criteria**

### **Functional Requirements**
- ✅ All 4 MCP tools working correctly
- ✅ Successful integration with VS Code + GitHub Copilot
- ✅ Successful integration with Claude Desktop
- ✅ Proper error handling and user feedback
- ✅ SSL certificate validation working

### **Quality Requirements**
- ✅ Professional PyPI package
- ✅ Comprehensive test suite (>80% coverage)
- ✅ Clear documentation for novice users
- ✅ GitHub Actions CI/CD pipeline
- ✅ Semantic versioning and changelog

### **Security Requirements**
- ✅ MCP security best practices implemented
- ✅ Input validation and sanitization
- ✅ Secure API key handling
- ✅ No sensitive data in logs or errors

---

## 💡 **Key Insights for Development**

### **What Makes This Unique**
- **First Salesforce MCP integration** in the ecosystem
- **SaaS model** - client is free, backend is monetized
- **Enterprise ready** - professional packaging and documentation
- **Security focused** - follows MCP compliance guidelines

### **Common Pitfalls to Avoid**
- **Don't expose backend logic** - client should only proxy requests
- **Don't hardcode URLs** - make backend URL configurable
- **Don't ignore SSL** - always validate certificates
- **Don't log to stdout** - MCP requires stderr logging
- **Don't make sync calls** - use async/await throughout

### **Testing Strategy**
- **Mock backend responses** for unit tests
- **Integration tests** with real API (using test keys)
- **Multi-platform testing** (macOS, Linux, Windows)
- **Different Python versions** (3.8+)

---

## 🎉 **Expected Outcome**

When complete, users should be able to:

```bash
# Install the client
pip install forceweaver-mcp-client

# Configure VS Code
# Add to .vscode/mcp.json with their API key

# Use with GitHub Copilot
"Check the health of my Salesforce org"
"Analyze my Revenue Cloud bundle structure"
"Show me my ForceWeaver usage this month"
```

And receive professional, formatted responses with actionable insights about their Salesforce Revenue Cloud setup.

---

**This is a high-impact project that bridges AI agents with enterprise Salesforce tooling. Focus on professional quality, security, and user experience!** 🚀