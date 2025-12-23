# Python Environment Setup

Set up Python and install workshop dependencies using **uv**.

---

## Requirements

- Python 3.10 or higher
- uv (recommended) or pip

---

## Step 1: Install uv

**uv** is a fast Python package manager. Install it first:

### macOS/Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Verify installation

```bash
uv --version
# Should show uv 0.4.x or higher
```

---

## Step 2: Check Python Version

```bash
python3 --version
# Should show Python 3.10.x or higher
```

If Python is not installed, let uv manage it (recommended for all platforms):

```bash
uv python install 3.12
```

---

## Step 3: Clone Repository

```bash
git clone https://github.com/yourusername/packt-netops-ai-workshop.git
cd packt-netops-ai-workshop
```

---

## Step 4: Install Dependencies with uv

```bash
# Create venv and install all dependencies in one command
uv sync

# Activate the virtual environment
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
```

That's it! uv handles:
- Creating the virtual environment
- Installing all dependencies from `pyproject.toml`
- Resolving compatible versions

---

## Step 5: Install Ansible Collections

```bash
# Install from requirements file (recommended)
ansible-galaxy collection install -r lab-01-copilots/ansible/requirements.yml

# Or install individually
ansible-galaxy collection install arista.eos ansible.netcommon ansible.utils
```

---

## Step 6: Verify Installation

```bash
# Check key packages
python -c "import ansible; print(f'Ansible: {ansible.__version__}')"
python -c "import netmiko; print('Netmiko: OK')"
python -c "import fastmcp; print('FastMCP: OK')"
python -c "import anthropic; print('Anthropic: OK')"
python -c "import openai; print('OpenAI: OK')"  # if using OpenAI
```

---

## Common uv Commands

```bash
# Install dependencies
uv sync

# Add a new package
uv add package-name

# Run a command in the venv
uv run python script.py

# Update all packages
uv sync --upgrade
```

---

## Troubleshooting

**"uv: command not found"**
- Restart your terminal after installing uv
- Or add to PATH: `export PATH="$HOME/.local/bin:$PATH"`

**"No Python found"**
```bash
# Let uv install Python
uv python install 3.12
```

**Package conflicts**
```bash
# Clear cache and reinstall
uv cache clean
uv sync --reinstall
```

**Permission errors**
- Never use `sudo` with uv or pip
- Always use a virtual environment

---

## VS Code Setup (Recommended)

1. Install VS Code: https://code.visualstudio.com/
2. Install extensions:
   - Python
   - Ansible
   - YAML
3. Open workshop folder: `code .`
4. Select Python interpreter: `.venv/bin/python`

---

## Next Step

Continue to [05-verification.md](05-verification.md)
