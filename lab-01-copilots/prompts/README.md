# AI Prompts for Lab 1: Network Automation

This folder contains example prompts to help you extend the working Ansible playbooks using Claude Code.

## How to Use These Prompts

1. **Open the prompt file** for the task you're working on
2. **Copy the prompt** content
3. **Use Claude Code** in one of these ways:
   - Run `claude` in your terminal and paste the prompt
   - In VS Code with Claude extension, use the chat panel
   - Use `/chat` command if available in your IDE
4. **Review the generated code** before using it
5. **Always validate** with `--check --diff` before applying

> **Tip**: Claude Code can read your existing playbook files directly. You can say:
> "Read playbooks/01-interfaces.yml and extend it for spine2 and leaf2-4"

## Available Prompts

| File | Purpose | Extends |
|------|---------|---------|
| `extend-interfaces.md` | Add L3 interfaces for spine2 and leaf2-4 | `01-interfaces.yml` |
| `extend-bgp.md` | Add BGP peering for spine2 and leaf2-4 | `02-bgp.yml` |
| `extend-vlans.md` | Add VLAN 30 and optional SVIs | `03-vlans.yml` |

## Tips for Better Results

### Provide Context
When using these prompts, share the existing playbook code with your AI. The more context you provide, the better the output.

### Be Specific About Format
The prompts ask for YAML output matching existing patterns. If the output doesn't match, ask the AI to adjust.

### Validate Before Applying
Always run playbooks with `--check --diff` first:
```bash
ansible-playbook playbooks/01-interfaces.yml --check --diff
```

### Iterate if Needed
If the first response isn't quite right, refine your prompt:
- "Use the exact same format as the spine1 example"
- "The IP should be 10.0.6.2/30, not 10.0.6.1/30"
- "Add the description field like in the working example"

## Device Reference

| Device | Management IP | BGP ASN | Router ID |
|--------|---------------|---------|-----------|
| spine1 | 198.18.1.11 | 65100 | 1.1.1.1 |
| spine2 | 198.18.1.12 | 65100 | 2.2.2.2 |
| leaf1 | 198.18.1.21 | 65101 | 11.11.11.11 |
| leaf2 | 198.18.1.22 | 65102 | 22.22.22.22 |
| leaf3 | 198.18.1.23 | 65103 | 33.33.33.33 |
| leaf4 | 198.18.1.24 | 65104 | 44.44.44.44 |

## IP Addressing Scheme

### Spine-to-Leaf Links

| Link | Subnet | Spine IP | Leaf IP |
|------|--------|----------|---------|
| spine1-leaf1 | 10.0.1.0/30 | 10.0.1.1 | 10.0.1.2 |
| spine1-leaf2 | 10.0.2.0/30 | 10.0.2.1 | 10.0.2.2 |
| spine1-leaf3 | 10.0.3.0/30 | 10.0.3.1 | 10.0.3.2 |
| spine1-leaf4 | 10.0.4.0/30 | 10.0.4.1 | 10.0.4.2 |
| spine2-leaf1 | 10.0.5.0/30 | 10.0.5.1 | 10.0.5.2 |
| spine2-leaf2 | 10.0.6.0/30 | 10.0.6.1 | 10.0.6.2 |
| spine2-leaf3 | 10.0.7.0/30 | 10.0.7.1 | 10.0.7.2 |
| spine2-leaf4 | 10.0.8.0/30 | 10.0.8.1 | 10.0.8.2 |
