"""Offline regression checks for the Gitea API client's output and URL boundaries."""
import http.server
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import unittest

CLIENT = Path(__file__).with_name("gitea_api.py")
SECRET = "sensitive-example-value"


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/v1/redirect":
            self.send_response(302)
            self.send_header("Location", "http://other.example/")
            self.end_headers()
            return
        body = json.dumps({
            "id": 7, "index": 3, "state": "open", "private": True,
            "authorization": SECRET, "client_secret": SECRET,
            "clone_url": "https://user:" + SECRET + "@example.invalid/repo",
            "nested": {"api_key": SECRET}, "body": SECRET,
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


class ClientTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
        cls.worker = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.worker.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.worker.join()

    def call(self, endpoint):
        env = dict(os.environ, GITEA_URL=f"http://127.0.0.1:{self.server.server_port}", GITEA_TOKEN="test-token")
        return subprocess.run([sys.executable, str(CLIENT), "GET", endpoint], env=env, text=True, capture_output=True)

    def test_metadata_only(self):
        result = self.call("/repos/owner/repo")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {
            "http_status": 200, "metadata": {"id": 7, "index": 3, "private": True, "state": "open"},
        })
        self.assertNotIn(SECRET, result.stdout + result.stderr)

    def test_redirect_refused(self):
        result = self.call("/redirect")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn(SECRET, result.stdout + result.stderr)

    def test_admin_and_token_endpoints_refused(self):
        for endpoint in ("/admin", "/admin/users", "/users/me/tokens", "/%61dmin"):
            with self.subTest(endpoint=endpoint):
                result = self.call(endpoint)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("outside this client's scope", result.stderr)

    def test_path_traversal_refused(self):
        for endpoint in ("/../admin", "//other.example/path", "/%2e%2e/admin"):
            with self.subTest(endpoint=endpoint):
                self.assertNotEqual(self.call(endpoint).returncode, 0)


if __name__ == "__main__":
    unittest.main()
