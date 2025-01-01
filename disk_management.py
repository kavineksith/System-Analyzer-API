#!/usr/bin/env python3

import json
import sys
import psutil
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

class DiskManager:
    def __init__(self):
        self.partitions = []  # Initialize as an empty list

    # Function to generate storage overall report
    def generate_overall_report(self):
        try:
            logger.info("Started generating overall storage report.")
            partition_info = []
            # Storage Overall Report
            local_partitions = psutil.disk_partitions()
            logger.debug(f"Local partitions retrieved: {local_partitions}")
            
            for partition in local_partitions:
                partition_dict = {
                    "Device": partition.device,
                    "MountPoint": partition.mountpoint,
                    "FileSystemType": partition.fstype,
                    "Opts": partition.opts,
                }
                
                # Try to get maxfile and maxpath if available
                try:
                    partition_dict["MaxFile"] = partition.maxfile
                    partition_dict["MaxPath"] = partition.maxpath
                except AttributeError:
                    pass  # Ignore the error if the attribute is not available

                self.partitions.append(partition.device)  # Store device name only
                partition_info.append(partition_dict)
            
            logger.info("Overall storage report generated successfully.")
            return partition_info
        except Exception as e:
            logger.error(f"Error generating overall report: {e}")
            return []  # Return empty list if error occurs

    # Function to generate storage statistics report
    def generate_statistics_report(self):
        try:
            logger.info("Started generating storage statistics report.")
            disk_info = []
            # Storage Statistics Report
            for partition in self.partitions:
                usage = psutil.disk_usage(partition)
                logger.debug(f"Disk usage for partition {partition}: {usage}")
                disk_dict = {
                    "Local Disk": partition,
                    "Total": f"{usage.total / (1024 ** 3):.2f} GB",
                    "Used": f"{usage.used / (1024 ** 3):.2f} GB",
                    "Free": f"{usage.free / (1024 ** 3):.2f} GB",
                    "Percentage Used": f"{usage.percent} %",
                    "Percentage Free": f"{(usage.free / usage.total * 100):.1f} %"
                }
                disk_info.append(disk_dict)

            logger.info("Storage statistics report generated successfully.")
            return disk_info
        except Exception as e:
            logger.error(f"Error generating statistics report: {e}")
            return []  # Return empty list if error occurs

    # Function to check storage level
    def check_storage_level(self):
        try:
            logger.info("Started checking storage level.")
            partition_info = []
            # Storage Level Checker
            for partition in self.partitions:
                disk = psutil.disk_usage(partition)
                free_percentage = disk.free / disk.total * 100
                free_gigabytes = disk.free / 2 ** 30
                minimum_gigabytes = 2
                minimum_percentage = 10

                if free_percentage < minimum_percentage or free_gigabytes < minimum_gigabytes:
                    status = "Storage isn't sufficient."
                else:
                    status = "Storage is sufficient."

                partition_dict = {
                    "Partition": partition,
                    "Status": status
                }

                partition_info.append(partition_dict)

            logger.info("Storage level check completed.")
            return partition_info
        except Exception as e:
            logger.error(f"Error checking storage level: {e}")
            return []  # Return empty list if error occurs

    # Function to manage disk statistics and save reports
    def manage_disk(self):
        try:
            logger.info("Started managing disk statistics.")
            overall_report = self.generate_overall_report()
            storage_report = self.generate_statistics_report()
            storage_level = self.check_storage_level()

            statistics = {
                'Disk Statistics': {
                    'Storage Overall Report': overall_report,
                    'Storage Statistics Report': storage_report,
                    'Storage Level Report': storage_level,
                    'Generated Time & Date': f'{TimeStampGenerator().generate_report()}'
                }
            }

            result = json.dumps(statistics, indent=4)
            json_output = json.loads(result)
            logger.info("Disk statistics successfully converted to JSON format.")
            
            return json_output  # Return the JSON output as a string
        except Exception as e:
            logger.error(f"Error during disk management: {e}")
            sys.exit(1)
