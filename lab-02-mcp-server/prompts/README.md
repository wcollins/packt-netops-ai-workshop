# AI Prompts for Lab 2: MCP Server

This folder contains prompts to help you add new tools to the MCP server using AI copilots.

## How to Use These Prompts

1. **Review a working tool** like `tools/get_device_info.py`
2. **Copy the prompt** from the appropriate file below
3. **Paste into your AI copilot** (Claude Code, GitHub Copilot, etc.)
4. **Review the generated code** in the new `tools/*.py` file
5. **Restart the MCP server** - your tool is auto-discovered!

## Available Prompts

| File | Purpose | Creates |
|------|---------|---------|
| `add-vlan-tool.md` | Add VLAN creation tool | `tools/add_vlan.py` |
| `add-config-backup.md` | Add configuration backup tool | `tools/backup_config.py` |
| `add-ansible-tools.md` | Add additional Ansible-invoking tools | `tools/*.py` |

## Modular Tool Structure

All tools use Ansible playbooks for device communication. Each tool file follows this pattern:

```python
#!/usr/bin/env python3
"""
MCP Tool: Tool Name

Description of what this tool does.
"""

from typing import Dict, Any
from helpers import run_ansible_playbook, VALID_DEVICES


async def your_tool_name(device: str) -> Dict[str, Any]:
    """
    Tool description.

    Args:
        device: Device name (spine1, spine2, leaf1-leaf4)

    Returns:
        Dictionary with results
    """
    # Validate device
    if device not in VALID_DEVICES:
        return {"error": f"Invalid device. Valid: {VALID_DEVICES}"}

    # Run playbook with JSON parsing for show commands
    result = run_ansible_playbook(
        "07-device-info.yml",
        {"target_host": device},
        parse_json=True
    )

    if not result["success"]:
        return {"error": result.get("error", "Playbook failed")}

    # Extract and return data
    data = result.get("data", {})
    return {"device": device, "info": data}


def register(mcp):
    """Register this tool with the MCP server."""
    mcp.tool()(your_tool_name)
```

### Key Requirements

1. **Async function**: Tool functions must be `async def`
2. **register(mcp) function**: Required for auto-discovery
3. **Device validation**: Validate against `VALID_DEVICES` or `VALID_LEAVES`
4. **Ansible playbook**: Use `run_ansible_playbook()` helper
5. **Docstring**: Include Args, Returns, and Example output

## Helper Function

```python
from helpers import run_ansible_playbook, VALID_DEVICES, VALID_LEAVES

def run_ansible_playbook(
    playbook: str,
    extra_vars: Dict[str, Any],
    parse_json: bool = False
) -> Dict[str, Any]:
    """
    Run an Ansible playbook with extra variables.

    Args:
        playbook: Playbook filename (e.g., '07-device-info.yml')
        extra_vars: Variables to pass (e.g., {"target_host": "spine1"})
        parse_json: If True, parse device JSON output into result["data"]

    Returns:
        {
            "success": bool,
            "stdout": str,
            "stderr": str,
            "data": dict  # Only if parse_json=True and successful
        }
    """
```

## Available Playbooks

| Playbook | Variables | Purpose |
|----------|-----------|---------|
| `04-add-vlan.yml` | target_host, vlan_id, vlan_name | Add VLAN to leaf |
| `05-show-config.yml` | target_host, (section) | Get running config |
| `06-backup-config.yml` | target_host | Backup config to file |
| `07-device-info.yml` | target_host | Get version/model/uptime |
| `08-interfaces-status.yml` | target_host | Get interface status |
| `09-bgp-neighbors.yml` | target_host | Get BGP neighbor info |

## Testing Your Tools

### 1. MCP Inspector (Browser-based)
```bash
cd lab-02-mcp-server
mcp dev network_mcp_server.py
```
Opens a browser interface to test tools interactively.

### 2. Pytest (Automated)
```bash
cd lab-02-mcp-server
python -m pytest tests/test_mcp_server.py -v
```

### 3. Claude Desktop
Add to your MCP config and test with natural language prompts.

## Reference Files

- `tools/_template.py` - Reference template showing the structure
- `tools/get_device_info.py` - Working Ansible-based tool example
- `tools/add_vlan.py` - Working Ansible-based tool (configuration)

## Device Reference

| Device | Name | BGP ASN |
|--------|------|---------|
| spine1 | spine1 | 65100 |
| spine2 | spine2 | 65100 |
| leaf1 | leaf1 | 65101 |
| leaf2 | leaf2 | 65102 |
| leaf3 | leaf3 | 65103 |
| leaf4 | leaf4 | 65104 |

Tools use device **names** (not IP addresses) which map to the Ansible inventory.
