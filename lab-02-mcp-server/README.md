# Lab 2: MCP Server with Ansible Integration

**Duration:** 70 minutes | **Difficulty:** Intermediate

---

## Learning Objectives

By the end of this lab, you will:

- Understand Model Context Protocol (MCP) architecture
- Review a working MCP server with Ansible-based tools
- Use natural language to manage network devices ("Add VLAN 30 to leaf1")
- Extend the server with new tools using Claude Code
- Integrate MCP server with Claude Desktop

**Lab 1 Connection:** This lab builds on Lab 1 by creating MCP tools that invoke the Ansible playbooks you created.

---

## What is MCP?

**Model Context Protocol (MCP)** is an open standard that enables AI assistants to connect with external tools and data sources.

Think of it as **"USB-C for AI"**:
- Universal interface for AI-to-system connections
- Standardized protocol (JSON-RPC)
- Enables autonomous AI workflows

```
┌─────────────┐
│ Claude      │  (AI Assistant)
│ Desktop     │  "Add VLAN 30 to leaf1"
└──────┬──────┘
       │ MCP Protocol
┌──────┴──────┐
│ Your MCP    │  (This lab!)
│ Server      │
└──────┬──────┘
       │
       │ Ansible Playbooks
       │ (from Lab 1)
 ┌─────┴─────┐
 │ ansible-  │
 │ playbook  │
 └─────┬─────┘
       │ SSH/eAPI
 ┌─────┴─────┐
 │ Network   │
 │ Devices   │
 └───────────┘
```

### Three Core Primitives

| Primitive | Purpose | Example |
|-----------|---------|---------|
| **Tools** | Actions the AI can invoke | `get_device_info()` |
| **Resources** | Read-only data | Network topology |
| **Prompts** | Reusable workflows | "Troubleshoot BGP" |

---

## Project Structure

The MCP server uses a **modular architecture** for easy extension:

```
lab-02-mcp-server/
├── network_mcp_server.py   # Main entry point (auto-discovery)
├── helpers/                # Shared helper functions
│   ├── ansible.py         # run_ansible_playbook()
│   └── constants.py       # Device names, valid devices
├── tools/                  # Auto-discovered tools
│   ├── _template.py       # Template for new tools
│   ├── get_device_info.py # Get device information
│   ├── get_interfaces.py  # Get interface status
│   ├── get_bgp_neighbors.py # Get BGP peer status
│   └── health_check.py    # Check all devices
├── resources/              # Auto-discovered resources
│   └── topology.py        # Network topology
├── tests/                  # Test suite
└── prompts/                # AI prompt templates
```

## What You Start With (Working Examples)

The MCP server has **working Ansible-based tools**:

### Tools (in tools/ directory)
| File | Tool | Description |
|------|------|-------------|
| `get_device_info.py` | `get_device_info(device)` | Get device hostname, model, version |
| `get_interfaces.py` | `get_interfaces(device)` | Get interface status |
| `get_bgp_neighbors.py` | `get_bgp_neighbors(device)` | Get BGP neighbor status |
| `health_check.py` | `health_check_all()` | Check all devices at once |

### Helpers (in helpers/ directory)
| File | Function | Description |
|------|----------|-------------|
| `ansible.py` | `run_ansible_playbook()` | Invoke Ansible playbooks |
| `constants.py` | Various | Device names, valid devices |

### Resources (in resources/ directory)
| File | Resource | Description |
|------|----------|-------------|
| `topology.py` | `topology://containerlab` | Network topology |

**Example:** In Claude Desktop, say: "Check the BGP neighbors on spine1"

## What You'll Add (Extension Tasks)

Use Claude Code to add new tools using prompts from the `prompts/` folder:

### Required Extensions
- [ ] `add_vlan(device, vlan_id, vlan_name)` - Add VLAN to leaf switch (~10 min)
- [ ] `backup_config(device)` - Backup device configuration (~10 min)

