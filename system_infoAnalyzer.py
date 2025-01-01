#!/usr/bin/env python3

import datetime  # importing datetime, os, json, platform, sys and psutil libraries
import os
import json
import platform
import sys
import psutil
import logging
from report_signatures import TimeStampGenerator  # importing date-time stamp generator library

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

class SystemInformation:
    @staticmethod
    def check_reboot():
        try:
            logger.info("Checking for pending reboot.")
            location = os.path.exists('run/reboot-required')
            reboot_status = "Pending Reboot." if location else "No pending Reboot."
            logger.info(f"Reboot status: {reboot_status}")
            return reboot_status
        except Exception as e:
            logger.error(f"Error checking reboot status: {e}")
            raise RuntimeError("Error checking reboot status:", e)

    @staticmethod
    def get_boot_time():
        try:
            logger.info("Fetching system boot time.")
            boot_time = psutil.boot_time()
            logger.info(f"System boot time fetched: {boot_time}")
            return boot_time
        except Exception as e:
            logger.error(f"Error fetching boot time: {e}")
            raise RuntimeError("Error fetching boot time:", e)

    @staticmethod
    def get_users():
        try:
            logger.info("Fetching system users.")
            users = psutil.users()
            user_list = [value[0] for value in users]
            logger.info(f"Users fetched: {user_list}")
            return user_list
        except Exception as e:
            logger.error(f"Error fetching user profiles: {e}")
            raise RuntimeError("Error fetching user profiles:", e)

    @staticmethod
    def system_info():
        try:
            logger.info("Retrieving system information.")
            
            # Retrieving basic system information using platform and os modules
            os_name = os.name.upper()
            system_architecture = sys.platform
            os_platform = platform.system()
            os_architecture = platform.architecture()[0]
            os_release = platform.release()
            os_version = platform.version()
            device_processor = platform.processor()
            machine_type = platform.machine()
            sys_platform = platform.platform()
            os_edition = platform.win32_edition()
            device_name = platform.node()

            system_users = SystemInformation().get_users()

            # System Info Statistics
            statistics = {
                'System Info Statistics': {
                    'System Information': {
                        'Device Name': f'{device_name}',
                        'Operating System': f'{os_platform} {os_name} {os_release} {os_architecture} {os_edition}',
                        'OS Release and Service Pack Version': f'{sys_platform}',
                        'Operating System Version': f'{os_version}',
                        'Processor Identity': f'{device_processor}',
                        'Machine Type': f'{machine_type}',
                        'System Platform': f'{system_architecture}',
                        'OS Architecture': f'{os_architecture}'
                    },
                    'System Boot Information': {
                        'Reboot Status': f'{SystemInformation().check_reboot()}',
                        'System Boot Time (sec)': f'{SystemInformation().get_boot_time()} seconds.',
                        'System Boot Time': f'{datetime.datetime.fromtimestamp(SystemInformation().get_boot_time()).strftime("%Y-%m-%d %H:%M:%S")}'
                    },
                    'System Users List': system_users,
                    'Generated Time & Date': f'{TimeStampGenerator().generate_report()}'
                }
            }

            logger.info("System information retrieved successfully.")
            result = json.dumps(statistics, indent=4)
            json_output = json.loads(result)
            return json_output  # Return the JSON output as a string
        
        except RuntimeError as re:
            logger.error(f"Error fetching system information: {re}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise RuntimeError("An error occurred:", e)
