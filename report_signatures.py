from datetime import datetime
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

class TimeStampGenerator:
    def __init__(self):
        pass

    @staticmethod
    def current_time():
        try:
            logger.info("Generating current time.")
            current_time = datetime.now().strftime('%H:%M:%S')
            logger.info(f"Current time generated: {current_time}")
            return current_time
        except Exception as e:
            logger.error(f"Error generating current time: {e}")

    @staticmethod
    def current_date():
        try:
            logger.info("Generating current date.")
            current_date = datetime.now().strftime('%d/%m/%Y')
            logger.info(f"Current date generated: {current_date}")
            return current_date
        except Exception as e:
            logger.error(f"Error generating current date: {e}")

    @staticmethod
    def generate_report():
        try:
            logger.info("Generating report with current time and date.")
            current_time = TimeStampGenerator.current_time()
            current_date = TimeStampGenerator.current_date()
            report = f'{current_time} | {current_date}'
            logger.info(f"Report generated: {report}")
            return report
        except Exception as e:
            logger.error(f"Error generating report: {e}")

    @staticmethod
    def convertTime(seconds):
        try:
            logger.info(f"Converting {seconds} seconds to standard time format.")
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            formatted_time = '%d:%02d:%02d' % (hours, minutes, seconds)
            logger.info(f"Converted time: {formatted_time}")
            return formatted_time
        except Exception as e:
            logger.error(f"Error converting time: {e}")
