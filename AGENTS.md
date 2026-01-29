# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A three-part workshop teaching network engineers to leverage AI and LLMs for network automation. Built around Containerlab with Arista cEOS switches, Ansible automation, Model Context Protocol (MCP) servers, and Prometheus observability.

## Commands

### Environment Setup
```bash
uv sync                                      # Install dependencies
./scripts/verify-setup.sh                    # Verify prerequisites
```

### Lab 1 - Containerlab
```bash
cd lab-01-copilots
sudo containerlab deploy -t topology.clab.yml      # Deploy network
sudo containerlab destroy -t topology.clab.yml     # Teardown network
```

### Lab 1 - Ansible
```bash
cd lab-01-copilots/ansible
source .venv/bin/activate
ansible-playbook playbooks/01-interfaces.yml -i inventories/clab.yml
ansible-playbook playbooks/04-set-interfaces.yml -i inventories/clab.yml \
  --extra-vars "target_host=leaf1 interface_name=Ethernet3 description='New Link' ip_address=10.0.0.1/30"
```

### Lab 2 - MCP Server
```bash
cd lab-02-mcp-server
mcp dev network_mcp_server.py                # Test in MCP Inspector
mcp run network_mcp_server.py                # Run for Claude Desktop
mcp run -t sse network_mcp_server.py         # Run for remote access
```

### Lab 3 - Observability Stack
```bash
cd lab-03-observability
docker compose up -d                         # Start Prometheus + Grafana
docker compose down                          # Stop stack
```

### Testing & Quality
```bash
python -m pytest lab-02-mcp-server/tests/ -v  # Run tests
ruff check .                                   # Lint
mypy lab-02-mcp-server/                        # Type check
```

## Architecture

### Network Topology
- **Spines (2):** spine1, spine2 - AS65100, IPs 198.18.1.11-12
- **Leaves (4):** leaf1-4 - AS65101-65104, IPs 198.18.1.21-24
- BGP spine-leaf fabric with point-to-point links

### Lab Structure

**Lab 1 (`lab-01-copilots/`):** Ansible playbook development with Claude Code
- `ansible/playbooks/01-03.yml`: Base configs for spine1 + leaf1
- `ansible/playbooks/01.5-03.5.yml`: Extended configs for remaining devices
- `ansible/playbooks/04-09.yml`: Single-operation playbooks for MCP integration
- `prompts/`: Claude Code prompts for extending playbooks

**Lab 2 (`lab-02-mcp-server/`):** MCP server with auto-discovery
- `network_mcp_server.py`: Main server entry point
- `tools/`: Auto-discovered tool modules (get_device_info, get_interfaces, etc.)
- `resources/`: Auto-discovered resources (topology)
- `helpers/`: Shared utilities (ansible.py, constants.py)
- `prompts/`: Claude Code prompts for adding new tools

**Lab 3 (`lab-03-observability/`):** Prometheus monitoring integration
- `network_exporter.py`: Synthetic metrics generator
- `alerting_tools.py`: MCP-compatible alerting functions
- `agent/alert_analyzer.py`: LLM-powered alert analysis
- `prometheus/alert_rules.yml`: Alert rule definitions

### MCP Tool Auto-Discovery Pattern

Tools in `lab-02-mcp-server/tools/` are auto-discovered if they:
1. Are `.py` files (not `_` prefixed)
2. Export a `register(mcp)` function

```python
# tools/my_tool.py
async def my_tool(device: str) -> Dict[str, Any]:
    """Tool description with examples."""
    pass

def register(mcp):
    mcp.tool()(my_tool)
```

## Coding Patterns

### MCP Tools
- All tools are async functions with full type hints
- Include docstrings with usage examples
- Return errors as `{"error": "message", "context": "..."}`
- Use `helpers/ansible.py` for playbook execution

### Ansible Playbooks
- Parameterize with `--extra-vars` for MCP integration
- Required vars: `target_host`, plus operation-specific vars
- YAML callback format for machine-readable output

### Device Validation
Valid device names: `spine1`, `spine2`, `leaf1`, `leaf2`, `leaf3`, `leaf4`

## Configuration

### pyproject.toml Settings
- Python 3.10+
- Ruff: line-length=100, select=["E", "F", "I", "W"]
- pytest: asyncio_mode="auto"
