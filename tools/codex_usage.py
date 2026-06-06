#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import glob
import json
import os
import sys
import time
from datetime import datetime, timezone, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from urllib import error, request

# =========================
# 配置
# =========================

SESSIONS_DIR = os.path.expanduser("~/.codex/sessions")
HOST = "0.0.0.0"
PORT = 8765
MAX_FILES_TO_SCAN = 300

# 固定显示为 UTC+8，台北 / 北京 / 中国时区
DISPLAY_TZ = timezone(timedelta(hours=8))
DEVICE_API_PATH = "/api/claude_usage"


# =========================
# 时间工具
# =========================

def now_ts():
    return int(datetime.now(timezone.utc).timestamp())


def unix_to_local_text(ts):
    if not ts:
        return None
    try:
        return datetime.fromtimestamp(int(ts), DISPLAY_TZ).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return None


def unix_to_hhmm(ts):
    if not ts:
        return None
    try:
        return datetime.fromtimestamp(int(ts), DISPLAY_TZ).strftime("%H:%M")
    except Exception:
        return None


def iso_to_local_text(iso_text):
    if not iso_text:
        return None
    try:
        dt = datetime.fromisoformat(iso_text.replace("Z", "+00:00"))
        return dt.astimezone(DISPLAY_TZ).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return iso_text


def reset_remaining_seconds(ts):
    if not ts:
        return None
    try:
        remain = int(ts) - now_ts()
        return max(0, remain)
    except Exception:
        return None


def seconds_to_human(seconds):
    try:
        seconds = int(seconds)
    except Exception:
        return None

    if seconds <= 0:
        return "00:00"

    days = seconds // 86400
    seconds %= 86400

    hours = seconds // 3600
    seconds %= 3600

    minutes = seconds // 60
    secs = seconds % 60

    if days > 0:
        return f"{days}d {hours}h {minutes}m"

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}"

    return f"{minutes:02d}:{secs:02d}"


def seconds_to_short(seconds):
    try:
        seconds = int(seconds)
    except Exception:
        return None

    if seconds <= 0:
        return "0m"

    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60

    if days > 0:
        return f"{days}d {hours}h"
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


# =========================
# 数据工具
# =========================

def safe_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return default


def safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def get_mood(percent):
    if percent < 40:
        return "happy"
    if percent < 75:
        return "busy"
    if percent < 95:
        return "tired"
    return "panic"


def get_color(percent):
    if percent < 40:
        return "#22c55e"
    if percent < 75:
        return "#f59e0b"
    if percent < 95:
        return "#f97316"
    return "#ef4444"


def list_session_files():
    pattern = os.path.join(SESSIONS_DIR, "**", "*.jsonl")
    files = glob.glob(pattern, recursive=True)
    files.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return files[:MAX_FILES_TO_SCAN]


def extract_token_count_from_file(file_path):
    results = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                if '"token_count"' not in line:
                    continue

                line = line.strip()
                if not line:
                    continue

                try:
                    obj = json.loads(line)
                except Exception:
                    continue

                payload = obj.get("payload", {})
                if payload.get("type") != "token_count":
                    continue

                obj["_source_file"] = file_path
                obj["_source_line"] = line_no
                results.append(obj)

    except Exception:
        pass

    return results


def find_latest_token_count():
    latest = None
    latest_ts = ""

    for file_path in list_session_files():
        for item in extract_token_count_from_file(file_path):
            ts = item.get("timestamp") or ""
            if ts > latest_ts:
                latest_ts = ts
                latest = item

    return latest


def find_recent_token_counts(limit=20):
    items = []

    for file_path in list_session_files():
        items.extend(extract_token_count_from_file(file_path))

    items.sort(key=lambda x: x.get("timestamp") or "", reverse=True)
    return items[:limit]


