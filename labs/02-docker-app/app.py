import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", "8080"))
APP_ENV = os.getenv("APP_ENV", "development")


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/":
            self._send_json(
                200,
                {
                    "service": "devops-docker-lab",
                    "status": "running",
                    "environment": APP_ENV,
                    "health_endpoint": "/health",
                },
            )
            return

        if self.path == "/health":
            self._send_json(200, {"status": "healthy"})
            return

        self._send_json(404, {"status": "not_found"})

    def log_message(self, format: str, *args) -> None:
        print(f"{self.address_string()} - {format % args}")


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"devops-docker-lab listening on http://{HOST}:{PORT}")
    server.serve_forever()
