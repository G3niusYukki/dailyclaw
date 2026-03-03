#!/usr/bin/env python3
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import json
import os
import subprocess
import threading
import time

# 可通过环境变量覆盖：
# - OC_MONITOR_ROOT: OpenClaw 工作区根目录（其下应有 monitor/）
# - MONITOR_PORT: 监听端口
DEFAULT_ROOT = Path(__file__).resolve().parents[1]
ROOT = Path(os.getenv('OC_MONITOR_ROOT', str(DEFAULT_ROOT))).expanduser().resolve()
MON = ROOT / 'monitor'
TASKS = MON / 'data/tasks.json'
CODE = MON / 'data/code_changes.json'
REFRESH = MON / 'scripts/refresh_status.py'
PORT = int(os.getenv('MONITOR_PORT', '8793'))

# 全局刷新节流：避免每个 SSE 客户端都单独触发 refresh_status.py
_REFRESH_LOCK = threading.Lock()
_LAST_REFRESH_AT = 0.0
_LAST_REFRESH_ERR: str | None = None
_CONSECUTIVE_REFRESH_FAILS = 0

REFRESH_INTERVAL_OK = 5.0
REFRESH_INTERVAL_FAIL_MIN = 8.0
REFRESH_INTERVAL_FAIL_MAX = 30.0
SSE_LOOP_INTERVAL = 0.5
SSE_KEEPALIVE_INTERVAL = 15.0
SSE_PUSH_MIN_INTERVAL = 1.5


def _refresh_backoff_seconds() -> float:
    if _CONSECUTIVE_REFRESH_FAILS <= 0:
        return REFRESH_INTERVAL_OK
    # 失败后指数退避（上限 30s），降低抖动和资源占用
    return min(REFRESH_INTERVAL_FAIL_MAX, REFRESH_INTERVAL_FAIL_MIN * (2 ** (_CONSECUTIVE_REFRESH_FAILS - 1)))


def maybe_run_refresh(now: float) -> None:
    global _LAST_REFRESH_AT, _LAST_REFRESH_ERR, _CONSECUTIVE_REFRESH_FAILS

    min_interval = _refresh_backoff_seconds()
    if now - _LAST_REFRESH_AT < min_interval:
        return

    # 仅允许一个请求线程执行 refresh，其他线程直接跳过
    acquired = _REFRESH_LOCK.acquire(blocking=False)
    if not acquired:
        return

    try:
        now2 = time.time()
        min_interval = _refresh_backoff_seconds()
        if now2 - _LAST_REFRESH_AT < min_interval:
            return

        p = subprocess.run(
            ['python3', str(REFRESH)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            timeout=12,
            check=False,
            text=True,
        )
        _LAST_REFRESH_AT = time.time()
        if p.returncode == 0:
            _CONSECUTIVE_REFRESH_FAILS = 0
            _LAST_REFRESH_ERR = None
        else:
            _CONSECUTIVE_REFRESH_FAILS += 1
            _LAST_REFRESH_ERR = (p.stderr or '').strip()[:200]
    except Exception as e:
        _LAST_REFRESH_AT = time.time()
        _CONSECUTIVE_REFRESH_FAILS += 1
        _LAST_REFRESH_ERR = str(e)[:200]
    finally:
        _REFRESH_LOCK.release()


class H(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        rel = path.split('?', 1)[0].split('#', 1)[0]
        return str((ROOT / rel.lstrip('/')).resolve())

    def do_GET(self):
        if self.path.startswith('/monitor/stream'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.end_headers()

            last_sig = None
            last_ping = 0.0
            last_push = 0.0
            last_err_sent = None

            while True:
                try:
                    now = time.time()
                    maybe_run_refresh(now)

                    tasks_mtime = TASKS.stat().st_mtime if TASKS.exists() else 0
                    code_mtime = CODE.stat().st_mtime if CODE.exists() else 0
                    sig = f"{tasks_mtime:.6f}|{code_mtime:.6f}"

                    # 推送节流：变化频繁时，至少间隔 SSE_PUSH_MIN_INTERVAL 再发，减少前端重绘抖动
                    if sig != last_sig and (now - last_push >= SSE_PUSH_MIN_INTERVAL or last_sig is None):
                        payload = {
                            'tasks_mtime': tasks_mtime,
                            'code_mtime': code_mtime,
                            'ts': time.time(),
                        }
                        self.wfile.write(f"data: {json.dumps(payload)}\n\n".encode())
                        self.wfile.flush()
                        last_sig = sig
                        last_push = now

                    # 刷新异常可见化：每次错误内容变化才通知一次，防止刷屏
                    if _LAST_REFRESH_ERR and _LAST_REFRESH_ERR != last_err_sent:
                        err_payload = {
                            'type': 'refresh_error',
                            'message': _LAST_REFRESH_ERR,
                            'fails': _CONSECUTIVE_REFRESH_FAILS,
                            'ts': time.time(),
                        }
                        self.wfile.write(f"event: refresh_error\ndata: {json.dumps(err_payload)}\n\n".encode())
                        self.wfile.flush()
                        last_err_sent = _LAST_REFRESH_ERR

                    if now - last_ping >= SSE_KEEPALIVE_INTERVAL:
                        self.wfile.write(b": keepalive\n\n")
                        self.wfile.flush()
                        last_ping = now

                    time.sleep(SSE_LOOP_INTERVAL)
                except (BrokenPipeError, ConnectionResetError, TimeoutError):
                    return
                except Exception:
                    # 单次循环异常自恢复，避免整个连接因偶发错误中断
                    time.sleep(1)
        else:
            super().do_GET()


if __name__ == '__main__':
    httpd = ThreadingHTTPServer(('127.0.0.1', PORT), H)
    print(f'monitor realtime server on http://127.0.0.1:{PORT}')
    httpd.serve_forever()
