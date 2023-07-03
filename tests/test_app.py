from http import HTTPStatus
from .base import LogMonitorTestCase


class TestLogMonitor(LogMonitorTestCase):
    def test_get_logs(self):
        log_file_name = self.create_log_file_with_lines(["test log"])
        response = self.make_request_to_endpoint("/logs", {"filename": log_file_name})
        json_response = response.get_json()
        lines = json_response.get("lines", [])
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(lines, ["test log"])