def normalize_usage(item):
    payload = item.get("payload", {})
    info = payload.get("info", {})
    limits = payload.get("rate_limits", {})

    primary = limits.get("primary") or {}
    secondary = limits.get("secondary") or {}

    total_usage = info.get("total_token_usage") or {}
    last_usage = info.get("last_token_usage") or {}

    p5h = safe_float(primary.get("used_percent"))
    pw = safe_float(secondary.get("used_percent"))

    primary_reset = primary.get("resets_at")
    secondary_reset = secondary.get("resets_at")

    primary_remaining = reset_remaining_seconds(primary_reset)
    secondary_remaining = reset_remaining_seconds(secondary_reset)

    return {
        "ok": True,

        "timestamp": item.get("timestamp"),
        "timestamp_local": iso_to_local_text(item.get("timestamp")),

        "source": {
            "file": item.get("_source_file"),
            "line": item.get("_source_line"),
        },

        "plan": {
            "type": limits.get("plan_type"),
            "limit_id": limits.get("limit_id"),
            "limit_name": limits.get("limit_name"),
            "rate_limit_reached_type": limits.get("rate_limit_reached_type"),
            "credits": limits.get("credits"),
        },

        "five_hour": {
            "used_percent": p5h,
            "window_minutes": primary.get("window_minutes"),
            "resets_at": primary_reset,
            "resets_at_local": unix_to_local_text(primary_reset),
            "resets_at_hhmm": unix_to_hhmm(primary_reset),
            "remaining_seconds": primary_remaining,
            "remaining_text": seconds_to_human(primary_remaining),
            "remaining_short": seconds_to_short(primary_remaining),
        },

        "weekly": {
            "used_percent": pw,
            "window_minutes": secondary.get("window_minutes"),
            "resets_at": secondary_reset,
            "resets_at_local": unix_to_local_text(secondary_reset),
            "resets_at_hhmm": unix_to_hhmm(secondary_reset),
            "remaining_seconds": secondary_remaining,
            "remaining_text": seconds_to_human(secondary_remaining),
            "remaining_short": seconds_to_short(secondary_remaining),
        },

        "tokens": {
            "total": {
                "input_tokens": safe_int(total_usage.get("input_tokens")),
                "cached_input_tokens": safe_int(total_usage.get("cached_input_tokens")),
                "output_tokens": safe_int(total_usage.get("output_tokens")),
                "reasoning_output_tokens": safe_int(total_usage.get("reasoning_output_tokens")),
                "total_tokens": safe_int(total_usage.get("total_tokens")),
            },
            "last": {
                "input_tokens": safe_int(last_usage.get("input_tokens")),
                "cached_input_tokens": safe_int(last_usage.get("cached_input_tokens")),
                "output_tokens": safe_int(last_usage.get("output_tokens")),
                "reasoning_output_tokens": safe_int(last_usage.get("reasoning_output_tokens")),
                "total_tokens": safe_int(last_usage.get("total_tokens")),
            },
            "model_context_window": info.get("model_context_window"),
        },

        "pet": {
            "mood": get_mood(p5h),
            "color": get_color(p5h),
        },

        "raw": item,
    }


def get_usage_data():
    item = find_latest_token_count()

    if not item:
        return {
            "ok": False,
            "error": "No token_count found",
            "sessions_dir": SESSIONS_DIR,
        }

    return normalize_usage(item)


def get_simple_data():
    data = get_usage_data()

    if not data.get("ok"):
        return data

    return {
        "ok": True,

        # 主要给 ESP32 显示：剩余时间
        "remain5h": data["five_hour"]["remaining_text"],
        "remain5h_short": data["five_hour"]["remaining_short"],
        "remain5h_sec": data["five_hour"]["remaining_seconds"],

        "remainw": data["weekly"]["remaining_text"],
        "remainw_short": data["weekly"]["remaining_short"],
        "remainw_sec": data["weekly"]["remaining_seconds"],

        # reset 时间
        "reset5h": data["five_hour"]["resets_at_hhmm"],
        "resetw": data["weekly"]["resets_at_hhmm"],

        # 状态
        "plan": data["plan"]["type"],
        "mood": data["pet"]["mood"],
        "color": data["pet"]["color"],

        # 仍保留已用百分比，但页面不主显示
        "p5h": round(data["five_hour"]["used_percent"], 1),
        "pw": round(data["weekly"]["used_percent"], 1),

        # token
        "total_tokens": data["tokens"]["total"]["total_tokens"],
        "last_tokens": data["tokens"]["last"]["total_tokens"],

        "ts": data["timestamp_local"],
    }


