#!/usr/bin/env python3
"""
MCP Tool: Backup Config

Backs up the running configuration of a network device to a local file.
Uses Ansible playbook for consistent device access.
"""

import re
from typing import Dict, Any
from helpers import run_ansible_playbook, VALID_DEVICES


async def backup_config(device: str) -> Dict[str, Any]:
    """
    Backup running configuration from a network device.

    Args:
        device: Device name (spine1, spine2, leaf1-leaf4)

    Returns:
        Dictionary with status, message, and backup file location

    Example output:
        {
            "status": "success",
            "message": "Configuration backed up for spine1",
            "file": "backups/spine1_20250124T103000.cfg"
        }
    """
    if device not in VALID_DEVICES:
        return {
            "status": "error",
            "message": f"Invalid device '{device}'. Valid devices: {VALID_DEVICES}"
        }

    result = run_ansible_playbook(
        "06-backup-config.yml",
        {"target_host": device}
    )

    if not result["success"]:
        return {
            "status": "error",
            "message": result.get("error", result.get("stderr", "Playbook failed"))
        }

    # Extract backup filename from playbook output
    stdout = result.get("stdout", "")
    match = re.search(r"backups/(\S+\.cfg)", stdout)
    backup_file = f"backups/{match.group(1)}" if match else f"backups/{device}_backup.cfg"

    return {
        "status": "success",
        "message": f"Configuration backed up for {device}",
        "file": backup_file
    }


def register(mcp):
    """Register backup_config tool with the MCP server."""
    mcp.tool()(backup_config)
