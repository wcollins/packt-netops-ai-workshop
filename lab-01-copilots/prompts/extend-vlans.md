# Extend VLAN Configuration

Use this prompt with Claude Code to add VLAN 30 and optional SVIs for inter-VLAN routing.

## How to Use

1. In your terminal, run `claude`
2. Copy and paste the prompt below
3. Review the generated YAML before adding to your playbook

---

## Prompt (Basic - VLAN 30)

```
I have an Ansible playbook that creates VLANs on Arista EOS leaf switches.
Currently it creates VLAN 10 (Web_Servers) and VLAN 20 (Database_Servers).
I need to add VLAN 30 for Management.

## Working Example

vlans:
  - vlan_id: 10
    name: Web_Servers
  - vlan_id: 20
    name: Database_Servers

## Extension Request

Add VLAN 30 with name "Management" to the vlans list.
Follow the exact same format as the existing entries.

Output as YAML that I can paste directly into the playbook.
```

---

## Expected Output (Basic)

```yaml
vlans:
  - vlan_id: 10
    name: Web_Servers
  - vlan_id: 20
    name: Database_Servers
  - vlan_id: 30
    name: Management
```

---

## Prompt (Bonus - SVIs)

```
I have an Ansible playbook with VLANs 10, 20, and 30 configured on Arista EOS
leaf switches. I want to add SVIs (Switched Virtual Interfaces) for inter-VLAN
routing on each leaf switch.

## SVI Requirements

- Vlan10: 192.168.10.1/24 (same IP on all leaves for anycast gateway)
- Vlan20: 192.168.20.1/24
- Vlan30: 192.168.30.1/24

## Extension Request

Create a new Ansible play that:
1. Defines SVI interfaces as a variable
2. Configures SVIs on all leaf switches using arista.eos.eos_l3_interfaces
3. Displays the configured SVIs

Use the same structure as the interface playbook (01-interfaces.yml).
Output as YAML that I can add to the playbook.
```

---

## Expected Output (Bonus)

```yaml
# Add as a new play at the end of the playbook

- name: Configure SVIs on leaf switches
  hosts: leaves
  gather_facts: false

  vars:
    # Note: eos_l3_interfaces only supports name, ipv4, ipv6.
    # Use eos_interfaces module for descriptions if needed.
    svi_interfaces:
      - name: Vlan10  # Web Servers Gateway
        ipv4:
          - address: 192.168.10.1/24
      - name: Vlan20  # Database Servers Gateway
        ipv4:
          - address: 192.168.20.1/24
      - name: Vlan30  # Management Gateway
        ipv4:
          - address: 192.168.30.1/24

  tasks:
    - name: Configure SVI interfaces
      arista.eos.eos_l3_interfaces:
        config: "{{ svi_interfaces }}"
        state: merged

    - name: Display SVI configuration
      arista.eos.eos_command:
        commands:
          - show ip interface brief | include Vlan
      register: svi_output

    - name: Show SVI status
      ansible.builtin.debug:
        var: svi_output.stdout_lines
```

---

## Validation

After adding VLAN 30:

```bash
ansible-playbook playbooks/03-vlans.yml --check --diff
```

After adding SVIs (bonus):

```bash
ansible-playbook playbooks/03-vlans.yml --check --diff
```

To verify VLANs are working:
```bash
ansible leaves -m arista.eos.eos_command -a "commands='show vlan brief'"
```

To verify SVIs are working:
```bash
ansible leaves -m arista.eos.eos_command -a "commands='show ip interface brief'"
```
