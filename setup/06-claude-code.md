# Claude Code Setup

Install and configure Claude Code, an AI coding assistant for your terminal.

---

## Installation

### Native installer (recommended)

**macOS/Linux:**

```bash
curl -fsSL https://claude.ai/install.sh | sh
```

**Windows (PowerShell):**

```powershell
irm https://claude.ai/install.ps1 | iex
```

### Alternative: npm

Requires Node.js 18+ (https://nodejs.org/)

```bash
npm install -g @anthropic-ai/claude-code
```

---

## API Key Configuration

1. Go to https://console.anthropic.com/
2. Sign in or create account
3. Navigate to **Settings → API Keys**
4. Click **Create Key**, copy the key

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, or `~/.profile`):

```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."
```

Reload: `source ~/.bashrc` (or restart terminal)

---

## VS Code Integration

1. Open VS Code
2. Open the integrated terminal (`` Ctrl+` ``)
3. Run `claude` to start Claude Code
4. Authenticate when prompted on first run
5. Use `Ctrl+Esc` (Windows/Linux) or `Cmd+Esc` (Mac) to toggle Claude Code

---

## Verify

```bash
claude --version
claude "hello"
```

---

## Troubleshooting

**"claude: command not found"**
- Restart your terminal after installation
- Or add to PATH: `export PATH="$HOME/.local/bin:$PATH"`

**Authentication fails**
- Check API key is set: `echo $ANTHROPIC_API_KEY`
- Verify key starts with `sk-ant-`

---

## Documentation

https://docs.anthropic.com/en/docs/claude-code

---

## Next Step

Continue to [05-verification.md](05-verification.md) (or return to [README.md](README.md))
