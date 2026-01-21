# Add Prometheus Alert Rules

Add new alerting rules to `prometheus/alert_rules.yml`.

## Existing Rules

- TestAlert (info) - always fires for testing
- HighMemoryUsage (warning) - memory > 85%
- InstanceDown (critical) - instance unreachable for 1 min

## Existing Rule Format

```yaml
- alert: InstanceDown
  expr: up == 0
  for: 1m
  labels:
    severity: critical
    team: network
  annotations:
    summary: "Instance {{ $labels.instance }} is down"
    description: "{{ $labels.instance }} has been unreachable for more than 1 minute."
```

## Requirements

Create 2-3 new alert rules:

1. **HighCPU** (warning)
   - Fire when CPU > 80% for 5 minutes
   - expr: `100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80`

2. **TargetMissing** (critical)
   - Fire when scrape target missing for 5 minutes
   - expr: `up == 0 or absent(up{job="network"})`

3. **HighNetworkErrors** (warning) - optional
   - Fire when network interface errors increasing
   - expr: `rate(node_network_receive_errs_total[5m]) > 0`

Format as YAML matching the existing structure. Add to the rules section in `alert_rules.yml`.
