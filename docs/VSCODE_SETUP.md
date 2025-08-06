# 🔧 **VS Code + GitHub Copilot Setup Guide**

**Complete setup for using ForceWeaver MCP Server with VS Code and GitHub Copilot**

---

## 📋 **Prerequisites**

- **VS Code** with latest updates
- **GitHub Copilot** extension installed and activated
- **GitHub Copilot Chat** extension installed
- **Python 3.8+** installed on your system
- **ForceWeaver MCP Client** installed (`pip install forceweaver-mcp-client`)

---

## 🚀 **Quick Setup**

### **Step 1: Install ForceWeaver MCP Client**

```bash
# Install from PyPI
pip install forceweaver-mcp-client

# Or install from source for development
git clone https://github.com/forceweaver/mcp-client.git
cd mcp-client
pip install -e .
```

### **Step 2: Configure MCP Server in VS Code**

The `.vscode/mcp.json` file is already configured in this repository:

```json
{
  "mcpServers": {
    "forceweaver": {
      "command": "python3",
      "args": ["-m", "mcp_client"],
      "env": {
        "FORCEWEAVER_API_URL": "https://mcp.forceweaver.com"
      }
    }
  }
}
```

### **Step 3: Restart VS Code**

Close and reopen VS Code to load the MCP server configuration.

---

## 🤖 **Using with GitHub Copilot**

### **Enable Agent Mode**

1. Open **GitHub Copilot Chat** (Ctrl/Cmd + Shift + I)
2. **IMPORTANT**: Switch to **Agent mode** by clicking the agent icon
3. The ForceWeaver MCP server will now be available

### **Example Queries**

Once configured, you can ask GitHub Copilot:

```
"Check the health of my Salesforce org using API key fk_abc123 for org production"

"Analyze my Revenue Cloud bundle structure for dev environment using fk_xyz789"

"List all my connected Salesforce organizations using my API key fk_abc123"

"Show me usage summary for my ForceWeaver account with key fk_def456"
```

---

## 🔧 **Available MCP Tools**

The ForceWeaver MCP Server provides these tools to GitHub Copilot:

### **1. `revenue_cloud_health_check`**
- **Purpose**: Comprehensive Salesforce org health analysis
- **Parameters**: 
  - `forceweaver_api_key` (required): Your ForceWeaver API key
  - `salesforce_org_id` (required): Your Salesforce org identifier
  - `check_types` (optional): Specific checks to run
  - `api_version` (optional): Salesforce API version

### **2. `get_detailed_bundle_analysis`**
- **Purpose**: In-depth Revenue Cloud bundle analysis
- **Parameters**:
  - `forceweaver_api_key` (required): Your ForceWeaver API key
  - `salesforce_org_id` (required): Your Salesforce org identifier
  - `api_version` (optional): Salesforce API version

### **3. `list_available_orgs`**
- **Purpose**: List connected Salesforce organizations
- **Parameters**:
  - `forceweaver_api_key` (required): Your ForceWeaver API key

### **4. `get_usage_summary`**
- **Purpose**: Current usage statistics and billing
- **Parameters**:
  - `forceweaver_api_key` (required): Your ForceWeaver API key

---

## 🛠️ **Development & Debugging**

### **Debug the MCP Server**

Use the provided launch configurations:

1. Open **Run and Debug** panel (Ctrl/Cmd + Shift + D)
2. Select "Debug ForceWeaver MCP Server"
3. Press F5 to start debugging

### **Monitor MCP Server Logs**

Enable debug logging:

```bash
export MCP_LOG_LEVEL=DEBUG
python -m mcp_client
```

### **Test MCP Server Directly**

```bash
# Test STDIO transport
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | python -m mcp_client

# Test HTTP transport (in another terminal)
python -m mcp_client --http
# Then make HTTP requests to http://localhost:8000
```

---

## 🚨 **Troubleshooting**

### **"Server has stopped" Error**

1. **Check Agent Mode**: Ensure GitHub Copilot Chat is in **Agent mode**
2. **Verify Installation**: `python -m mcp_client --help`
3. **Check Python Path**: Ensure `python3` command is available
4. **Restart VS Code**: Close and reopen VS Code completely

### **"Authentication Failed" Error**

1. Verify your ForceWeaver API key at [Dashboard](https://mcp.forceweaver.com/dashboard/keys)
2. Ensure your Salesforce org is connected
3. Check that your org ID is correct

### **"No MCP Tools Available" Error**

1. Check VS Code Output panel → "MCP: forceweaver"
2. Verify the MCP server is running: look for startup logs
3. Ensure GitHub Copilot Chat is in Agent mode

### **Connection Issues**

1. Check internet connectivity
2. Verify ForceWeaver service status
3. Check firewall settings for HTTPS connections

---

## 📊 **MCP Server Architecture**

This ForceWeaver MCP Client acts as an **MCP Server** that:

1. **Receives requests** from VS Code/GitHub Copilot via MCP protocol
2. **Proxies requests** to ForceWeaver cloud services on Heroku
3. **Returns formatted responses** optimized for AI consumption

```
VS Code + GitHub Copilot
         ↓ (MCP Protocol)
ForceWeaver MCP Server (this project)
         ↓ (HTTPS API calls)
ForceWeaver Cloud Services (Heroku)
         ↓ (Salesforce API calls)
Salesforce Revenue Cloud
```

---

## 🔒 **Security Notes**

- **API Keys**: Never commit API keys to version control
- **Environment Variables**: Use environment variables for sensitive data
- **HTTPS**: All communications with ForceWeaver services use HTTPS
- **User Approval**: MCP protocol requires user approval for all tool executions

---

## 📞 **Support**

If you encounter issues:

1. **Check Logs**: Enable debug logging and check VS Code Output panel
2. **Documentation**: [GitHub Repository](https://github.com/forceweaver/mcp-client)
3. **Issues**: [GitHub Issues](https://github.com/forceweaver/mcp-client/issues)
4. **Support**: [ForceWeaver Support](https://mcp.forceweaver.com/support)

---

## 🎉 **You're Ready!**

Once configured, you can seamlessly use natural language to interact with your Salesforce Revenue Cloud through GitHub Copilot, powered by the ForceWeaver MCP Server!