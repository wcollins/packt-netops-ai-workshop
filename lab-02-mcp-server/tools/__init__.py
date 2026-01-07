"""
Auto-discovery and registration of MCP tools.

This module automatically imports all tool modules and registers them
with the MCP server. Tools are discovered by scanning for .py files
that don't start with underscore (_).

Usage in network_mcp_server.py:
    from tools import register_all_tools
    register_all_tools(mcp)
"""

import importlib
import sys
from pathlib import Path


def register_all_tools(mcp):
    """
    Auto-discover and register all tools with the MCP server.

    Scans the tools/ directory for .py files (excluding _prefixed files)
    and calls each module's register(mcp) function.

    Args:
        mcp: The FastMCP server instance

    Returns:
        List of successfully registered tool names
    """
    tools_dir = Path(__file__).parent
    registered = []
    errors = []

    # Add parent directory to path for helpers import
    parent_dir = str(tools_dir.parent)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

    # Find all .py files (skip __init__.py and _prefixed files)
    for tool_file in sorted(tools_dir.glob("*.py")):
        module_name = tool_file.stem

        # Skip __init__.py and files starting with underscore
        if module_name.startswith("_") or module_name == "__init__":
            continue

        try:
            module = importlib.import_module(f"tools.{module_name}")

            if hasattr(module, "register"):
                module.register(mcp)
                registered.append(module_name)
                print(f"  [OK] Registered tool: {module_name}")
            else:
                errors.append(f"{module_name}: missing register() function")
                print(f"  [SKIP] {module_name}: no register() function")

        except Exception as e:
            errors.append(f"{module_name}: {str(e)}")
            print(f"  [ERROR] {module_name}: {e}")

    if errors:
        print(f"\nTool registration errors ({len(errors)}):")
        for error in errors:
            print(f"  - {error}")

    return registered
