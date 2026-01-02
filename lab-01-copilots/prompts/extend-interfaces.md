# Extend Interface Configuration

Use this prompt with Claude Code to add L3 interface configuration for spine2 and leaf2-4.

## How to Use

1. In your terminal, run `claude`
2. Copy and paste the prompt below
3. Review the generated YAML before adding to your playbook

---

## Prompt

```
I have an Ansible playbook that configures L3 interfaces on Arista EOS switches
in a spine-leaf topology. The playbook is complete for spine1 and leaf1.
I need to extend it to configure spine2 and leaf2-4.

IMPORTANT: Arista EOS interfaces default to switchport (L2) mode. Before
assigning IPs, we must set interfaces to layer3 mode using eos_interfaces.

## Working Example - Setting Layer3 Mode (spine1)

- name: Set spine1 interfaces to layer3 mode
  when: inventory_hostname == 'spine1'
  arista.eos.eos_interfaces:
    config:
      - name: Ethernet1
        mode: layer3
        enabled: true
      - name: Ethernet2
        mode: layer3
        enabled: true
      - name: Ethernet3
        mode: layer3
        enabled: true
      - name: Ethernet4
        mode: layer3
        enabled: true
    state: merged

## Working Example - IP Addresses (spine1)

spine1_interfaces:
  - name: Ethernet1  # Link to leaf1
    ipv4:
      - address: 10.0.1.1/30
  - name: Ethernet2  # Link to leaf2
    ipv4:
      - address: 10.0.2.1/30
  - name: Ethernet3  # Link to leaf3
    ipv4:
      - address: 10.0.3.1/30
  - name: Ethernet4  # Link to leaf4
    ipv4:
      - address: 10.0.4.1/30

## Working Example (leaf1)

leaf_interfaces:
  leaf1:
    - name: Ethernet1  # Link to spine1
      ipv4:
        - address: 10.0.1.2/30
    - name: Ethernet2  # Link to spine2
      ipv4:
        - address: 10.0.5.2/30

## Extension Request

Generate YAML for:

1. A task to set spine2 interfaces (Ethernet1-4) to layer3 mode
   - Use arista.eos.eos_interfaces module with mode: layer3
   - Use 'when: inventory_hostname == "spine2"'

2. spine2_interfaces variable - Ethernet1-4 connecting to leaf1-4
   - Use subnets 10.0.5.0/30 through 10.0.8.0/30
   - spine2 gets the .1 address in each subnet

3. A task to configure spine2 IP addresses
   - Use arista.eos.eos_l3_interfaces module
   - Use 'when: inventory_hostname == "spine2"'

4. Tasks to set leaf2, leaf3, leaf4 interfaces to layer3 mode
   - Each leaf has Ethernet1 and Ethernet2

5. leaf2, leaf3, leaf4 entries in leaf_interfaces
   - Each leaf has Ethernet1 to spine1, Ethernet2 to spine2
   - IP addressing:
     - leaf2: 10.0.2.2/30 (spine1), 10.0.6.2/30 (spine2)
     - leaf3: 10.0.3.2/30 (spine1), 10.0.7.2/30 (spine2)
     - leaf4: 10.0.4.2/30 (spine1), 10.0.8.2/30 (spine2)

Output as YAML that I can paste directly into the playbook.
```

---

## Expected Output

The AI should generate something like:

```yaml
# =========================================================================
# SPINE2 - Add to vars section for spines play
# =========================================================================
spine2_interfaces:
  - name: Ethernet1  # Link to leaf1
    ipv4:
      - address: 10.0.5.1/30
  - name: Ethernet2  # Link to leaf2
    ipv4:
      - address: 10.0.6.1/30
  - name: Ethernet3  # Link to leaf3
    ipv4:
      - address: 10.0.7.1/30
  - name: Ethernet4  # Link to leaf4
    ipv4:
      - address: 10.0.8.1/30

# =========================================================================
# SPINE2 - Add to tasks section for spines play
# =========================================================================
- name: Set spine2 interfaces to layer3 mode
  when: inventory_hostname == 'spine2'
  arista.eos.eos_interfaces:
    config:
      - name: Ethernet1
        mode: layer3
        enabled: true
      - name: Ethernet2
        mode: layer3
        enabled: true
      - name: Ethernet3
        mode: layer3
        enabled: true
      - name: Ethernet4
        mode: layer3
        enabled: true
    state: merged

- name: Configure IP addresses on spine2
  when: inventory_hostname == 'spine2'
  arista.eos.eos_l3_interfaces:
    config: "{{ spine2_interfaces }}"
    state: merged

# =========================================================================
# LEAVES - Add to tasks section for leaves play (before IP configuration)
# =========================================================================
- name: Set leaf2 interfaces to layer3 mode
  when: inventory_hostname == 'leaf2'
  arista.eos.eos_interfaces:
    config:
      - name: Ethernet1
        mode: layer3
        enabled: true
      - name: Ethernet2
        mode: layer3
        enabled: true
    state: merged

- name: Set leaf3 interfaces to layer3 mode
  when: inventory_hostname == 'leaf3'
  arista.eos.eos_interfaces:
    config:
      - name: Ethernet1
        mode: layer3
        enabled: true
      - name: Ethernet2
        mode: layer3
        enabled: true
    state: merged

- name: Set leaf4 interfaces to layer3 mode
  when: inventory_hostname == 'leaf4'
  arista.eos.eos_interfaces:
    config:
      - name: Ethernet1
        mode: layer3
        enabled: true
      - name: Ethernet2
        mode: layer3
        enabled: true
    state: merged

# =========================================================================
# LEAVES - Add to leaf_interfaces in vars section
# =========================================================================
leaf2:
  - name: Ethernet1  # Link to spine1
    ipv4:
      - address: 10.0.2.2/30
  - name: Ethernet2  # Link to spine2
    ipv4:
      - address: 10.0.6.2/30

leaf3:
  - name: Ethernet1  # Link to spine1
    ipv4:
      - address: 10.0.3.2/30
  - name: Ethernet2  # Link to spine2
    ipv4:
      - address: 10.0.7.2/30

leaf4:
  - name: Ethernet1  # Link to spine1
    ipv4:
      - address: 10.0.4.2/30
  - name: Ethernet2  # Link to spine2
    ipv4:
      - address: 10.0.8.2/30
```

---

## Validation

After adding the generated code, run:

```bash
ansible-playbook playbooks/01-interfaces.yml --check --diff
```

Verify that:
- All 6 devices show interface changes
- IP addresses match the expected scheme
- No syntax errors occur
