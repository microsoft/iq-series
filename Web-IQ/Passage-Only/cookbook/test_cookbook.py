import ast
import contextlib
import io
import json
import os
import random
import unittest
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import MagicMock, Mock, patch


NOTEBOOK = Path(__file__).with_name("web-iq-passage-only-cookbook.ipynb")
CELLS = json.loads(NOTEBOOK.read_text(encoding="utf-8"))["cells"]
CODE = ["".join(cell["source"]) for cell in CELLS if cell["cell_type"] == "code"]


def cell_containing(text):
    return next(source for source in CODE if text in source)


def response(status, body, headers=None):
    return SimpleNamespace(status_code=status, headers=headers or {}, json=Mock(return_value=body))


def load_definitions(source, namespace):
    parsed = ast.parse(source)
    definitions = [
        node for node in parsed.body
        if isinstance(node, (ast.FunctionDef, ast.ClassDef))
    ]
    exec(compile(ast.Module(body=definitions, type_ignores=[]), str(NOTEBOOK), "exec"), namespace)


class PassageOnlyCookbookTests(unittest.TestCase):
    def setUp(self):
        self.namespace = {
            "session": Mock(),
            "WEBIQ_BASE_URL": "https://example.invalid/v3",
            "time": SimpleNamespace(sleep=Mock()),
            "random": random,
            "datetime": datetime,
            "timezone": timezone,
            "parsedate_to_datetime": parsedate_to_datetime,
        }
        load_definitions(cell_containing("class WebIQError"), self.namespace)

    def run_notebook(self, media=True):
        session = Mock()
        passage = "Evidence preserved in the complete prompt. " * 40 + "END_OF_EVIDENCE"

        def post(url, **kwargs):
            if url.endswith("/search/web"):
                body = {"webResults": [{"title": "Tree research", "url": "https://example.invalid/trees", "content": passage}]}
            elif url.endswith("/search/images"):
                body = {"imageResults": [{"title": "Tree photo", "url": "https://example.invalid/tree.jpg", "hostPageUrl": "https://example.invalid/photo"}] if media else []}
            elif url.endswith("/search/videos"):
                body = {"videoResults": [{"title": "Tree explainer", "url": "https://example.invalid/video", "viewCount": None}] if media else []}
            else:
                self.fail(f"Unexpected endpoint: {url}")
            return response(200, body)

        session.post.side_effect = post
        requests_module = ModuleType("requests")
        requests_module.Session = Mock(return_value=session)
        dotenv_module = ModuleType("dotenv")
        dotenv_module.load_dotenv = Mock()
        output = io.StringIO()
        namespace = {}
        with patch.dict("sys.modules", {"requests": requests_module, "dotenv": dotenv_module}), patch.dict(
            os.environ,
            {
                "WEBIQ_API_KEY": "test-key-not-a-credential",
                "WEBIQ_BASE_URL": "https://example.invalid/v3",
                "FOUNDRY_PROJECT_ENDPOINT": "",
                "FOUNDRY_MODEL_DEPLOYMENT_NAME": "",
            },
        ), contextlib.redirect_stdout(output):
            for source in CODE:
                if not source.startswith("%pip"):
                    exec(compile(source, str(NOTEBOOK), "exec"), namespace)
        return namespace, session, output.getvalue()

    def test_notebook_runs_with_native_media_and_complete_fallback_prompt(self):
        namespace, session, output = self.run_notebook()
        self.assertEqual(session.post.call_count, 6)
        self.assertEqual(len(namespace["sources"]), 3)
        self.assertIn(namespace["grounded_input"], output)
        self.assertIn("END_OF_EVIDENCE", output)
        self.assertIn(f"Question: {namespace['question']}", output)
        self.assertEqual(namespace["sources"][1]["url"], "https://example.invalid/photo")
        for call in session.post.call_args_list:
            payload = call.kwargs["json"]
            if call.args[0].endswith("/search/web"):
                self.assertEqual(payload["contentFormat"], "passage")
            else:
                self.assertNotIn("contentFormat", payload)
        self.assertFalse(session.get.called)

    def test_notebook_handles_empty_media_results_without_losing_web_grounding(self):
        namespace, _, output = self.run_notebook(media=False)
        self.assertEqual(len(namespace["sources"]), 1)
        self.assertIn("No images.", output)
        self.assertIn("No videos.", output)
        self.assertIn(namespace["grounded_input"], output)

    def test_retry_honors_body_or_header_delay(self):
        for body, headers in [
            ({"retryAfter": "2s"}, {}),
            ({}, {"Retry-After": "2"}),
            ({}, {"Retry-After": "Wed, 21 Oct 2026 12:00:02 GMT"}),
        ]:
            with self.subTest(body=body, headers=headers):
                self.setUp()
                self.namespace["datetime"] = Mock()
                self.namespace["datetime"].now.return_value = datetime(2026, 10, 21, 12, tzinfo=timezone.utc)
                self.namespace["session"].post.side_effect = [
                    response(429, {"errorCode": "AuthUserThrottled", **body}, headers),
                    response(200, {"webResults": []}),
                ]
                with contextlib.redirect_stdout(io.StringIO()):
                    result = self.namespace["web_post"](
                        "/search/web", {"query": "trees", "contentFormat": "passage"},
                    )
                self.assertEqual(result, {"webResults": []})
                self.namespace["time"].sleep.assert_called_once_with(2)

    def test_daily_cap_and_permission_failures_are_not_retried(self):
        for status, error_code in [(429, "AuthUserDailyUsageExceeded"), (403, "AuthUnauthorizedService")]:
            with self.subTest(status=status):
                self.setUp()
                self.namespace["session"].post.return_value = response(status, {"errorCode": error_code, "traceId": "test-trace"})
                with self.assertRaises(self.namespace["WebIQError"]) as error:
                    self.namespace["web_post"](
                        "/search/web", {"query": "trees", "contentFormat": "passage"},
                    )
                self.assertIn("test-trace", str(error.exception))
                self.namespace["session"].post.assert_called_once()
                self.namespace["time"].sleep.assert_not_called()

    def test_server_failure_is_bounded_and_remains_an_error(self):
        self.namespace["session"].post.return_value = response(503, {"errorCode": "InternalServerError"})
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(self.namespace["WebIQError"]):
            self.namespace["web_post"](
                "/search/web", {"query": "trees", "contentFormat": "passage"},
            )
        self.assertEqual(self.namespace["session"].post.call_count, 4)
        self.assertEqual(self.namespace["time"].sleep.call_count, 3)

    def test_non_json_server_failure_can_retry_but_bad_success_cannot(self):
        bad_response = response(503, None)
        bad_response.json.side_effect = ValueError("not JSON")
        self.namespace["session"].post.side_effect = [bad_response, response(200, {"webResults": []})]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(
                self.namespace["web_post"]("/search/web", {"query": "trees", "contentFormat": "passage"}),
                {"webResults": []},
            )
        self.setUp()
        bad_response.status_code = 200
        self.namespace["session"].post.return_value = bad_response
        with self.assertRaisesRegex(ValueError, "not JSON"):
            self.namespace["web_post"](
                "/search/web", {"query": "trees", "contentFormat": "passage"},
            )

    def test_video_moment_requires_an_in_range_index_and_url(self):
        load_definitions(cell_containing("def video_source_url"), self.namespace)
        main_url = "https://example.invalid/video"
        for extra, expected in [
            ({}, main_url),
            ({"moments": None}, main_url),
            ({"moments": [{"momentUrl": "https://example.invalid/moment"}], "bestMomentIndex": -1}, main_url),
            ({"moments": [{}], "bestMomentIndex": 0}, main_url),
            ({"moments": [{}], "bestMomentIndex": 1}, main_url),
            ({"moments": [{"momentUrl": "https://example.invalid/moment"}], "bestMomentIndex": 0}, "https://example.invalid/moment"),
        ]:
            with self.subTest(extra=extra):
                self.assertEqual(self.namespace["video_source_url"]({"url": main_url, **extra}), expected)

    def test_optional_foundry_receives_complete_input_and_surfaces_model_errors(self):
        namespace, _, _ = self.run_notebook()
        identity = ModuleType("azure.identity")
        identity.DefaultAzureCredential = MagicMock()
        projects = ModuleType("azure.ai.projects")
        projects.AIProjectClient = MagicMock()
        project = projects.AIProjectClient.return_value.__enter__.return_value
        model = project.get_openai_client.return_value.__enter__.return_value
        model.responses.create.return_value.output_text = "A grounded answer [1]."
        modules = {"azure.identity": identity, "azure.ai.projects": projects}
        environment = {
            "FOUNDRY_PROJECT_ENDPOINT": "https://example.invalid/api/projects/test",
            "FOUNDRY_MODEL_DEPLOYMENT_NAME": "test-deployment",
        }
        with patch.dict("sys.modules", modules), patch.dict(os.environ, environment), contextlib.redirect_stdout(io.StringIO()):
            exec(cell_containing("answer_text = None"), namespace)
            self.assertEqual(namespace["answer_text"], "A grounded answer [1].")
            model.responses.create.assert_called_once_with(
                model="test-deployment",
                instructions=namespace["instructions"],
                input=namespace["grounded_input"],
            )
            model.responses.create.side_effect = RuntimeError("model unavailable")
            with self.assertRaisesRegex(RuntimeError, "model unavailable"):
                exec(cell_containing("answer_text = None"), namespace)

    def test_citation_events_use_each_original_response_and_validate_ids(self):
        namespace, session, _ = self.run_notebook()
        for name in ("web", "images", "videos"):
            namespace[name]["instrumentationCitationBase"] = f"https://example.invalid/{name}?DATA="
        for _, result in namespace["source_results"]:
            result["instrumentationSuffix"] = "Test,1000"
        namespace["answer_text"] = "Trees cool streets [1]. Image [2]. Video [3]."
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(cell_containing("def citation_ping_url"), namespace)
        for name in ("web", "images", "videos"):
            self.assertIn(f"https://example.invalid/{name}?DATA=", output.getvalue())
        self.assertFalse(session.get.called)
        namespace["answer_text"] = "Unsupported citation [999]."
        with self.assertRaisesRegex(ValueError, "source ID that does not exist"):
            exec(cell_containing("def citation_ping_url"), namespace)


if __name__ == "__main__":
    unittest.main()
