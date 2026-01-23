#!/usr/bin/env python3
"""
Network Operations MCP Server
Workshop: Build Intelligent Networks with AI

This MCP server uses auto-discovery to load tools from the tools/ directory.
To add a new tool, simply create a file in tools/ following the template.

WORKING EXAMPLES:
- tools/get_device_info.py - Get device information via SSH
- tools/get_interfaces.py - Get interface status via SSH
- tools/add_vlan.py - Add VLAN via Ansible
- resources/topology.py - Network topology resource

EXTENSION TASKS:
- Copy tools/_template.py to create new tools
- See prompts/ folder for AI assistance

Run with: mcp dev network_mcp_server.py
Test with: python -m pytest tests/test_mcp_server.py
"""

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

# Initialize MCP server
# Disable DNS rebinding protection to allow remote access via IP address
# This is required for connecting from Claude Desktop on another machine
mcp = FastMCP(
    "Network Operations",
    host="0.0.0.0",  # Bind to all interfaces for remote access
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False
    ),
)


# =============================================================================
# AUTO-DISCOVERY: Register all tools and resources
# =============================================================================

print("\n=== Registering MCP Components ===")

print("\nTools:")
from tools import register_all_tools
registered_tools = register_all_tools(mcp)

print("\nResources:")
from resources import register_all_resources
registered_resources = register_all_resources(mcp)

print(f"\n=== Registration Complete ===")
print(f"Tools: {len(registered_tools)}, Resources: {len(registered_resources)}")
print()


# =============================================================================
# WORKING EXAMPLE: BGP Troubleshooting Prompt (inline)
# =============================================================================

@mcp.prompt()
def troubleshoot_bgp(device: str) -> str:
    """
    Generate a troubleshooting workflow for BGP issues.

    Args:
        device: Device name to troubleshoot (e.g., 'spine1')
    """
    return f"""Help me troubleshoot BGP on {device}.

Please follow these steps:
1. First, use get_device_info() to verify the device is responding
2. Then use get_interfaces() to check interface status
3. Analyze the results:
   - Are all interfaces up?
   - Is the device healthy?
4. Suggest next steps based on findings

Device IP mapping:
- spine1: 198.18.1.11
- spine2: 198.18.1.12
- leaf1-4: 198.18.1.21-24
"""


# =============================================================================
# EXTENSION TASKS: Add new tools
# =============================================================================
# To add a new tool:
# 1. Copy tools/_template.py to tools/your_tool_name.py
# 2. Implement your tool function inside register(mcp)
# 3. Restart the MCP server - your tool is auto-discovered!
#
# See prompts/ folder for AI assistance with these tasks:
# - prompts/add-vlan-tool.md - Add VLAN creation tool (Required)
# - prompts/add-config-backup.md - Add configuration backup tool (Required)
# - prompts/add-get-config-tool.md - Add get running config tool (Optional)


# =============================================================================
# LAB 3 EXTENSION: Alerting Tools (uncomment after Lab 3 setup)
# =============================================================================
# After completing Lab 3, uncomment these lines to add alerting tools:
#
# import os
# import sys
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lab-03-observability"))
# from alerting_tools import query_prometheus, get_active_alerts
# mcp.tool()(query_prometheus)
# mcp.tool()(get_active_alerts)


if __name__ == "__main__":
    mcp.run()
