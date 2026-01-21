# Add Prometheus MCP Tools

Create `../lab-02-mcp-server/tools/prometheus_alerts.py` - integrate alerting with the MCP server.

**This is the primary extension task for Lab 3.**

## Current Setup

- MCP server: `../lab-02-mcp-server/network_mcp_server.py`
- Alerting tools: `./alerting_tools.py` (this directory)
- Prometheus: `http://localhost:9090`

## Working Tools in alerting_tools.py

The file has two async functions ready to use:
1. `query_prometheus(query: str)` - Execute PromQL queries
2. `get_active_alerts()` - Get all active alerts with severity breakdown

## Requirements

Create `../lab-02-mcp-server/tools/prometheus_alerts.py` that:
1. Imports the functions from `alerting_tools.py`
2. Includes a `register(mcp)` function for auto-discovery
3. Handles the path import correctly (lab-03 is sibling to lab-02)

## Expected Structure

```python
#!/usr/bin/env python3
"""
MCP Tool: Prometheus Alerting
"""

import sys
import os

# Add lab-03 to path for importing alerting_tools
lab03_path = os.path.join(os.path.dirname(__file__), "..", "..", "lab-03-observability")
sys.path.insert(0, lab03_path)

from alerting_tools import query_prometheus, get_active_alerts


def register(mcp):
    """Register Prometheus alerting tools with the MCP server."""
    mcp.tool()(query_prometheus)
    mcp.tool()(get_active_alerts)
```

Create the file directly.