### Optional Extensions
- [ ] `get_running_config(device)` - Get config via Ansible (~10 min)

## AI Prompts

Ready-to-use prompts are in the `prompts/` folder:

- `prompts/add-vlan-tool.md` - Add VLAN creation tool
- `prompts/add-config-backup.md` - Add configuration backup tool
- `prompts/add-get-config-tool.md` - Get running configuration

---

## Prerequisites

- Lab 1 completed (Containerlab running)
- Python virtual environment activated
- Claude Desktop or Cursor installed

---

## Task 1: Review Working Examples (15 min)

### Step 1.1: Navigate to lab directory

```bash
cd lab-02-mcp-server
```

### Step 1.2: Verify dependencies

```bash
python -c "from mcp.server.fastmcp import FastMCP; print('FastMCP: OK')"
python -c "import paramiko; print('Paramiko: OK')"
```

### Step 1.3: Review the working code

Explore the modular structure:

1. **Main server** - `network_mcp_server.py` (auto-discovery)
2. **Helpers** - `helpers/ansible.py` for Ansible integration
3. **Tools** - `tools/get_device_info.py` for device info
4. **Template** - `tools/_template.py` for creating new tools

### Step 1.4: Run the tests

```bash
python -m pytest tests/test_mcp_server.py -v
```

---

## Task 2: Test with MCP Inspector (10 min)

### Step 2.1: Start MCP development server

```bash
mcp dev network_mcp_server.py
```

This opens an interactive inspector in your browser.

### Step 2.2: Test the working tools

In the inspector:
1. Find `get_device_info` tool
2. Enter device: `spine1`
3. Click "Run"
4. Verify output shows device information

### Step 2.3: Test the topology resource

1. Find `topology://containerlab` resource
2. Click to view topology data
3. Note the device names and ASNs

---

## Task 3: Test BGP Tool (15 min)

### Step 3.1: Test in MCP Inspector

The BGP tool is already implemented. Test it:

```bash
mcp dev network_mcp_server.py
```

Test `get_bgp_neighbors` with device `spine1`.

### Step 3.2: Review the code

Check `tools/get_bgp_neighbors.py` to see how it:
- Validates the device name
- Calls the Ansible playbook with `parse_json=True`
- Extracts BGP peer information from the response

---

## Task 4: Integrate with Claude Desktop (15 min)

### Step 4.1: Find config file location

**Claude Desktop:**

| OS | Config Path |
|----|-------------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

**AnythingLLM:**

| OS | Config Path |
|----|-------------|
| Linux | `~/.config/anythingLLM/storage/plugins/anythingllm_mcp_servers.json` |

### Step 4.2: Add MCP server configuration

Add this to your config file (same format for Claude Desktop and AnythingLLM):

```json
{
  "mcpServers": {
    "network-ops": {
      "command": "/full/path/to/packt-netops-ai-workshop/.venv/bin/python",
      "args": ["/full/path/to/packt-netops-ai-workshop/lab-02-mcp-server/network_mcp_server.py"]
    }
  }
}
```

**Important:**
- Replace `/full/path/to` with your actual path. Find it with `pwd`.
- Use the **virtual environment Python** (`.venv/bin/python`), not system Python, to ensure MCP dependencies are available.

### Step 4.2b: Remote Access (Claude Desktop on Another Machine)

If Claude Desktop is running on a **different machine** (e.g., your Mac laptop connecting to a Linux workshop VM), you need to run the MCP server with SSE transport instead.

**On the workshop VM**, start the MCP server in SSE mode:

```bash
cd lab-02-mcp-server
mcp run -t sse network_mcp_server.py
```

The server will start on `http://0.0.0.0:8000/sse`.

**On your Mac/Windows machine**, configure Claude Desktop to connect via `mcp-remote`:

```json
{
  "mcpServers": {
    "network-ops": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://<WORKSHOP_VM_IP>:8000/sse",
        "--allow-http"
      ]
    }
  }
}
```

