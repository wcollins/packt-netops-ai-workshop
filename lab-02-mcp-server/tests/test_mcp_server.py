#!/usr/bin/env python3
"""
Tests for Network MCP Server
Run with: python -m pytest tests/test_mcp_server.py -v
"""

import pytest
import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import tools and resources from the modular structure
from tools.get_device_info import get_device_info
from tools.get_interfaces import get_interfaces
from resources.topology import get_topology
from helpers import DEVICE_USERNAME, DEVICE_PASSWORD


class TestTopologyResource:
    """Tests for the topology resource (no network required)"""

    def test_topology_returns_json(self):
        """Topology should return valid JSON"""
        result = get_topology()
        data = json.loads(result)
        assert "devices" in data
        assert "lab_name" in data

    def test_topology_has_all_devices(self):
        """Topology should include all 6 devices"""
        result = get_topology()
        data = json.loads(result)
        assert len(data["devices"]) == 6

    def test_topology_device_structure(self):
        """Each device should have required fields"""
        result = get_topology()
        data = json.loads(result)
        for device in data["devices"]:
            assert "name" in device
            assert "ip" in device
            assert "role" in device


@pytest.mark.asyncio
class TestDeviceTools:
    """
    Tests for device tools (require Containerlab running)
    Skip these if network is not available
    """

    @pytest.fixture
    def device_ip(self):
        """Test device IP - spine1"""
        return "198.18.1.11"

    async def test_get_device_info_returns_dict(self, device_ip):
        """get_device_info should return a dictionary"""
        result = await get_device_info(device_ip)
        assert isinstance(result, dict)

    async def test_get_device_info_error_handling(self):
        """get_device_info should handle invalid hosts gracefully"""
        result = await get_device_info("invalid-host")
        assert isinstance(result, dict)
        # Should return error, not raise exception
        assert "error" in result or "status" in result

    async def test_get_interfaces_returns_dict(self, device_ip):
        """get_interfaces should return a dictionary"""
        result = await get_interfaces(device_ip)
        assert isinstance(result, dict)


class TestHelperFunctions:
    """Tests for helper functions"""

    def test_credentials_from_environment(self):
        """Credentials should be configurable via environment"""
        # Default values
        assert DEVICE_USERNAME == "admin"
        assert DEVICE_PASSWORD == "admin"


class TestAutoDiscovery:
    """Tests for the auto-discovery mechanism"""

    def test_tools_directory_exists(self):
        """tools/ directory should exist"""
        tools_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tools")
        assert os.path.isdir(tools_dir)

    def test_resources_directory_exists(self):
        """resources/ directory should exist"""
        resources_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources")
        assert os.path.isdir(resources_dir)

    def test_helpers_directory_exists(self):
        """helpers/ directory should exist"""
        helpers_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "helpers")
        assert os.path.isdir(helpers_dir)

    def test_template_file_exists(self):
        """_template.py should exist for students to copy"""
        template = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tools", "_template.py")
        assert os.path.isfile(template)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
