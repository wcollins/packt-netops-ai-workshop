#!/usr/bin/env python3
"""
MCP Tool Template (Reference)

This file shows the structure for MCP tools. Use AI prompts in the
prompts/ folder to create new tools - they will generate properly
structured files based on this pattern.

See prompts/add-vlan-tool.md for an example.

Structure:
1. Module docstring with tool description
2. Imports (typing, helpers)
3. Async function with docstring
4. register(mcp) function to register with server

Files starting with underscore (_) are skipped by auto-discovery.
"""

from typing import Dict, Any
from helpers import run_ansible_playbook, VALID_DEVICES


async def example_tool(device: str) -> Dict[str, Any]:
    """
    Brief description of what the tool does.

    Args:
        device: Device name (spine1, spine2, leaf1-leaf4)

    Returns:
        Dictionary with result data

    Example output:
        {
            "key": "value"
        }
    """
    # Validate device name
    if device not in VALID_DEVICES:
        return {"error": f"Invalid device '{device}'. Valid: {VALID_DEVICES}"}

    # Run Ansible playbook with JSON parsing for show commands
    result = run_ansible_playbook(
        "07-device-info.yml",  # Replace with your playbook
        {"target_host": device},
        parse_json=True  # Set to True for JSON output, False for text
    )

    if not result["success"]:
        return {"error": result.get("error", "Playbook failed")}

    # Extract data from parsed JSON (if parse_json=True)
    data = result.get("data", {})
    if not data:
        return {"error": "Failed to parse response"}

    # Return formatted result
    return {
        "device": device,
        "result": data.get("some_field", "unknown")
    }


def register(mcp):
    """Register tool with the MCP server."""
    mcp.tool()(example_tool)
