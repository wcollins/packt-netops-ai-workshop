# Lab 1: Build Playbooks with Claude Code

**Duration:** 75 minutes | **Difficulty:** Beginner

---

## Learning Objectives

By the end of this lab, you will:

- Deploy a spine-leaf network topology using Containerlab
- Configure network devices using working Ansible playbooks
- Use **Claude Code** to extend playbooks for additional devices
- Validate AI-generated configurations before deployment
- Create parameterized playbooks ready for MCP integration (Lab 2)

**Note:** The playbooks in this lab support `--extra-vars` for MCP integration.
In Lab 2, you'll create MCP tools that invoke these playbooks via natural language.

---

## Lab Architecture

```
         ┌─────────┐     ┌─────────┐
         │ Spine 1 │     │ Spine 2 │
         │ AS65100 │     │ AS65100 │
         └────┬────┘     └────┬────┘
              │               │
    ┌─────────┼───────────────┼─────────┐
    │         │               │         │
┌───┴───┐ ┌───┴───┐     ┌───┴───┐ ┌───┴───┐
│ Leaf1 │ │ Leaf2 │     │ Leaf3 │ │ Leaf4 │
│AS65101│ │AS65102│     │AS65103│ │AS65104│
└───────┘ └───────┘     └───────┘ └───────┘
```

### Device Information

| Device | Management IP | BGP ASN | Router ID |
|--------|---------------|---------|-----------|
| spine1 | 198.18.1.11 | 65100 | 1.1.1.1 |
| spine2 | 198.18.1.12 | 65100 | 2.2.2.2 |
| leaf1 | 198.18.1.21 | 65101 | 11.11.11.11 |
| leaf2 | 198.18.1.22 | 65102 | 22.22.22.22 |
| leaf3 | 198.18.1.23 | 65103 | 33.33.33.33 |
| leaf4 | 198.18.1.24 | 65104 | 44.44.44.44 |

**Credentials:** admin / admin

---

## Lab Overview

This lab has two phases:

| Phase | Duration | What You Do |
|-------|----------|-------------|
| **Phase 1** | 30 min | Deploy topology and run working playbooks (spine1 + leaf1) |
| **Phase 2** | 45 min | Use Claude Code to extend playbooks for remaining devices |

### What's Provided (Working Examples)

| Playbook | Working Example | Extension Task |
|----------|-----------------|----------------|
| `01-interfaces.yml` | spine1 + leaf1 interfaces | Add spine2, leaf2-4 |
| `02-bgp.yml` | spine1 + leaf1 BGP | Add spine2, leaf2-4 |
| `03-vlans.yml` | VLANs 10 and 20 | Add VLAN 30, SVIs |

### MCP-Ready Playbooks

These additional playbooks are designed for MCP integration in Lab 2:

| Playbook | Purpose | MCP Usage |
|----------|---------|-----------|
| `04-add-vlan.yml` | Add single VLAN | `--extra-vars "target_host=leaf1 vlan_id=30 vlan_name=Management"` |
| `05-show-config.yml` | Get running config | `--extra-vars "target_host=spine1"` |
| `06-backup-config.yml` | Backup to file | `--extra-vars "target_host=spine1"` |

---

# Phase 1: Deploy and Configure Working Infrastructure

**Duration:** 30 minutes

In this phase, you'll deploy the network topology and run the working playbooks to configure spine1 and leaf1. This establishes a baseline you'll extend in Phase 2.

---

## Task 1: Deploy Network Lab (10 min)

### Step 1.1: Deploy the topology

```bash
cd lab-01-copilots
containerlab deploy -t topology.clab.yml
```

### Step 1.2: Verify deployment

```bash
# Check containers are running
docker ps | grep clab-netops-workshop

# Inspect the lab
containerlab inspect -t topology.clab.yml
```

### Step 1.3: Test connectivity

```bash
# SSH to spine1
ssh admin@198.18.1.11
# Password: admin

# Once connected, verify EOS:
show version
exit
```

---

## Task 2: Configure Working Examples (20 min)

### Step 2.1: Install Ansible collections

```bash
cd ansible
ansible-galaxy collection install -r requirements.yml
```

### Step 2.2: Test Ansible connectivity

```bash
ansible all -m arista.eos.eos_facts
```

You should see facts from all 6 devices.

### Step 2.3: Configure interfaces (spine1 + leaf1)

```bash
ansible-playbook playbooks/01-interfaces.yml
```

### Step 2.4: Verify interfaces

```bash
ssh admin@198.18.1.11 "show ip interface brief"
```

**Expected output:**
```
Interface              IP Address         Status     Protocol
Ethernet1              10.0.1.1/30        up         up
Ethernet2              10.0.2.1/30        up         up
Ethernet3              10.0.3.1/30        up         up
Ethernet4              10.0.4.1/30        up         up
Management0            198.18.1.11/24     up         up
```

