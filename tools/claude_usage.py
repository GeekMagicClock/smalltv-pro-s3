#!/usr/bin/env python3
"""Push mock Claude usage to ESP32 via HTTP.

Stage-1 helper for device integration:
- no Claude token required
- no Anthropic API call
- uploads synthetic usage payload to /api/claude_usage
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional
from urllib import error, request

KEYCHAIN_SERVICE = "Claude Code-credentials"
KEYCHAIN_SERVICE_CANDIDATES = (
    "Claude Code-credentials",
    "Claude Code credentials",
    "Claude-credentials",
    "Claude credentials",
)
API_URL = "https://api.anthropic.com/v1/messages"
DEFAULT_MODEL = "claude-haiku-4-5-20251001"


def _ts() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


def log(level: str, event: str, **fields: Any) -> None:
    base = f"{_ts()} | {level:<5} | {event}"
    if fields:
        kv = " ".join(f"{k}={json.dumps(v, ensure_ascii=False)}" for k, v in fields.items())
        base = f"{base} | {kv}"
    print(base, flush=True)


def log_runtime_info(args: argparse.Namespace, device_url: str) -> None:
    log("INFO", "runtime.start", platform=sys.platform, python=sys.version.split()[0])
    log(
        "INFO",
        "runtime.config",
        mode=args.mode,
        target=device_url,
        interval_seconds=max(10, args.interval),
        dry_run=args.dry_run,
    )


def extract_access_token(blob: str) -> Optional[str]:
    blob = blob.strip()
    if not blob:
        return None
    try:
        data = json.loads(blob)
    except json.JSONDecodeError:
        data = None

    if isinstance(data, dict):
        if isinstance(data.get("accessToken"), str):
            return data["accessToken"]
        for value in data.values():
            if isinstance(value, dict) and isinstance(value.get("accessToken"), str):
                return value["accessToken"]

    match = re.search(r'"accessToken"\s*:\s*"([^"]+)"', blob)
    if match:
        return match.group(1)

    if re.fullmatch(r"[A-Za-z0-9_\-.~+/=]{20,}", blob):
        return blob
    return None


def read_token_from_keychain(service: str) -> Optional[str]:
    # First try by service+account, then service only as fallback.
    user = os.getenv("USER", "")
    attempts = [
        ["security", "find-generic-password", "-s", service, "-a", user, "-w"],
        ["security", "find-generic-password", "-s", service, "-w"],
    ]
    last_err = ""
    for cmd in attempts:
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=10, check=True)
            tok = extract_access_token(out.stdout)
            if tok:
                return tok
        except subprocess.CalledProcessError as exc:
            last_err = f"rc={exc.returncode} {exc.stderr.strip()}"
        except Exception as exc:  # noqa: BLE001
            last_err = str(exc)
    if last_err:
        log("WARN", "token.keychain.read_failed", service=service, error=last_err)
    return None


def read_token_from_keychain_candidates(primary: str) -> Optional[str]:
    tried: List[str] = []
    services = [primary] + [s for s in KEYCHAIN_SERVICE_CANDIDATES if s != primary]
    for svc in services:
        tried.append(svc)
        tok = read_token_from_keychain(svc)
        if tok:
            log("INFO", "token.keychain.found", service=svc)
            return tok
    log("WARN", "token.keychain.exhausted", tried_services=tried)
    return None


def read_token_from_credentials_file(path: str, label: str) -> Optional[str]:
    if not os.path.exists(path):
        log("WARN", "token.file.not_found", label=label, path=path)
        return None
    try:
        with open(path, encoding="utf-8") as f:
            raw = f.read()
    except Exception as exc:  # noqa: BLE001
        log("WARN", "token.file.read_failed", label=label, path=path, error=str(exc))
        return None

    tok = extract_access_token(raw)
    if tok:
        log("INFO", "token.file.found", label=label, path=path)
        return tok

    log("WARN", "token.file.missing_access_token", label=label, path=path)
    return None


def read_token_from_linux_credentials() -> Optional[str]:
    path = os.path.expanduser("~/.claude/.credentials.json")
    return read_token_from_credentials_file(path, "Linux")


def read_token_from_windows_credentials() -> Optional[str]:
    user_profile = os.environ.get("USERPROFILE", "")
    home_drive = os.environ.get("HOMEDRIVE", "")
    home_path = os.environ.get("HOMEPATH", "")
    candidates = [
        os.path.join(user_profile, ".claude", ".credentials.json") if user_profile else "",
        os.path.join(home_drive + home_path, ".claude", ".credentials.json") if home_drive and home_path else "",
        os.path.expanduser("~/.claude/.credentials.json"),
    ]
    for path in candidates:
        if not path:
            continue
        tok = read_token_from_credentials_file(path, "Windows")
        if tok:
            return tok
    return None


def hdr(headers: Any, name: str, default: str = "0") -> str:
    v = headers.get(name)
    return v if v is not None else default


def parse_pct(value: str) -> int:
    try:
        x = float(value)
    except ValueError:
        return 0
    n = int(round(x * 100))
    if n < 0:
        return 0
    if n > 100:
        return 100
    return n


def parse_reset_minutes(epoch_ts: str) -> int:
    try:
        target = float(epoch_ts)
    except ValueError:
        return 0
    mins = int(round((target - time.time()) / 60.0))
    return mins if mins > 0 else 0


def fetch_usage_payload(token: str, model: str) -> Dict[str, Any]:
    req_body = {
        "model": model,
        "max_tokens": 1,
        "messages": [{"role": "user", "content": "hi"}],
    }
    body_bytes = json.dumps(req_body).encode("utf-8")
    req = request.Request(
        API_URL,
        data=body_bytes,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "anthropic-version": "2023-06-01",
            "anthropic-beta": "oauth-2025-04-20",
            "Content-Type": "application/json",
            "User-Agent": "cubic-claude-usage-http/0.1",
        },
    )

    with request.urlopen(req, timeout=20) as resp:
        headers = resp.headers

    return {
        "s": parse_pct(hdr(headers, "anthropic-ratelimit-unified-5h-utilization")),
        "sr": parse_reset_minutes(hdr(headers, "anthropic-ratelimit-unified-5h-reset")),
        "w": parse_pct(hdr(headers, "anthropic-ratelimit-unified-7d-utilization")),
        "wr": parse_reset_minutes(hdr(headers, "anthropic-ratelimit-unified-7d-reset")),
        "st": hdr(headers, "anthropic-ratelimit-unified-5h-status", "unknown"),
        "ok": True,
    }


def post_payload(device_url: str, payload: Dict[str, Any]) -> None:
    api = device_url.rstrip("/") + "/api/claude_usage"
    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    req = request.Request(
        api,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json", "User-Agent": "cubic-claude-usage-http/0.1"},
    )

    with request.urlopen(req, timeout=8) as resp:
        resp_body = resp.read().decode("utf-8", errors="replace")
        log("INFO", "device.post.ok", url=api, status=resp.status, body=resp_body[:200])


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Push mock Claude usage to cubic device over HTTP")
    p.add_argument("ip", help="Device IP, e.g. 192.168.1.112")
    p.add_argument("--interval", type=int, default=60, help="Poll interval seconds (default: 60)")
    p.add_argument(
        "--mode",
        choices=("mock", "real"),
        default="mock",
        help="mock: synthetic data (default), real: query Anthropic headers with Claude OAuth token",
    )
    p.add_argument("--once", action="store_true", help="Run once and exit")
    p.add_argument("--dry-run", action="store_true", help="Do not POST, only print payload")
    p.add_argument("--model", default=DEFAULT_MODEL, help="Anthropic model for minimal probe call (real mode)")
    p.add_argument("--token", default="", help="Claude OAuth access token (real mode)")
    p.add_argument("--keychain-service", default=KEYCHAIN_SERVICE, help="macOS keychain service name (real mode)")
    return p.parse_args()


def build_mock_payload() -> Dict[str, Any]:
    # Always vary on each poll so bar animation can be observed continuously.
    tick = int(time.time())
    return {
        "s": 30 + ((tick * 7) % 45),   # 30..74
        "sr": 45 + ((tick * 3) % 120), # 45..164 mins
        "w": 15 + ((tick * 5) % 55),   # 15..69
        "wr": 2400 + ((tick * 11) % 3600),  # 2400..5999
        "st": "allowed",
        "ok": True,
    }


def render_bar(pct: int, width: int = 18, tick: int = 0) -> str:
    n = max(0, min(100, int(pct)))
    filled = int(round((n / 100.0) * width))
    pulse = "░▒▓█"
    head = pulse[tick % len(pulse)]
    if filled <= 0:
        return "·" * width
    if filled >= width:
        return "█" * width
    return ("█" * (filled - 1)) + head + ("·" * (width - filled))


def log_usage_payload(payload: Dict[str, Any], tick: int) -> None:
    s = int(payload.get("s", 0))
    w = int(payload.get("w", 0))
    log(
        "INFO",
        "usage.payload",
        s=s,
        s_bar=render_bar(s, 18, tick),
        sr=payload.get("sr", 0),
        w=w,
        w_bar=render_bar(w, 18, tick + 1),
        wr=payload.get("wr", 0),
        st=payload.get("st", "unknown"),
        ok=payload.get("ok", False),
    )


def main() -> int:
    args = parse_args()
    interval = max(10, args.interval)
    device_url = f"http://{args.ip}"
    token = ""
    token_source = "none"

    log_runtime_info(args, device_url)

    if args.mode == "real":
        token = args.token.strip() or os.getenv("CLAUDE_ACCESS_TOKEN", "").strip()
        if args.token.strip():
            token_source = "--token"
        elif os.getenv("CLAUDE_ACCESS_TOKEN", "").strip():
            token_source = "CLAUDE_ACCESS_TOKEN"

        if not token:
            if sys.platform == "darwin":
                log("INFO", "token.lookup", backend="macos_keychain", service=args.keychain_service)
                token = read_token_from_keychain_candidates(args.keychain_service) or ""
                if token:
                    token_source = "macOS Keychain"
            elif sys.platform.startswith("linux"):
                log("INFO", "token.lookup", backend="linux_credentials_file")
                token = read_token_from_linux_credentials() or ""
                if token:
                    token_source = "Linux credentials file"
            elif sys.platform in ("win32", "cygwin", "msys"):
                log("INFO", "token.lookup", backend="windows_credentials_file")
                token = read_token_from_windows_credentials() or ""
                if token:
                    token_source = "Windows credentials file"
            else:
                log("WARN", "token.lookup.unsupported_platform", platform=sys.platform)
        if not token:
            log("ERROR", "token.missing")
            log("INFO", "hint.free_plan", message="Free plan may not mint Claude Code OAuth token (403).")
            log("INFO", "hint.next_step", message="Use --mode mock or sign in with a Pro/Max-enabled account.")
            return 2
        log("INFO", "token.source", source=token_source)

    while True:
        try:
            payload = build_mock_payload() if args.mode == "mock" else fetch_usage_payload(token, args.model)
            log_usage_payload(payload, int(time.time()))
            if not args.dry_run:
                post_payload(device_url, payload)
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace") if hasattr(exc, "read") else ""
            if args.mode == "real" and exc.code == 403 and "requires a Pro or Max subscription" in body:
                log("ERROR", "anthropic.auth.denied", status=exc.code, reason=exc.reason)
                log("INFO", "hint.next_step", message="Switch to --mode mock, or use a Pro/Max-enabled account.")
            else:
                log("WARN", "http.error", status=exc.code, reason=exc.reason, body=body[:200])
        except Exception as exc:  # noqa: BLE001
            log("ERROR", "runtime.exception", error=str(exc))

        if args.once:
            return 0
        time.sleep(interval)


if __name__ == "__main__":
    raise SystemExit(main())
