#!/usr/bin/env python3
"""
Alerting MCP Tools
Workshop: Build Intelligent Networks with AI

This module provides MCP-compatible tools for querying Prometheus alerts.
These tools can be imported and registered with the MCP server from Lab 2.

WORKING EXAMPLE: query_prometheus() and get_active_alerts() are complete.
EXTENSION TASK: Add analyze_alerts() using the alert_analyzer.py logic.
See prompts/ folder for AI assistance.

Usage:
    # In network_mcp_server.py, add:
    from alerting_tools import query_prometheus, get_active_alerts
    mcp.tool()(query_prometheus)
    mcp.tool()(get_active_alerts)
"""

import requests
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

# Configuration
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")


# =============================================================================
# WORKING EXAMPLE: Query Prometheus
# =============================================================================

async def query_prometheus(query: str) -> Dict[str, Any]:
    """
    Execute a PromQL query against Prometheus.

    This tool allows natural language access to Prometheus metrics through
    PromQL queries. Use it to check specific metrics or create custom queries.

    Args:
        query: PromQL query string (e.g., 'up', 'ALERTS{severity="critical"}')

    Returns:
        Dictionary with query results and metadata

    Example queries:
        - "up" - Check which instances are up
        - "up == 0" - Find down instances
        - "count(ALERTS) by (severity)" - Count alerts by severity
        - "rate(http_requests_total[5m])" - Request rate over 5 minutes

    Example:
        query_prometheus("up == 0")
        -> {"status": "success", "result_count": 2, "results": [...]}
    """
    try:
        url = f"{PROMETHEUS_URL}/api/v1/query"
        response = requests.get(
            url,
            params={"query": query},
            timeout=10
        )
        response.raise_for_status()

        data = response.json()

        if data.get("status") != "success":
            return {
                "status": "error",
                "error": data.get("error", "Unknown Prometheus error"),
                "errorType": data.get("errorType", "unknown")
            }

        results = data.get("data", {}).get("result", [])

        return {
            "status": "success",
            "query": query,
            "result_type": data.get("data", {}).get("resultType", "unknown"),
            "result_count": len(results),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }

    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "error": f"Cannot connect to Prometheus at {PROMETHEUS_URL}. Is it running?"
        }
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "error": "Prometheus query timed out after 10 seconds"
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error": f"Request failed: {str(e)}"
        }


# =============================================================================
# WORKING EXAMPLE: Get Active Alerts
# =============================================================================

async def get_active_alerts() -> Dict[str, Any]:
    """
    Get all active alerts from Prometheus.

    This tool fetches and summarizes all currently firing alerts from
    Prometheus. Use it to get a quick overview of network health.

    Returns:
        Dictionary with alert list, counts, and summary by severity

    Example:
        get_active_alerts()
        -> {
            "status": "success",
            "alert_count": 3,
            "alerts": [...],
            "by_severity": {"critical": 1, "warning": 2}
        }
    """
    try:
        url = f"{PROMETHEUS_URL}/api/v1/alerts"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get("status") != "success":
            return {
                "status": "error",
                "error": data.get("error", "Unknown error from Prometheus")
            }

        alerts = data.get("data", {}).get("alerts", [])

        # Process and summarize alerts
        processed_alerts = []
        by_severity = {}
        by_state = {"firing": 0, "pending": 0}

        for alert in alerts:
            labels = alert.get("labels", {})
            annotations = alert.get("annotations", {})
            state = alert.get("state", "unknown")

            severity = labels.get("severity", "unknown")
            by_severity[severity] = by_severity.get(severity, 0) + 1

            if state in by_state:
                by_state[state] += 1

            processed_alerts.append({
                "name": labels.get("alertname", "Unknown"),
                "severity": severity,
                "state": state,
                "instance": labels.get("instance", "N/A"),
                "job": labels.get("job", "N/A"),
                "summary": annotations.get("summary", "No summary"),
                "description": annotations.get("description", "No description"),
                "active_at": alert.get("activeAt", "unknown")
            })

        # Sort by severity (critical first)
        severity_order = {"critical": 0, "warning": 1, "info": 2, "unknown": 3}
        processed_alerts.sort(key=lambda x: severity_order.get(x["severity"], 3))

        return {
            "status": "success",
            "alert_count": len(alerts),
            "alerts": processed_alerts,
            "by_severity": by_severity,
            "by_state": by_state,
            "prometheus_url": PROMETHEUS_URL,
            "timestamp": datetime.now().isoformat()
        }

    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "error": f"Cannot connect to Prometheus at {PROMETHEUS_URL}. Is it running?",
            "help": "Start Prometheus with: docker compose up -d"
        }
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "error": "Prometheus request timed out"
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error": f"Request failed: {str(e)}"
        }


# =============================================================================
# EXTENSION TASK: Add analyze_alerts() tool
# =============================================================================
# See prompts/add-alert-analysis-tool.md for AI assistance
#
# This tool should:
# 1. Call get_active_alerts() to fetch current alerts
# 2. Use the format_alerts_for_llm() function from alert_analyzer.py
# 3. Return a structured analysis with priorities and recommendations
#
# For AI-powered analysis, you can optionally integrate with:
# - OpenAI API
# - Anthropic API
# - Local Ollama
#
# Or provide rule-based analysis without an LLM.


# =============================================================================
# Standalone testing
# =============================================================================

if __name__ == "__main__":
    import asyncio

    async def test_tools():
        print("Testing alerting tools...")
        print("\n" + "=" * 50)
        print("Testing query_prometheus('up'):")
        print("=" * 50)
        result = await query_prometheus("up")
        print(f"Status: {result.get('status')}")
        print(f"Results: {result.get('result_count', 0)} items")

        print("\n" + "=" * 50)
        print("Testing get_active_alerts():")
        print("=" * 50)
        result = await get_active_alerts()
        print(f"Status: {result.get('status')}")
        print(f"Alerts: {result.get('alert_count', 0)}")
        if result.get("by_severity"):
            print(f"By severity: {result['by_severity']}")

    asyncio.run(test_tools())
