#!/usr/bin/env python3
"""
AI Alert Analyzer
Workshop: Build Intelligent Networks with AI

This script fetches alerts from Prometheus and uses an LLM to analyze,
prioritize, and recommend actions.

WORKING EXAMPLE: This analyzer is fully functional with OpenAI/Anthropic/Ollama support.
EXTENSION TASK: Add Slack notifications, new alert rules, or custom dashboard panels.
See prompts/ folder for AI assistance.

Usage:
    python alert_analyzer.py          # Run continuous monitoring
    python alert_analyzer.py --test   # Run single analysis

Requirements:
    pip install requests openai anthropic python-dotenv

Environment Variables:
    OPENAI_API_KEY - Your OpenAI API key (or ANTHROPIC_API_KEY for Claude)
"""

import requests
import json
import os
import sys
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        # Uncomment to also log to file:
        # logging.FileHandler('alert_analyzer.log')
    ]
)
logger = logging.getLogger(__name__)

# Configuration
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))  # seconds


# =============================================================================
# WORKING EXAMPLE: Fetch Alerts from Prometheus
# =============================================================================

def get_prometheus_alerts() -> List[Dict[str, Any]]:
    """
    Fetch active alerts from Prometheus.

    Returns:
        List of alert dictionaries from Prometheus API

    Example response structure:
        [
            {
                "labels": {"alertname": "HighCPU", "severity": "warning"},
                "annotations": {"summary": "CPU > 80%"},
                "state": "firing"
            }
        ]
    """
    try:
        url = f"{PROMETHEUS_URL}/api/v1/alerts"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        alerts = data.get("data", {}).get("alerts", [])

        logger.info(f"Fetched {len(alerts)} alerts from Prometheus")
        return alerts

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch alerts: {e}")
        return []


# =============================================================================
# WORKING EXAMPLE: Format Alerts for LLM Analysis
# =============================================================================

def format_alerts_for_llm(alerts: List[Dict[str, Any]]) -> str:
    """
    Format alerts into a readable summary for the LLM.

    Args:
        alerts: List of alert dictionaries from Prometheus

    Returns:
        Formatted string describing all alerts

    Example output:
        "Alert 1: HighCPU
         Severity: warning
         Instance: server1:9090
         Summary: CPU usage above 80%
         Description: The CPU has been above 80% for 5 minutes.
         ---"
    """
    if not alerts:
        return "No active alerts."

    formatted = []
    for i, alert in enumerate(alerts, 1):
        labels = alert.get("labels", {})
        annotations = alert.get("annotations", {})

        # Extract alert details
        name = labels.get("alertname", "Unknown")
        severity = labels.get("severity", "unknown")
        instance = labels.get("instance", "N/A")
        job = labels.get("job", "N/A")
        summary = annotations.get("summary", "No summary provided")
        description = annotations.get("description", "No description provided")
        state = alert.get("state", "unknown")

        # Format as readable text
        alert_text = f"""Alert {i}: {name}
  Severity: {severity}
  State: {state}
  Instance: {instance}
  Job: {job}
  Summary: {summary}
  Description: {description}"""

        formatted.append(alert_text)

    return "\n---\n".join(formatted)


# =============================================================================
# WORKING EXAMPLE: Analyze Alerts with LLM
# =============================================================================

