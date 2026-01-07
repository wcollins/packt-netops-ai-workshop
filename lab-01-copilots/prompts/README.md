# AI Prompts for Lab 1: Network Automation

This folder contains example prompts to help you extend the working Ansible playbooks using Claude Code.

## How to Use These Prompts

1. **Open the prompt file** for the task you're working on
2. **Copy the prompt** content (from the code block)
3. **Run Claude Code** in your terminal with `claude`
4. **Paste the prompt** - Claude Code will create the extension playbook directly
5. **Review the generated file** before applying
6. **Always validate** with `--check --diff` before applying

> **Note**: Claude Code creates extension files directly (e.g., `01.5-interfaces.yml`) rather than requiring you to copy-paste YAML. This streamlines the workflow.

## Available Prompts

| File | Purpose | Creates |
|------|---------|---------|
| `extend-interfaces.md` | Add L3 interfaces for spine2 and leaf2-4 | `01.5-interfaces.yml` |
| `extend-bgp.md` | Add BGP peering for spine2 and leaf2-4 | `02.5-bgp.yml` |
| `extend-vlans.md` | Add VLAN 30 and optional SVIs | `03.5-vlans.yml` |

## Playbook Execution Order

Run the playbooks in sequence - first the base playbooks, then the extensions:

```bash
# Base configuration (spine1, leaf1)
ansible-playbook playbooks/01-interfaces.yml
ansible-playbook playbooks/02-bgp.yml
ansible-playbook playbooks/03-vlans.yml

# Extension configuration (spine2, leaf2-4)
ansible-playbook playbooks/01.5-interfaces.yml
ansible-playbook playbooks/02.5-bgp.yml
ansible-playbook playbooks/03.5-vlans.yml
```

## Tips for Better Results

### Provide Context
The prompts reference existing playbooks for Claude Code to learn patterns from. Make sure you're in the `lab-01-copilots` directory when running Claude Code.

### Validate Before Applying
Always run playbooks with `--check --diff` first:
```bash
ansible-playbook playbooks/01.5-interfaces.yml --check --diff
```

### Iterate if Needed
If the generated file needs adjustments, ask Claude Code to modify it:
- "Change the IP on Ethernet2 to 10.0.6.2/30"
- "Add a description comment for each interface"
- "Use the same task structure as the original playbook"

## Device Reference

| Device | Management IP | BGP ASN | Router ID |
|--------|---------------|---------|-----------|
| spine1 | 198.18.1.11 | 65100 | 1.1.1.1 |
| spine2 | 198.18.1.12 | 65100 | 2.2.2.2 |
| leaf1 | 198.18.1.21 | 65101 | 11.11.11.11 |
| leaf2 | 198.18.1.22 | 65102 | 22.22.22.22 |
| leaf3 | 198.18.1.23 | 65103 | 33.33.33.33 |
| leaf4 | 198.18.1.24 | 65104 | 44.44.44.44 |

## IP Addressing Scheme

### Spine-to-Leaf Links

| Link | Subnet | Spine IP | Leaf IP |
|------|--------|----------|---------|
| spine1-leaf1 | 10.0.1.0/30 | 10.0.1.1 | 10.0.1.2 |
| spine1-leaf2 | 10.0.2.0/30 | 10.0.2.1 | 10.0.2.2 |
| spine1-leaf3 | 10.0.3.0/30 | 10.0.3.1 | 10.0.3.2 |
| spine1-leaf4 | 10.0.4.0/30 | 10.0.4.1 | 10.0.4.2 |
| spine2-leaf1 | 10.0.5.0/30 | 10.0.5.1 | 10.0.5.2 |
| spine2-leaf2 | 10.0.6.0/30 | 10.0.6.1 | 10.0.6.2 |
| spine2-leaf3 | 10.0.7.0/30 | 10.0.7.1 | 10.0.7.2 |
| spine2-leaf4 | 10.0.8.0/30 | 10.0.8.1 | 10.0.8.2 |
