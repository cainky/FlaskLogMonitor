import unittest
import os
import tempfile
from pathlib import Path

from flask import Response

from app import create_app
from constants import Config


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
        full_path: The full path to the temporary file.
        log_file_name: The name of the temporary file.

    How to use this class:
        When writing tests for the Flask Log Monitor, extend this class instead
        of unittest.TestCase. This gives your test access to the app, client,
        db_fd, and log_file_name attributes, and ensures your test runs in its
        own isolated context.
    """

    def setUp(self):
        config = Config(testing=True)
        self.app = create_app(config.__dict__)
        self.client = self.app.test_client()
        self.db_fd = None
        self.full_path = None
        self.log_directory = config.LOG_DIRECTORY

    def tearDown(self):
        if self.db_fd:
            os.close(self.db_fd)
        if self.full_path:
            os.unlink(self.full_path)

    def create_log_file_with_lines(self, lines: list[str]) -> str:
        self.db_fd, self.full_path = tempfile.mkstemp(dir=self.log_directory)
        with open(self.full_path, "w") as f:
            for index, line in enumerate(lines):
                if index == len(lines) - 1:
                    f.write(line)
                else:
                    f.write(f"{line}\n")
        self.log_file_name = Path(self.full_path).name
        return self.log_file_name

    def make_request_to_endpoint(self, endpoint: str, params: dict = None) -> Response:
        if params is None:
            params = {}
        with self.app.test_client() as client:
            return client.get(endpoint, query_string=params)
