# Setup Verification

Verify all components are correctly installed.

---

## Quick Verification

Run the verification script:

```bash
./scripts/verify-setup.sh
```

Or check each component manually below.

---

## Manual Verification Checklist

### 1. Docker

```bash
docker --version
# Expected: Docker version 24.x or higher

docker compose version
# Expected: Docker Compose version v2.20.x or higher

docker run hello-world
# Expected: "Hello from Docker!" message
```

### 2. Containerlab

```bash
containerlab version
# Expected: version 0.50.x or higher
```

### 3. Arista cEOS Image

```bash
docker images | grep ceos
# Expected: ceos    4.35.0.1F    ...
```

### 4. Python Environment

```bash
# Activate venv first
source .venv/bin/activate

python --version
# Expected: Python 3.10.x or higher

pip list | grep -E "ansible|netmiko|fastmcp"
# Expected: Shows ansible, netmiko, fastmcp packages
```

### 5. API Keys (Choose One)

```bash
# Anthropic (Recommended)
echo $ANTHROPIC_API_KEY | head -c 10
# Expected: Shows first 10 chars (sk-ant-...)

# OR OpenAI (Alternative)
echo $OPENAI_API_KEY | head -c 10
# Expected: Shows first 10 chars (sk-proj-...)

# OR Ollama (Free)
ollama list
# Expected: Shows downloaded models
```

### 6. Claude Code

```bash
claude --version
# Expected: Shows version number
```

### 7. Ansible Collections

```bash
ansible-galaxy collection list | grep arista
# Expected: arista.eos
```

---

## Full System Test

Test the complete lab environment:

```bash
cd lab-01-copilots

# Deploy test topology
containerlab deploy -t topology.clab.yml

# Wait for devices to boot
sleep 60

# Test SSH connectivity
ssh admin@198.18.1.11 -o StrictHostKeyChecking=no "show version"
# Password: admin
# Expected: Shows Arista EOS version

# Clean up
containerlab destroy -t topology.clab.yml
```

---

## Verification Summary

| Component | Command | Expected |
|-----------|---------|----------|
| Docker | `docker --version` | 24.x+ |
| Compose | `docker compose version` | 2.20+ |
| Containerlab | `containerlab version` | 0.50+ |
| cEOS | `docker images \| grep ceos` | ceos:4.35.0.1F |
| Python | `python --version` | 3.10+ |
| Ansible | `ansible --version` | 9.x |
| Claude Code | `claude --version` | any |
| API Key | `echo $ANTHROPIC_API_KEY` | sk-ant-... |

---

## Troubleshooting

**Docker issues**
- See [01-docker.md](01-docker.md) troubleshooting section

**cEOS not found**
- Re-import: `docker import cEOS-lab-4.35.0.1F.tar.xz ceos:4.35.0.1F`

**Python packages missing**
- Activate venv: `source .venv/bin/activate`
- Reinstall: `pip install -r requirements.txt`

**Claude Code not found**
- Restart terminal after installation
- See [05-claude-code.md](05-claude-code.md) troubleshooting section

**Containerlab deploy fails**
- Ensure Docker is running: `docker ps`

**SSH connection refused**
- Wait longer (devices need 60-90s to boot)
- Check container is running: `docker ps`

---

## Ready for Workshop!

If all checks pass, you're ready for the workshop.

**Workshop day:**
1. Arrive 10 minutes early
2. Have terminal ready
3. Have VS Code open with project folder
4. Join the video call

**Questions?**
- Email: wvanhorn33@gmail.com
- Pre-workshop office hours: 2 hours before start

---

## Next Steps

Explore the lab directories:
- [lab-01-copilots/](../lab-01-copilots/)
- [lab-02-mcp-server/](../lab-02-mcp-server/)
- [lab-03-observability/](../lab-03-observability/)
