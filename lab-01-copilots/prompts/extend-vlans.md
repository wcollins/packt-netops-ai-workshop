# Extend VLAN Configuration

Use this prompt with Claude Code to create a new playbook that adds VLAN 30 and optional SVIs for inter-VLAN routing.

## How to Use

1. In your terminal, run `claude`
2. Copy and paste the prompt below
3. Claude Code will create the extension playbook directly
4. Review the generated file and validate before applying

---

## Prompt (Basic - VLAN 30)

```
Read the existing playbook at ansible/playbooks/03-vlans.yml to understand the
patterns and structure used for VLAN configuration on leaf switches.

Then create a new playbook at ansible/playbooks/03.5-vlans.yml that adds
VLAN 30 for Management on all leaf switches.

## Requirements

Create a complete, standalone Ansible playbook that:

1. Creates VLAN 30 with name "Management" on all leaf switches
2. Uses arista.eos.eos_vlans module with state: merged
3. Includes display tasks to show VLAN configuration

## Conventions
- Use arista.eos FQCN for all modules
- Use 2-space YAML indentation
- Use the same structure as 03-vlans.yml
- Include header comments explaining the playbook purpose

Create the file directly - do not output the YAML.
```

---

## Prompt (Bonus - SVIs)

```
Read the existing playbook at ansible/playbooks/03-vlans.yml to understand the
patterns and structure used for VLAN configuration.

Then create a new playbook at ansible/playbooks/03.5-vlans.yml that:
1. Creates VLAN 30 for Management
2. Configures SVIs (Switched Virtual Interfaces) for inter-VLAN routing

## SVI Requirements

Configure these SVIs on all leaf switches:
- Vlan10: 192.168.10.1/24 (Web Servers gateway)
- Vlan20: 192.168.20.1/24 (Database Servers gateway)
- Vlan30: 192.168.30.1/24 (Management gateway)

Note: Using the same IP on all leaves enables anycast gateway functionality.

## Requirements

Create a complete, standalone Ansible playbook with two plays:

### Play 1: Create VLAN 30
- Target: all leaf switches
- Use arista.eos.eos_vlans to create VLAN 30 (Management)
- Include display task for VLANs

### Play 2: Configure SVIs
- Target: all leaf switches
- Use arista.eos.eos_l3_interfaces to configure SVI IPs
- Note: eos_l3_interfaces only supports name, ipv4, ipv6 - use comments for documentation
- Include display task for IP interfaces

## Conventions
- Use arista.eos FQCN for all modules
- Use 2-space YAML indentation
- Include header comments explaining the playbook purpose

Create the file directly - do not output the YAML.
```

---

## Validation

After the file is created, run:

```bash
ansible-playbook playbooks/03.5-vlans.yml --check --diff
```

Verify that:
- VLAN 30 is created on all leaf switches
- SVIs are configured with correct IPs (if using bonus prompt)

To apply the configuration:
```bash
ansible-playbook playbooks/03.5-vlans.yml
```

To verify VLANs:
```bash
ansible leaves -m arista.eos.eos_command -a "commands='show vlan brief'"
```

To verify SVIs:
```bash
ansible leaves -m arista.eos.eos_command -a "commands='show ip interface brief'"
```

---

## Reference

### VLANs

| VLAN ID | Name | Purpose |
|---------|------|---------|
| 10 | Web_Servers | Web tier |
| 20 | Database_Servers | Database tier |
| 30 | Management | Management network |

### SVIs (Bonus)

| Interface | IP Address | Purpose |
|-----------|------------|---------|
| Vlan10 | 192.168.10.1/24 | Web gateway |
| Vlan20 | 192.168.20.1/24 | Database gateway |
| Vlan30 | 192.168.30.1/24 | Management gateway |
