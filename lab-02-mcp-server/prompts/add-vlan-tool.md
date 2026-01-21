# Add VLAN Tool

Create `tools/add_vlan.py` - a tool to add VLANs to leaf switches.

## Working Example (tools/get_device_info.py)

```python
#!/usr/bin/env python3
"""
MCP Tool: Get Device Info
"""

from typing import Dict, Any
from helpers import run_ansible_playbook, VALID_DEVICES


async def get_device_info(device: str) -> Dict[str, Any]:
    """Retrieve basic information from a network device."""
    if device not in VALID_DEVICES:
        return {"error": f"Invalid device '{device}'. Valid: {VALID_DEVICES}"}

    result = run_ansible_playbook(
        "07-device-info.yml",
        {"target_host": device},
        parse_json=True
    )

    if not result["success"]:
        return {"error": result.get("error", "Playbook failed")}

    data = result.get("data", {})
    return {
        "hostname": data.get("hostname", "unknown"),
        "model": data.get("modelName", "unknown"),
        "version": data.get("version", "unknown"),
        "uptime_seconds": data.get("uptime", 0)
    }


def register(mcp):
    """Register get_device_info tool with the MCP server."""
    mcp.tool()(get_device_info)
```

## Playbook Info

`04-add-vlan.yml` requires: target_host, vlan_id, vlan_name

## Available Constants

```python
from helpers import VALID_LEAVES
# VALID_LEAVES = ["leaf1", "leaf2", "leaf3", "leaf4"]
```

## Requirements

Create `tools/add_vlan.py` with:
1. An async function `add_vlan(device: str, vlan_id: int, vlan_name: str)` that:
   - Validates device is in VALID_LEAVES (VLANs only on leaf switches)
   - Validates vlan_id is between 1 and 4094
   - Calls the 04-add-vlan.yml playbook (no parse_json needed)
   - Returns status and message
2. A `register(mcp)` function that registers the tool

## Expected Output Format

```json
{"status": "success", "message": "VLAN 30 (Management) created on leaf1"}
```

```json
{"status": "error", "error": "Invalid device. VLANs can only be added to: ['leaf1', 'leaf2', 'leaf3', 'leaf4']"}
```
