# Extend BGP Configuration

Create `ansible/playbooks/02.5-bgp.yml` - eBGP peering for spine2 and leaf2-4.

Read the existing playbook at `ansible/playbooks/02-bgp.yml` to understand the patterns used for spine1 and leaf1.

## BGP Design

- Spines (spine1, spine2): AS 65100
- leaf1: AS 65101, leaf2: AS 65102, leaf3: AS 65103, leaf4: AS 65104

## Requirements

Create a complete Ansible playbook with two plays:

### Play 1: Configure BGP on spine2
- Use `arista.eos.eos_bgp_global` for AS 65100, Router ID 2.2.2.2
- Use `arista.eos.eos_config` to add neighbors:
  - 10.0.5.2 (leaf1, AS 65101)
  - 10.0.6.2 (leaf2, AS 65102)
  - 10.0.7.2 (leaf3, AS 65103)
  - 10.0.8.2 (leaf4, AS 65104)

### Play 2: Configure BGP on leaf2, leaf3, leaf4
- Each leaf peers with both spines (AS 65100)
- Router IDs: leaf2=22.22.22.22, leaf3=33.33.33.33, leaf4=44.44.44.44
- Neighbor IPs:
  - leaf2: 10.0.2.1 (spine1), 10.0.6.1 (spine2)
  - leaf3: 10.0.3.1 (spine1), 10.0.7.1 (spine2)
  - leaf4: 10.0.4.1 (spine1), 10.0.8.1 (spine2)

## Conventions
- Use `arista.eos` FQCN for all modules
- Use 2-space YAML indentation
- Use `when: inventory_hostname ==` conditions for device-specific tasks

Create the file directly.
