#!/usr/bin/env python3
"""
MCP Resource: Network Topology

Provides the lab network topology information as a resource.
The AI can use this to understand what devices are available.
"""

import json


def get_topology() -> str:
    """
    Returns the network topology information.

    This resource provides context about the lab network structure.
    """
    topology = {
        "lab_name": "netops-workshop",
        "description": "Spine-leaf topology with 2 spines and 4 leaves",
        "devices": [
            {"name": "spine1", "role": "spine", "ip": "198.18.1.11", "asn": 65100},
            {"name": "spine2", "role": "spine", "ip": "198.18.1.12", "asn": 65100},
            {"name": "leaf1", "role": "leaf", "ip": "198.18.1.21", "asn": 65101},
            {"name": "leaf2", "role": "leaf", "ip": "198.18.1.22", "asn": 65102},
            {"name": "leaf3", "role": "leaf", "ip": "198.18.1.23", "asn": 65103},
            {"name": "leaf4", "role": "leaf", "ip": "198.18.1.24", "asn": 65104},
        ],
        "credentials": {
            "username": "admin",
            "note": "Password is 'admin' for all devices"
        }
    }
    return json.dumps(topology, indent=2)


def register(mcp):
    """Register the topology resource with the MCP server."""
    mcp.resource("topology://containerlab")(get_topology)
