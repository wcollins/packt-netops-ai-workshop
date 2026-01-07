# Extend BGP Configuration

Use this prompt with Claude Code to create a new playbook that configures eBGP peering for spine2 and leaf2-4.

## How to Use

1. In your terminal, run `claude`
2. Copy and paste the prompt below
3. Claude Code will create the extension playbook directly
4. Review the generated file and validate before applying

---

## Prompt

```
Read the existing playbook at ansible/playbooks/02-bgp.yml to understand the
patterns and structure used for spine1 and leaf1 BGP configuration.

Then create a new playbook at ansible/playbooks/02.5-bgp.yml that configures
eBGP peering for the remaining devices: spine2 and leaf2-4.

## BGP Design

- Spines (spine1, spine2): AS 65100
- leaf1: AS 65101
- leaf2: AS 65102
- leaf3: AS 65103
- leaf4: AS 65104

## Requirements

Create a complete, standalone Ansible playbook with two plays:

### Play 1: Configure BGP on spine2
- Use arista.eos.eos_bgp_global to configure:
  - AS number: 65100 (use bgp_asn variable from group_vars)
  - Router ID: 2.2.2.2
- Use arista.eos.eos_config to add neighbors:
  - 10.0.5.2 (leaf1, AS 65101)
  - 10.0.6.2 (leaf2, AS 65102)
  - 10.0.7.2 (leaf3, AS 65103)
  - 10.0.8.2 (leaf4, AS 65104)
- Include display tasks to show BGP summary

### Play 2: Configure BGP on leaf2, leaf3, leaf4
- Each leaf peers with both spines (AS 65100)
- Router IDs:
  - leaf2: 22.22.22.22
  - leaf3: 33.33.33.33
  - leaf4: 44.44.44.44
- Neighbor IPs:
  - leaf2: 10.0.2.1 (spine1), 10.0.6.1 (spine2)
  - leaf3: 10.0.3.1 (spine1), 10.0.7.1 (spine2)
  - leaf4: 10.0.4.1 (spine1), 10.0.8.1 (spine2)
- Include display tasks

## Conventions
- Use arista.eos FQCN for all modules
- Use 2-space YAML indentation
- Use 'when: inventory_hostname ==' conditions for device-specific tasks
- Use the same variable structure as 02-bgp.yml
- Include header comments explaining the playbook purpose

Create the file directly - do not output the YAML.
```

---

## Validation

After the file is created, run:

```bash
ansible-playbook playbooks/02.5-bgp.yml --check --diff
```

Verify that:
- BGP configuration is applied to spine2 and leaf2-4
- Router IDs are unique per device
- Neighbor relationships are correct (eBGP between different ASes)

To apply the configuration:
```bash
ansible-playbook playbooks/02.5-bgp.yml
```

To verify BGP is working:
```bash
ansible spine2 -m arista.eos.eos_command -a "commands='show ip bgp summary'"
```

---

## Device Reference

| Device | BGP ASN | Router ID |
|--------|---------|-----------|
| spine2 | 65100 | 2.2.2.2 |
| leaf2 | 65102 | 22.22.22.22 |
| leaf3 | 65103 | 33.33.33.33 |
| leaf4 | 65104 | 44.44.44.44 |

### BGP Neighbor IPs

| Device | Neighbor | Remote AS | Description |
|--------|----------|-----------|-------------|
| spine2 | 10.0.5.2 | 65101 | leaf1 |
| spine2 | 10.0.6.2 | 65102 | leaf2 |
| spine2 | 10.0.7.2 | 65103 | leaf3 |
| spine2 | 10.0.8.2 | 65104 | leaf4 |
| leaf2 | 10.0.2.1 | 65100 | spine1 |
| leaf2 | 10.0.6.1 | 65100 | spine2 |
| leaf3 | 10.0.3.1 | 65100 | spine1 |
| leaf3 | 10.0.7.1 | 65100 | spine2 |
| leaf4 | 10.0.4.1 | 65100 | spine1 |
| leaf4 | 10.0.8.1 | 65100 | spine2 |
