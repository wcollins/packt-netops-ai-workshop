# Lab 3: AI-Powered Network Observability

**Duration:** 60 minutes | **Difficulty:** Intermediate

---

## Learning Objectives

By the end of this lab, you will:

- Deploy a monitoring stack (Prometheus + Grafana) with one command
- Review working MCP-compatible alerting tools
- **Integrate alerting tools** into the MCP server from Lab 2
- Query alerts through Claude Desktop ("Are there any alerts?")
- Understand how MCP unifies network operations with observability

**Lab 2 Connection:** This lab extends the MCP server from Lab 2 with alerting tools, enabling natural language access to network monitoring.

---

## Lab Architecture

```
┌─────────────┐
│ Claude      │  "Are there any alerts?"
│ Desktop     │
└──────┬──────┘
       │ MCP Protocol
┌──────┴──────┐
│ MCP Server  │  (Extended from Lab 2)
│ + Alerting  │
└──────┬──────┘
       │
   ┌───┴───────────────┐
   │                   │
   │ Alerting Tools    │
   │ (NEW in Lab 3)    │
   │                   │
   └─────────┬─────────┘
             │ HTTP API
┌────────────┴────────────────────────────┐
│        Monitoring Stack (Docker)        │
│                                         │
│  ┌──────────┐       ┌──────────┐       │
│  │Prometheus│       │  Grafana │       │
│  │  :9090   │──────▶│   :3000  │       │
│  └──────────┘       └──────────┘       │
└─────────────────────────────────────────┘
```

---

## What You Start With (Working Examples)

### Monitoring Stack
| Component | Status | Description |
|-----------|--------|-------------|
| `docker-compose.yml` | Working | Prometheus + Grafana + Network Exporter |
| `network_exporter.py` | Working | Synthetic metrics for BGP, interfaces, device health |
| `alert_rules.yml` | Working | 7 alert rules (BGP, interfaces, CPU, memory, temperature) |
| `network-overview.json` | Working | Grafana dashboard with 4 panels |

### MCP Alerting Tools
| Component | Status | Description |
|-----------|--------|-------------|
| `alerting_tools.py` | Working | MCP-compatible alerting functions |
| `query_prometheus()` | Working | Execute PromQL queries |
| `get_active_alerts()` | Working | Fetch and summarize alerts |

### Standalone AI Analyzer (Optional)
| Component | Status | Description |
|-----------|--------|-------------|
| `agent/alert_analyzer.py` | Working | LLM-powered alert analysis (OpenAI/Anthropic/Ollama) |

**Example:** In Claude Desktop, say: "Are there any alerts firing?"

## What You'll Add (Extension Tasks)

Use Claude Code to extend the observability stack:

### Required Extension
- [ ] Integrate alerting tools into Lab 2 MCP server (~20 min)

### Optional Extensions (if time permits)
- [ ] Add custom Prometheus alert rules (~10 min)
- [ ] Run standalone AI alert analyzer (~10 min)

## AI Prompts

Ready-to-use prompts are in the `prompts/` folder:

- `prompts/add-prometheus-tools.md` - Integrate alerting with MCP server (PRIMARY)
- `prompts/add-alert-rules.md` - Add new Prometheus alerting rules
- `prompts/add-alert-analysis-tool.md` - Add AI-powered analysis to MCP

---

## Prerequisites

- Lab 2 completed (MCP server working)
- Docker Compose installed
- Claude Desktop configured with MCP server

---

## Task 1: Deploy Monitoring Stack (10 min)

### Step 1.1: Start the stack

```bash
cd lab-03-observability
docker compose up -d
```

### Step 1.2: Verify services

```bash
docker compose ps
```

Expected output:
```
NAME               STATUS    PORTS
prometheus         running   0.0.0.0:9090->9090/tcp
grafana            running   0.0.0.0:3000->3000/tcp
network_exporter   running   0.0.0.0:8888->8888/tcp
```

### Step 1.3: Access dashboards

- **Prometheus:** http://localhost:9090
- **Grafana:** http://localhost:3000 (admin/admin)
- **Network Exporter Metrics:** http://localhost:8888/metrics

### Step 1.4: View existing alerts

1. Open http://localhost:9090/alerts
2. You should see 7 configured alert rules (TestAlert, BGPSessionDown, InterfaceDown, HighCPU, HighMemory, InterfaceErrors, HighTemperature)
3. The "TestAlert" fires constantly; other alerts fire based on simulated network conditions

**Note:** This lab includes a synthetic network metrics exporter that generates realistic BGP, interface, and device health metrics for the spine-leaf topology. These metrics enable meaningful alerting demonstrations without requiring real network device exporters.

---

## Task 2: Review Alerting Tools (10 min)

### Step 2.1: Examine the alerting tools

Review `alerting_tools.py` to understand the MCP-compatible functions:

```python
# Two working tools ready for MCP integration:
async def query_prometheus(query: str) -> Dict[str, Any]
async def get_active_alerts() -> Dict[str, Any]
```

### Step 2.2: Test tools standalone

```bash
python alerting_tools.py
```

Expected output:
```
Testing alerting tools...
==================================================
Testing query_prometheus('up'):
==================================================
Status: success
Results: 1 items

==================================================
Testing get_active_alerts():
==================================================
Status: success
Alerts: 1
By severity: {'info': 1}
```

### Step 2.3: Review the code patterns

Note how `alerting_tools.py` follows the same patterns as Lab 2 tools:
- Async functions with type hints
- Docstrings with examples
- Error handling with helpful messages
- Ready for `mcp.tool()` registration

