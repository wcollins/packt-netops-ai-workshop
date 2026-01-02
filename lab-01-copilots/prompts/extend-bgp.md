# Extend BGP Configuration

Use this prompt with Claude Code to add BGP peering configuration for spine2 and leaf2-4.

## How to Use

1. In your terminal, run `claude`
2. Copy and paste the prompt below
3. Review the generated YAML before adding to your playbook

---

## Prompt

```
I have an Ansible playbook that configures eBGP peering on Arista EOS switches
in a spine-leaf topology. The playbook is complete for spine1 and leaf1.
I need to extend it to configure spine2 and leaf2-4.

## BGP Design

- Spines (spine1, spine2): AS 65100
- leaf1: AS 65101
- leaf2: AS 65102
- leaf3: AS 65103
- leaf4: AS 65104

## Working Example (spine1 neighbors)

spine1_bgp_neighbors:
  - neighbor: 10.0.1.2
    remote_as: 65101
    description: "leaf1"
  - neighbor: 10.0.2.2
    remote_as: 65102
    description: "leaf2"
  - neighbor: 10.0.3.2
    remote_as: 65103
    description: "leaf3"
  - neighbor: 10.0.4.2
    remote_as: 65104
    description: "leaf4"

## Working Example (leaf1 config)

leaf_bgp_config:
  leaf1:
    router_id: 11.11.11.11
    neighbors:
      - neighbor: 10.0.1.1
        remote_as: 65100
        description: "spine1"
      - neighbor: 10.0.5.1
        remote_as: 65100
        description: "spine2"

## Extension Request

Generate YAML for:

1. spine2_bgp_neighbors - 4 neighbors (leaf1-4)
   - Use IPs 10.0.5.2, 10.0.6.2, 10.0.7.2, 10.0.8.2
   - Same AS numbers as spine1's neighbors

2. Ansible tasks to configure BGP on spine2
   - router_id: 2.2.2.2
   - Use arista.eos.eos_bgp_global for BGP config
   - Use arista.eos.eos_config for neighbors

3. leaf2, leaf3, leaf4 entries in leaf_bgp_config
   - router_ids: 22.22.22.22, 33.33.33.33, 44.44.44.44
   - Each leaf peers with both spines (AS 65100)
   - Neighbor IPs:
     - leaf2: 10.0.2.1 (spine1), 10.0.6.1 (spine2)
     - leaf3: 10.0.3.1 (spine1), 10.0.7.1 (spine2)
     - leaf4: 10.0.4.1 (spine1), 10.0.8.1 (spine2)

Output as YAML that I can paste directly into the playbook.
```

---

## Expected Output

The AI should generate something like:

```yaml
# Add to vars section for spines play
spine2_bgp_neighbors:
  - neighbor: 10.0.5.2
    remote_as: 65101
    description: "leaf1"
  - neighbor: 10.0.6.2
    remote_as: 65102
    description: "leaf2"
  - neighbor: 10.0.7.2
    remote_as: 65103
    description: "leaf3"
  - neighbor: 10.0.8.2
    remote_as: 65104
    description: "leaf4"

# Add to tasks section for spines play
- name: Configure BGP on spine2
  when: inventory_hostname == 'spine2'
  arista.eos.eos_bgp_global:
    config:
      as_number: "{{ bgp_asn }}"
      router_id: 2.2.2.2
    state: merged

- name: Configure BGP neighbors on spine2
  when: inventory_hostname == 'spine2'
  arista.eos.eos_config:
    lines:
      - "neighbor {{ item.neighbor }} remote-as {{ item.remote_as }}"
      - "neighbor {{ item.neighbor }} description {{ item.description }}"
    parents:
      - router bgp {{ bgp_asn }}
  loop: "{{ spine2_bgp_neighbors }}"

# Add to leaf_bgp_config in leaves play
leaf2:
  router_id: 22.22.22.22
  neighbors:
    - neighbor: 10.0.2.1
      remote_as: 65100
      description: "spine1"
    - neighbor: 10.0.6.1
      remote_as: 65100
      description: "spine2"

leaf3:
  router_id: 33.33.33.33
  neighbors:
    - neighbor: 10.0.3.1
      remote_as: 65100
      description: "spine1"
    - neighbor: 10.0.7.1
      remote_as: 65100
      description: "spine2"

leaf4:
  router_id: 44.44.44.44
  neighbors:
    - neighbor: 10.0.4.1
      remote_as: 65100
      description: "spine1"
    - neighbor: 10.0.8.1
      remote_as: 65100
      description: "spine2"
```

---

## Validation

After adding the generated code, run:

```bash
ansible-playbook playbooks/02-bgp.yml --check --diff
```

Verify that:
- BGP configuration is applied to all 6 devices
- Router IDs are unique per device
- Neighbor relationships are correct (eBGP between different ASes)

To verify BGP is working after applying:
```bash
ansible spine1 -m arista.eos.eos_command -a "commands='show ip bgp summary'"
```
