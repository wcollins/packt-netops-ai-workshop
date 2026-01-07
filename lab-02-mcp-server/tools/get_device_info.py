#!/usr/bin/env python3
"""
MCP Tool: Get Device Info

Retrieves basic information (hostname, model, version, uptime) from a network device.
Uses Ansible for consistent device access.
"""

from typing import Dict, Any
from helpers import run_ansible_playbook, VALID_DEVICES


async def get_device_info(device: str) -> Dict[str, Any]:
    """
    Retrieve basic information from a network device.

    Args:
        device: Device name (spine1, spine2, leaf1-leaf4)

    Returns:
        Dictionary with hostname, model, version, uptime

    Example output:
        {
            "hostname": "spine1",
            "model": "cEOS-lab",
            "version": "4.35.0.1F",
            "uptime_seconds": 12345.67
        }
    """
    # Validate device name
    if device not in VALID_DEVICES:
        return {
            "error": f"Invalid device '{device}'. Valid devices: {VALID_DEVICES}"
        }

    # Run the Ansible playbook with JSON parsing
    result = run_ansible_playbook(
        "07-device-info.yml",
        {"target_host": device},
        parse_json=True
    )

    if not result["success"]:
        return {"error": result.get("error", result.get("stderr", "Playbook failed"))}

    # Extract device data from parsed JSON
    data = result.get("data", {})
    if not data:
        return {"error": "Failed to parse device response"}

    return {
        "hostname": data.get("hostname", "unknown"),
        "model": data.get("modelName", "unknown"),
        "version": data.get("version", "unknown"),
        "uptime_seconds": data.get("uptime", 0),
        "serial_number": data.get("serialNumber", "unknown"),
        "mac_address": data.get("systemMacAddress", "unknown")
    }


def register(mcp):
    """Register get_device_info tool with the MCP server."""
    mcp.tool()(get_device_info)
