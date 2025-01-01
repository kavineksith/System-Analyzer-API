#!/usr/bin/env python3

import json
import psutil
import socket
import netifaces
import sys
from report_signatures import TimeStampGenerator
import logging  # Import logging module

# Configure logging
logger = logging.getLogger(__name__)

# Create file handler for logging to a file
file_handler = logging.FileHandler('system_analysis.log')
file_handler.setLevel(logging.DEBUG)  # Write all logs (DEBUG and higher) to the file

# Create a formatter and attach it to the file handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Set the logger's level to DEBUG to capture all log levels
logger.setLevel(logging.DEBUG)

class NetworkManager:
    def __init__(self):
        self.data = {
            "interface_stats": {},
            "interface_addrs": {},
            "connections": {}
        }

    @staticmethod
    # Function to check localhost connectivity
    def check_localhost_connectivity():
        try:
            logger.info("Checking localhost connectivity.")
            socket.gethostbyname('127.0.0.1')
            status = "PC is connected to localhost."
            logger.info("PC is connected to localhost.")
        except socket.gaierror:
            status = "PC isn't connected to localhost."
            logger.warning("PC isn't connected to localhost.")
        finally:
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).close()

        return status

    @staticmethod
    # Function to check network connectivity
    def check_network_connectivity():
        try:
            logger.info("Checking network connectivity.")
            socket.gethostbyname('www.google.com')
            status = "PC is connected to the internet."
            logger.info("PC is connected to the internet.")
        except socket.gaierror:
            status = "PC isn't connected to the internet."
            logger.warning("PC isn't connected to the internet.")
        finally:
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).close()

        return status

    @staticmethod
    # Function to monitor network traffic
    def monitor_network_traffic():
        try:
            logger.info("Monitoring network traffic.")
            network = psutil.net_io_counters()
            logger.debug(f"Network Traffic: {network}")
            return {
                'Network Traffic Information': {
                    'Send': f'{network.bytes_sent / (1024 ** 2):.2f} Mbps',
                    'Received': f'{network.bytes_recv / (1024 ** 2):.2f} Mbps',
                },
                'Extra Information': {
                    'Packets Sent': f'{network.packets_sent}',
                    'Packet Received': f'{network.packets_recv}',
                    'ErrorIn': f'{network.errin}',
                    'ErrorOut': f'{network.errout}',
                    'DropIn': f'{network.dropin}',
                    'DropOut': f'{network.dropout}'
                }
            }
        except Exception as e:
            logger.error(f"Error monitoring network traffic: {e}")
            sys.exit(1)

    def gather_interface_stats(self):
        """Gathers network interface statistics."""
        try:
            logger.info("Gathering network interface statistics.")
            stats = psutil.net_if_stats()
            for iface, info in stats.items():
                self.data["interface_stats"][iface] = {
                    "isup": info.isup,
                    "duplex": self._get_duplex_name(info.duplex),
                    "speed": info.speed,
                    "mtu": info.mtu,
                    "flags": info.flags
                }
            logger.info("Network interface statistics gathered successfully.")
        except Exception as e:
            logger.error(f"Error gathering interface stats: {e}")

    def gather_interface_addrs(self):
        """Gathers network interface addresses."""
        try:
            logger.info("Gathering network interface addresses.")
            addrs = psutil.net_if_addrs()
            for iface, info_list in addrs.items():
                self.data["interface_addrs"][iface] = []
                for info in info_list:
                    self.data["interface_addrs"][iface].append({
                        "family": self._get_family_name(info.family),
                        "address": info.address,
                        "netmask": info.netmask,
                        "broadcast": info.broadcast,
                        "ptp": info.ptp
                    })
            logger.info("Network interface addresses gathered successfully.")
        except Exception as e:
            logger.error(f"Error gathering interface addresses: {e}")

    def gather_connections(self, kind: str):
        """Gathers network connections of a specific kind."""
        try:
            logger.info(f"Gathering network connections for kind: {kind}")
            connections = psutil.net_connections(kind=kind)
            self.data["connections"][kind] = []
            for conn in connections:
                self.data["connections"][kind].append({
                    "fd": conn.fd,
                    "family": self._get_family_name(conn.family),
                    "type": self._get_socket_type_name(conn.type),
                    "local_address": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "None",
                    "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "None",
                    "status": conn.status,
                    "pid": conn.pid if conn.pid is not None else 'None'
                })
            logger.info(f"Network connections for kind '{kind}' gathered successfully.")
        except Exception as e:
            logger.error(f"Error gathering connections for kind='{kind}': {e}")

    def gather_all_info(self):
        """Gathers all network-related information."""
        logger.info("Gathering all network-related information.")
        self.gather_interface_stats()
        self.gather_interface_addrs()
        kinds = [
            "inet",  # IPv4 and IPv6
            "inet4", # IPv4
            "inet6", # IPv6
            "tcp",   # TCP
            "tcp4",  # TCP over IPv4
            "tcp6",  # TCP over IPv6
            "udp",   # UDP
            "udp4",  # UDP over IPv4
            "udp6",  # UDP over IPv6
        ]
        for kind in kinds:
            self.gather_connections(kind)
        logger.info("All network-related information gathered successfully.")

    def _get_duplex_name(self, duplex):
        """Safely get the name of the duplex type."""
        try:
            return duplex.name
        except AttributeError:
            return str(duplex)

    def _get_family_name(self, family):
        """Safely get the name of the address family."""
        try:
            return family.name
        except AttributeError:
            return str(family)

    def _get_socket_type_name(self, socket_type):
        """Safely get the name of the socket type."""
        try:
            return socket_type.name
        except AttributeError:
            return str(socket_type)

    def to_json(self) -> str:
        """Returns the gathered data as a JSON string."""
        return json.dumps(self.data, indent=4)

    @staticmethod
    def get_network_info():
        """Gathers detailed network interface information."""
        logger.info("Gathering detailed network interface information.")
        addr_family_map = {
            netifaces.AF_INET: 'IPv4',
            netifaces.AF_INET6: 'IPv6',
            netifaces.AF_LINK: 'MAC'
        }

        network_info = {}

        try:
            interfaces = netifaces.interfaces()
            gateways = netifaces.gateways()

            for interface in interfaces:
                addrs = netifaces.ifaddresses(interface)
                interface_info = {
                    'interface_name': interface,
                    'mac_address': None,
                    'default_gateway': None,
                    'ip_addresses': []
                }

                if netifaces.AF_LINK in addrs:
                    mac_info = addrs[netifaces.AF_LINK][0]
                    interface_info['mac_address'] = mac_info.get('addr')

                if 'default' in gateways:
                    for key, value in gateways['default'].items():
                        if value[1] == interface:
                            interface_info['default_gateway'] = value[0]
                            break

                if interface_info['default_gateway'] is None:
                    interface_info['default_gateway'] = "None"

                for addr_family, addr_info in addrs.items():
                    for addr in addr_info:
                        family_name = addr_family_map.get(addr_family, 'Unknown')
                        address_details = {
                            'address_family': family_name,
                            'ip_address': addr.get('addr') if addr.get('addr') is not None else "None",
                            'subnet_mask': addr.get('netmask') if addr.get('netmask') is not None else "None",
                            'broadcast_address': addr.get('broadcast') if addr.get('broadcast') is not None else "None",
                            'peer_address': addr.get('peer') if addr.get('peer') is not None else "None"
                        }
                        interface_info['ip_addresses'].append(address_details)
                
                network_info[interface] = interface_info

            logger.info("Detailed network interface information gathered successfully.")
            return network_info

        except Exception as e:
            logger.error(f"Error getting network information: {str(e)}")

    @staticmethod
    # Function to manage network statistics
    def network_report():
        try:
            logger.info("Generating network report.")
            localhost_connectivity = NetworkManager().check_localhost_connectivity()
            network_connectivity = NetworkManager().check_network_connectivity()
            network_traffic = NetworkManager().monitor_network_traffic()

            statistics = {
                'Network Usage Statistics': {
                    'Localhost Connectivity': localhost_connectivity,
                    'Network Connectivity': network_connectivity,
                    'Network Traffic': network_traffic,
                    'Generated Time & Date': f'{TimeStampGenerator().generate_report()}'
                }
            }

            statistics_report = json.dumps(statistics, indent=4)
            deep_analyzer = NetworkManager()
            deep_analyzer.gather_all_info()
            deep_analyzed_report = deep_analyzer.to_json()

            network_interface_report = json.dumps(NetworkManager().get_network_info(), indent=4)

            combined_report = dict(json.loads(statistics_report), **json.loads(deep_analyzed_report), **json.loads(network_interface_report))

            result = json.dumps(combined_report, indent=4)
            json_output = json.loads(result)
            logger.info("Network report generated successfully.")
            return json_output
        except Exception as e:
            logger.error(f"Error generating network report: {e}")
            sys.exit(1)