def build_device_payload():
    data = get_simple_data()
    if not data.get("ok"):
        return {
            "ok": False,
            "s": 0,
            "sr": 0,
            "w": 0,
            "wr": 0,
            "st": "no_data",
            "src": "codex",
        }

    return {
        "ok": True,
        "s": max(0, min(100, int(round(safe_float(data.get("p5h")))))),
        "sr": max(0, int(round(safe_float(data.get("remain5h_sec")) / 60.0))),
        "w": max(0, min(100, int(round(safe_float(data.get("pw")))))),
        "wr": max(0, int(round(safe_float(data.get("remainw_sec")) / 60.0))),
        "st": f'{data.get("plan") or "unknown"}:{data.get("mood") or "unknown"}',
        "src": "codex",
    }


# =========================
# HTTP 响应
# =========================

def json_response(handler, data, status=200):
    body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def html_response(handler, html, status=200):
    body = html.encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "text/html; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def post_device_payload(device_url, payload):
    api = device_url.rstrip("/") + DEVICE_API_PATH
    body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    req = request.Request(
        api,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "User-Agent": "codex-usage-pusher/0.1",
        },
    )

    with request.urlopen(req, timeout=10) as resp:
        resp_body = resp.read().decode("utf-8", errors="replace")
        return resp.status, resp_body


def normalize_device_url(device_target):
    if not device_target:
        return ""

    target = str(device_target).strip()
    if not target:
        return ""

    if "://" in target:
        return target.rstrip("/")

    return "http://" + target.strip("/")


# =========================
# 页面
# =========================

def render_index():
    data = get_usage_data()

    if not data.get("ok"):
        return f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Codex Remaining</title>
