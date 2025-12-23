# Docker Desktop Setup

Install and configure Docker Desktop for the workshop.

---

## System Requirements

- **RAM:** 8GB minimum (12GB+ recommended)
- **Disk:** 30GB available
- **OS:** macOS 11+, Windows 10/11, or Ubuntu 20.04+

---

## Installation

### macOS

**Option A: Docker Desktop**

1. Download Docker Desktop from https://www.docker.com/products/docker-desktop
2. Open the `.dmg` and drag Docker to Applications
3. Launch Docker from Applications
4. Grant permissions when prompted

**Option B: OrbStack (Recommended)**

OrbStack is a fast, lightweight Docker Desktop alternative for macOS.

1. Download from https://orbstack.dev/ or install via Homebrew:
   ```bash
   brew install orbstack
   ```
2. Launch OrbStack from Applications
3. OrbStack includes Docker — no additional configuration needed

> [!TIP]
> You can find more details on setting up OrbStack for MacOS [here.](https://containerlab.dev/macos/)

### Windows (WSL2 Required)

1. Enable WSL2 (PowerShell as Admin):
   ```powershell
   wsl --install
   ```
2. Restart computer
3. Download Docker Desktop from https://www.docker.com/products/docker-desktop
4. Run installer, ensure "Use WSL 2" is checked
5. Enable WSL integration: Settings → Resources → WSL Integration

### Linux (Ubuntu/Debian)

```bash

# Install Docker!
curl -fsSL https://get.docker.com | sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

---

## Configuration

### Docker Desktop

Open Docker Desktop → Settings → Resources:

- **Memory:** 8GB minimum (12GB recommended)
- **Disk image size:** 60GB
- Click "Apply & Restart"

### OrbStack

No configuration needed — OrbStack automatically manages resources.

---

## Install Containerlab

```bash
bash -c "$(curl -sL https://get.containerlab.dev)"
```

---

## Verify Installation

```bash
docker --version          # Should show version 24+
docker compose version    # Should show version 2.20+
containerlab version      # Should show version
docker run hello-world    # Should complete successfully
```

---

## Troubleshooting

**"Cannot connect to Docker daemon"**
- Ensure Docker Desktop is running (check system tray)
- Restart Docker Desktop

**"Permission denied" (Linux)**
```bash
sudo usermod -aG docker $USER
newgrp docker
```

**"Not enough memory"**
- Docker Desktop → Settings → Resources → Increase memory to 8GB+

---

## Next Step

Continue to [02-arista.md](02-arista.md)
