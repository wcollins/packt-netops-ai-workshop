# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Lab 3 provides an AI-powered network observability stack (Prometheus + Grafana) with MCP-compatible alerting tools. It extends the Lab 2 MCP server with alerting capabilities, enabling natural language queries like "Are there any alerts?" through Claude Desktop.

## Commands

### Stack Management
```bash
docker compose up -d              # Start Prometheus + Grafana + Network Exporter
docker compose down               # Stop stack
docker compose ps                 # Check service status
docker compose logs prometheus    # View Prometheus logs
docker compose restart prometheus # Reload after alert rule changes
```

### Testing Tools
```bash
python alerting_tools.py                    # Test MCP alerting functions
python agent/alert_analyzer.py --test       # Single LLM analysis (requires API key)
```

### Validation
```bash
curl http://localhost:9090/api/v1/alerts    # Query active alerts
curl http://localhost:8888/metrics | grep bgp  # Check exporter metrics
curl -s http://localhost:9090/api/v1/rules | jq '.data.groups[].rules[].name'  # List alert rules
```

### MCP Integration Testing
```bash
cd ../lab-02-mcp-server
mcp dev network_mcp_server.py    # Test in MCP Inspector
```

## Architecture

### Data Flow
```
Network Exporter (:8888) → Prometheus (:9090) → alerting_tools.py → MCP Server → Claude Desktop
      ↓                           ↓
  Synthetic metrics         Alert evaluation
  (BGP, interfaces,         (alert_rules.yml)
   CPU, memory, temp)             ↓
                               Grafana (:3000)
```

### Key Components

**`network_exporter.py`** - Generates synthetic metrics for the spine-leaf topology:
- BGP: `bgp_session_state`, `bgp_prefixes_received` (10% flap chance)
- Interfaces: `interface_up`, `interface_errors_total`, `interface_traffic_bytes` (5% flap chance)
- Health: `device_cpu_percent`, `device_memory_percent`, `device_temperature_celsius`

**`alerting_tools.py`** - MCP-compatible functions:
- `query_prometheus(query: str)` - Execute PromQL queries
- `get_active_alerts()` - Fetch alerts with severity breakdown

**`agent/alert_analyzer.py`** - Standalone LLM-powered analysis (OpenAI/Anthropic/Ollama)

### Alert Rules (`prometheus/alert_rules.yml`)
| Alert | Severity | Expression |
|-------|----------|------------|
| TestAlert | info | `vector(1)` (always fires) |
| BGPSessionDown | critical | `bgp_session_state == 0` |
| InterfaceDown | critical | `interface_up == 0` |
| HighCPU | warning | `device_cpu_percent > 80` |
| HighMemory | warning | `device_memory_percent > 85` |
| InterfaceErrors | warning | `rate(interface_errors_total[5m]) > 10` |
| HighTemperature | warning | `device_temperature_celsius > 65` |

## Integration with Lab 2

The primary extension task creates `lab-02-mcp-server/tools/prometheus_alerts.py`:
```python
import sys, os
lab03_path = os.path.join(os.path.dirname(__file__), "..", "..", "lab-03-observability")
sys.path.insert(0, lab03_path)
from alerting_tools import query_prometheus, get_active_alerts

def register(mcp):
    mcp.tool()(query_prometheus)
    mcp.tool()(get_active_alerts)
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PROMETHEUS_URL` | `http://localhost:9090` | Prometheus API endpoint |
| `CHECK_INTERVAL` | `60` | Alert analyzer check interval (seconds) |
| `OPENAI_API_KEY` | - | For OpenAI LLM analysis |
| `ANTHROPIC_API_KEY` | - | For Anthropic Claude analysis |

## Service Ports

| Service | Port | URL |
|---------|------|-----|
| Prometheus | 9090 | http://localhost:9090 |
| Grafana | 3000 | http://localhost:3000 (admin/admin) |
| Network Exporter | 8888 | http://localhost:8888/metrics |

## Extension Prompts

Located in `prompts/`:
- `add-prometheus-tools.md` - **Primary**: Integrate alerting with Lab 2 MCP server
- `add-alert-rules.md` - Add custom Prometheus alert rules
- `add-alert-analysis-tool.md` - Add AI-powered analysis to MCP
- `add-alert-output.md` - Add Slack notifications
- `add-dashboard-panel.md` - Add custom Grafana panels
