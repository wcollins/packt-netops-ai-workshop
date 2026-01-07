"""
Shared constants for MCP tools.

This module provides configuration values used across all tools.
"""

import os

# Device credentials (in production, use environment variables!)
DEVICE_USERNAME = os.getenv("DEVICE_USERNAME", "admin")
DEVICE_PASSWORD = os.getenv("DEVICE_PASSWORD", "admin")

# Ansible directory for MCP-Ansible integration
ANSIBLE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "..",
    "lab-01-copilots",
    "ansible"
)

# Valid device names for validation
VALID_DEVICES = ["spine1", "spine2", "leaf1", "leaf2", "leaf3", "leaf4"]
VALID_LEAVES = ["leaf1", "leaf2", "leaf3", "leaf4"]

# Device name to IP mapping (for tools that receive IP but need device name)
DEVICE_IPS = {
    "spine1": "198.18.1.11",
    "spine2": "198.18.1.12",
    "leaf1": "198.18.1.21",
    "leaf2": "198.18.1.22",
    "leaf3": "198.18.1.23",
    "leaf4": "198.18.1.24",
}

# Reverse lookup: IP to device name
IP_TO_DEVICE = {ip: name for name, ip in DEVICE_IPS.items()}
