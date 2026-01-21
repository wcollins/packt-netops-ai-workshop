# Add Slack Notifications

Add Slack webhook support to `agent/alert_analyzer.py`.

## Requirements

Create `send_to_slack(analysis: str, alert_count: int, has_critical: bool)` function that:
1. Gets webhook URL from `SLACK_WEBHOOK_URL` environment variable
2. Formats message with color coding:
   - Green (#36a64f) - no alerts
   - Yellow (#ffcc00) - warnings only
   - Red (#ff0000) - critical alerts
3. Posts to Slack webhook

## Slack Webhook Format

```python
requests.post(webhook_url, json={
    "attachments": [{
        "color": "#36a64f",
        "title": "Alert Analysis",
        "text": "Analysis content here",
        "footer": "Network Operations Workshop",
        "ts": timestamp
    }]
})
```

## Integration

Update `run_single_analysis()` to accept `send_slack: bool = False` parameter.
Update `main()` to handle `--slack` command line flag.

## Usage

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
python agent/alert_analyzer.py --test --slack
```