<style>
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: #0f172a;
    color: #e5e7eb;
    padding: 40px;
}}
.card {{
    max-width: 760px;
    margin: auto;
    background: #111827;
    border: 1px solid #334155;
    border-radius: 20px;
    padding: 28px;
}}
code {{
    background: #020617;
    padding: 2px 6px;
    border-radius: 6px;
}}
</style>
</head>
<body>
<div class="card">
<h1>Codex Remaining</h1>
<p>没有找到 token_count 数据。</p>
<p>扫描目录：<code>{SESSIONS_DIR}</code></p>
<p>先在 VS Code / Codex 里对话一次，然后刷新。</p>
</div>
</body>
</html>
"""

    p5h = data["five_hour"]["used_percent"]
    pw = data["weekly"]["used_percent"]

    color = data["pet"]["color"]
    mood = data["pet"]["mood"]
    plan = str(data["plan"]["type"] or "").upper()

    remain5h = data["five_hour"]["remaining_text"]
    remain5h_short = data["five_hour"]["remaining_short"]
    reset5h = data["five_hour"]["resets_at_hhmm"]

    remainw = data["weekly"]["remaining_text"]
    remainw_short = data["weekly"]["remaining_short"]
    resetw = data["weekly"]["resets_at_hhmm"]

    normalized = json.dumps(
        {k: v for k, v in data.items() if k != "raw"},
        ensure_ascii=False,
        indent=2,
    )

    return f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Codex Remaining Monitor</title>
<style>
:root {{
    --bg: #0f172a;
    --card: #111827;
    --muted: #94a3b8;
    --text: #e5e7eb;
    --line: #334155;
    --accent: {color};
}}

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background:
        radial-gradient(circle at top left, rgba(59,130,246,.18), transparent 30%),
        radial-gradient(circle at bottom right, rgba(34,197,94,.12), transparent 32%),
        var(--bg);
    color: var(--text);
    padding: 32px;
}}

.wrap {{
    max-width: 980px;
    margin: 0 auto;
}}

.header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 20px;
    margin-bottom: 22px;
}}

h1 {{
    margin: 0;
    font-size: 32px;
    letter-spacing: -0.04em;
}}

.sub {{
    color: var(--muted);
    margin-top: 6px;
    font-size: 14px;
}}

.badge {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    border: 1px solid var(--line);
    background: rgba(15,23,42,.7);
    border-radius: 999px;
    padding: 8px 14px;
    color: var(--text);
    font-size: 14px;
}}

.dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 18px var(--accent);
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px;
}}

.card {{
    background: rgba(17,24,39,.86);
    border: 1px solid var(--line);
    border-radius: 22px;
    padding: 24px;
    box-shadow: 0 18px 60px rgba(0,0,0,.22);
}}

.label {{
    color: var(--muted);
    font-size: 14px;
}}

.big {{
    font-size: 64px;
    line-height: 1;
    font-weight: 850;
    letter-spacing: -0.06em;
    margin: 14px 0 18px;
}}

.small-note {{
    color: var(--muted);
    font-size: 13px;
    margin-top: 8px;
}}

.meta {{
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
    margin-top: 16px;
}}

.meta div {{
    background: rgba(2,6,23,.5);
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 12px;
}}

.meta span {{
    display: block;
    color: var(--muted);
    font-size: 12px;
    margin-bottom: 4px;
}}

.meta b {{
    font-size: 14px;
}}

.full {{
    grid-column: 1 / -1;
}}

pre {{
    white-space: pre-wrap;
    word-break: break-word;
    background: #020617;
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 16px;
    color: #cbd5e1;
    font-size: 12px;
    max-height: 420px;
    overflow: auto;
}}

a {{
    color: #93c5fd;
    text-decoration: none;
}}

.links {{
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 14px;
}}

.links a {{
    border: 1px solid var(--line);
    border-radius: 999px;
    padding: 8px 12px;
    background: rgba(2,6,23,.45);
    font-size: 13px;
}}

.kv {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
    margin-top: 16px;
}}

.kv div {{
    background: rgba(2,6,23,.5);
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 12px;
}}

.kv span {{
    display: block;
    color: var(--muted);
    font-size: 12px;
    margin-bottom: 4px;
}}

.kv b {{
    font-size: 14px;
}}

@media (max-width: 720px) {{
    body {{
        padding: 18px;
    }}

    .grid {{
        grid-template-columns: 1fr;
    }}

    .header {{
        flex-direction: column;
    }}

    .big {{
        font-size: 52px;
    }}

    .kv {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }}
}}
</style>
<script>
setTimeout(function() {{
    location.reload();
}}, 10000);
</script>
</head>

<body>
<div class="wrap">
    <div class="header">
        <div>
            <h1>Codex Remaining Monitor</h1>
            <div class="sub">Last update: {data["timestamp_local"]} · Auto refresh every 10s · UTC+8</div>
        </div>

        <div class="badge">
            <span class="dot"></span>
            <span>{mood.upper()} · {plan}</span>
        </div>
    </div>

    <div class="grid">
        <div class="card">
            <div class="label">5-hour window remaining</div>
            <div class="big">{remain5h}</div>
            <div class="small-note">Reset at {reset5h} · Short: {remain5h_short}</div>

            <div class="meta">
                <div>
                    <span>Window</span>
                    <b>{data["five_hour"]["window_minutes"]} min</b>
                </div>
                <div>
                    <span>Reset Time</span>
                    <b>{data["five_hour"]["resets_at_local"]}</b>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="label">Weekly window remaining</div>
            <div class="big">{remainw}</div>
            <div class="small-note">Reset at {resetw} · Short: {remainw_short}</div>

            <div class="meta">
                <div>
                    <span>Window</span>
                    <b>{data["weekly"]["window_minutes"]} min</b>
                </div>
                <div>
                    <span>Reset Time</span>
                    <b>{data["weekly"]["resets_at_local"]}</b>
                </div>
            </div>
        </div>

        <div class="card full">
            <div class="label">Summary</div>

            <div class="kv">
                <div>
                    <span>Plan</span>
                    <b>{plan}</b>
                </div>

                <div>
                    <span>Mood</span>
                    <b>{mood}</b>
                </div>

                <div>
                    <span>5H Used</span>
                    <b>{p5h:.1f}%</b>
                </div>

                <div>
                    <span>Week Used</span>
                    <b>{pw:.1f}%</b>
                </div>

                <div>
                    <span>Total Tokens</span>
                    <b>{data["tokens"]["total"]["total_tokens"]:,}</b>
                </div>

                <div>
                    <span>Last Tokens</span>
                    <b>{data["tokens"]["last"]["total_tokens"]:,}</b>
                </div>

                <div>
                    <span>Context</span>
                    <b>{data["tokens"]["model_context_window"]}</b>
                </div>

                <div>
                    <span>Source Line</span>
                    <b>{data["source"]["line"]}</b>
                </div>
            </div>

            <div class="links">
                <a href="/api/simple">/api/simple</a>
                <a href="/api/usage">/api/usage</a>
                <a href="/api/raw">/api/raw</a>
                <a href="/api/recent">/api/recent</a>
                <a href="/health">/health</a>
            </div>
        </div>

        <div class="card full">
            <div class="label">Normalized data</div>
            <pre>{normalized}</pre>
        </div>
    </div>
</div>
</body>
</html>
"""


