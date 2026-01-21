# Extend Interface Configuration

Create `ansible/playbooks/01.5-interfaces.yml` - L3 interfaces for spine2 and leaf2-4.

Read the existing playbook at `ansible/playbooks/01-interfaces.yml` to understand the patterns used for spine1 and leaf1.

## Requirements

Create a complete Ansible playbook with two plays:

### Play 1: Configure spine2 interfaces
- Set Ethernet1-4 to layer3 mode using `arista.eos.eos_interfaces`
- Configure IP addresses using `arista.eos.eos_l3_interfaces`:
  - Ethernet1: 10.0.5.1/30 (link to leaf1)
  - Ethernet2: 10.0.6.1/30 (link to leaf2)
  - Ethernet3: 10.0.7.1/30 (link to leaf3)
  - Ethernet4: 10.0.8.1/30 (link to leaf4)

### Play 2: Configure leaf2, leaf3, leaf4 interfaces
- Set Ethernet1-2 to layer3 mode on each leaf
- Configure IP addresses:
  - leaf2: Eth1 -> 10.0.2.2/30 (spine1), Eth2 -> 10.0.6.2/30 (spine2)
  - leaf3: Eth1 -> 10.0.3.2/30 (spine1), Eth2 -> 10.0.7.2/30 (spine2)
  - leaf4: Eth1 -> 10.0.4.2/30 (spine1), Eth2 -> 10.0.8.2/30 (spine2)

## Conventions
- Use `arista.eos` FQCN for all modules
- Use 2-space YAML indentation
- Use `when: inventory_hostname ==` conditions for device-specific tasks
- The `ipv4` parameter must be a list: `ipv4: [{address: "10.0.5.1/30"}]`

Create the file directly.
