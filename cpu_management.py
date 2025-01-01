#!/usr/bin/env python3

import json
import psutil
import sys
from report_signatures import TimeStampGenerator
import logging  # Import the logging module

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

class CPUManager:
    def __init__(self):
        self.cpu_usage = None
        self.cpu_count = None
        self.cpu_time = None
        self.cpu_time_percentages = None
        self.cpu_frequents = None
        self.cpu_stats = None

    # Function to monitor CPU usage and related statistics
    def monitor_cpu(self):
        try:
            logger.info("Started CPU monitoring process.")
            
            # Retrieve total CPU usage
            self.cpu_usage = psutil.cpu_percent(interval=1, percpu=False)
            logger.debug(f"Total CPU Usage: {self.cpu_usage}%")
            
            # Retrieve total processor cores count (Logical)
            self.logical_cpu_count = psutil.cpu_count(logical=True)
            # Retrieve total processor cores count (Physical)
            self.physical_cpu_count = psutil.cpu_count(logical=False)
            logger.debug(f"Logical CPU cores: {self.logical_cpu_count}, Physical CPU cores: {self.physical_cpu_count}")

            # Retrieve system CPU times statistics as time durations
            self.cpu_time = psutil.cpu_times(percpu=False)
            logger.debug(f"CPU Times: {self.cpu_time}")

            # Retrieve system CPU times statistics as percentages
            self.cpu_time_percentages = psutil.cpu_times_percent(interval=1, percpu=False)
            logger.debug(f"CPU Times Percentages: {self.cpu_time_percentages}")

            # Retrieve current, min, and max CPU frequencies
            self.cpu_frequents = psutil.cpu_freq(percpu=False)
            logger.debug(f"CPU Frequencies: Current = {self.cpu_frequents.current} MHz, Min = {self.cpu_frequents.min} MHz, Max = {self.cpu_frequents.max} MHz")

            # Retrieve CPU stats
            self.cpu_stats = psutil.cpu_stats()
            logger.debug(f"CPU Stats: {self.cpu_stats}")

            statistics = {
                'CPU Usage Statistics': {
                    'Total CPU Usage': f'{self.cpu_usage} %',
                    'Total Processor Cores Count (Logical)': f'{self.logical_cpu_count}',
                    'Total Processor Cores Count (Physical)': f'{self.physical_cpu_count}',
                    'CPU Load Status': f'{"CPU load is normal." if self.cpu_usage < 75 else "CPU load is too high."}',
                    'System CPU Time Statistics (Time)': {
                        'User': f'{TimeStampGenerator().convertTime(self.cpu_time[0])}',
                        'System': f'{TimeStampGenerator().convertTime(self.cpu_time[1])}',
                        'IDLE': f'{TimeStampGenerator().convertTime(self.cpu_time[2])}',
                        'Interrupt': f'{TimeStampGenerator().convertTime(self.cpu_time[3])}',
                        'DPC': f'{TimeStampGenerator().convertTime(self.cpu_time[4])}'
                    },
                    'System CPU Time Statistics (Percentages)': {
                        'User': f'{self.cpu_time_percentages[0]} %',
                        'System': f'{self.cpu_time_percentages[1]} %',
                        'IDLE': f'{self.cpu_time_percentages[2]} %',
                        'Interrupt': f'{self.cpu_time_percentages[3]} %',
                        'DPC': f'{self.cpu_time_percentages[4]} %'
                    },
                    'CPU Frequency Statistics': {
                        'Current': f'{self.cpu_frequents.current} Mhz',
                        'Min': f'{self.cpu_frequents.min} Mhz',
                        'Max': f'{self.cpu_frequents.max} Mhz',
                    },
                    'CPU Stats Statistics': {
                        'Context Switches': f'{self.cpu_stats.ctx_switches}',
                        'Interrupts': f'{self.cpu_stats.interrupts}',
                        'Software Interrupts': f'{self.cpu_stats.soft_interrupts}',
                        'System Calls': f'{self.cpu_stats.syscalls}'
                    },
                    'Generated Time & Date': f'{TimeStampGenerator().generate_report()}'
                }
            }

            result = json.dumps(statistics, indent=4)
            json_output = json.loads(result)
            logger.info("CPU statistics successfully converted to JSON format.")
            
            return json_output  # Return the JSON output as a string

        except Exception as e:
            logger.error(f"Error during CPU monitoring: {e}")
            sys.exit(1)
