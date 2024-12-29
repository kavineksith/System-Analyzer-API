# System Analyzing and Monitoring Documentation

## Overview
This Python script provides comprehensive system monitoring capabilities, offering insights into various aspects of system performance and configuration. It covers functionalities such as battery usage statistics, CPU usage, disk management, memory usage, network statistics, process management, system information overview, and more. The script utilizes the `psutil` library for accessing system-related information and generating reports with date-time stamps.

## Features
- **Battery Usage Statistics**: Displays battery percentage, power connectivity status, and remaining battery time.
- **CPU Usage Monitoring**: Provides CPU usage percentage, processor cores count, system CPU times statistics, CPU frequencies, and CPU stats.
- **Disk Management**: Offers storage overall report, storage statistics report, and storage level checker.
- **Memory Usage Statistics**: Presents system memory usage statistics including total memory, available memory, percentage used, and swap memory statistics.
- **Network Usage Statistics**: Shows network connectivity status, network traffic analysis, and extra information about network packets.
- **Process Management**: Lists system process IDs and their names.
- **System Information Overview**: Retrieves basic system information such as operating system details, processor identity, machine type, and more.

## Script Components

### 1. Various Monitoring Functions
- **Battery Management**: Displays battery usage statistics including percentage, power status, and remaining time.
- **CPU Management**: Monitors CPU usage, CPU times, CPU frequencies, and CPU stats.
- **Disk Management**: Manages storage including storage reports and storage level checking.
- **Memory Management**: Provides memory usage statistics including system memory and swap memory.
- **Network Management**: Offers network connectivity status, network traffic analysis, and extra network information.
- **Process Management**: Lists system processes and their IDs.
- **System Information**: Retrieves basic system information such as OS details, processor identity, and more.

### 2. Utility Functions
- **ConvertTime**: Converts seconds to a standard time format.
- **BatteryStatus**: Checks power connectivity status (plugged or unplugged).
- **CheckCpu**: Checks CPU load and returns status (normal or too high).

### 3. Main Functionality
- Orchestrates the execution of monitoring functions and report generation.
- Provides an entry point for executing the script.

## Dependencies
- Python 3.x
  - `psutil` library for accessing system-related information
  - `os` library for system-specific functions
  - `platform` library for accessing system platform information
  - `datetime` library for date-time operations
  - `socket` library for network-related operations
  - `netifaces` library for network interface information and IP address retrieval
  - `report_signatures` module for generating reports with date-time stamps
  
  - `Flask`: A lightweight Python web framework to build web applications.
  - `jsonify`: A Flask helper function to convert Python data structures (like dictionaries) into JSON format, which is typically used in REST APIs.
  - `request`: Used to access incoming HTTP requests, including data from headers, query parameters, or JSON body.
  - `Limiter`: A Flask extension for rate limiting, helpful to prevent abuse of the API by limiting the number of requests a user can make in a given period.
  - `get_remote_address`: A utility function from `flask_limiter.util` to fetch the IP address of the client making the request.
  - `CORS`: Enables Cross-Origin Resource Sharing (CORS) in the Flask app, useful when your frontend is served from a different domain than your API.
  - `time`: The built-in Python library for time-related operations.
  - `sqlite3`: A built-in Python library for interacting with SQLite databases, helpful for storing and querying data in a lightweight database.

## Usage
1. **Execution**: Run the script using Python 3.x.
2. **Monitoring**: View the output to monitor various system aspects such as battery usage, CPU usage, memory usage, network statistics, etc.
3. **Reports**: Reports are generated with date-time stamps for reference.

## Conclusion
The System Analyzer script offers a robust tool for monitoring and reporting on various system metrics. By providing detailed insights into CPU usage, process management, memory, disk, network, system information, and battery status, it helps users maintain a clear understanding of their system's performance. With features like customizable reporting, screen management, and JSON output, the script is a versatile solution for both casual users and system administrators. Its comprehensive error handling ensures reliability and ease of use in various scenarios.

*Tailor every script to meet specific user requirements, allowing for easy upgrades and customization to suit individual needs.*

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### **Disclaimer:**
Kindly note that this project is developed solely for educational purposes, not intended for industrial use, as its sole intention lies within the realm of education. We emphatically underscore that this endeavor is not sanctioned for industrial application. It is imperative to bear in mind that any utilization of this project for commercial endeavors falls outside the intended scope and responsibility of its creators. Thus, we explicitly disclaim any liability or accountability for such usage.
