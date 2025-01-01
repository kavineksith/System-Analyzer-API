#!/usr/bin/env python3

import json
import psutil
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

class ProcessManager:
    def __init__(self):
        self.process_list = None

    def get_process_list(self):
        try:
            logger.info("Retrieving process list.")
            self.process_list = [{'pid': pid} for pid in psutil.pids()]
            logger.info(f"Retrieved process list: {self.process_list}")
            return self.process_list
        except Exception as e:
            logger.error(f"Error retrieving process list: {e}")
            sys.exit(1)

    def get_process_info(self):
        process_info_list = []
        try:
            logger.info("Gathering process information.")
            for process in self.process_list:
                process_id = process['pid']
                proc = psutil.Process(process_id)
                process_info = proc.as_dict(attrs=['pid', 'name'])
                process_info_list.append(process_info)

            logger.info(f"Retrieved process information: {process_info_list}")
            return process_info_list
        except psutil.NoSuchProcess as e:
            logger.error(f"Error retrieving process info: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error: {e}")
            sys.exit(1)

    def manage_processes(self):
        try:
            logger.info("Managing system processes.")
            process_list = self.get_process_list()
            process_info = self.get_process_info()

            # Check if process_list is a string, if not convert it to a string
            if not isinstance(process_list, str):
                process_list = ", ".join(map(str, process_list))

            statistics = {
                'System Processes Statistics': {
                    'Process List': process_list,
                    'Process Info': process_info,
                    'Generated Time & Date': f'{TimeStampGenerator().generate_report()}'
                }
            }

            result = json.dumps(statistics, indent=4)
            json_output = json.loads(result)

            logger.info("System processes managed successfully.")
            return json_output  # Return the JSON output as a string
        except Exception as e:
            logger.error(f"Error managing processes: {e}")
            sys.exit(1)