Note: spine1 has IPs configured, but only leaf1's side of the link is active (the other leaf switches aren't configured yet).

### Step 2.5: Configure BGP (spine1 + leaf1)

```bash
ansible-playbook playbooks/02-bgp.yml
```

### Step 2.6: Verify BGP

```bash
ssh admin@198.18.1.11 "show ip bgp summary"
```

**Expected output:**
```
BGP summary information for VRF default
Router identifier 1.1.1.1, local AS number 65100
  Description              Neighbor   AS      State   PfxRcd PfxAcc
  leaf1                    10.0.1.2   65101   Estab   0      0
  leaf2                    10.0.2.2   65102   Active
  leaf3                    10.0.3.2   65103   Active
  leaf4                    10.0.4.2   65104   Active
```

Note: Only leaf1 is `Estab` (established). The others show `Active` because leaf2-4 don't have their interfaces or BGP configured yet. After Phase 2, all 4 will show `Estab`.

### Step 2.7: Configure VLANs (all leaves)

```bash
ansible-playbook playbooks/03-vlans.yml
```

### Step 2.8: Verify VLANs

```bash
ssh admin@198.18.1.21 "show vlan"
```

**Expected output:**
```
VLAN  Name                             Status    Ports
----- -------------------------------- --------- ------
1     default                          active
10    Web_Servers                      active
20    Database_Servers                 active
```

You now have a partially configured fabric:
- **spine1 + leaf1**: Fully configured with interfaces, BGP, and VLANs
- **spine2 + leaf2-4**: VLANs only (no interfaces or BGP yet)

---

# Phase 2: Extend with AI Copilot

**Duration:** 45 minutes

In this phase, you'll use Claude Code to extend the working playbooks for the remaining devices.

---

## Using Claude Code

Run `claude` in your terminal and use the prompts from the `prompts/` folder:

```bash
# Start Claude Code
claude

# Or ask Claude Code directly to extend a playbook:
# "Read playbooks/01-interfaces.yml and extend it for spine2 and leaf2-4"
```

Ready-to-use prompts are in the `prompts/` folder:

- `prompts/extend-interfaces.md` - Add interfaces for spine2 and leaf2-4
- `prompts/extend-bgp.md` - Add BGP peering for spine2 and leaf2-4
- `prompts/extend-vlans.md` - Add VLAN 30 and optional SVIs

### Review AI Context (Optional - 2 min)

The `CLAUDE.md` file in this directory provides Claude Code with lab-specific conventions. Review it to understand:

- Arista EOS module syntax requirements (the `ipv4` list format is critical)
- Playbook patterns and variable naming used in this lab
- Device IP addressing and BGP ASN reference

This context helps Claude Code generate correct Ansible code on the first try.

---

## Task 3: Extend Interface Configuration (15 min)

### Step 3.1: Open the AI prompt

Open `prompts/extend-interfaces.md` and copy the prompt.

### Step 3.2: Use Claude Code

In your terminal, run `claude` and paste the prompt. Alternatively, you can ask Claude Code directly:

```
Read playbooks/01-interfaces.yml and extend it for spine2 and leaf2-4
```

Review the generated code before adding it to the playbook.

### Step 3.3: Add the generated code to the playbook

Edit `ansible/playbooks/01-interfaces.yml` and add:
1. `spine2_interfaces` variable
2. Task to configure spine2
3. `leaf2`, `leaf3`, `leaf4` entries in `leaf_interfaces`

### Step 3.4: Validate and apply

```bash
# Always validate first
ansible-playbook playbooks/01-interfaces.yml --check --diff

# Apply if validation looks good
ansible-playbook playbooks/01-interfaces.yml
```

### Step 3.5: Verify on devices

```bash
ssh admin@198.18.1.12 "show ip interface brief"  # spine2
```

**Expected output:**
```
Interface              IP Address         Status     Protocol
Ethernet1              10.0.5.1/30        up         up
Ethernet2              10.0.6.1/30        up         up
Ethernet3              10.0.7.1/30        up         up
Ethernet4              10.0.8.1/30        up         up
Management0            198.18.1.12/24     up         up
```

```bash
ssh admin@198.18.1.22 "show ip interface brief"  # leaf2
```

**Expected output:**
```
Interface              IP Address         Status     Protocol
Ethernet1              10.0.2.2/30        up         up
Ethernet2              10.0.6.2/30        up         up
Management0            198.18.1.22/24     up         up
```

---

## Task 4: Extend BGP Configuration (15 min)

### Step 4.1: Use the BGP prompt

Open `prompts/extend-bgp.md` and use Claude Code to generate the code.

### Step 4.2: Add the code to the playbook

