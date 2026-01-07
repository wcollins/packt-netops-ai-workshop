# Extend Interface Configuration

Use this prompt with Claude Code to create a new playbook that configures L3 interfaces for spine2 and leaf2-4.

## How to Use

1. In your terminal, run `claude`
2. Copy and paste the prompt below
3. Claude Code will create the extension playbook directly
4. Review the generated file and validate before applying

---

## Prompt

```
Read the existing playbook at ansible/playbooks/01-interfaces.yml to understand the
patterns and structure used for spine1 and leaf1 interface configuration.

Then create a new playbook at ansible/playbooks/01.5-interfaces.yml that configures
L3 interfaces for the remaining devices: spine2 and leaf2-4.

IMPORTANT: Arista EOS interfaces default to switchport (L2) mode. Before
assigning IPs, we must set interfaces to layer3 mode using eos_interfaces.

## Requirements

Create a complete, standalone Ansible playbook with two plays:

### Play 1: Configure spine2 interfaces
- Set Ethernet1-4 to layer3 mode using arista.eos.eos_interfaces
- Configure IP addresses using arista.eos.eos_l3_interfaces:
  - Ethernet1: 10.0.5.1/30 (link to leaf1)
  - Ethernet2: 10.0.6.1/30 (link to leaf2)
  - Ethernet3: 10.0.7.1/30 (link to leaf3)
  - Ethernet4: 10.0.8.1/30 (link to leaf4)
- Include display tasks to show configured interfaces

### Play 2: Configure leaf2, leaf3, leaf4 interfaces
- Set Ethernet1-2 to layer3 mode on each leaf
- Configure IP addresses:
  - leaf2: Eth1 -> 10.0.2.2/30 (spine1), Eth2 -> 10.0.6.2/30 (spine2)
  - leaf3: Eth1 -> 10.0.3.2/30 (spine1), Eth2 -> 10.0.7.2/30 (spine2)
  - leaf4: Eth1 -> 10.0.4.2/30 (spine1), Eth2 -> 10.0.8.2/30 (spine2)
- Include display tasks

## Conventions
- Use arista.eos FQCN for all modules
- Use 2-space YAML indentation
- Use 'when: inventory_hostname ==' conditions for device-specific tasks
- Use the same variable structure as 01-interfaces.yml
- Include header comments explaining the playbook purpose

Create the file directly - do not output the YAML.
```

---

## Validation

After the file is created, run:

```bash
ansible-playbook playbooks/01.5-interfaces.yml --check --diff
```

Verify that:
- spine2 and leaf2-4 show interface changes
- IP addresses match the expected scheme
- No syntax errors occur

To apply the configuration:
```bash
ansible-playbook playbooks/01.5-interfaces.yml
```

---

## Device Reference

| Link | Subnet | Spine IP | Leaf IP |
|------|--------|----------|---------|
| spine2-leaf1 | 10.0.5.0/30 | 10.0.5.1 | 10.0.5.2 |
| spine2-leaf2 | 10.0.6.0/30 | 10.0.6.1 | 10.0.6.2 |
| spine2-leaf3 | 10.0.7.0/30 | 10.0.7.1 | 10.0.7.2 |
| spine2-leaf4 | 10.0.8.0/30 | 10.0.8.1 | 10.0.8.2 |
