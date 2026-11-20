"""No-network validation tests. These tests never publish or call APIs."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from scripts.prepare_request import prepare, validate_url, write_github_env


class RequestValidationTests(unittest.TestCase):
    def test_valid_manual_request(self):
        values = prepare({"EVENT_NAME": "workflow_dispatch", "MANUAL_URL": "https://www.youtube.com/watch?v=abcd", "MANUAL_CAPTION": "test"})
        self.assertEqual(values["DRY_RUN"], "false")
        self.assertEqual(values["VIDEO_URL"], "https://www.youtube.com/watch?v=abcd")

    def test_explicit_dry_run(self):
        values = prepare({"EVENT_NAME": "workflow_dispatch", "MANUAL_URL": "https://youtu.be/xyz", "MANUAL_DRY_RUN": "true"})
        self.assertEqual(values["DRY_RUN"], "true")

    def test_dispatch_cannot_switch_to_dry_run(self):
        values = prepare({"EVENT_NAME": "repository_dispatch", "DISPATCH_URL": "https://video.example.org/v", "MANUAL_DRY_RUN": "true", "DISPATCH_CHAT_ID": "-1001234567890"})
        self.assertEqual(values["DRY_RUN"], "false")

    def test_https_required(self):
        for url in ["http://example.com/video", "file:///etc/passwd", "ftp://example.com/file", "", "javascript:alert(1)"]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                validate_url(url)

    def test_local_targets_rejected(self):
        for url in ["https://127.0.0.1/video", "https://10.1.2.3/x", "https://192.168.0.1/x", "https://localhost/x", "https://metadata.internal/x", "https://127.1/x", "https://2130706433/x", "https://[::1]/x"]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                validate_url(url)

    def test_url_injection_rejected(self):
        for url in ["https://example.org/v\nBAD=1", "https://example.org/v\rBAD=1", "https://example.org/v with space", "https://alice:password@example.com/v", "https://example.com:8443/v"]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                validate_url(url)

    def test_multiline_caption_env_encoding(self):
        values = prepare({"EVENT_NAME": "workflow_dispatch", "MANUAL_URL": "https://example.org/v", "MANUAL_CAPTION": "line 1\nline 2"})
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / "env"
            write_github_env(target, values)
            data = target.read_text(encoding="utf-8")
            self.assertIn("CAPTION<<CAPTION_", data)
            self.assertIn("line 1\nline 2\n", data)
            self.assertNotIn("CAPTION=line 1\nline 2", data)

    def test_reject_bad_telegram_ids(self):
        with self.assertRaises(ValueError):
            prepare({"EVENT_NAME":"repository_dispatch", "DISPATCH_URL":"https://example.org/v", "DISPATCH_CHAT_ID":"-1\nSNEAKY=1"})
        with self.assertRaises(ValueError):
            prepare({"EVENT_NAME":"repository_dispatch", "DISPATCH_URL":"https://example.org/v", "DISPATCH_STATUS_MESSAGE_ID":"not-a-number"})

    def test_caption_limit(self):
        with self.assertRaises(ValueError):
            prepare({"EVENT_NAME":"workflow_dispatch", "MANUAL_URL":"https://example.org/v", "MANUAL_CAPTION":"x"*2201})

    def test_allowlist(self):
        with patch.dict(os.environ,{"ALLOWED_SOURCE_HOSTS":"youtube.com,youtu.be"}):
            self.assertEqual(validate_url("https://m.youtube.com/watch?v=1"),"https://m.youtube.com/watch?v=1")
            with self.assertRaises(ValueError):
                validate_url("https://youtube.com.attacker.invalid-domain.example/v")

    def test_unsupported_event(self):
        with self.assertRaises(ValueError):
            prepare({"EVENT_NAME": "pull_request", "MANUAL_URL": "https://example.org/v"})


if __name__ == "__main__":
    unittest.main()
