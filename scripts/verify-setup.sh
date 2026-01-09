#!/bin/bash
# =============================================================================
# Workshop Setup Verification Script
# =============================================================================
# Verifies all prerequisites for the "Build Intelligent Networks with AI" workshop.
# Run from the repository root: ./scripts/verify-setup.sh
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASS=0
FAIL=0
WARN=0

# =============================================================================
# Helper Functions
# =============================================================================

print_header() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

check_pass() {
    echo -e "  ${GREEN}✓${NC} $1"
    ((PASS++)) || true
}

check_fail() {
    echo -e "  ${RED}✗${NC} $1"
    ((FAIL++)) || true
}

check_warn() {
    echo -e "  ${YELLOW}!${NC} $1"
    ((WARN++)) || true
}

version_gte() {
    # Returns 0 if $1 >= $2 (version comparison)
    [ "$(printf '%s\n' "$2" "$1" | sort -V | head -n1)" = "$2" ]
}

# =============================================================================
# Check: Docker
# =============================================================================

check_docker() {
    print_header "Docker"

    # Docker installed
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version | grep -oE '[0-9]+\.[0-9]+' | head -1)
        if version_gte "$DOCKER_VERSION" "24.0"; then
            check_pass "Docker version $DOCKER_VERSION (required: 24.x+)"
        else
            check_fail "Docker version $DOCKER_VERSION (required: 24.x+)"
        fi
    else
        check_fail "Docker not installed"
        return
    fi

    # Docker daemon running
    if docker ps &> /dev/null; then
        check_pass "Docker daemon is running"
    else
        check_fail "Docker daemon is not running (start Docker Desktop or dockerd)"
        return
    fi

    # Docker Compose
    if docker compose version &> /dev/null; then
        COMPOSE_VERSION=$(docker compose version | grep -oE '[0-9]+\.[0-9]+' | head -1)
        if version_gte "$COMPOSE_VERSION" "2.20"; then
            check_pass "Docker Compose version $COMPOSE_VERSION (required: 2.20+)"
        else
            check_fail "Docker Compose version $COMPOSE_VERSION (required: 2.20+)"
        fi
    else
        check_fail "Docker Compose not installed"
    fi
}

# =============================================================================
# Check: Containerlab
# =============================================================================

