#!/usr/bin/env python3
"""
MCP Tool: Get Running Config

Retrieves the running configuration from a network device.
Supports optional section filtering (interfaces, bgp, vlans).
"""

import re
from typing import Dict, Any, Optional
from helpers import run_ansible_playbook, VALID_DEVICES


VALID_SECTIONS = ["interfaces", "bgp", "vlans"]


async def get_running_config(device: str, section: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve running configuration from a network device.

    Args:
        device: Device name (spine1, spine2, leaf1-leaf4)
        section: Optional config section (interfaces, bgp, vlans)

    Returns:
        Dictionary with status, device, section, and config text

    Example output:
        {
            "status": "success",
            "device": "leaf1",
            "section": "bgp",
            "config": "router bgp 65101\\n   router-id 11.11.11.11\\n..."
        }
    """
    if device not in VALID_DEVICES:
        return {
            "status": "error",
            "message": f"Invalid device '{device}'. Valid devices: {VALID_DEVICES}"
        }

    if section is not None and section not in VALID_SECTIONS:
        return {
            "status": "error",
            "message": f"Invalid section '{section}'. Valid sections: {VALID_SECTIONS}"
        }

    extra_vars = {"target_host": device}
    if section:
        extra_vars["section"] = section

    result = run_ansible_playbook(
        "05-show-config.yml",
        extra_vars
    )

    if not result["success"]:
        return {
            "status": "error",
            "message": result.get("error", result.get("stderr", "Playbook failed"))
        }

    # Extract config from ansible debug output
    stdout = result.get("stdout", "")

    # Look for the "msg" content in ansible verbose output
    # The config appears after "msg": in the debug task output
    match = re.search(r'"msg":\s*"(.+?)"\s*\}', stdout, re.DOTALL)
    if match:
        config = match.group(1)
        # Unescape newlines and quotes
        config = config.replace("\\n", "\n").replace('\\"', '"')
    else:
        # Fallback: return raw stdout if parsing fails
        config = stdout

    return {
        "status": "success",
        "device": device,
        "section": section,
        "config": config
    }


def register(mcp):
    """Register get_running_config tool with the MCP server."""
    mcp.tool()(get_running_config)
