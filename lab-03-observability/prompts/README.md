# AI Prompts for Lab 3: Observability

Copy the contents of these files and paste into Claude Code.

## Available Prompts

| File | Purpose | Priority |
|------|---------|----------|
| `add-prometheus-tools.md` | Integrate alerting with Lab 2 MCP server | **Primary** |
| `add-alert-rules.md` | Add new Prometheus alerting rules | Optional |
| `add-alert-analysis-tool.md` | Add AI-powered alert analysis | Optional |
| `add-alert-output.md` | Add Slack notifications | Optional |
| `add-dashboard-panel.md` | Add custom Grafana panels | Optional |

## Usage

1. Start monitoring stack: `docker compose up -d`
2. Open a prompt file
3. Copy the entire contents
4. Paste into Claude Code
5. Test changes

## Testing

```bash
# MCP Inspector (after adding tools)
cd ../lab-02-mcp-server
mcp dev network_mcp_server.py

# Prometheus rules (after adding rules)
docker compose restart prometheus
curl -s http://localhost:9090/api/v1/rules | jq '.data.groups[].rules[].name'

# Grafana (after dashboard changes)
docker compose restart grafana
# Open http://localhost:3000
```
