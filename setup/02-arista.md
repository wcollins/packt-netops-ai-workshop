# Arista cEOS Image Setup

Download and import the Arista cEOS-lab container image.

---

## What is cEOS-lab?

A containerized version of Arista EOS for labs and testing:
- Full EOS feature set
- Same CLI as physical switches
- Free for testing
- Low resource requirements (~2GB per container)

---

## Step 1: Create Arista Account

1. Visit https://www.arista.com/en/support/software-download
2. Click "Create Account" or "Register"
3. Fill in registration (use "Individual" for company if needed)
4. Verify your email

**Note:** Account approval is usually instant but can take up to 24 hours.

---

## Step 2: Download cEOS Image

1. Log in at https://www.arista.com/en/login
2. Go to Support → Software Downloads
3. Find and click "cEOS-lab"
4. Select version **4.35.0.1F** (What I'll be using for the lab)
5. Download `cEOS-lab-4.35.0.1F.tar.xz` (~500MB - Be sure to select the ARM image if using Apple silicon)

---

## Step 3: Import into Docker

```bash
cd ~/Downloads  # or wherever you saved the file
docker import cEOS-lab-4.35.0.1F.tar.xz ceos:4.35.0.1F
```

This takes 2-5 minutes.

---

## Step 4: Verify Import

```bash
docker images | grep ceos
```

Expected output:
```
ceos    4.35.0.1F    abc123def456    2 minutes ago    1.8GB
```

---

## Resource Usage

| Resource | Per Container |
|----------|--------------|
| Disk | ~1.8GB |
| Memory | 1-2GB |
| Workshop total (6 containers) | ~12GB RAM |

---

## Next Step

Continue to [03-api-keys.md](03-api-keys.md)
