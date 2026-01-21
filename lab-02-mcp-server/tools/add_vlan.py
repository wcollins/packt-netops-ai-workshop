#!/usr/bin/env python3
"""
MCP Tool: Add VLAN

Adds a VLAN to a leaf switch.
VLANs can only be configured on leaf switches, not spines.
"""

from typing import Dict, Any
from helpers import run_ansible_playbook, VALID_LEAVES


async def add_vlan(device: str, vlan_id: int, vlan_name: str) -> Dict[str, Any]:
    """
    Add a VLAN to a leaf switch.

    Args:
        device: Leaf switch name (leaf1-leaf4)
        vlan_id: VLAN ID (1-4094)
        vlan_name: Name for the VLAN

    Returns:
        Dictionary with status and message

    Example output:
        {"status": "success", "message": "VLAN 30 (Management) created on leaf1"}
    """
    if device not in VALID_LEAVES:
        return {
            "status": "error",
            "error": f"Invalid device. VLANs can only be added to: {VALID_LEAVES}"
        }

    if not (1 <= vlan_id <= 4094):
        return {
            "status": "error",
            "error": f"Invalid vlan_id '{vlan_id}'. Must be between 1 and 4094"
        }

    result = run_ansible_playbook(
        "04-add-vlan.yml",
        {
            "target_host": device,
            "vlan_id": vlan_id,
            "vlan_name": vlan_name
        }
    )

    if not result["success"]:
        return {
            "status": "error",
            "error": result.get("error", result.get("stderr", "Playbook failed"))
        }

    return {
        "status": "success",
        "message": f"VLAN {vlan_id} ({vlan_name}) created on {device}"
    }


def register(mcp):
    """Register add_vlan tool with the MCP server."""
    mcp.tool()(add_vlan)
