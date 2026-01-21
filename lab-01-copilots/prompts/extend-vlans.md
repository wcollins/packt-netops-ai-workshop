# Extend VLAN Configuration

Create `ansible/playbooks/03.5-vlans.yml` - VLAN 30 and optional SVIs.

Read the existing playbook at `ansible/playbooks/03-vlans.yml` to understand the patterns used.

## Basic Version - VLAN 30 Only

Create a playbook that:
1. Creates VLAN 30 with name "Management" on all leaf switches
2. Uses `arista.eos.eos_vlans` module with `state: merged`
3. Includes display tasks to show VLAN configuration

## Bonus Version - With SVIs

Create a playbook with two plays:

### Play 1: Create VLAN 30
- Target: all leaf switches
- Create VLAN 30 (Management)

### Play 2: Configure SVIs
- Target: all leaf switches
- Use `arista.eos.eos_l3_interfaces` to configure:
  - Vlan10: 192.168.10.1/24 (Web gateway)
  - Vlan20: 192.168.20.1/24 (Database gateway)
  - Vlan30: 192.168.30.1/24 (Management gateway)

Note: Using the same IP on all leaves enables anycast gateway functionality.

## Conventions
- Use `arista.eos` FQCN for all modules
- Use 2-space YAML indentation
- The `ipv4` parameter must be a list: `ipv4: [{address: "192.168.10.1/24"}]`

Create the file directly.
