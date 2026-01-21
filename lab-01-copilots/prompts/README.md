# AI Prompts for Lab 1: Network Automation

Copy the contents of these files and paste into Claude Code to create extension playbooks.

## Available Prompts

| File | Creates |
|------|---------|
| `extend-interfaces.md` | `playbooks/01.5-interfaces.yml` - L3 interfaces for spine2, leaf2-4 |
| `extend-bgp.md` | `playbooks/02.5-bgp.yml` - BGP peering for spine2, leaf2-4 |
| `extend-vlans.md` | `playbooks/03.5-vlans.yml` - VLAN 30 and optional SVIs |

## Usage

1. Open a prompt file (e.g., `extend-interfaces.md`)
2. Copy the entire contents
3. Paste into Claude Code
4. Review the generated playbook
5. Validate before applying: `ansible-playbook playbooks/01.5-interfaces.yml --check --diff`

## Playbook Order

```bash
# Base configuration (already done)
ansible-playbook playbooks/01-interfaces.yml
ansible-playbook playbooks/02-bgp.yml
ansible-playbook playbooks/03-vlans.yml

# Extension configuration (your task)
ansible-playbook playbooks/01.5-interfaces.yml
ansible-playbook playbooks/02.5-bgp.yml
ansible-playbook playbooks/03.5-vlans.yml
```
