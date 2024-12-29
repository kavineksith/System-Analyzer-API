#!/usr/bin/env python3

from flask import jsonify
from battery_management import BatteryManager
from cpu_management import CPUManager
from disk_management import DiskManager
from memory_management import MemoryManager
from network_management import NetworkManager
from process_management import ProcessManager
from system_infoAnalyzer import SystemInformation


class systemAnalyzer:
    @staticmethod
    def all_in_one():
        try:
            cpu_status = CPUManager().monitor_cpu()
            process_status = ProcessManager().manage_processes()
            memory_status = MemoryManager().memory_statistics()
            disk_status = DiskManager().manage_disk()
            network_status = NetworkManager().network_report()
            system_status = SystemInformation().system_info()
            battery_status = BatteryManager().batteryManagement()

            status_list = [cpu_status, process_status, memory_status, disk_status, network_status, system_status,
                           battery_status]

            return status_list

        except Exception as e:
            return jsonify({'error': f'Error in generating all-in-one report: {e}'}), 500

    @staticmethod
    def once_status_one_report(token):
        try:
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
        except ValueError and Exception as e:
            return jsonify({'error':f'Error executing report: {e}'}), 400