Edit `ansible/playbooks/02-bgp.yml` and add:
1. `spine2_bgp_neighbors` variable
2. Tasks to configure spine2 BGP
3. `leaf2`, `leaf3`, `leaf4` entries in `leaf_bgp_config`

### Step 4.3: Apply

```bash
ansible-playbook playbooks/02-bgp.yml --check --diff
ansible-playbook playbooks/02-bgp.yml
```

### Step 4.4: Verify BGP peering

```bash
# Check BGP on spine1 - should now see 4 neighbors (one per leaf)
ssh admin@198.18.1.11 "show ip bgp summary"
```

**Expected output (after extension):**
```
BGP summary information for VRF default
Router identifier 1.1.1.1, local AS number 65100
  Description              Neighbor   AS      State   PfxRcd PfxAcc
  leaf1                    10.0.1.2   65101   Estab   0      0
  leaf2                    10.0.2.2   65102   Estab   0      0
  leaf3                    10.0.3.2   65103   Estab   0      0
  leaf4                    10.0.4.2   65104   Estab   0      0
```

Note: All 4 neighbors now show `Estab` - the full spine-leaf fabric is operational.

```bash
# Check BGP on leaf2 - should see 2 neighbors (both spines)
ssh admin@198.18.1.22 "show ip bgp summary"
```

**Expected output:**
```
BGP summary information for VRF default
Router identifier 22.22.22.22, local AS number 65102
  Description              Neighbor   AS      State   PfxRcd PfxAcc
  spine1                   10.0.2.1   65100   Estab   0      0
  spine2                   10.0.6.1   65100   Estab   0      0
```

---

## Task 5: Extend VLAN Configuration (10 min)

### Step 5.1: Use the VLAN prompt

Open `prompts/extend-vlans.md` and generate the code for VLAN 30.

### Step 5.2: Add VLAN 30 to the playbook

Edit `ansible/playbooks/03-vlans.yml` and add VLAN 30 (Management) to the vlans list.

### Step 5.3: Apply and verify

```bash
ansible-playbook playbooks/03-vlans.yml
ssh admin@198.18.1.21 "show vlan"
```

**Expected output:**
```
VLAN  Name                             Status    Ports
----- -------------------------------- --------- ------
1     default                          active
10    Web_Servers                      active
20    Database_Servers                 active
30    Management                       active
```

### (Bonus) Step 5.4: Add SVIs

If time permits, use the SVI section of the prompt to add inter-VLAN routing interfaces.

---

## Success Criteria

After completing both phases:

- [ ] All 6 devices running and accessible
- [ ] Interface IPs configured on **all** spine and leaf switches
- [ ] BGP neighbors established between **all** devices (8 sessions per spine, 2 per leaf)
- [ ] VLANs 10, 20, 30 created on leaf switches
- [ ] (Bonus) SVIs configured for inter-VLAN routing

---

## Validation Commands

Run on any switch:

```bash
show ip interface brief     # Check interface IPs
show ip bgp summary         # Check BGP neighbors
show vlan                   # Check VLANs (leaves only)
show lldp neighbors         # Check physical connectivity
```

---

## Troubleshooting

### Can't SSH to devices
```bash
# Check containers are running
docker ps | grep clab

# Wait 60-90 seconds after deploy for devices to boot
ping 198.18.1.11
```

### Ansible connection fails
```bash
# Test with verbose output
ansible spine1 -m ping -vvv

# Check inventory
ansible-inventory --list
```

### BGP not establishing
```bash
# Ensure interfaces are configured FIRST
# BGP needs the interface IPs to peer

# Check interface IPs
show ip interface brief

# Check BGP configuration
show running-config | section bgp

# Verify neighbor reachability
ping 10.0.1.2
```

### AI-generated code doesn't work
1. Compare with the working examples in the playbook
2. Check IP addresses match the scheme in `prompts/README.md`
3. Ensure YAML indentation is correct (2 spaces)
4. Ask your AI to "fix this error" with the error message

---

## Cleanup

When finished with the lab:

```bash
containerlab destroy -t topology.clab.yml
```

---

## Key Takeaways

1. **Start with working examples** - Run and verify before extending
2. **Claude Code accelerates development** - Generate similar configurations quickly
3. **Always validate first** - Use `--check --diff` before applying
4. **Review AI output** - AI can make mistakes, always verify
5. **Parameterized playbooks enable MCP** - Your playbooks are now ready for Lab 2

---

## Next Lab

Continue to [Lab 2: MCP Server with Ansible Integration](../lab-02-mcp-server/)

In Lab 2, you'll build MCP tools that invoke these playbooks, enabling commands like:
- "Add VLAN 30 to leaf1"
- "Show the running config for spine2"
- "Backup the configuration for leaf3"
