# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Lab Overview

Lab 1 teaches building Ansible playbooks with Claude Code assistance. The lab uses Containerlab with Arista cEOS switches in a spine-leaf topology.

## Commands

### Containerlab
```bash
sudo containerlab deploy -t topology.clab.yml      # Deploy network
sudo containerlab destroy -t topology.clab.yml     # Teardown
containerlab inspect -t topology.clab.yml          # Show status
```

### Ansible
```bash
cd ansible
ansible-galaxy collection install -r requirements.yml  # Install collections
ansible all -m arista.eos.eos_facts                    # Test connectivity

# Run playbooks
ansible-playbook playbooks/01-interfaces.yml
ansible-playbook playbooks/01-interfaces.yml --check --diff  # Dry-run

# MCP-ready playbooks (single device operations)
ansible-playbook playbooks/04-add-vlan.yml \
  --extra-vars "target_host=leaf1 vlan_id=30 vlan_name=Management"
```

## Network Topology

```
         spine1 (AS65100)     spine2 (AS65100)
         198.18.1.11          198.18.1.12
              │                    │
    ┌─────────┼────────────────────┼─────────┐
    │         │                    │         │
  leaf1     leaf2              leaf3     leaf4
  AS65101   AS65102            AS65103   AS65104
  .21       .22                .23       .24
```

**Credentials:** admin / admin

## IP Addressing Scheme

Point-to-point /30 subnets:
- spine1-leaf[1-4]: 10.0.[1-4].0/30 (spine .1, leaf .2)
- spine2-leaf[1-4]: 10.0.[5-8].0/30 (spine .1, leaf .2)

## Playbook Structure

| Playbook | Purpose | MCP-Ready |
|----------|---------|-----------|
| `01-interfaces.yml` | L3 interface IPs (spine1, leaf1) | Yes |
| `02-bgp.yml` | BGP peering (spine1, leaf1) | Yes |
| `03-vlans.yml` | VLANs 10, 20 on leaves | No |
| `04-09.yml` | Single operations for MCP | Yes |

Extension playbooks (`01.5-`, `02.5-`, `03.5-`) are created by following prompts in `prompts/`.

## Arista EOS Ansible Conventions

**Critical:** The `eos_l3_interfaces` module requires `ipv4` as a list:
```yaml
# Correct
- name: Ethernet1
  ipv4:
    - address: 10.0.1.1/30

# Incorrect - will fail
- name: Ethernet1
  ipv4: 10.0.1.1/30
```

Set interfaces to layer3 mode before assigning IPs:
```yaml
- name: Set to layer3
  arista.eos.eos_interfaces:
    config:
      - name: Ethernet1
        mode: layer3
        enabled: true
    state: merged
```

Use `when: inventory_hostname ==` for device-specific tasks.

## MCP Integration Pattern

Playbooks 04-09 accept `--extra-vars "target_host=<device>"` for single-device operations. This enables MCP tools in Lab 2 to invoke playbooks via natural language.

Valid devices: `spine1`, `spine2`, `leaf1`, `leaf2`, `leaf3`, `leaf4`
