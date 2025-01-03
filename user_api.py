#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import time
import sqlite3
from sys_analyze_api import SystemAnalyzer
import logging

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

class Database:
    """Class responsible for interacting with the SQLite database for request limits."""

    def __init__(self, db_name='request_limit.db'):
        self.db_name = db_name

    def get_connection(self):
        """Establish and return a connection to the SQLite database."""
        try:
            return sqlite3.connect(self.db_name)
        except sqlite3.DatabaseError as e:
            raise Exception(f"Database connection error: {e}")

    def check_request_limit(self, ip, limit=5, window=60):
        """Check if the IP has exceeded the request limit within the given window."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            current_time = int(time.time())
            cursor.execute('SELECT request_count, last_request_time FROM request_limits WHERE ip_address = ?', (ip,))
            row = cursor.fetchone()

            if row:
                request_count, last_request_time = row
                # Reset counter if the time window has passed
                if current_time - last_request_time > window:
                    request_count = 0
                    last_request_time = current_time

                if request_count >= limit:
                    conn.close()
                    return False
                else:
                    # Increment the request count and update the timestamp
                    cursor.execute('UPDATE request_limits SET request_count = ?, last_request_time = ? WHERE ip_address = ?',
                                   (request_count + 1, current_time, ip))
            else:
                # Create a new entry for this IP if it does not exist
                cursor.execute('INSERT INTO request_limits (ip_address, request_count, last_request_time) VALUES (?, ?, ?)',
                               (ip, 1, current_time))

            conn.commit()
            conn.close()
            return True

        except sqlite3.DatabaseError as e:
            logger.error(f"Database error during request limit check: {e}")
            raise Exception(f"Database error during request limit check: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise Exception(f"Unexpected error: {e}")


class RateLimiter:
    """Class responsible for handling rate-limiting logic using the Database class."""

    def __init__(self, database, limit=5, window=60):
        self.database = database
        self.limit = limit
        self.window = window

    def check_and_update(self, ip):
        """Check if the IP has exceeded the request limit and update the database."""
        try:
            return self.database.check_request_limit(ip, self.limit, self.window)
        except Exception as e:
            logger.error(f"Error checking or updating rate limit for IP {ip}: {e}")
            raise Exception(f"Error checking or updating rate limit: {e}")


class ReportGenerator:
    """Class responsible for generating reports."""

    @staticmethod
    def get_report(report_type, report_id):
        """Generate a report based on the report type and ID."""
        try:
            if report_type == 'single_report':
                if report_id < 0 or report_id > 7:
                    logger.warning(f"Invalid report ID: {report_id}. Must be between 0 and 7.")
                    return None, 'Invalid report ID. Please enter a number between 0 and 7.'
                statistics = SystemAnalyzer.once_status_one_report(report_id)
                if statistics is None:
                    logger.error(f"Failed to generate report with Report ID {report_id}.")
                    return None, f'Failed to generate report with Report ID {report_id}.'
                return statistics, None

            elif report_type == 'all_in_one':
                statistics = SystemAnalyzer.all_in_one()
                if statistics is None:
                    logger.error('Failed to generate all-in-one report.')
                    return None, 'Failed to generate all-in-one report.'
                return statistics, None

            else:
                logger.warning(f"Invalid report type: {report_type}. Must be 'single_report' or 'all_in_one'.")
                return None, 'Invalid report type. Please choose "single_report" or "all_in_one".'

        except Exception as e:
            logger.error(f"Error generating report: {e}")
            raise Exception(f"Error generating report: {e}")


class App:
    """Class responsible for setting up the Flask app and routes."""

    def __init__(self):
        self.app = Flask(__name__)
        self.database = Database()
        self.rate_limiter = RateLimiter(self.database)
        self.report_generator = ReportGenerator()
        self.configure_app()

    def configure_app(self):
        """Configure the Flask app, set up CORS and routes."""
        CORS(self.app, resources={r"/api/*": {"origins": ["http://127.0.0.1"]}})  # Please add the appropriate origin
        self.app.add_url_rule('/report', view_func=self.get_report, methods=['GET'])
        limiter = Limiter(get_remote_address, app=self.app)
        limiter.init_app(self.app)

    def get_report(self):
        """Endpoint to handle the report generation."""
        ip = request.remote_addr  # Get the client's IP address
        
        # Check if the IP has exceeded the rate limit
        try:
            if not self.rate_limiter.check_and_update(ip):
                logger.warning(f"Rate limit exceeded for IP {ip}.")
                return jsonify({'error': 'Request limit exceeded. Please try again later.'}), 429

            report_type = request.args.get('type', default='single_report', type=str)
            report_id = request.args.get('id', default=0, type=int)

            logger.info(f"Received request for report type: {report_type}, report ID: {report_id}")
            statistics, error = self.report_generator.get_report(report_type, report_id)
            if error:
                logger.error(f"Error generating report: {error}")
                return jsonify({'error': error}), 400

            logger.info(f"Successfully generated report for {report_type} with ID {report_id}")
            return jsonify(statistics), 200

        except Exception as e:
            logger.error(f"Internal server error: {e}", exc_info=True)
            return jsonify({'error': 'An internal error has occurred. Please try again later.'}), 500

    def run(self):
        """Run the Flask app."""
        try:
            self.app.run(host='0.0.0.0', port=5000, debug=True)
        except Exception as e:
            logger.error(f"Error running the app: {e}")
            print(f"Error running the app: {e}")


if __name__ == "__main__":
    app = App()
    app.run()