---

## Task 3: Integrate with MCP Server (20 min)

This is the primary extension task - adding alerting capabilities to your Lab 2 MCP server.

### Step 3.1: Open the AI prompt

Open `prompts/add-prometheus-tools.md` and copy the prompt into Claude Code.

### Step 3.2: Apply the integration

Claude Code will create a new file at `../lab-02-mcp-server/tools/prometheus_alerts.py` that:
1. Imports the alerting functions from `lab-03-observability/alerting_tools.py`
2. Includes a `register(mcp)` function for auto-discovery
3. Handles the path correctly so Lab 2's MCP server can find Lab 3's tools

**Expected file location:** `lab-02-mcp-server/tools/prometheus_alerts.py`

### Step 3.3: Verify in MCP Inspector

```bash
cd ../lab-02-mcp-server
mcp dev network_mcp_server.py
```

In the inspector:
1. Find `query_prometheus` and `get_active_alerts` tools
2. Test `get_active_alerts` - should show the TestAlert
3. Test `query_prometheus` with query: `up`

### Step 3.4: Test in Claude Desktop

Restart Claude Desktop, then try:
- "Are there any alerts firing?"
- "Query Prometheus for the up metric"
- "What's the network health status?"

---

## Task 4: Test Natural Language Queries (10 min)

### Step 4.1: Query alerts

In Claude Desktop:
```
Check if there are any active alerts in Prometheus
```

Expected response includes alert details from `get_active_alerts()`.

### Step 4.2: Execute PromQL

```
Query Prometheus: count(ALERTS) by (severity)
```

### Step 4.3: Combine with Lab 2 tools

Try combining alerting with device operations:
```
Check if there are any alerts, and if so, show me the BGP neighbors on spine1
```

---

## Task 5: Optional Extensions (10 min)

Choose one if time permits:

### Option A: Add Custom Alert Rules

Use `prompts/add-alert-rules.md` to add a new alert:

```bash
# Edit alert rules
# Then reload Prometheus
docker compose restart prometheus

# Verify new rule loaded
curl -s http://localhost:9090/api/v1/rules | jq '.data.groups[].rules[].name'
```

### Option B: Run Standalone AI Analyzer

If you have an API key or Ollama installed:

```bash
# Set API key (or use Ollama)
export OPENAI_API_KEY="sk-..."

# Run single analysis
python agent/alert_analyzer.py --test
```

The analyzer uses an LLM to provide:
- Priority ranking of alerts
- Root cause analysis
- Recommended actions

---

## Success Criteria

- [ ] Prometheus and Grafana running (`docker compose ps`)
- [ ] Alert rules visible at http://localhost:9090/alerts
- [ ] Alerting tools integrated into Lab 2 MCP server
- [ ] Claude Desktop can query alerts via natural language

---

## Validation Commands

```bash
# Check monitoring stack
docker compose ps

# Check network exporter metrics
curl -s http://localhost:8888/metrics | grep bgp

# Query Prometheus alerts API
curl http://localhost:9090/api/v1/alerts | python -m json.tool

# Check alert rules
curl -s http://localhost:9090/api/v1/rules | jq '.data.groups[].rules[].name'

# Query BGP session states
curl -s 'http://localhost:9090/api/v1/query?query=bgp_session_state' | jq

# Test alerting tools
python alerting_tools.py
```

---

## Troubleshooting

### Docker Compose won't start

```bash
# Check for port conflicts
lsof -i :9090
lsof -i :3000

# View logs
docker compose logs prometheus
docker compose logs grafana
```

### Prometheus shows no alerts

```bash
# Check alert rules loaded
curl http://localhost:9090/api/v1/rules

# Verify configuration
docker exec prometheus cat /etc/prometheus/prometheus.yml
```

### MCP tools not appearing

1. Verify `alerting_tools.py` is in `lab-02-mcp-server/tools/`
2. Check for Python syntax errors: `python -m py_compile tools/alerting_tools.py`
3. Restart Claude Desktop completely
4. Check MCP Inspector for errors

### Cannot connect to Prometheus from MCP

Ensure the `PROMETHEUS_URL` environment variable is set correctly:
```bash
export PROMETHEUS_URL="http://localhost:9090"
```

---

## Key Takeaways

1. **MCP unifies operations and observability** - Same interface for device management and alert queries
2. **Quick deployment** - Monitoring stack in one command (`docker compose up -d`)
3. **Reusable patterns** - Alerting tools follow the same structure as Lab 2 tools
4. **Natural language access** - "Are there any alerts?" instead of remembering PromQL

---

## Cleanup

When finished:

```bash
docker compose down
```

---

## Workshop Complete!

Congratulations! You've completed all three labs:

1. **Lab 1** - Built Ansible playbooks with Claude Code (parameterized for MCP)
2. **Lab 2** - Created MCP server that invokes playbooks ("Add VLAN 30 to leaf1")
3. **Lab 3** - Extended MCP with alerting tools ("Are there any alerts?")

### What You Built

By the end of this workshop, you have an MCP server that can:
- Query device information via Ansible
- Configure VLANs and interfaces
- Backup configurations
- Query Prometheus alerts
- Analyze network health

All through natural language in Claude Desktop!

### Next Steps

- Add more MCP tools for your specific network operations
- Explore MCP resources for topology and inventory data
- Build custom dashboards in Grafana
- Add Slack/email notifications for critical alerts

Return to the main README for additional resources and next steps.
