# 🚀 **ForceWeaver MCP Client Setup Guide**

**Complete setup instructions for VS Code, Claude Desktop, and other MCP clients**

---

## 📋 **Prerequisites**

- **Python 3.8+** installed on your system
- **ForceWeaver Account** - Sign up at [mcp.forceweaver.com](https://mcp.forceweaver.com)
- **API Key** - Generate from your [ForceWeaver Dashboard](https://mcp.forceweaver.com/dashboard/keys)
- **Connected Salesforce Org** - Connect your org in the dashboard

---

## 📦 **Installation**

### **Option 1: Install from PyPI (Recommended)**
```bash
pip install forceweaver-mcp-client
```

### **Option 2: Install from Source**
```bash
git clone https://github.com/forceweaver/mcp-client.git
cd mcp-client
pip install -e .
```

### **Verify Installation**
```bash
python -m forceweaver_mcp_client --help
```

---

## 🔑 **Get Your Credentials**

### **Step 1: Create ForceWeaver Account**
1. Visit [mcp.forceweaver.com](https://mcp.forceweaver.com)
2. Sign up or log in
3. Complete account verification

### **Step 2: Generate API Key**
1. Go to [API Keys](https://mcp.forceweaver.com/dashboard/keys)
2. Click **"Generate New Key"**
3. Copy your API key (starts with `fk_`)
4. Store it securely

### **Step 3: Connect Salesforce Org**
1. Go to [Organizations](https://mcp.forceweaver.com/dashboard/orgs)
2. Click **"Connect New Org"**
3. Complete OAuth flow
4. Note your **Org ID** (e.g., `entdev1`, `production`)

---

## 🔧 **VS Code + GitHub Copilot Setup**

### **Step 1: Install VS Code Extensions**
- **GitHub Copilot** extension
- **GitHub Copilot Chat** extension

### **Step 2: Create MCP Configuration**
Create `.vscode/mcp.json` in your project root:

```json
{
  "servers": {
    "forceweaver": {
      "command": "python3",
      "args": ["-m", "forceweaver_mcp_client"],
      "env": {
        "FORCEWEAVER_API_KEY": "fk_your_api_key_here",
        "SALESFORCE_ORG_ID": "your_org_id_here"
      }
    }
  }
}
```

### **Step 3: Restart VS Code**
- Close and reopen VS Code
- The MCP server will start automatically

### **Step 4: Test Integration**
1. Open **GitHub Copilot Chat**
2. Switch to **Agent mode** (important!)
3. Ask: *"Check the health of my Salesforce org"*

### **Troubleshooting VS Code**
- **"Server as stopped"** → Make sure you're in **Agent mode**
- **"Command not found"** → Verify Python path and installation
- **"Authentication failed"** → Check your API key and org ID

---

## 🤖 **Claude Desktop Setup**

### **Step 1: Install Claude Desktop**
Download from [claude.ai](https://claude.ai/download)

### **Step 2: Configure MCP Server**
Edit `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "forceweaver": {
      "command": "python3",
      "args": ["-m", "forceweaver_mcp_client"],
      "env": {
        "FORCEWEAVER_API_KEY": "fk_your_api_key_here",
        "SALESFORCE_ORG_ID": "your_org_id_here"
      }
    }
  }
}
```

### **Step 3: Restart Claude Desktop**
- Close and reopen Claude Desktop
- The MCP server will connect automatically

### **Step 4: Test Integration**
Ask Claude: *"Check the health of my Salesforce org"*

---

## 🌐 **Claude Web (Custom Connectors)**

### **Step 1: Access Claude Web**
Go to [claude.ai](https://claude.ai) in your browser

### **Step 2: Add Custom Connector**
1. Go to **Settings** → **Connectors**
2. Click **"Add custom connector"**
3. Enter URL: `https://mcp.forceweaver.com/connector`
4. Complete authentication flow

### **Step 3: Test Integration**
Ask Claude: *"Check the health of my Salesforce org"*

---

## 🔧 **Advanced Configuration**

### **Environment Variables**
Set these in your shell profile (`.bashrc`, `.zshrc`, etc.):

```bash
export FORCEWEAVER_API_KEY="fk_your_api_key_here"
export SALESFORCE_ORG_ID="your_org_id"
export FORCEWEAVER_API_URL="https://mcp.forceweaver.com"  # Optional
export MCP_TRANSPORT="stdio"  # or "http"
export MCP_LOG_LEVEL="INFO"   # DEBUG for troubleshooting
```

### **Multiple Organizations**
If you have multiple Salesforce orgs:

```json
{
  "servers": {
    "forceweaver-dev": {
      "command": "python3",
      "args": ["-m", "forceweaver_mcp_client"],
      "env": {
        "FORCEWEAVER_API_KEY": "fk_your_api_key",
        "SALESFORCE_ORG_ID": "dev_org_id"
      }
    },
    "forceweaver-prod": {
      "command": "python3",
      "args": ["-m", "forceweaver_mcp_client"],
      "env": {
        "FORCEWEAVER_API_KEY": "fk_your_api_key",
        "SALESFORCE_ORG_ID": "prod_org_id"
      }
    }
  }
}
```

### **Custom API Endpoint**
For enterprise deployments:

```json
{
  "servers": {
    "forceweaver": {
      "command": "python3",
      "args": ["-m", "forceweaver_mcp_client"],
      "env": {
        "FORCEWEAVER_API_KEY": "fk_your_api_key",
        "SALESFORCE_ORG_ID": "your_org_id",
        "FORCEWEAVER_API_URL": "https://your-enterprise-instance.com"
      }
    }
  }
}
```

---

## 🧪 **Testing Your Setup**

### **Test Connection**
```bash
python -c "
import asyncio
from forceweaver_mcp_client import ForceWeaverMCPClient

async def test():
    client = ForceWeaverMCPClient()
    try:
        result = await client.call_mcp_api(
            'health/check',
            forceweaver_api_key='fk_your_api_key',
            org_id='your_org_id',
            check_types=['basic_org_info']
        )
        print('✅ Connection successful!')
        print(result[:200] + '...' if len(result) > 200 else result)
    except Exception as e:
        print(f'❌ Connection failed: {e}')
    finally:
        await client.close()

asyncio.run(test())
"
```

### **Test MCP Tools**
In your AI agent, try these commands:
- *"Check the health of my Salesforce org"*
- *"Show me detailed bundle analysis"*
- *"List my connected Salesforce organizations"*
- *"What's my current ForceWeaver usage?"*

---

## 🚨 **Troubleshooting**

### **Common Issues**

#### **"Module not found" Error**
```bash
# Check Python path
which python3
python3 -m pip show forceweaver-mcp-client

# Reinstall if needed
pip install --upgrade forceweaver-mcp-client
```

#### **"Authentication Failed"**
1. Verify API key at [Dashboard](https://mcp.forceweaver.com/dashboard/keys)
2. Check org ID at [Organizations](https://mcp.forceweaver.com/dashboard/orgs)
3. Ensure org is connected and active

#### **"Connection Timeout"**
1. Check internet connectivity
2. Verify ForceWeaver service status
3. Check firewall settings

#### **"Server as stopped" (VS Code)**
1. Ensure you're in **Agent mode** in Copilot Chat
2. Check MCP configuration in `.vscode/mcp.json`
3. Restart VS Code
4. Check VS Code Output panel for errors

### **Debug Mode**
Enable detailed logging:

```bash
export MCP_LOG_LEVEL=DEBUG
python -m forceweaver_mcp_client
```

### **Check Logs**
- **VS Code**: Check Output panel → "MCP: forceweaver"
- **Claude Desktop**: Check application logs
- **Terminal**: Logs appear in stderr

---

## 📞 **Support**

If you need help:

1. **Check Documentation**: [GitHub Repository](https://github.com/forceweaver/mcp-client)
2. **Search Issues**: [GitHub Issues](https://github.com/forceweaver/mcp-client/issues)
3. **Contact Support**: [ForceWeaver Support](https://mcp.forceweaver.com/support)
4. **Dashboard Help**: [ForceWeaver Dashboard](https://mcp.forceweaver.com/dashboard)

---

## 🎉 **You're Ready!**

Once configured, you can ask your AI agent natural language questions about your Salesforce org:

- *"How healthy is my Salesforce org?"*
- *"Are there any issues with my Revenue Cloud setup?"*
- *"Show me bundle analysis with detailed statistics"*
- *"What organizations do I have connected?"*

**Happy health checking!** 🚀