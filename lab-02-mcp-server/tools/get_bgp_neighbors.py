#!/usr/bin/env python3
"""
MCP Tool: Get BGP Neighbors

Retrieves BGP neighbor status from a network device using Ansible.
"""

from typing import Dict, Any
from helpers import run_ansible_playbook, VALID_DEVICES


async def get_bgp_neighbors(device: str) -> Dict[str, Any]:
    """
    Retrieve BGP neighbor status from a network device.

    Args:
        device: Device name (spine1, spine2, leaf1-leaf4)

    Returns:
        Dictionary with router_id, local_asn, neighbor_count, and neighbors

    Example output:
        {
            "device": "spine1",
            "router_id": "1.1.1.1",
            "local_asn": "65100",
            "neighbor_count": 4,
            "neighbors": {
                "10.0.1.2": {
                    "remote_asn": "65101",
                    "state": "Established",
                    "prefixes_received": 5
                }
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
        "09-bgp-neighbors.yml",
        {"target_host": device},
        parse_json=True
    )

    if not result["success"]:
        return {"error": result.get("error", result.get("stderr", "Playbook failed"))}

    # Extract BGP data from parsed JSON
    data = result.get("data", {})
    if not data:
        return {"error": "Failed to parse device response"}

    # Extract default VRF data
    vrf_data = data.get("vrfs", {}).get("default", {})
    peers = vrf_data.get("peers", {})

    # Build neighbors dict
    neighbors = {}
    for peer_ip, peer_data in peers.items():
        neighbors[peer_ip] = {
            "remote_asn": peer_data.get("asn", "unknown"),
            "state": peer_data.get("peerState", "unknown"),
            "prefixes_received": peer_data.get("prefixReceived", 0)
        }

    return {
        "device": device,
        "router_id": vrf_data.get("routerId", "unknown"),
        "local_asn": vrf_data.get("asn", "unknown"),
        "neighbor_count": len(neighbors),
        "neighbors": neighbors
    }


def register(mcp):
    """Register get_bgp_neighbors tool with the MCP server."""
    mcp.tool()(get_bgp_neighbors)
