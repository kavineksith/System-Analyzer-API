#!/usr/bin/env python3

import json
import psutil  # importing psutil library
from report_signatures import TimeStampGenerator  # importing generate_report and convert time library functions
import sys  # importing sys library
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

class BatteryManager:
    @staticmethod
    def batteryManagement():
        try:
            logger.info("Started battery management process.")
            
            # Battery Usage Statistics
            battery = psutil.sensors_battery()  # assign battery variable to psutil battery function
            logger.debug(f"Battery info retrieved: {battery}")

            # Convert time if battery time left is available
            remaining_battery_time = TimeStampGenerator().convertTime(battery.secsleft)
            logger.debug(f"Remaining battery time: {remaining_battery_time}")

            # Prepare the statistics
            statistics = {
                'Battery Usage Statistics': {
                    'Battery Percentage': f'{battery.percent} %',
                    'Power Connectivity': 'Power Connected' if battery.power_plugged else 'Power Disconnected',
                    'Battery Remaining Time': 'Fully Charged' if battery.percent == 100 or not battery else f'{remaining_battery_time}',
                    'Generated Time & Date': f'{TimeStampGenerator().generate_report()}'
                }
            }
            logger.info("Battery statistics prepared.")

            # Convert statistics to JSON string
            result = json.dumps(statistics, indent=4)
            json_output = json.loads(result)
            logger.info("Battery statistics successfully converted to JSON format.")

            return json_output  # Return the JSON output as a string

        except Exception as e:
            logger.error(f"Error during battery management: {e}")
            sys.exit(1)

print(BatteryManager().batteryManagement())