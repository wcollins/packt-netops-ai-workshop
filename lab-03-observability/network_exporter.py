#!/usr/bin/env python3
"""
Synthetic Network Metrics Exporter

Generates realistic network device metrics (BGP, interfaces, device health)
for the lab-03-observability monitoring stack. Exposes Prometheus metrics
on port 8888.

Simulates a spine-leaf topology with 6 devices:
- spine1, spine2 (BGP ASN 65100)
- leaf1-4 (BGP ASN 65101-65104)
"""

import random
import time
import threading
from prometheus_client import start_http_server, Gauge, Counter, Info

# =============================================================================
# Device Topology (from CLAUDE.md)
# =============================================================================

DEVICES = {
    "spine1": {"asn": 65100, "router_id": "1.1.1.1", "mgmt_ip": "198.18.1.11"},
    "spine2": {"asn": 65100, "router_id": "2.2.2.2", "mgmt_ip": "198.18.1.12"},
    "leaf1": {"asn": 65101, "router_id": "11.11.11.11", "mgmt_ip": "198.18.1.21"},
    "leaf2": {"asn": 65102, "router_id": "22.22.22.22", "mgmt_ip": "198.18.1.22"},
    "leaf3": {"asn": 65103, "router_id": "33.33.33.33", "mgmt_ip": "198.18.1.23"},
    "leaf4": {"asn": 65104, "router_id": "44.44.44.44", "mgmt_ip": "198.18.1.24"},
}

# BGP peering relationships (device -> list of peers with their info)
BGP_PEERS = {
    "spine1": [
        {"peer": "leaf1", "peer_ip": "10.0.1.2", "local_ip": "10.0.1.1"},
        {"peer": "leaf2", "peer_ip": "10.0.2.2", "local_ip": "10.0.2.1"},
        {"peer": "leaf3", "peer_ip": "10.0.3.2", "local_ip": "10.0.3.1"},
        {"peer": "leaf4", "peer_ip": "10.0.4.2", "local_ip": "10.0.4.1"},
    ],
    "spine2": [
        {"peer": "leaf1", "peer_ip": "10.0.5.2", "local_ip": "10.0.5.1"},
        {"peer": "leaf2", "peer_ip": "10.0.6.2", "local_ip": "10.0.6.1"},
        {"peer": "leaf3", "peer_ip": "10.0.7.2", "local_ip": "10.0.7.1"},
        {"peer": "leaf4", "peer_ip": "10.0.8.2", "local_ip": "10.0.8.1"},
    ],
    "leaf1": [
        {"peer": "spine1", "peer_ip": "10.0.1.1", "local_ip": "10.0.1.2"},
        {"peer": "spine2", "peer_ip": "10.0.5.1", "local_ip": "10.0.5.2"},
    ],
    "leaf2": [
        {"peer": "spine1", "peer_ip": "10.0.2.1", "local_ip": "10.0.2.2"},
        {"peer": "spine2", "peer_ip": "10.0.6.1", "local_ip": "10.0.6.2"},
    ],
    "leaf3": [
        {"peer": "spine1", "peer_ip": "10.0.3.1", "local_ip": "10.0.3.2"},
        {"peer": "spine2", "peer_ip": "10.0.7.1", "local_ip": "10.0.7.2"},
    ],
    "leaf4": [
        {"peer": "spine1", "peer_ip": "10.0.4.1", "local_ip": "10.0.4.2"},
        {"peer": "spine2", "peer_ip": "10.0.8.1", "local_ip": "10.0.8.2"},
    ],
}

# Interface mappings (device -> list of interfaces)
INTERFACES = {
    "spine1": ["Ethernet1", "Ethernet2", "Ethernet3", "Ethernet4"],
    "spine2": ["Ethernet1", "Ethernet2", "Ethernet3", "Ethernet4"],
    "leaf1": ["Ethernet1", "Ethernet2"],
    "leaf2": ["Ethernet1", "Ethernet2"],
    "leaf3": ["Ethernet1", "Ethernet2"],
    "leaf4": ["Ethernet1", "Ethernet2"],
}

# =============================================================================
# Prometheus Metrics
# =============================================================================

# BGP metrics
bgp_session_state = Gauge(
    "bgp_session_state",
    "BGP session state (1=established, 0=down)",
    ["device", "peer", "asn"],
)
bgp_prefixes_received = Gauge(
    "bgp_prefixes_received",
    "Number of prefixes received from BGP peer",
    ["device", "peer"],
)

# Interface metrics
interface_up = Gauge(
    "interface_up",
    "Interface operational state (1=up, 0=down)",
    ["device", "interface"],
)
interface_errors_total = Counter(
    "interface_errors_total",
    "Total interface errors",
    ["device", "interface"],
)
interface_traffic_bytes = Counter(
    "interface_traffic_bytes",
    "Interface traffic in bytes",
    ["device", "interface", "direction"],
)

# Device health metrics
device_cpu_percent = Gauge(
    "device_cpu_percent",
    "Device CPU utilization percentage",
    ["device"],
)
device_memory_percent = Gauge(
    "device_memory_percent",
    "Device memory utilization percentage",
    ["device"],
)
device_temperature_celsius = Gauge(
    "device_temperature_celsius",
    "Device temperature in Celsius",
    ["device", "sensor"],
)

