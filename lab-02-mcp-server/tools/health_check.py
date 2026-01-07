#!/usr/bin/env python3
"""
MCP Tool: Health Check

Checks the health of all network devices in the topology using Ansible.
"""

from typing import Dict, Any
from tools.get_device_info import get_device_info
from helpers import VALID_DEVICES
import asyncio


async def health_check_all() -> Dict[str, Any]:
    """
    Check health of all devices in the topology.

    Returns:
        Dictionary with health summary and per-device status

    Example output:
        {
            "total_devices": 6,
            "healthy": 6,
            "unhealthy": 0,
            "status": "healthy",
            "devices": {
                "spine1": {"status": "ok", "version": "4.35.0.1F", "uptime_seconds": 12345},
                ...
            }
        }
    """
    # Query all devices in parallel
    results = await asyncio.gather(
        *[get_device_info(device) for device in VALID_DEVICES]
    )

    # Process results
    devices = {}
    healthy_count = 0

    for device, result in zip(VALID_DEVICES, results):
        if "error" in result:
            devices[device] = {"status": "unreachable", "error": result["error"]}
        else:
            devices[device] = {
                "status": "ok",
                "version": result.get("version", "unknown"),
                "uptime_seconds": result.get("uptime_seconds", 0)
            }
            healthy_count += 1

    # Determine overall status
    total = len(VALID_DEVICES)
    unhealthy_count = total - healthy_count

    if unhealthy_count == 0:
        status = "healthy"
    elif unhealthy_count > total / 2:
        status = "critical"
    else:
        status = "degraded"

    return {
        "total_devices": total,
        "healthy": healthy_count,
        "unhealthy": unhealthy_count,
        "status": status,
        "devices": devices
    }


def register(mcp):
    """Register health_check_all tool with the MCP server."""
    mcp.tool()(health_check_all)
