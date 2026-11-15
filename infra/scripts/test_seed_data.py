import unittest
from unittest.mock import Mock, patch

from azure.core.exceptions import HttpResponseError

import seed_data


class SeedDataTests(unittest.TestCase):
    @patch("seed_data.time.sleep")
    def test_retries_permission_propagation(self, sleep):
        forbidden = HttpResponseError(message="RBAC not propagated")
        forbidden.status_code = 403
        operation = Mock(side_effect=[forbidden, "ready"])

        self.assertEqual(seed_data.retry_operation(operation, "Index"), "ready")
        self.assertEqual(operation.call_count, 2)
        sleep.assert_called_once()

    @patch("seed_data.time.sleep")
    def test_invalid_configuration_fails_without_retry(self, sleep):
        invalid = HttpResponseError(message="Invalid model")
        invalid.status_code = 400
        operation = Mock(side_effect=invalid)

        with self.assertRaises(HttpResponseError):
            seed_data.retry_operation(operation, "Knowledge base")
        operation.assert_called_once()
        sleep.assert_not_called()

    @patch("seed_data.time.monotonic", side_effect=[0, 601])
    def test_permission_retries_are_bounded(self, monotonic):
        forbidden = HttpResponseError(message="Access denied")
        forbidden.status_code = 403
        operation = Mock(side_effect=forbidden)

        with self.assertRaises(HttpResponseError):
            seed_data.retry_operation(operation, "Index")
        operation.assert_called_once()

    def test_partial_upload_failure_is_not_reported_as_success(self):
        client = Mock()
        client.merge_or_upload_documents.return_value = [
            Mock(succeeded=True),
            Mock(succeeded=False, key="page-2", status_code=400, error_message="Bad vector"),
        ]

        with self.assertRaisesRegex(RuntimeError, "page-2: 400 Bad vector"):
            seed_data.upload_documents(client, [{"id": "page-1"}, {"id": "page-2"}])

    @patch("seed_data.HTTPServer")
    @patch("seed_data.seed_data", side_effect=RuntimeError("Seeding failed"))
    @patch("sys.argv", ["seed-data.py", "--serve"])
    def test_failed_seed_never_opens_readiness_port(self, seed, server):
        with self.assertRaisesRegex(RuntimeError, "Seeding failed"):
            seed_data.main()
        server.assert_not_called()


if __name__ == "__main__":
    unittest.main()
