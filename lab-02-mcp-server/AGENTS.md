# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

MCP (Model Context Protocol) server that exposes network operations as AI-callable tools. Uses auto-discovery to load tools from modular files, with Ansible playbooks handling device communication.

## Commands

```bash
# Development
mcp dev network_mcp_server.py          # Interactive MCP Inspector
mcp run network_mcp_server.py          # Run for Claude Desktop (local)
mcp run -t sse network_mcp_server.py   # Run for remote access

# Testing
python -m pytest tests/ -v             # Run all tests
python -m pytest tests/test_mcp_server.py::TestTopologyResource -v  # Single class

# Validation
python -c "from mcp.server.fastmcp import FastMCP; print('OK')"     # Check MCP
python -m py_compile network_mcp_server.py                           # Syntax check
```

## Architecture

### Auto-Discovery Pattern

The server auto-discovers and registers components at startup:

```
network_mcp_server.py
    ├── tools/__init__.py → register_all_tools(mcp)
    │   └── scans tools/*.py for register(mcp) functions
    └── resources/__init__.py → register_all_resources(mcp)
        └── scans resources/*.py for register(mcp) functions
```

Files prefixed with `_` (like `_template.py`) are skipped by auto-discovery.

### Tool Structure

Every tool follows this pattern:

```python
from typing import Dict, Any
from helpers import run_ansible_playbook, VALID_DEVICES

async def my_tool(device: str) -> Dict[str, Any]:
    """Docstring with Args/Returns/Example output."""
    if device not in VALID_DEVICES:
        return {"error": f"Invalid device '{device}'. Valid: {VALID_DEVICES}"}

    result = run_ansible_playbook("playbook.yml", {"target_host": device}, parse_json=True)

    if not result["success"]:
        return {"error": result.get("error", "Playbook failed")}

    return {"device": device, "data": result.get("data", {})}

def register(mcp):
    mcp.tool()(my_tool)
```

### Ansible Integration

All device operations go through `helpers/ansible.py`:

```python
run_ansible_playbook(
    playbook: str,           # e.g., "07-device-info.yml"
    extra_vars: dict,        # e.g., {"target_host": "spine1"}
    parse_json: bool = False # True for show commands that return JSON
) -> Dict with: success, return_code, stdout, stderr, data (if parse_json)
```

Playbooks live in `../lab-01-copilots/ansible/playbooks/`.

### Available Constants

From `helpers/constants.py`:
- `VALID_DEVICES`: `["spine1", "spine2", "leaf1", "leaf2", "leaf3", "leaf4"]`
- `VALID_LEAVES`: `["leaf1", "leaf2", "leaf3", "leaf4"]`
- `DEVICE_IPS`: Device name to IP mapping
- `IP_TO_DEVICE`: Reverse IP to device name lookup

## Adding New Tools

1. Copy `tools/_template.py` to `tools/your_tool.py`
2. Implement async function with type hints
3. Add validation for device names
4. Call appropriate Ansible playbook
5. Include `register(mcp)` function
6. Restart server - auto-discovered

See `prompts/` folder for guided tool creation prompts.

## Error Handling

Return errors as dictionaries, never raise exceptions:

```python
{"error": "Description", "context": "Additional info"}
```

## Testing Without Network

`TestTopologyResource` tests run without Containerlab. `TestDeviceTools` tests require the lab running.
