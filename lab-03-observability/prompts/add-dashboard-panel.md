# Add Grafana Dashboard Panels

Add new panels to `grafana/dashboards/network-overview.json`.

## Current Dashboard

- Data source: Prometheus (default)
- Existing panels: Active Alerts stat, Prometheus Up stat, Alert Timeline graph
- Grid width: 24 units

## Requirements

Create JSON for two panels:

### 1. Alerts by Severity (Pie Chart)

```json
{
  "id": 10,
  "title": "Alerts by Severity",
  "type": "piechart",
  "gridPos": {"h": 8, "w": 8, "x": 16, "y": 0},
  "targets": [{
    "expr": "count(ALERTS{alertstate=\"firing\"}) by (severity)",
    "legendFormat": "{{severity}}"
  }]
}
```

Use color overrides: red=critical, yellow=warning, blue=info.

### 2. Active Alerts Table

```json
{
  "id": 11,
  "title": "Active Alerts",
  "type": "table",
  "gridPos": {"h": 8, "w": 24, "x": 0, "y": 8},
  "targets": [{
    "expr": "ALERTS{alertstate=\"firing\"}",
    "format": "table",
    "instant": true
  }]
}
```

Add transformations to show: Alert name, Severity (color-coded), Instance, Time.

## How to Add

1. Open `grafana/dashboards/network-overview.json`
2. Find the `panels` array
3. Add the new panel objects (adjust `id` to be unique)
4. Restart Grafana: `docker compose restart grafana`
