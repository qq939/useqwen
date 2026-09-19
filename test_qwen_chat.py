"""TDD 测试：不依赖真实 localhost:1234，用本地 mock 服务验证 LangChain 调用链路。
运行： .venv/bin/python test_qwen_chat.py
"""
import contextlib
import io
import json
import os
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TIMEOUT = 30  # 全局超时（秒）：超过就强制退出，避免测试挂死


def _watchdog():
    time.sleep(TIMEOUT)  # 先睡满超时时间；测试按时结束则本线程随主进程一起退出
    print(f"[FAIL] 测试超时（>{TIMEOUT}s），强制退出", flush=True)
    os._exit(1)


FAKE_REPLY = "Blue is the hue I love the most."
RESPONSE = {
    "id": "chatcmpl-test",
    "object": "chat.completion",
    "created": 0,
    "model": "qwen/qwen3.8-27b",
    "choices": [
        {"index": 0, "message": {"role": "assistant", "content": FAKE_REPLY}, "finish_reason": "stop"}
    ],
    "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
}

captured = {}


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        captured["path"] = self.path
        captured["body"] = json.loads(self.rfile.read(length) or b"{}")
        data = json.dumps(RESPONSE).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


def test_langchain_calls_qwen():
    threading.Thread(target=_watchdog, daemon=True).start()

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)  # 随机端口模拟 localhost:1234
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()

    try:
        import qwen_chat

        qwen_chat.BASE_URL = f"http://127.0.0.1:{port}/v1"  # 把被测代码指向 mock 服务

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            qwen_chat.main()
        out = buf.getvalue()

        assert FAKE_REPLY in out, f"输出里没有模型回复: {out!r}"
        assert captured["path"] == "/v1/chat/completions", captured["path"]
        body = captured["body"]
        assert body["model"] == qwen_chat.MODEL, body["model"]
        assert body["messages"][0] == {"role": "system", "content": qwen_chat.SYSTEM_PROMPT}
        assert body["messages"][1] == {"role": "user", "content": qwen_chat.USER_INPUT}
    finally:
        server.shutdown()

    print("[PASS] LangChain 调用 qwen 链路正确")


if __name__ == "__main__":
    test_langchain_calls_qwen()
    sys.exit(0)