check_containerlab() {
    print_header "Containerlab"

    if command -v containerlab &> /dev/null; then
        CLAB_VERSION=$(containerlab version | grep -oE 'version: [0-9]+\.[0-9]+' | grep -oE '[0-9]+\.[0-9]+')
        if [ -n "$CLAB_VERSION" ] && version_gte "$CLAB_VERSION" "0.50"; then
            check_pass "Containerlab version $CLAB_VERSION (required: 0.50+)"
        else
            # Try alternate version extraction
            CLAB_VERSION=$(containerlab version 2>&1 | head -1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
            if [ -n "$CLAB_VERSION" ] && version_gte "$CLAB_VERSION" "0.50"; then
                check_pass "Containerlab version $CLAB_VERSION (required: 0.50+)"
            else
                check_warn "Containerlab installed but version could not be verified"
            fi
        fi
    else
        check_fail "Containerlab not installed (see setup/01-docker.md)"
    fi
}

# =============================================================================
# Check: Arista cEOS Image
# =============================================================================

check_ceos() {
    print_header "Arista cEOS Image"

    if ! command -v docker &> /dev/null || ! docker ps &> /dev/null; then
        check_fail "Cannot check cEOS image - Docker not available"
        return
    fi

    if docker images | grep -q "ceos.*4.35.0.1F"; then
        check_pass "cEOS image found: ceos:4.35.0.1F"
    elif docker images | grep -q "ceos"; then
        CEOS_TAG=$(docker images | grep ceos | awk '{print $2}' | head -1)
        check_warn "cEOS image found with tag '$CEOS_TAG' (expected: 4.35.0.1F)"
    else
        check_fail "cEOS image not found (see setup/02-arista.md)"
    fi
}

# =============================================================================
# Check: Python Environment
# =============================================================================

check_python() {
    print_header "Python Environment"

    # Python version
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | grep -oE '[0-9]+\.[0-9]+')
        if version_gte "$PYTHON_VERSION" "3.10"; then
            check_pass "Python version $PYTHON_VERSION (required: 3.10+)"
        else
            check_fail "Python version $PYTHON_VERSION (required: 3.10+)"
        fi
    else
        check_fail "Python 3 not installed"
        return
    fi

    # uv package manager
    if command -v uv &> /dev/null; then
        UV_VERSION=$(uv --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
        check_pass "uv package manager installed (version $UV_VERSION)"
    else
        check_warn "uv package manager not installed (optional but recommended)"
    fi

    # Virtual environment
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    REPO_ROOT="$(dirname "$SCRIPT_DIR")"

    if [ -d "$REPO_ROOT/.venv" ]; then
        check_pass "Virtual environment exists at .venv/"
    else
        check_fail "Virtual environment not found (run: uv sync or python -m venv .venv)"
    fi
}

# =============================================================================
# Check: Python Packages
# =============================================================================

check_python_packages() {
    print_header "Python Packages"

    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    REPO_ROOT="$(dirname "$SCRIPT_DIR")"

    # Determine Python path
    if [ -f "$REPO_ROOT/.venv/bin/python" ]; then
        PYTHON="$REPO_ROOT/.venv/bin/python"
    elif command -v python3 &> /dev/null; then
        PYTHON="python3"
        check_warn "Using system Python (virtual environment recommended)"
    else
        check_fail "Python not available for package checks"
        return
    fi

    # Check required packages (format: "display_name:import_name" or just "name" if same)
    PACKAGES=("ansible" "netmiko" "fastmcp" "anthropic" "pyyaml:yaml" "pytest" "pydantic")

    for pkg_spec in "${PACKAGES[@]}"; do
        # Parse package spec - supports "display:import" or just "name"
        if [[ "$pkg_spec" == *":"* ]]; then
            display_name="${pkg_spec%%:*}"
            import_name="${pkg_spec##*:}"
        else
            display_name="$pkg_spec"
            import_name="$pkg_spec"
        fi

        if $PYTHON -c "import $import_name" 2>/dev/null; then
            check_pass "$display_name installed"
        else
            check_fail "$display_name not installed (run: uv sync or pip install -r requirements.txt)"
        fi
    done
}

# =============================================================================
# Check: Ansible Collections
# =============================================================================

check_ansible_collections() {
    print_header "Ansible Collections"

    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    REPO_ROOT="$(dirname "$SCRIPT_DIR")"

    # Determine ansible-galaxy path
    if [ -f "$REPO_ROOT/.venv/bin/ansible-galaxy" ]; then
        ANSIBLE_GALAXY="$REPO_ROOT/.venv/bin/ansible-galaxy"
    elif command -v ansible-galaxy &> /dev/null; then
        ANSIBLE_GALAXY="ansible-galaxy"
    else
        check_fail "ansible-galaxy not found"
        return
    fi

    # Check arista.eos collection
    if $ANSIBLE_GALAXY collection list 2>/dev/null | grep -q "arista.eos"; then
        EOS_VERSION=$($ANSIBLE_GALAXY collection list 2>/dev/null | grep "arista.eos" | awk '{print $2}')
        if version_gte "${EOS_VERSION:-0}" "12.0.0"; then
            check_pass "arista.eos collection $EOS_VERSION (required: 12.0.0+)"
        else
            check_warn "arista.eos collection $EOS_VERSION (recommended: 12.0.0+)"
        fi
    else
        check_fail "arista.eos collection not installed"
    fi

    # Check ansible.netcommon collection
    if $ANSIBLE_GALAXY collection list 2>/dev/null | grep -q "ansible.netcommon"; then
        NETCOMMON_VERSION=$($ANSIBLE_GALAXY collection list 2>/dev/null | grep "ansible.netcommon" | awk '{print $2}')
        check_pass "ansible.netcommon collection $NETCOMMON_VERSION"
    else
        check_fail "ansible.netcommon collection not installed"
    fi

    # Check ansible.utils collection
    if $ANSIBLE_GALAXY collection list 2>/dev/null | grep -q "ansible.utils"; then
        UTILS_VERSION=$($ANSIBLE_GALAXY collection list 2>/dev/null | grep "ansible.utils" | awk '{print $2}')
        check_pass "ansible.utils collection $UTILS_VERSION"
    else
        check_fail "ansible.utils collection not installed"
    fi
}

# =============================================================================
# Check: Claude Code CLI
# =============================================================================

check_claude_code() {
    print_header "Claude Code CLI"

    if command -v claude &> /dev/null; then
        CLAUDE_VERSION=$(claude --version 2>/dev/null | head -1)
        check_pass "Claude Code installed ($CLAUDE_VERSION)"
    else
        check_fail "Claude Code CLI not installed (npm install -g @anthropic-ai/claude-code)"
    fi
}

# =============================================================================
# Check: Git
# =============================================================================

check_git() {
    print_header "Git Configuration"

    if command -v git &> /dev/null; then
        GIT_VERSION=$(git --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
        check_pass "Git version $GIT_VERSION"
    else
        check_fail "Git not installed"
        return
    fi

    # User configuration
    GIT_USER=$(git config user.name 2>/dev/null)
    GIT_EMAIL=$(git config user.email 2>/dev/null)

    if [ -n "$GIT_USER" ] && [ -n "$GIT_EMAIL" ]; then
        check_pass "Git user configured: $GIT_USER <$GIT_EMAIL>"
    else
        check_warn "Git user not fully configured (git config --global user.name/user.email)"
    fi
}

# =============================================================================
# Summary
# =============================================================================

print_summary() {
    print_header "Verification Summary"

    echo ""
    echo -e "  ${GREEN}Passed:${NC}   $PASS"
    echo -e "  ${RED}Failed:${NC}   $FAIL"
    echo -e "  ${YELLOW}Warnings:${NC} $WARN"
    echo ""

    if [ $FAIL -eq 0 ]; then
        echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${GREEN}  All required checks passed! You're ready for the workshop.${NC}"
        echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        exit 0
    else
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${RED}  $FAIL check(s) failed. Please review the setup guides.${NC}"
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
        echo "  Setup guides are located in the setup/ directory:"
        echo "    - setup/01-docker.md"
        echo "    - setup/02-arista.md"
        echo "    - setup/03-api-keys.md"
        echo "    - setup/04-python.md"
        echo ""
        exit 1
    fi
}

# =============================================================================
# Main
# =============================================================================

echo ""
echo "========================================"
echo "  Workshop Setup Verification"
echo "  Build Intelligent Networks with AI"
echo "========================================"

check_docker
check_containerlab
check_ceos
check_python
check_python_packages
check_ansible_collections
check_claude_code
check_git
print_summary
