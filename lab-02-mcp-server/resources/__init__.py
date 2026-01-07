"""
Auto-discovery and registration of MCP resources.

This module automatically imports all resource modules and registers them
with the MCP server. Resources are discovered by scanning for .py files
that don't start with underscore (_).

Usage in network_mcp_server.py:
    from resources import register_all_resources
    register_all_resources(mcp)
"""

import importlib
import sys
from pathlib import Path


def register_all_resources(mcp):
    """
    Auto-discover and register all resources with the MCP server.

    Scans the resources/ directory for .py files (excluding _prefixed files)
    and calls each module's register(mcp) function.

    Args:
        mcp: The FastMCP server instance

    Returns:
        List of successfully registered resource names
    """
    resources_dir = Path(__file__).parent
    registered = []

    # Add parent directory to path for helpers import
    parent_dir = str(resources_dir.parent)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

    # Find all .py files (skip __init__.py and _prefixed files)
    for resource_file in sorted(resources_dir.glob("*.py")):
        module_name = resource_file.stem

        if module_name.startswith("_") or module_name == "__init__":
            continue

        try:
            module = importlib.import_module(f"resources.{module_name}")

            if hasattr(module, "register"):
                module.register(mcp)
                registered.append(module_name)
                print(f"  [OK] Registered resource: {module_name}")
            else:
                print(f"  [SKIP] {module_name}: no register() function")

        except Exception as e:
            print(f"  [ERROR] {module_name}: {e}")

    return registered