# Device info (static labels)
device_info = Info(
    "device",
    "Device information",
    ["device"],
)

# =============================================================================
# State tracking for realistic simulation
# =============================================================================

# Track BGP session states to simulate occasional flaps
bgp_states: dict[str, dict[str, bool]] = {}

# Track interface states
interface_states: dict[str, dict[str, bool]] = {}

# Base values for counters (to simulate increments)
traffic_counters: dict[str, dict[str, dict[str, int]]] = {}
error_counters: dict[str, dict[str, int]] = {}


def init_state():
    """Initialize simulation state."""
    for device in DEVICES:
        bgp_states[device] = {}
        for peer_info in BGP_PEERS.get(device, []):
            bgp_states[device][peer_info["peer"]] = True  # Start established

        interface_states[device] = {}
        traffic_counters[device] = {}
        error_counters[device] = {}
        for iface in INTERFACES.get(device, []):
            interface_states[device][iface] = True  # Start up
            traffic_counters[device][iface] = {"in": 0, "out": 0}
            error_counters[device][iface] = 0


def update_metrics():
    """Update all metrics with realistic values."""
    for device, info in DEVICES.items():
        # Set device info (static)
        device_info.labels(device=device).info({
            "asn": str(info["asn"]),
            "router_id": info["router_id"],
            "management_ip": info["mgmt_ip"],
        })

        # BGP session metrics
        for peer_info in BGP_PEERS.get(device, []):
            peer = peer_info["peer"]
            peer_asn = DEVICES[peer]["asn"]

            # 10% chance of BGP flap
            if random.random() < 0.10:
                bgp_states[device][peer] = not bgp_states[device][peer]

            state = 1 if bgp_states[device][peer] else 0
            bgp_session_state.labels(
                device=device, peer=peer, asn=str(peer_asn)
            ).set(state)

            # Prefixes received (only if session is up)
            if state == 1:
                prefixes = random.randint(5, 25)
            else:
                prefixes = 0
            bgp_prefixes_received.labels(device=device, peer=peer).set(prefixes)

        # Interface metrics
        for iface in INTERFACES.get(device, []):
            # 5% chance of interface flap
            if random.random() < 0.05:
                interface_states[device][iface] = not interface_states[device][iface]

            state = 1 if interface_states[device][iface] else 0
            interface_up.labels(device=device, interface=iface).set(state)

            # Traffic counters (only increment if interface is up)
            if state == 1:
                # Simulate 1-10 MB of traffic per interval
                in_bytes = random.randint(1_000_000, 10_000_000)
                out_bytes = random.randint(1_000_000, 10_000_000)
                traffic_counters[device][iface]["in"] += in_bytes
                traffic_counters[device][iface]["out"] += out_bytes

            interface_traffic_bytes.labels(
                device=device, interface=iface, direction="in"
            )._value.set(traffic_counters[device][iface]["in"])
            interface_traffic_bytes.labels(
                device=device, interface=iface, direction="out"
            )._value.set(traffic_counters[device][iface]["out"])

            # Error counters (occasional errors, more likely if interface flapping)
            if random.random() < 0.02 or (state == 0 and random.random() < 0.3):
                error_counters[device][iface] += random.randint(1, 5)
            interface_errors_total.labels(
                device=device, interface=iface
            )._value.set(error_counters[device][iface])

        # Device health metrics
        # CPU: 15-45% normal, occasional spikes to 60-85%
        if random.random() < 0.15:
            cpu = random.uniform(60, 85)
        else:
            cpu = random.uniform(15, 45)
        device_cpu_percent.labels(device=device).set(round(cpu, 1))

        # Memory: 40-70% normal, occasional spikes to 75-90%
        if random.random() < 0.10:
            memory = random.uniform(75, 90)
        else:
            memory = random.uniform(40, 70)
        device_memory_percent.labels(device=device).set(round(memory, 1))

        # Temperature: 35-55C normal, occasional spikes to 60-70C
        for sensor in ["CPU", "Inlet", "Outlet"]:
            if random.random() < 0.08:
                temp = random.uniform(60, 70)
            else:
                temp = random.uniform(35, 55)
            device_temperature_celsius.labels(device=device, sensor=sensor).set(
                round(temp, 1)
            )


def metrics_loop(interval: int = 15):
    """Continuously update metrics at the specified interval."""
    while True:
        update_metrics()
        time.sleep(interval)


def main():
    """Start the metrics exporter."""
    print("Initializing synthetic network metrics exporter...")
    init_state()

    # Start Prometheus HTTP server on port 8888
    port = 8888
    print(f"Starting metrics server on port {port}")
    start_http_server(port)

    # Initial metrics update
    update_metrics()
    print(f"Metrics available at http://localhost:{port}/metrics")
    print("Updating metrics every 15 seconds...")

    # Start background update loop
    update_thread = threading.Thread(target=metrics_loop, args=(15,), daemon=True)
    update_thread.start()

    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")


if __name__ == "__main__":
    main()
