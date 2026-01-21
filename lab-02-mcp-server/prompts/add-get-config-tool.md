# Add Get Running Config Tool

Create `tools/get_running_config.py` - a tool to retrieve device configuration.

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

`05-show-config.yml` requires: target_host, optional: section (interfaces, bgp, vlans)

## Requirements

Create `tools/get_running_config.py` with:
1. An async function `get_running_config(device: str, section: str = None)` that:
   - Validates device is in VALID_DEVICES
   - Calls the 05-show-config.yml playbook (no parse_json needed)
   - Optionally filters by section (interfaces, bgp, vlans)
   - Returns the configuration text from stdout
2. A `register(mcp)` function that registers the tool

## Expected Output Format

```json
{
    "status": "success",
    "device": "leaf1",
    "section": "bgp",
    "config": "router bgp 65101\n   router-id 11.11.11.11\n..."
}
```
