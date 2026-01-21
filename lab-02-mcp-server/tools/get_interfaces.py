#!/usr/bin/env python3
"""
MCP Tool: Get Interfaces

Retrieves interface status from a network device using Ansible.
"""

from typing import Dict, Any
from helpers import run_ansible_playbook, VALID_DEVICES


async def get_interfaces(device: str) -> Dict[str, Any]:
    """
    Get status of all interfaces on a device.

    Args:
        device: Device name (spine1, spine2, leaf1-leaf4)

    Returns:
        Dictionary with interface names and their status

    Example output:
        {
            "device": "spine1",
            "interface_count": 4,
            "interfaces": {
                "Ethernet1": {"status": "connected", "description": "Link to leaf1"},
                "Ethernet2": {"status": "connected", "description": "Link to leaf2"}
            }
        }
    """
    # Validate device name
    if device not in VALID_DEVICES:
        return {
            "error": f"Invalid device '{device}'. Valid devices: {VALID_DEVICES}"
        }

    # Run the Ansible playbook with JSON parsing
    result = run_ansible_playbook(
        "08-interfaces-status.yml",
        {"target_host": device},
        parse_json=True
    )

    if not result["success"]:
        return {"error": result.get("error", result.get("stderr", "Playbook failed"))}

    # Extract interface data from parsed JSON
    data = result.get("data", {})
    if not data:
        error_detail = result.get("parse_error", "Unknown parsing error")
        return {"error": f"Failed to parse interface data: {error_detail}"}

    # Arista "show interfaces status | json" structure
    interface_statuses = data.get("interfaceStatuses", {})

    interfaces = {}
    for name, info in interface_statuses.items():
        interfaces[name] = {
            "status": info.get("linkStatus", "unknown"),
            "description": info.get("description", ""),
            "line_protocol": info.get("lineProtocolStatus", "unknown")
        }

    return {
        "device": device,
        "interface_count": len(interfaces),
        "interfaces": interfaces
    }


def register(mcp):
    """Register get_interfaces tool with the MCP server."""
    mcp.tool()(get_interfaces)
