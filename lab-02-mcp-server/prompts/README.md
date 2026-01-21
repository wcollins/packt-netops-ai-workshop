# AI Prompts for Lab 2: MCP Server

Copy the contents of these files and paste into Claude Code to create new MCP tools.

## Available Prompts

| File | Creates |
|------|---------|
| `add-vlan-tool.md` | `tools/add_vlan.py` - Add VLANs to leaf switches (Required) |
| `add-config-backup.md` | `tools/backup_config.py` - Backup device configuration (Required) |
| `add-get-config-tool.md` | `tools/get_running_config.py` - Get running config (Optional) |

## Usage

1. Open a prompt file (e.g., `add-vlan-tool.md`)
2. Copy the entire contents
3. Paste into Claude Code
4. Review the generated file in `tools/`
5. Restart MCP server - new tool is auto-discovered

## Testing

```bash
# Test in MCP Inspector
mcp dev network_mcp_server.py

# Run tests
python -m pytest tests/ -v
```
