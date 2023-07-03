import unittest
import os
import tempfile
from app import create_app


class LogMonitorTestCase(unittest.TestCase):
    """
    This is a base test case class for testing the Flask Log Monitor application.

    It extends the unittest.TestCase class and sets up a new application instance
    and a test client for each test. This ensures each test runs in its own
    isolated context.

    Additionally, it creates a temporary file before each test and deletes it
    after each test. This can be used as a log file in tests to simulate
    the /var/log files that the actual application works with.

    Attributes:
        app: An instance of the Flask Log Monitor application.
        client: A test client for the application. This can be used to send
            requests to the application.
        db_fd: A file descriptor for the temporary file.
        log_file_name: The name of the temporary file.

    How to use this class:
        When writing tests for the Flask Log Monitor, extend this class instead
        of unittest.TestCase. This gives your test access to the app, client,
        db_fd, and log_file_name attributes, and ensures your test runs in its
        own isolated context.
    """

    def setUp(self):
        self.db_fd, self.log_file_name = tempfile.mkstemp()
        self.app = create_app({"TESTING": True, "LOG_DIRECTORY": "/tmp/test_logs"})
        self.client = self.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.log_file_name)

    @staticmethod
    def create_log_file_with_lines(lines):
        db_fd, log_file_name = tempfile.mkstemp()
        with open(log_file_name, "w") as f:
            for line in lines:
                f.write(f"{line}\n")
        return log_file_name

    def make_request_to_endpoint(self, endpoint, params={}):
        with self.app.test_client() as client:
            return client.get(endpoint, query_string=params)
