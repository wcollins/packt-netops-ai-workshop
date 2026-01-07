# Add VLAN Tool

Use this prompt to add a tool that creates VLANs on leaf switches.

---

## Prompt

```
I have an MCP server for network operations with a modular tools/ directory.
I want to add a tool to create VLANs on leaf switches using Ansible.

## File to Create

Create `tools/add_vlan.py` following the modular pattern.

## Working Example (tools/get_device_info.py)

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


## Ansible Playbook (04-add-vlan.yml)

The playbook:
- Adds a VLAN to a leaf switch
- Takes target_host, vlan_id, and vlan_name as variables
- Uses arista.eos.eos_vlans module

## Available Constants

from helpers import VALID_LEAVES
# VALID_LEAVES = ["leaf1", "leaf2", "leaf3", "leaf4"]

## Extension Request

Create a new file `tools/add_vlan.py` with:
1. An async function `add_vlan(device: str, vlan_id: int, vlan_name: str)` that:
   - Validates device is in VALID_LEAVES (VLANs only on leaf switches)
   - Validates vlan_id is between 1 and 4094
   - Calls the 04-add-vlan.yml playbook
   - Returns status and message
2. A `register(mcp)` function that registers the tool

## Expected Output Format

{
    "status": "success",
    "message": "VLAN 30 (Management) created on leaf1"
}

Or on error:

{
    "status": "error",
    "error": "Invalid device. VLANs can only be added to: ['leaf1', 'leaf2', 'leaf3', 'leaf4']"
}

Follow the patterns from the working example.
```

---

## Expected Output

The AI should create `tools/add_vlan.py`:

```python
#!/usr/bin/env python3
"""
MCP Tool: Add VLAN

Adds a VLAN to a leaf switch using Ansible.
"""

from typing import Dict, Any
from helpers import run_ansible_playbook, VALID_LEAVES


async def add_vlan(device: str, vlan_id: int, vlan_name: str) -> Dict[str, Any]:
    """
    Add a VLAN to a leaf switch.

    Args:
        device: Leaf switch name (leaf1-leaf4)
        vlan_id: VLAN ID (1-4094)
        vlan_name: VLAN name

    Returns:
        Dictionary with status and message

    Example:
        add_vlan("leaf1", 30, "Management")
        -> {"status": "success", "message": "VLAN 30 (Management) created on leaf1"}
    """
    if device not in VALID_LEAVES:
        return {
            "status": "error",
            "error": f"Invalid device. VLANs can only be added to: {VALID_LEAVES}"
        }

    if not 1 <= vlan_id <= 4094:
        return {
            "status": "error",
            "error": "VLAN ID must be between 1 and 4094"
        }

    result = run_ansible_playbook("04-add-vlan.yml", {
        "target_host": device,
        "vlan_id": vlan_id,
        "vlan_name": vlan_name
    })

    if result["success"]:
        return {
            "status": "success",
            "message": f"VLAN {vlan_id} ({vlan_name}) created on {device}"
        }
    else:
        return {
            "status": "failed",
            "error": result.get("error", result.get("stderr", "Unknown error"))
        }


def register(mcp):
    """Register add_vlan tool with the MCP server."""
    mcp.tool()(add_vlan)
```

---

## Validation

After creating the file:

1. **Restart MCP server** - tool is auto-discovered:
   ```bash
   mcp dev network_mcp_server.py
   ```

2. **Test in MCP Inspector:**
   Call `add_vlan` with:
   - device: `leaf1`
   - vlan_id: `30`
   - vlan_name: `Management`

3. **Verify the response** includes:
   - status: "success"
   - message confirming VLAN creation

4. **Verify on device:**
   ```bash
   ssh admin@198.18.1.21 "show vlan"
   ```
