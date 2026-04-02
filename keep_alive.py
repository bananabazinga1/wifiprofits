"""
keep_alive.py

Starts a minimal HTTP health-check server in a background daemon thread.
Required on Replit to prevent the process from being killed due to inactivity.
Responds to any request with 200 OK so Replit's uptime monitor sees the app as alive.

Uses only Python stdlib — no extra dependencies.
"""

import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

logger = logging.getLogger(__name__)

_PORT = 8080


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"alive")

    def log_message(self, format, *args):
        # Suppress the default per-request stderr logging.
        pass


def keep_alive() -> None:
    """Start the health-check HTTP server in a background daemon thread."""
    server = HTTPServer(("0.0.0.0", _PORT), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    logger.info("Keep-alive server running on port %d", _PORT)
