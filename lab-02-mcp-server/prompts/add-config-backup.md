# Add Config Backup Tool

Use this prompt to add a tool that backs up device configuration.

---

## Prompt

```
I have an MCP server for network operations with a modular tools/ directory.
I want to add a tool to backup the running configuration from a device.

## File to Create

Create `tools/backup_config.py` following the modular pattern.

## Working Example (tools/add_vlan.py)

#!/usr/bin/env python3
"""
MCP Tool: Add VLAN
"""

from typing import Dict, Any
from helpers import run_ansible_playbook, VALID_LEAVES


async def add_vlan(device: str, vlan_id: int, vlan_name: str) -> Dict[str, Any]:
    """Add a VLAN to a leaf switch using Ansible."""
    if device not in VALID_LEAVES:
        return {"status": "error", "error": f"Invalid device. Valid: {VALID_LEAVES}"}

    if not 1 <= vlan_id <= 4094:
        return {"status": "error", "error": "VLAN ID must be 1-4094"}

    result = run_ansible_playbook("04-add-vlan.yml", {
        "target_host": device,
        "vlan_id": vlan_id,
        "vlan_name": vlan_name
    })

    if result["success"]:
        return {"status": "success", "message": f"VLAN {vlan_id} created on {device}"}
    else:
        return {"status": "failed", "error": result.get("stderr", "Unknown error")}


def register(mcp):
    """Register add_vlan tool with the MCP server."""
    mcp.tool()(add_vlan)


## Ansible Playbook (06-backup-config.yml)

The playbook:
- Runs "show running-config" on the device
- Saves output to backups/<hostname>_<timestamp>.cfg
- Displays the backup location in output

## Extension Request

Create a new file `tools/backup_config.py` with:
1. An async function `backup_config(device: str)` that:
   - Validates device is in VALID_DEVICES
   - Calls the 06-backup-config.yml playbook
   - Returns status, message, and backup file location
2. A `register(mcp)` function that registers the tool

## Expected Output Format

{
    "status": "success",
    "message": "Configuration backed up for spine1",
    "file": "backups/spine1_20250124T103000.cfg"
}

Follow the patterns from the add_vlan.py example.
```

---

## Expected Output

The AI should create `tools/backup_config.py`:

```python
#!/usr/bin/env python3
"""
MCP Tool: Backup Config

Backs up the running configuration from a network device using Ansible.
"""

from typing import Dict, Any
from helpers import run_ansible_playbook, VALID_DEVICES
import re


async def backup_config(device: str) -> Dict[str, Any]:
    """
    Backup the running configuration from a network device.

    Args:
        device: Device name (spine1, spine2, leaf1-leaf4)

    Returns:
        Dictionary with status, message, and backup location

    Example:
        backup_config("leaf1")
        -> {"status": "success", "message": "Configuration backed up", "file": "backups/leaf1_20250124T103000.cfg"}
    """
    if device not in VALID_DEVICES:
        return {
            "status": "error",
            "error": f"Invalid device '{device}'. Valid devices: {VALID_DEVICES}"
        }

    result = run_ansible_playbook("06-backup-config.yml", {
        "target_host": device
    })

    if result["success"]:
        # Extract backup filename from output
        stdout = result.get("stdout", "")
        backup_file = f"backups/{device}_backup.cfg"

        # Try to find actual filename from output
        for line in stdout.splitlines():
            if "backups/" in line and ".cfg" in line:
                match = re.search(r'backups/\S+\.cfg', line)
                if match:
                    backup_file = match.group(0)
                    break

        return {
            "status": "success",
            "message": f"Configuration backed up for {device}",
            "file": backup_file
        }
    else:
        return {
            "status": "failed",
            "error": result.get("error", result.get("stderr", "Unknown error"))
        }


def register(mcp):
    """Register backup_config tool with the MCP server."""
    mcp.tool()(backup_config)
```

---

## Validation

After creating the file:

1. **Restart MCP server** - tool is auto-discovered:
   ```bash
   mcp dev network_mcp_server.py
   ```

2. **Test in MCP Inspector:**
   Call `backup_config` with device `spine1`

3. **Verify the response** includes:
   - status: "success"
   - file path in backups/ directory

4. **Check the backup file:**
   ```bash
   ls -la ../lab-01-copilots/ansible/backups/
   cat ../lab-01-copilots/ansible/backups/spine1_*.cfg
   ```
