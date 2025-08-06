# 🚀 **ForceWeaver MCP Client**

**Professional Salesforce Revenue Cloud health checking for AI agents**

[![PyPI version](https://badge.fury.io/py/forceweaver-mcp-client.svg)](https://badge.fury.io/py/forceweaver-mcp-client)
[![Python Support](https://img.shields.io/pypi/pyversions/forceweaver-mcp-client.svg)](https://pypi.org/project/forceweaver-mcp-client/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/forceweaver/mcp-client/workflows/Tests/badge.svg)](https://github.com/forceweaver/mcp-client/actions)

The ForceWeaver MCP Client provides seamless integration between AI agents and Salesforce Revenue Cloud health checking services. Built following MCP Security Best Practices, it offers enterprise-grade reliability and security.

---

## ✨ **Features**

- **🔍 Comprehensive Health Checks** - Advanced Salesforce Revenue Cloud analysis
- **🛡️ Enterprise Security** - MCP Security Best Practices compliance
- **🔄 Dual Transport** - STDIO (local) and HTTP (remote) support
- **🎯 AI Agent Ready** - Works with VS Code, Claude Desktop, and more
- **📊 Detailed Analytics** - Bundle analysis, sharing model validation, data integrity checks
- **🚀 Easy Integration** - Simple installation and configuration

---

## 🚀 **Quick Start**

### **Installation**

```bash
pip install forceweaver-mcp-client
```

### **Get Your API Key**

1. Visit [ForceWeaver Dashboard](https://mcp.forceweaver.com/dashboard)
2. Sign up or log in
3. Navigate to **API Keys** section
4. Generate a new API key
5. Connect your Salesforce org

---

## 🔧 **Configuration**

### **VS Code + GitHub Copilot**

Create or update `.vscode/mcp.json`:

```json
{
  "servers": {
    "forceweaver": {
      "command": "python3",
      "args": ["-m", "forceweaver_mcp_client"],
      "env": {
        "FORCEWEAVER_API_KEY": "your_api_key_here",
        "SALESFORCE_ORG_ID": "your_org_id_here"
      }
    }
  }
}
```

### **Claude Desktop**

Update `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "forceweaver": {
      "command": "python3",
      "args": ["-m", "forceweaver_mcp_client"],
      "env": {
        "FORCEWEAVER_API_KEY": "your_api_key_here",
        "SALESFORCE_ORG_ID": "your_org_id_here"
      }
    }
  }
}
```

### **Environment Variables**

```bash
export FORCEWEAVER_API_KEY="fk_your_api_key_here"
export SALESFORCE_ORG_ID="your_org_id"
export FORCEWEAVER_API_URL="https://mcp.forceweaver.com"  # Optional
```

---

## 🎯 **Usage**

### **With AI Agents**

Once configured, you can ask your AI agent:

- *"Check the health of my Salesforce org"*
- *"Analyze my Revenue Cloud bundle structure"*
- *"Show me detailed bundle analysis statistics"*
- *"List my connected Salesforce organizations"*
- *"What's my current ForceWeaver usage?"*

### **Available Tools**

#### **`revenue_cloud_health_check`**
Comprehensive Salesforce org health analysis including:
- Organization setup validation
- Sharing model analysis
- Bundle hierarchy analysis
- Attribute picklist integrity

#### **`get_detailed_bundle_analysis`**
In-depth bundle analysis with:
- Component count statistics
- Hierarchy depth analysis
- Circular dependency detection
- Performance impact metrics

#### **`list_available_orgs`**
Lists all connected Salesforce organizations in your ForceWeaver account.

#### **`get_usage_summary`**
Current usage statistics and subscription status.

---

## 🔒 **Security**

ForceWeaver MCP Client implements comprehensive security measures:

- **✅ MCP Security Best Practices** - Full compliance with official guidelines
- **✅ Token Validation** - Ensures tokens are issued to the MCP server
- **✅ Input Sanitization** - Comprehensive parameter validation
- **✅ SSL/TLS Security** - Proper certificate validation
- **✅ Session Security** - Secure session management
- **✅ Error Handling** - User-friendly error messages

---

## 🛠️ **Development**

### **Setup Development Environment**

```bash
git clone https://github.com/forceweaver/mcp-client.git
cd mcp-client
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

### **Run Tests**

```bash
pytest tests/
```

### **Code Quality**

```bash
black forceweaver_mcp_client/
flake8 forceweaver_mcp_client/
mypy forceweaver_mcp_client/
```

---

## 📊 **Supported Platforms**

| Platform | Status | Transport | Notes |
|----------|--------|-----------|-------|
| **VS Code + GitHub Copilot** | ✅ Supported | STDIO | Requires Agent mode |
| **Claude Desktop** | ✅ Supported | STDIO | Full integration |
| **Claude Web** | ✅ Supported | HTTP | Via Custom Connectors |
| **Other MCP Clients** | ✅ Supported | STDIO/HTTP | Standard MCP protocol |

---

## 🔍 **Health Check Types**

| Check Type | Description | Cost |
|------------|-------------|------|
| **basic_org_info** | Organization details and setup validation | 1¢ |
| **sharing_model** | Organization-Wide Default sharing settings | 1¢ |
| **bundle_analysis** | Bundle hierarchy and dependency analysis | 1¢ |
| **attribute_picklist_integrity** | Attribute integrity and orphaned records | 1¢ |

---

## 🚨 **Troubleshooting**

### **Common Issues**

#### **"Server as stopped" in VS Code**
- Ensure you're using **Agent mode** in GitHub Copilot Chat
- Check that your API key is valid
- Verify the MCP server configuration in `.vscode/mcp.json`

#### **"Authentication Failed"**
- Verify your API key at [ForceWeaver Dashboard](https://mcp.forceweaver.com/dashboard/keys)
- Ensure your Salesforce org is connected
- Check that your org ID is correct

#### **"Connection Error"**
- Verify internet connectivity
- Check ForceWeaver service status
- Ensure firewall allows HTTPS connections

### **Debug Mode**

Enable debug logging:

```bash
export MCP_LOG_LEVEL=DEBUG
python -m forceweaver_mcp_client
```

---

## 📚 **Documentation**

- **[Setup Guide](docs/SETUP.md)** - Detailed installation instructions
- **[Configuration Guide](docs/CONFIGURATION.md)** - Advanced configuration options
- **[API Reference](docs/API_REFERENCE.md)** - Complete API documentation
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[Security Guide](docs/SECURITY.md)** - Security best practices

---

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### **Quick Contribution Steps**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run quality checks
6. Submit a pull request

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 **Support**

- **Documentation**: [GitHub Repository](https://github.com/forceweaver/mcp-client)
- **Issues**: [GitHub Issues](https://github.com/forceweaver/mcp-client/issues)
- **Support**: [ForceWeaver Support](https://mcp.forceweaver.com/support)
- **Dashboard**: [ForceWeaver Dashboard](https://mcp.forceweaver.com/dashboard)

---

## 🎉 **About ForceWeaver**

ForceWeaver is the leading platform for Salesforce Revenue Cloud health checking and optimization. Our AI-powered analysis helps organizations maintain peak performance and identify potential issues before they impact business operations.

**[Get Started Today →](https://mcp.forceweaver.com)**

---

*Made with ❤️ by the ForceWeaver team*