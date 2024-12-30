#!/usr/bin/env python3

import json
import os
import sys
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG,  # Log all levels (DEBUG and above)
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

# Create a logger
logger = logging.getLogger(__name__)

def create_directory_and_generate_file_path(base_directory, file_name):
    """
    Creates a directory if it doesn't already exist and generates a file path.

    Args:
    - base_directory (str): Base directory path where the directory will be created and the file path will be generated.
    - file_name (str): Name of the file (including extension).

    Returns:
    - str: Full file path.
    """
    try:
        # Create directory if it doesn't exist
        directory_path = Path(base_directory)
        directory_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory created or already exists: {directory_path}")

        # Generate file path
        file_path = directory_path / file_name
        logger.info(f"Generated file path: {file_path}")
        
        return str(file_path)
    except Exception as e:
        logger.error(f"Error creating directory or generating file path: {e}")
        raise

def control_result_to_json(statistics):
    try:
        # User input for base directory and file name
        base_directory = input("Enter base directory path: ").strip()
        file_name = input("Enter file name (including extension): ").strip()

        logger.info(f"User provided base directory: {base_directory}, file name: {file_name}")

        # Generate file path and create directory if necessary
        file_path = create_directory_and_generate_file_path(base_directory, file_name)
        logger.info(f"Generated file path: {file_path}")

        # Write the dictionary to JSON file
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(statistics, json_file, indent=4, ensure_ascii=False)
        logger.info(f"JSON data has been saved to {file_path}")
        print("JSON data has been saved to", file_path)

    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        print(ve)
        sys.exit(1)
    except PermissionError:
        logger.error("Permission denied to access the source or export file.")
        print("Permission denied to access the source or export file.")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Process interrupted by the user.")
        print("Process interrupted by the user.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error uploading data: {e}")
        print("Error uploading data:", e)
        sys.exit(1)

