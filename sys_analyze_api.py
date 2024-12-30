#!/usr/bin/env python3

import logging
from flask import jsonify
from battery_management import BatteryManager
from cpu_management import CPUManager
from disk_management import DiskManager
from memory_management import MemoryManager
from network_management import NetworkManager
from process_management import ProcessManager
from system_infoAnalyzer import SystemInformation

# Configure the logger
logging.basicConfig(level=logging.DEBUG,  # Log all levels (DEBUG and above)
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

# Create a logger
logger = logging.getLogger(__name__)

class SystemAnalyzer:
    @staticmethod
    def all_in_one():
        try:
            logger.info("Generating all-in-one system status report.")
            cpu_status = CPUManager().monitor_cpu()
            process_status = ProcessManager().manage_processes()
            memory_status = MemoryManager().memory_statistics()
            disk_status = DiskManager().manage_disk()
            network_status = NetworkManager().network_report()
            system_status = SystemInformation().system_info()
            battery_status = BatteryManager().batteryManagement()

            status_list = [cpu_status, process_status, memory_status, disk_status, network_status, system_status, battery_status]
            logger.info("All-in-one system status report generated successfully.")
            return status_list

        except Exception as e:
            logger.error(f"Error generating all-in-one report: {e}")
            return jsonify({'error': 'An internal error has occurred while generating the report.'}), 500

    @staticmethod
    def once_status_one_report(token):
        try:
            logger.info(f"Generating single report for token: {token}")
            match token:
                case 1:
                    return CPUManager().monitor_cpu()
                case 2:
                    return ProcessManager().manage_processes()
                case 3:
                    return MemoryManager().memory_statistics()
                case 4:
                    return DiskManager().manage_disk()
                case 5:
                    return NetworkManager().network_report()
                case 6:
                    return SystemInformation().system_info()
                case 7:
                    return BatteryManager().batteryManagement()
                case _:
                    raise ValueError('Invalid selection. Please enter a number between 1 and 7.')
        except ValueError as ve:
            logger.warning(f"Value error: {ve}")
            return jsonify({'error': f'Value error: {ve}'}), 400
        except Exception as e:
            logger.error(f"Error executing report for token {token}: {e}")
            return jsonify({'error': 'An internal error has occurred while executing the report.'}), 500
