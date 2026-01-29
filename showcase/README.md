# Community Showcase

This workshop is just the beginning. This directory is a space for you to share your derivatives, custom MCP tools, or unique implementations built on top of what you learned.

---

## Why Share?

| Benefit | Description |
|---------|-------------|
| **Feedback** | Get eyes on your code from the instructor and peers |
| **Portfolio** | A public link demonstrating your Applied AI skills |
| **Community** | Help future learners by providing more examples |

---

## Submission Process

This project uses the **fork-and-pull** workflow. You'll create your own copy of the repository, make changes there, then submit those changes back via a Pull Request.

### Step 1: Fork the Repository

1. Go to the [repository on GitHub](https://github.com/wcollins/packt-netops-ai-workshop)
2. Click the **Fork** button (top right)
3. Select your GitHub account as the destination

You now have your own copy at `https://github.com/YOUR-USERNAME/packt-netops-ai-workshop`

### Step 2: Clone Your Fork

```bash
git clone https://github.com/YOUR-USERNAME/packt-netops-ai-workshop
cd packt-netops-ai-workshop
```

### Step 3: Create a Branch

```bash
git checkout -b showcase/your-name-project-name
```

Example: `git checkout -b showcase/jdoe-prometheus-alerting`

### Step 4: Add Your Project

```bash
cp -r showcase/_template showcase/your-name-project-name
```

Then edit `showcase/your-name-project-name/README.md` with your project details.

### Step 5: Commit and Push

```bash
git add showcase/your-name-project-name
git commit -m "docs: add showcase submission for project-name"
git push origin showcase/your-name-project-name
```

### Step 6: Create a Pull Request

1. Go to your fork on GitHub
2. Click **"Compare & pull request"** (appears after pushing)
3. Ensure the base repository is `wcollins/packt-netops-ai-workshop` and base branch is `main`
4. Add a brief description and click **"Create pull request"**

### Keeping Your Fork Updated (Optional)

If time passes before your PR is reviewed:

```bash
git remote add upstream https://github.com/wcollins/packt-netops-ai-workshop
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

## Submission Guidelines

- Keep your submission focused and well-documented
- Include the "Lessons Learned" section - it's the most valuable part
- Code should be functional (or clearly marked as work-in-progress)
- Be respectful and constructive in PR discussions

---

## Featured Projects

*Projects will be listed here as submissions are accepted.*

<!-- Example format:
| Project | Creator | Description |
|---------|---------|-------------|
| [prometheus-alerting](./jdoe-prometheus-alerting) | @jdoe | Extended Lab 3 with custom alert rules |
-->
