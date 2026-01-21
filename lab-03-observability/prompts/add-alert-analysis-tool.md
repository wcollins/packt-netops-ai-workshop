# Add Alert Analysis Tool

Create `../lab-02-mcp-server/tools/analyze_alerts.py` - add intelligent alert analysis to the MCP server.

## Current Setup

- MCP server: `../lab-02-mcp-server/network_mcp_server.py`
- Alerting tools: `./alerting_tools.py` (this directory)
- Prometheus: `http://localhost:9090`

## Working Tools in alerting_tools.py

```python
async def get_active_alerts() -> Dict[str, Any]:
    """Returns: {"status": "success", "alert_count": 3, "alerts": [...], "by_severity": {...}}"""
```

## Network Context

- 2 spine switches (spine1, spine2) - AS 65100
- 4 leaf switches (leaf1-4) - AS 65101-65104
- eBGP peering between spines and leaves

## Requirements

Create `../lab-02-mcp-server/tools/analyze_alerts.py` that:
1. Imports `get_active_alerts` from `alerting_tools.py`
2. Implements `analyze_alerts()` async function
3. Includes a `register(mcp)` function for auto-discovery
4. Handles the path import correctly (lab-03 is sibling to lab-02)

## Expected Structure

```python
#!/usr/bin/env python3
"""
MCP Tool: Alert Analysis
"""

import sys
import os
from typing import Dict, Any

# Add lab-03 to path for importing alerting_tools
lab03_path = os.path.join(os.path.dirname(__file__), "..", "..", "lab-03-observability")
sys.path.insert(0, lab03_path)

from alerting_tools import get_active_alerts


def generate_recommendation(alert_name: str, severity: str, instance: str) -> Dict[str, str]:
    """Generate recommendations for common alert types."""
    recommendations = {
        "InstanceDown": {
            "cause": "Device not responding to health checks",
            "action": "Verify power, network connectivity, and service status"
        },
        "HighMemoryUsage": {
            "cause": "Memory utilization exceeded threshold",
            "action": "Check for memory leaks, consider scaling resources"
        },
        "HighCPU": {
            "cause": "CPU utilization exceeded threshold",
            "action": "Identify high-CPU processes, check for runaway tasks"
        },
        "BGPNeighborDown": {
            "cause": "BGP session lost with peer",
            "action": "Check physical links, verify BGP configuration on both ends"
        }
    }

    default = {
        "cause": "Alert condition met",
        "action": f"Investigate {alert_name} on {instance}"
    }

    rec = recommendations.get(alert_name, default)
    return {"alert": alert_name, "instance": instance, "severity": severity, **rec}


async def analyze_alerts() -> Dict[str, Any]:
    """
    Analyze active alerts and provide recommendations.

    This tool fetches current alerts and provides intelligent analysis
    including priority ranking, potential root causes, and recommended
    actions based on network context.

    Returns:
        Dictionary with analysis summary and recommendations

    Example:
        analyze_alerts()
        -> {
            "status": "success",
            "summary": "2 alerts require attention",
            "network_health": "degraded",
            "recommendations": [...]
        }
    """
    # Fetch current alerts
    alerts_result = await get_active_alerts()

    if alerts_result.get("status") != "success":
        return alerts_result

    alerts = alerts_result.get("alerts", [])
    by_severity = alerts_result.get("by_severity", {})

    # Determine network health
    if by_severity.get("critical", 0) > 0:
        network_health = "critical"
    elif by_severity.get("warning", 0) > 0:
        network_health = "degraded"
    else:
        network_health = "healthy"

    # Generate recommendations for each alert
    recommendations = []
    for alert in alerts:
        rec = generate_recommendation(
            alert.get("name", "Unknown"),
            alert.get("severity", "unknown"),
            alert.get("instance", "N/A")
        )
        recommendations.append(rec)

    # Build summary
    alert_count = len(alerts)
    if alert_count == 0:
        summary = "No active alerts - network is healthy"
    elif alert_count == 1:
        summary = "1 alert requires attention"
    else:
        summary = f"{alert_count} alerts require attention"

    return {
        "status": "success",
        "summary": summary,
        "network_health": network_health,
        "alert_count": alert_count,
        "by_severity": by_severity,
        "priority_alerts": alerts,  # Already sorted by severity
        "recommendations": recommendations
    }


def register(mcp):
    """Register alert analysis tool with the MCP server."""
    mcp.tool()(analyze_alerts)
```

Create the file directly.