Replace `<WORKSHOP_VM_IP>` with the IP address of your workshop VM (e.g., `172.16.10.10`).

**Note:** The `--allow-http` flag is required since the workshop uses HTTP (not HTTPS).

**Requirements:**
- Node.js installed on the Claude Desktop machine (for `npx`)
- Network connectivity between machines (verify with `ping <WORKSHOP_VM_IP>`)
- Port 8000 open on the workshop VM firewall

**Verify connectivity:**

```bash
# From your Mac/Windows machine
curl http://<WORKSHOP_VM_IP>:8000/sse
# Should return: event: endpoint, data: /messages/?session_id=...
```

### Step 4.3: Restart your AI client

Close and reopen Claude Desktop or AnythingLLM completely.

### Step 4.4: Test integration

In your AI client, try:
- "Use get_device_info to check spine1"
- "What's the topology of the network?"
- "Check interfaces on spine1"
- "Get BGP neighbors on spine1"
- "Run a health check on all devices"

---

## Task 5: Add Extension Tools (15 min)

Use Claude Code to add the extension tools:

### Step 5.1: Add VLAN Tool

Open `prompts/add-vlan-tool.md` and copy the prompt into Claude Code.

Claude Code will create `tools/add_vlan.py`.

### Step 5.2: Add Backup Config Tool

Open `prompts/add-config-backup.md` and copy the prompt into Claude Code.

Claude Code will create `tools/backup_config.py`.

### Step 5.3: Test your new tools

Restart the MCP server and test in Claude Desktop:
- "Add VLAN 30 called Management to leaf1"
- "Backup the config for spine1"

---

## Success Criteria

- [ ] MCP server runs without errors
- [ ] `get_device_info` returns device information
- [ ] `get_interfaces` returns interface status
- [ ] `get_bgp_neighbors` returns BGP peer information
- [ ] Claude Desktop can invoke your tools
- [ ] `add_vlan` tool created and tested (extension task)
- [ ] `backup_config` tool created and tested (extension task)

---

## Validation Commands

```bash
# Run MCP server directly
python network_mcp_server.py

# Run tests
python -m pytest tests/ -v

# Test in development mode
mcp dev network_mcp_server.py
```

---

## Troubleshooting

### MCP server won't start

```bash
# Check for syntax errors
python -m py_compile network_mcp_server.py

# Verify imports
python -c "from mcp.server.fastmcp import FastMCP"
```

### Can't connect to devices

```bash
# Verify Containerlab is running
docker ps | grep clab

# Test SSH manually
ssh admin@198.18.1.11
```

### Claude Desktop doesn't see MCP server

1. Check config file syntax: `cat config.json | python -m json.tool`
2. Use absolute path in config
3. Restart Claude Desktop completely
4. Check logs: `~/Library/Logs/Claude/` (macOS)

### AI-generated tool doesn't work

1. Compare with `tools/get_device_info.py`
2. Check imports: `from helpers import run_ansible_playbook, VALID_DEVICES`
3. Verify the `register(mcp)` function is present
4. Check the tool function is async: `async def my_tool(...)`
5. Test in MCP Inspector before Claude Desktop

---

## Key Takeaways

1. **MCP connects AI to real network operations** - Natural language to device actions
2. **Modular architecture makes extension easy** - Just add a file to `tools/`
3. **Ansible integration enables powerful workflows** - Reuse existing playbooks
4. **All tools use Ansible playbooks** - Consistent approach for all device interactions
5. **Always test in Inspector first** - Debug before Claude Desktop integration

---

## Next Lab

Continue to [Lab 3: Add Alerting to MCP](../lab-03-observability/)

In Lab 3, you'll extend this MCP server with Prometheus alerting tools, enabling:
- "Are there any alerts firing?"
- "Query Prometheus for instances that are down"
- "What's the network health status?"
