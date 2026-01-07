# Add Ansible-Invoking MCP Tools

Use this prompt with Claude Code to add MCP tools that invoke Ansible playbooks.

## How to Use

1. In your terminal, run `claude`
2. Copy and paste the prompt below
3. Review the generated file in `tools/`

---

## Prompt

```
I have an MCP server with a modular tools/ directory. There's a working
`tools/add_vlan.py` that invokes an Ansible playbook. I want to add similar tools.

## File to Create

Create `tools/show_running_config.py` following the modular pattern.

## Working Example (tools/add_vlan.py)

#!/usr/bin/env python3
"""
MCP Tool: Add VLAN
"""

from typing import Dict, Any
from helpers import run_ansible_playbook, VALID_LEAVES


async def add_vlan(device: str, vlan_id: int, vlan_name: str) -> Dict[str, Any]:
    """Add a VLAN to a leaf switch using Ansible playbook."""

    if device not in VALID_LEAVES:
        return {
            "status": "error",
            "error": f"Invalid device. VLANs can only be added to: {VALID_LEAVES}"
        }

    if not 1 <= vlan_id <= 4094:
        return {"status": "error", "error": "VLAN ID must be between 1 and 4094"}

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
        return {"status": "failed", "error": result.get("stderr", "Unknown error")}


def register(mcp):
    """Register add_vlan tool with the MCP server."""
    mcp.tool()(add_vlan)


## Helper Function Available

from helpers import run_ansible_playbook, VALID_DEVICES, VALID_LEAVES

def run_ansible_playbook(
    playbook: str,
    extra_vars: Dict[str, Any],
    parse_json: bool = False
) -> Dict[str, Any]:
    """
    Run ansible-playbook with --extra-vars.

    Args:
        playbook: Playbook filename
        extra_vars: Variables to pass to playbook
        parse_json: If True, parse JSON from device output into result["data"]

    Returns:
        {
            "success": bool,
            "stdout": str,
            "stderr": str,
            "return_code": int,
            "data": dict  # Only if parse_json=True and successful
        }
    """

## Available Playbooks

| Playbook | Required Variables | Purpose |
|----------|-------------------|---------|
| 04-add-vlan.yml | target_host, vlan_id, vlan_name | Add single VLAN |
| 05-show-config.yml | target_host, (optional: section) | Get running config |
| 06-backup-config.yml | target_host | Backup config to file |
| 07-device-info.yml | target_host | Get version/model (JSON) |
| 08-interfaces-status.yml | target_host | Get interfaces (JSON) |
| 09-bgp-neighbors.yml | target_host | Get BGP peers (JSON) |

## Extension Request

Create a new file `tools/show_running_config.py` with:
1. An async function `show_running_config(device: str, section: str = None)` that:
   - Validates device is in VALID_DEVICES list
   - Calls the 05-show-config.yml playbook
   - Optionally filters by section (interfaces, bgp, vlans)
   - Returns the configuration text
2. A `register(mcp)` function that registers the tool

Follow the same pattern as add_vlan.py.
```

---

## Expected Output

The AI should create `tools/show_running_config.py`:

```python
#!/usr/bin/env python3
"""
MCP Tool: Show Running Config

Retrieves running configuration from a network device using Ansible.
"""

from typing import Dict, Any, Optional
from helpers import run_ansible_playbook, VALID_DEVICES


async def show_running_config(device: str, section: Optional[str] = None) -> Dict[str, Any]:
    """
    Get the running configuration from a device.

    This tool invokes the 05-show-config.yml playbook to retrieve the
    running configuration of the specified device.

    Args:
        device: Device name (spine1, spine2, leaf1-4)
        section: Optional config section (interfaces, bgp, vlans)

    Returns:
        Dictionary with status and configuration

    Example:
        show_running_config("leaf1")
        show_running_config("leaf1", section="bgp")
    """
    if device not in VALID_DEVICES:
        return {
            "status": "error",
            "error": f"Invalid device '{device}'. Must be one of: {VALID_DEVICES}"
        }

    extra_vars = {"target_host": device}
    if section:
        extra_vars["section"] = section

    result = run_ansible_playbook("05-show-config.yml", extra_vars)

    if result["success"]:
        return {
            "status": "success",
            "device": device,
            "section": section or "full",
            "config": result["stdout"]
        }
    else:
        return {
            "status": "failed",
            "error": result.get("error", result.get("stderr", "Unknown error"))
        }


def register(mcp):
    """Register show_running_config tool with the MCP server."""
    mcp.tool()(show_running_config)
```

---

## Validation

After creating the file:

1. **Restart MCP server** - tool is auto-discovered:
   ```bash
   mcp dev network_mcp_server.py
   ```

2. **Test in MCP Inspector** or Claude Desktop:
   "Show the running config for spine1"
   "Show BGP config for leaf1"

---

## Additional Tools to Add

Use similar prompts to add these tools:

### configure_interfaces(device)
- Calls: 01-interfaces.yml
- Extra vars: target_host
- Returns: Interface configuration status

### configure_bgp(device)
- Calls: 02-bgp.yml
- Extra vars: target_host
- Returns: BGP configuration status