# =========================
# 路由
# =========================

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/":
            html_response(self, render_index())
            return

        if path == "/api/usage":
            json_response(self, get_usage_data())
            return

        if path == "/api/simple":
            json_response(self, get_simple_data())
            return

        if path == "/api/raw":
            item = find_latest_token_count()
            if not item:
                json_response(self, {
                    "ok": False,
                    "error": "No token_count found",
                    "sessions_dir": SESSIONS_DIR,
                }, 404)
            else:
                json_response(self, item)
            return

        if path == "/api/recent":
            items = []
            for item in find_recent_token_counts(limit=20):
                try:
                    items.append(normalize_usage(item))
                except Exception:
                    pass

            json_response(self, {
                "ok": True,
                "count": len(items),
                "items": items,
            })
            return

        if path == "/health":
            json_response(self, {
                "ok": True,
                "time": int(time.time()),
                "time_text": unix_to_local_text(int(time.time())),
                "sessions_dir": SESSIONS_DIR,
            })
            return

        json_response(self, {
            "ok": False,
            "error": "Not found",
            "path": path,
        }, 404)

    def log_message(self, fmt, *args):
        print("[%s] %s" % (
            datetime.now(DISPLAY_TZ).strftime("%Y-%m-%d %H:%M:%S"),
            fmt % args
        ))


# =========================
# 启动
# =========================

def main():
    parser = argparse.ArgumentParser(description="Codex usage dashboard and device pusher")
    parser.add_argument("device_ip", nargs="?", default="", help="Device IP or base URL for push mode, e.g. 192.168.1.112")
    parser.add_argument("--device-url", default="", help="Deprecated alias for device_ip; kept for compatibility")
    parser.add_argument("--interval", type=int, default=60, help="Push interval seconds (push mode only)")
    parser.add_argument("--once", action="store_true", help="Run once and exit (push mode only)")
    parser.add_argument("--dry-run", action="store_true", help="Print payload but do not POST (push mode only)")
    args = parser.parse_args()

    device_url = normalize_device_url(args.device_url or args.device_ip)

    if device_url:
        interval = max(10, args.interval)
        print("Codex Usage Pusher")
        print("------------------")
        print(f"Sessions dir: {SESSIONS_DIR}")
        print(f"Device URL:   {device_url}")
        print(f"Interval:     {interval}s")
        print()

        while True:
            payload = build_device_payload()
            print(f"[{datetime.now(DISPLAY_TZ).strftime('%Y-%m-%d %H:%M:%S')}] payload={json.dumps(payload, ensure_ascii=False)}")
            try:
                if not args.dry_run:
                    status, body = post_device_payload(device_url, payload)
                    print(f"[{datetime.now(DISPLAY_TZ).strftime('%Y-%m-%d %H:%M:%S')}] POST -> HTTP {status} {body}")
            except error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace") if hasattr(exc, "read") else ""
                print(f"[{datetime.now(DISPLAY_TZ).strftime('%Y-%m-%d %H:%M:%S')}] HTTP error: {exc.code} {exc.reason} {body[:200]}")
            except Exception as exc:  # noqa: BLE001
                print(f"[{datetime.now(DISPLAY_TZ).strftime('%Y-%m-%d %H:%M:%S')}] Error: {exc}")

            if args.once:
                return
            time.sleep(interval)

    print("Codex Remaining Local Server")
    print("----------------------------")
    print(f"Sessions dir: {SESSIONS_DIR}")
    print(f"Web:         http://127.0.0.1:{PORT}/")
    print(f"Simple API:  http://127.0.0.1:{PORT}/api/simple")
    print(f"Full API:    http://127.0.0.1:{PORT}/api/usage")
    print()
    print("LAN access:")
    print("  ipconfig getifaddr en0")
    print(f"  http://你的Mac局域网IP:{PORT}/")
    print()

    server = HTTPServer((HOST, PORT), Handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
