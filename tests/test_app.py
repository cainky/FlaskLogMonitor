from http import HTTPStatus
from .base import LogMonitorTestCase

TEST_LOG_LINES = ["test log"]
TEST_LOG_ENDPOINT = "/logs"


class TestLogMonitor(LogMonitorTestCase):
    def test_invalid_request_parameters(self):
        response = self.make_request_to_endpoint(
            TEST_LOG_ENDPOINT, {"filename": "/invalid"}
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_file_not_found(self):
        response = self.make_request_to_endpoint(
            TEST_LOG_ENDPOINT, {"filename": "nonexistent"}
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_valid_request_parameters(self):
        self.log_file_name = self.create_log_file_with_lines(TEST_LOG_LINES)
        response = self.make_request_to_endpoint(
            TEST_LOG_ENDPOINT,
            {"filename": self.log_file_name, "term": "test", "limit": 1},
        )
        json_response = response.get_json()
        lines = json_response.get("lines", [])
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(lines, TEST_LOG_LINES)

    def test_no_matching_lines(self):
        self.log_file_name = self.create_log_file_with_lines(TEST_LOG_LINES)
        response = self.make_request_to_endpoint(
            TEST_LOG_ENDPOINT, {"filename": self.log_file_name, "term": "no match"}
        )
        json_response = response.get_json()
        lines = json_response.get("lines", [])
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(lines, [])

    def test_less_lines_than_limit(self):
        self.log_file_name = self.create_log_file_with_lines(TEST_LOG_LINES)
        response = self.make_request_to_endpoint(
            TEST_LOG_ENDPOINT, {"filename": self.log_file_name, "limit": 10}
        )
        json_response = response.get_json()
        lines = json_response.get("lines", [])
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(lines, TEST_LOG_LINES)

    def test_more_lines_than_limit(self):
        lines = [f"log {i}" for i in range(10)]
        self.log_file_name = self.create_log_file_with_lines(lines)
        response = self.make_request_to_endpoint(
            TEST_LOG_ENDPOINT, {"filename": self.log_file_name, "limit": 5}
        )
        json_response = response.get_json()
        lines = json_response.get("lines", [])
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(lines, ["log 5", "log 6", "log 7", "log 8", "log 9"])

    def test_default_parameters(self):
        self.log_file_name = self.create_log_file_with_lines(TEST_LOG_LINES)
        response = self.make_request_to_endpoint(
            TEST_LOG_ENDPOINT, {"filename": self.log_file_name}
        )
        json_response = response.get_json()
        lines = json_response.get("lines", [])
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(lines, TEST_LOG_LINES)

    def test_long_search_term(self):
        long_term = "a" * 101
        response = self.make_request_to_endpoint(TEST_LOG_ENDPOINT, {"term": long_term})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_invalid_limit(self):
        response = self.make_request_to_endpoint(TEST_LOG_ENDPOINT, {"limit": 0})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        response = self.make_request_to_endpoint(TEST_LOG_ENDPOINT, {"limit": 1001})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
