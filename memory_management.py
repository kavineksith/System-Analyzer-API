#!/usr/bin/env python3

import json
import psutil
import sys
from report_signatures import TimeStampGenerator
import logging  # Import logging module

# Configure the logger
logging.basicConfig(level=logging.DEBUG,  # Log all levels (DEBUG and above)
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

# Create a logger
logger = logging.getLogger(__name__)

class MemoryManager:
    @staticmethod
    # Function to retrieve and print memory statistics
    def memory_statistics():
        try:
            logger.info("Started retrieving memory statistics.")
            
            # System memory usage statistics
            v_memory = psutil.virtual_memory()
            logger.debug(f"Virtual memory: {v_memory}")
            
            # System swap memory statistics
            s_memory = psutil.swap_memory()
            logger.debug(f"Swap memory: {s_memory}")
            
            statistics = {
                'Memory Usage Statistics': {
                    'System Memory': {
                        'Total': f'{v_memory.total / (1024 ** 3):.2f} GB',
                        'Available': f'{v_memory.available / (1024 ** 3):.2f} GB',
                        'Percentage': f'{v_memory.percent} %',
                        'Used': f'{v_memory.used / (1024 ** 3):.2f} GB',
                        'Free': f'{v_memory.free / (1024 ** 3):.2f} GB'
                    },
                    'THRESHOLD': f'{"Warning: Available memory is below the threshold of 100MB." if v_memory.available <= (100 * 1024 * 1024) else "Available memory is sufficient."}',
                    'Swap Memory': {
                        'Total': f'{s_memory.total / (1024 ** 3):.2f} GB',
                        'Used': f'{s_memory.used / (1024 ** 3):.2f} GB',
                        'Free': f'{s_memory.free / (1024 ** 3):.2f} GB',
                        'Percentage': f'{s_memory.percent} %',
                        'System IN': f'{s_memory.sin / (1024 ** 3):.2f} GB',
                        'System OUT': f'{s_memory.sout / (1024 ** 3):.2f} GB'
                    },
                    'Generated Time & Date': f'{TimeStampGenerator().generate_report()}'
                }
            }

            result = json.dumps(statistics, indent=4)
            json_output = json.loads(result)
            
            logger.info("Memory statistics retrieved and converted to JSON successfully.")
            return json_output  # Return the JSON output as a string
        except Exception as e:
            logger.error(f"Error retrieving memory statistics: {e}")
            sys.exit(1)