def analyze_alerts_with_llm(alerts: List[Dict[str, Any]]) -> str:
    """
    Use LLM to analyze and prioritize alerts.

    Args:
        alerts: List of alert dictionaries

    Returns:
        LLM's analysis with prioritization and recommendations

    The function:
        1. Formats alerts for the LLM
        2. Creates an effective prompt
        3. Calls the appropriate LLM API
        4. Returns the analysis
    """
    if not alerts:
        return "No active alerts. Network is healthy."

    # Format alerts for LLM
    alert_summary = format_alerts_for_llm(alerts)

    # Create the analysis prompt
    prompt = f"""You are a network operations expert analyzing alerts from a spine-leaf data center network.

## Current Alerts

{alert_summary}

## Network Context
- Topology: 2 spine switches + 4 leaf switches
- Devices: spine1, spine2, leaf1-4
- Running eBGP for routing (AS 65100 for spines, 65101-65104 for leaves)
- Management IPs: 198.18.1.11-12 (spines), 198.18.1.21-24 (leaves)

## Analysis Required

Please provide:

1. **Priority Ranking** - Order alerts from most to least critical
   - Critical: Service-affecting issues requiring immediate action
   - Warning: Issues that may become critical if not addressed
   - Info: Informational alerts for awareness

2. **Root Cause Analysis** - For each alert:
   - What is likely causing this alert?
   - Are any alerts related or correlated?

3. **Recommended Actions** - Specific, actionable steps:
   - Immediate actions to take
   - Commands to run for investigation
   - Configuration changes if needed

4. **Overall Network Health** - Brief summary (1-2 sentences)

Be concise and focus on actionable recommendations."""

    # Check which LLM API is available and call it
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if openai_key:
        return _call_openai(prompt, openai_key)
    elif anthropic_key:
        return _call_anthropic(prompt, anthropic_key)
    else:
        return _call_ollama(prompt)


# =============================================================================
# WORKING EXAMPLE: LLM API Integrations
# =============================================================================

def _call_openai(prompt: str, api_key: str) -> str:
    """Call OpenAI API for analysis."""
    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful network operations assistant specializing in data center networks."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.3  # Lower = more focused/deterministic
        )

        return response.choices[0].message.content

    except ImportError:
        return "Error: openai package not installed. Run: pip install openai"
    except Exception as e:
        return f"Error calling OpenAI: {e}"


def _call_anthropic(prompt: str, api_key: str) -> str:
    """Call Anthropic Claude API for analysis."""
    try:
        from anthropic import Anthropic

        client = Anthropic(api_key=api_key)

        response = client.messages.create(
            model="claude-3-5-haiku-latest",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.content[0].text

    except ImportError:
        return "Error: anthropic package not installed. Run: pip install anthropic"
    except Exception as e:
        return f"Error calling Anthropic: {e}"


def _call_ollama(prompt: str) -> str:
    """Call local Ollama for analysis (free, no API key needed)."""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",  # or your preferred model
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json().get("response", "No response from Ollama")

    except requests.exceptions.RequestException as e:
        return f"Error calling Ollama: {e}\nMake sure Ollama is running: ollama serve"


# =============================================================================
# WORKING EXAMPLE: Main Analysis Functions
# =============================================================================

def run_single_analysis() -> None:
    """Run a single alert analysis."""
    logger.info("Running single alert analysis...")

    alerts = get_prometheus_alerts()
    analysis = analyze_alerts_with_llm(alerts)

    print("\n" + "=" * 60)
    print("AI ALERT ANALYSIS")
    print("=" * 60)
    print(f"\nTimestamp: {datetime.now().isoformat()}")
    print(f"Alerts found: {len(alerts)}")
    print("\n" + "-" * 60)
    print(analysis)
    print("=" * 60 + "\n")


def run_continuous_monitoring() -> None:
    """Run continuous monitoring loop."""
    logger.info(f"Starting continuous monitoring (interval: {CHECK_INTERVAL}s)")
    logger.info("Press Ctrl+C to stop")

    try:
        while True:
            run_single_analysis()
            logger.info(f"Sleeping for {CHECK_INTERVAL} seconds...")
            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")


# =============================================================================
# EXTENSION TASKS: Add new features below
# =============================================================================
# See prompts/ folder for AI assistance with these tasks:
#
# 1. Add Slack notification output
#    See: prompts/add-alert-output.md
#
# 2. Add new Prometheus alert rules
#    See: prompts/add-alert-rules.md
#
# 3. Add custom Grafana dashboard panels
#    See: prompts/add-dashboard-panel.md


def main():
    """Main entry point."""
    print("""
    ╔═══════════════════════════════════════╗
    ║     AI Alert Analyzer                 ║
    ║     Network Operations Workshop       ║
    ╚═══════════════════════════════════════╝
    """)

    # Check for test mode
    if "--test" in sys.argv or "-t" in sys.argv:
        run_single_analysis()
    else:
        run_continuous_monitoring()


if __name__ == "__main__":
    main()
