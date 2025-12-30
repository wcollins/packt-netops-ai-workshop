# ⏰ Getting Started

Setup instructions for the **Build Intelligent Networks with AI** workshop. All of these steps should be completed and validated prior to beginning the workshop.

**Time required:** 45-60 minutes

---

## 💻 System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| RAM | 8 GB | 12+ GB |
| Disk | 30 GB | 60 GB |
| OS | macOS 11+, Windows 10/11 (WSL2), Linux | - |

---

## 📋 Setup Checklist

Complete each step in order. Click the guide link for detailed instructions.

| Step | Component | Guide |
|------|-----------|-------|
| 1 | Docker + Containerlab | [setup/01-docker.md](setup/01-docker.md) |
| 2 | Arista cEOS Image | [setup/02-arista.md](setup/02-arista.md) |
| 3 | API Keys | [setup/03-api-keys.md](setup/03-api-keys.md) |
| 4 | Python Environment | [setup/04-python.md](setup/04-python.md) |
| 5 | Claude Code | [setup/06-claude-code.md](setup/06-claude-code.md) |
| 6 | Verification | [setup/05-verification.md](setup/05-verification.md) |

---

## ✅ Quick Verification

```bash
./scripts/verify-setup.sh
```

Or manually:

```bash
docker --version          # 24+
containerlab version      # any
uv --version              # any
claude --version          # any
docker images | grep ceos # ceos:4.35.0.1F
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Docker not starting | Ensure Docker Desktop or OrbStack is running |
| Containerlab fails | Restart Docker, wait 60s for devices |
| cEOS not found | Re-import: see [setup/02-arista.md](setup/02-arista.md) |
| API key errors | Check: `echo $ANTHROPIC_API_KEY` |
| Claude Code not found | Restart terminal after installation |

**Full guide:** [resources/troubleshooting.md](resources/troubleshooting.md)