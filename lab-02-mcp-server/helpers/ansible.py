"""
Ansible helper function for running playbooks.
"""

import subprocess
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from .constants import ANSIBLE_DIR


def _get_ansible_playbook_path() -> str:
    """
    Get the path to ansible-playbook in the same environment as the running Python.

    When running as an MCP server spawned by an IDE, the PATH may not include
    the virtual environment. This function finds ansible-playbook relative to
    the Python interpreter.

    Returns:
        Path to ansible-playbook executable
    """
    # Get the bin/Scripts directory containing the Python interpreter
    python_bin_dir = Path(sys.executable).parent

    # Use shutil.which() with the venv bin dir prepended to PATH
    # This handles platform differences (Windows .exe, etc.)
    venv_path = f"{python_bin_dir}{os.pathsep}{os.environ.get('PATH', '')}"
    ansible_path = shutil.which("ansible-playbook", path=venv_path)

    if ansible_path:
        return ansible_path

    # Fall back to system PATH lookup
    return shutil.which("ansible-playbook") or "ansible-playbook"


def _extract_device_json(ansible_json_output: str) -> Tuple[Optional[Any], Optional[str]]:
    """
    Extract device command output from Ansible JSON callback format.

    The JSON callback outputs structured data. We look for the 'msg' field
    from debug tasks which contains the device's JSON response.

    Args:
        ansible_json_output: Raw stdout from ansible-playbook with JSON callback

    Returns:
        Tuple of (data, error):
            - On success: (parsed_data, None)
            - On failure: (None, descriptive_error_string)
    """
    # Ansible may output text before JSON (e.g., "Using ... config file")
    # Find the start of JSON data
    json_start = ansible_json_output.find('{')
    if json_start == -1:
        return None, "No JSON object found in Ansible output"

    json_text = ansible_json_output[json_start:]

    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as e:
        return None, f"JSON decode error at position {e.pos}: {e.msg}"

    # Navigate Ansible JSON callback structure:
    # plays[0].tasks[-1].hosts.<hostname>.msg contains our data
    plays = data.get("plays", [])
    if not plays:
        return None, "No plays found in Ansible output"

    tasks = plays[0].get("tasks", [])
    if not tasks:
        return None, "No tasks found in Ansible play"

    # Check for host unreachable/failed status in any task
    for task in tasks:
        hosts = task.get("hosts", {})
        for hostname, host_data in hosts.items():
            if host_data.get("unreachable"):
                msg = host_data.get("msg", "No route to host")
                return None, f"Host {hostname} unreachable: {msg}"
            if host_data.get("failed"):
                msg = host_data.get("msg", "Task failed")
                return None, f"Host {hostname} task failed: {msg}"

    # Find the debug task (usually last task with 'msg')
    for task in reversed(tasks):
        hosts = task.get("hosts", {})
        for hostname, host_data in hosts.items():
            if "msg" in host_data:
                msg = host_data["msg"]
                # msg might be string (needs parsing) or already dict
                if isinstance(msg, str):
                    try:
                        return json.loads(msg), None
                    except json.JSONDecodeError as e:
                        return None, f"Failed to parse device JSON: {e.msg}"
                return msg, None

    return None, "No debug task output found in Ansible response"


def run_ansible_playbook(
    playbook: str,
    extra_vars: Dict[str, Any],
    parse_json: bool = False
) -> Dict[str, Any]:
    """
    Run an Ansible playbook with extra variables.

    This function invokes ansible-playbook as a subprocess, passing extra
    variables via --extra-vars.

    Args:
        playbook: Playbook filename (e.g., '04-add-vlan.yml')
        extra_vars: Dictionary of extra variables to pass
        parse_json: If True, use JSON callback and parse device output

    Returns:
        Dictionary with:
            - success: bool indicating if playbook succeeded
            - return_code: Process exit code
            - stdout: Playbook output
            - stderr: Error output if any
            - data: Parsed JSON data (only if parse_json=True and successful)

    Example:
        result = run_ansible_playbook("04-add-vlan.yml", {
            "target_host": "leaf1",
            "vlan_id": 30,
            "vlan_name": "Management"
        })
    """
    extra_vars_str = " ".join(f"{k}={v}" for k, v in extra_vars.items())

    cmd = [
        _get_ansible_playbook_path(),
        f"playbooks/{playbook}",
        "--extra-vars", extra_vars_str,
        "-v"
    ]

    # Set up environment for JSON callback if parsing
    env = os.environ.copy()
    if parse_json:
        env["ANSIBLE_STDOUT_CALLBACK"] = "json"

    try:
        result = subprocess.run(
            cmd,
            cwd=ANSIBLE_DIR,
            capture_output=True,
            text=True,
            timeout=120,
            env=env
        )

        response = {
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

        # Parse JSON output if requested and successful
        if parse_json and result.returncode == 0:
            data, parse_error = _extract_device_json(result.stdout)
            if data is not None:
                response["data"] = data
            elif parse_error:
                response["parse_error"] = parse_error

        return response

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "return_code": -1,
            "error": "Playbook execution timed out after 120 seconds"
        }
    except FileNotFoundError:
        return {
            "success": False,
            "return_code": -1,
            "error": "ansible-playbook not found. Ensure Ansible is installed."
        }
    except Exception as e:
        return {
            "success": False,
            "return_code": -1,
            "error": str(e)
        }
