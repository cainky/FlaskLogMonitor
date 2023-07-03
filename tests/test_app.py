from http import HTTPStatus
from .base import LogMonitorTestCase


class TestLogMonitor(LogMonitorTestCase):
    def test_invalid_request_parameters(self):
        response = self.make_request_to_endpoint("/logs", {"filename": "/invalid"})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_file_not_found(self):
        response = self.make_request_to_endpoint("/logs", {"filename": "nonexistent"})
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_valid_request_parameters(self):
        log_file_name = self.create_log_file_with_lines(["test log"])
        response = self.make_request_to_endpoint(
            "/logs", {"filename": log_file_name, "term": "test", "limit": 1}
        )
        json_response = response.get_json()
        lines = json_response.get("lines", [])
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(lines, ["test log"])

    def test_no_matching_lines(self):
        log_file_name = self.create_log_file_with_lines(["test log"])
        response = self.make_request_to_endpoint(
            "/logs", {"filename": log_file_name, "term": "no match"}
        )
        json_response = response.get_json()
        lines = json_response.get("lines", [])
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(lines, [])

    def test_less_lines_than_limit(self):
        log_file_name = self.create_log_file_with_lines(["test log"])
        response = self.make_request_to_endpoint(
            "/logs", {"filename": log_file_name, "limit": 10}
        )
        json_response = response.get_json()
        lines = json_response.get("lines", [])
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(lines, ["test log"])

    def test_more_lines_than_limit(self):
        lines = [f"log {i}" for i in range(10)]
        log_file_name = self.create_log_file_with_lines(lines)
        response = self.make_request_to_endpoint(
            "/logs", {"filename": log_file_name, "limit": 5}
        )
        json_response = response.get_json()
        lines = json_response.get("lines", [])
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(lines, ["log 5", "log 6", "log 7", "log 8", "log 9"])

    def test_default_parameters(self):
        log_file_name = self.create_log_file_with_lines(["test log"])
        response = self.make_request_to_endpoint("/logs", {"filename": log_file_name})
        json_response = response.get_json()
        lines = json_response.get("lines", [])
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(lines, ["test log"])

    def test_long_search_term(self):
        long_term = "a" * 101
        response = self.make_request_to_endpoint("/logs", {"term": long_term})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_invalid_limit(self):
        response = self.make_request_to_endpoint("/logs", {"limit": 0})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        response = self.make_request_to_endpoint("/logs", {"limit": 1001})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

