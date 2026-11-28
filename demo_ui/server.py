"""Local demo adapter. Run from any directory with Python 3.10+."""
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "codebase"))
import agent
import ai
import tracing

LOCK = threading.Lock()
ORIGIN = "http://127.0.0.1:8000"
ASSETS = {"/": ("index.html", "text/html"), "/styles.css": ("styles.css", "text/css"),
          "/app.js": ("app.js", "text/javascript")}


def status():
    mock = ai.MODEL_PROVIDER == "fake"
    ready = mock or (ai.MODEL_PROVIDER == "openrouter"
                     and ai.MODEL_NAME == "baidu/ernie-5.5-flash-preview:free" and bool(ai.API_KEY))
    return {"mode": "mock" if mock else "live", "ready": ready}


def process(text):
    observed = {}
    def observe(decision, order):
        observed.update(decision=decision, order=order)
    tracing.begin("localhost-demo")
    try:
        result = agent.answer(text, on_decision=observe)
    finally:
        summary, events = tracing.end()
    output = result["output"]
    if ai.API_KEY and ai.API_KEY in output:
        raise ValueError("Sensitive response")
    data = {"output": output, "mode": status()["mode"],
            "model": ", ".join(summary["models"]) or None,
            "tokens_in": summary["tokens_in"], "tokens_out": summary["tokens_out"],
            "model_calls": summary["model_calls"], "tool_calls": summary["tool_calls"]}
    # The observer executes before validation. Only expose its values after the
    # backend returns successfully without a guardrail rejection.
    rejected = any(e.get("kind") == "note" and "guardrail:" in e.get("text", "") for e in events)
    if observed and not rejected and not summary["errors"]:
        decision = observed["decision"]
        # A valid proposal can still be rejected by the final per-item limit check.
        if decision["action"] == "propose" and not output.startswith(("Bản nháp AI:", "Bản nháp mock:")):
            return data
        data.update(order_id=observed["order"]["id"], action=decision["action"],
                    item=decision["item"], amount=decision["amount"])
        if decision["action"] == "propose":
            data["approval"] = "Cần nhân viên xác minh và quyết định"
    return data


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def respond(self, status_code, body, content_type="application/json"):
        raw = json.dumps(body, ensure_ascii=False).encode() if content_type == "application/json" else body
        self.send_response(status_code)
        self.send_header("Content-Type", content_type + "; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self'; script-src 'self'; connect-src 'self'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(raw)

    def local_request(self):
        return self.headers.get("Host") == "127.0.0.1:8000"

    def do_GET(self):
        if not self.local_request():
            return self.respond(403, {"error": "Chỉ truy cập qua địa chỉ localhost đã cấu hình."})
        path = urlsplit(self.path).path
        if path == "/api/status":
            return self.respond(200, status())
        if path not in ASSETS:
            return self.respond(404, {"error": "Không tìm thấy."})
        name, mime = ASSETS[path]
        self.respond(200, (ROOT / "demo_ui" / name).read_bytes(), mime)

    def do_POST(self):
        if not self.local_request() or self.headers.get("Origin") != ORIGIN:
            return self.respond(403, {"error": "Nguồn yêu cầu không hợp lệ."})
        if urlsplit(self.path).path != "/api/answer":
            return self.respond(404, {"error": "Không tìm thấy."})
        if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
            return self.respond(415, {"error": "Yêu cầu JSON."})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 20000:
                raise ValueError()
            body = json.loads(self.rfile.read(length))
            text = body.get("text") if isinstance(body, dict) else None
            if not isinstance(text, str) or not text.strip() or len(text) > 2000:
                raise ValueError()
        except (ValueError, UnicodeError):
            return self.respond(400, {"error": "Nhập nội dung từ 1 đến 2.000 ký tự."})
        if not status()["ready"]:
            return self.respond(503, {"error": "Kiểm tra cấu hình OpenRouter ERNIE và API_KEY phía server."})
        if not LOCK.acquire(blocking=False):
            return self.respond(409, {"error": "Hệ thống đang xử lý một yêu cầu. Hãy đợi rồi gửi lại."})
        try:
            try:
                result = process(text.strip())
            except Exception:
                return self.respond(502, {"error": "Xử lý chưa thành công. Kiểm tra kết nối hoặc quota phía server. Chưa thực hiện giao dịch."})
            self.respond(200, result)
        finally:
            LOCK.release()


if __name__ == "__main__":
    print(f"Demo tại {ORIGIN} · {'MOCK MODE' if status()['mode'] == 'mock' else 'LIVE · OpenRouter ERNIE'}")
    ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
