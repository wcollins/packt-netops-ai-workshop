# AI API Keys Setup

Configure API access for AI/LLM services. In this workshop, I'll be working with [Claude](https://platform.claude.com/) specifically, using Claude propietary features to enhance our Co-Pilot experience. Other models will work just fine, but to get the most out of this workshop, it is recommended to use Claude.

---

## Choose Your Option

| Option | Cost | Best For |
|--------|------|----------|
| **Anthropic Claude** | $5-10 | Recommended for workshop |
| **OpenAI** | $1-10 | Alternative |
| **Ollama** | Free | Local/offline |

You only need **one** option.

---

## Recommended Models

### For This Workshop

| Provider | Recommended Model | Est. Cost | Notes |
|----------|-------------------|-----------|-------|
| **Anthropic** | Claude 3.5 Sonnet | $5-10 | Recommended - native MCP & Claude Code |
| OpenAI | GPT-4o-mini | $1-3 | Good alternative |
| OpenAI | GPT-4o | $10-20 | Fallback if mini struggles |
| **Ollama** | llama3.1:8b | Free | Requires 8GB+ RAM |

### Why Claude?

Claude is the recommended model for this workshop because:
- **Native MCP support** - Lab 2 builds an MCP server that integrates seamlessly with Claude
- **Claude Code integration** - The workshop uses Claude Code as the primary AI coding assistant
- **Strong reasoning** - Excellent at network configurations, Ansible playbooks, and async Python patterns

**Alternative:** GPT-4o-mini is a solid choice if you prefer OpenAI. It handles the "extend working examples" pattern well at lower cost. Upgrade to GPT-4o if you encounter issues with complex configurations.

### Pricing Reference (as of Jan 2025)

| Model | Input | Output |
|-------|-------|--------|
| GPT-4o-mini | $0.15/1M tokens | $0.60/1M tokens |
| GPT-4o | $2.50/1M tokens | $10/1M tokens |
| Claude 3.5 Sonnet | $3/1M tokens | $15/1M tokens |

---

## Option 1: Anthropic Claude API (Recommended)

### Create Account & Get Key

1. Sign up at https://console.anthropic.com/
2. Add credits at https://console.anthropic.com/account/billing ($10 recommended)
3. Create API key at https://console.anthropic.com/account/keys
4. Copy key (starts with `sk-ant-`)

### Configure Environment

```bash
# macOS/Linux
echo 'export ANTHROPIC_API_KEY="sk-ant-your-key-here"' >> ~/.bashrc
source ~/.bashrc

# Windows PowerShell
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', 'sk-ant-your-key-here', 'User')
```

---

## Option 2: OpenAI API (Alternative)

### Create Account & Get Key

1. Sign up at https://platform.openai.com/signup
2. Add payment method at https://platform.openai.com/account/billing
3. Add $10 credit (workshop uses ~$5-10)
4. Create API key at https://platform.openai.com/api-keys
5. Copy key (starts with `sk-proj-`)

### Configure Environment

```bash
# macOS/Linux
echo 'export OPENAI_API_KEY="sk-proj-your-key-here"' >> ~/.bashrc
source ~/.bashrc

# Windows PowerShell
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', 'sk-proj-your-key-here', 'User')
```

### Test

```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" | head -20
```

---

## Option 3: Ollama (Free)

### Install

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows: Download from https://ollama.ai/download
```

### Pull Model

```bash
ollama serve &  # Start service
ollama pull llama3.2:3b  # Fast, 4GB RAM
# Or: ollama pull llama3.1:8b  # Better quality, 8GB RAM
```

### Test

```bash
ollama run llama3.2:3b "Hello!"
```

---

## Using .env Files (Recommended)

Create `.env` in project root:

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-proj-your-key-here  # if using OpenAI as alternative
```

Load in Python:
```python
from dotenv import load_dotenv
load_dotenv()
```

**Important:** `.env` is already in `.gitignore` - never commit API keys!

---

## Security Tips

- Set usage limits in API console
- Never commit keys to Git
- Rotate keys if exposed

---

## Next Step

Continue to [04-python.md](04-python.md)
