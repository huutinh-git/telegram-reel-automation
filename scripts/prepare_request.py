"""Validate a Telegram → Facebook Reel request before network operations.

Dependencies: Python 3.11+ standard library only.
All untrusted GitHub event values arrive via step env, not shell interpolation.
"""

from __future__ import annotations

import ipaddress
import os
import re
import sys
import uuid
from pathlib import Path
from urllib.parse import urlsplit

MAX_URL_LENGTH = 2048
MAX_CAPTION_LENGTH = 2200
CHAT_ID_RE = re.compile(r"-?[0-9]{1,20}\Z")
MESSAGE_ID_RE = re.compile(r"[0-9]{1,20}\Z")
BAD_HOST_SUFFIXES = (".localhost", ".local", ".internal", ".lan", ".test", ".invalid", ".onion")


def validate_url(raw: str) -> str:
    url = raw.strip()
    if not url or len(url) > MAX_URL_LENGTH:
        raise ValueError("The video URL must be 1–2048 characters long")
    if any(ord(char) < 33 or ord(char) == 127 for char in url):
        raise ValueError("The video URL must not contain spaces or control characters")
    try:
        parsed = urlsplit(url)
        host = (parsed.hostname or "").lower().rstrip(".")
        port = parsed.port
    except ValueError as exc:
        raise ValueError("Malformed video URL") from exc
    if parsed.scheme != "https" or not host or parsed.username is not None or parsed.password is not None:
        raise ValueError("A valid HTTPS video URL without embedded credentials is required")
    if port not in (None, 443):
        raise ValueError("Non-standard HTTPS ports are not supported")
    if host == "localhost" or host.endswith(BAD_HOST_SUFFIXES) or host.startswith("."):
        raise ValueError("Local or reserved hostnames are not supported")
    if "." not in host and ":" not in host:
        raise ValueError("A publicly qualified hostname is required")
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        # Guard against alternate numeric IPv4 forms, e.g. 2130706433 and 127.1.
        # A DNS name may still resolve to private IPs: the allowlist / egress policy
        # must handle that threat. This validator is not a complete SSRF firewall.
        if host.replace(".", "").isdecimal():
            raise ValueError("Ambiguous numeric hostnames are not supported")
    else:
        if not address.is_global:
            raise ValueError("Private, loopback and other non-public IPs are not supported")
    allowlist = [h.strip().lower().lstrip(".") for h in os.environ.get("ALLOWED_SOURCE_HOSTS", "").split(",") if h.strip()]
    if allowlist and not any(host == allowed or host.endswith("." + allowed) for allowed in allowlist):
        raise ValueError("The video URL domain is not in ALLOWED_SOURCE_HOSTS")
    return url


def validate_id(value: str, pattern: re.Pattern[str], label: str) -> str:
    if value and not pattern.fullmatch(value):
        raise ValueError(f"{label} must contain a valid numeric identifier")
    return value


def prepare(env: dict[str, str]) -> dict[str, str]:
    event = env.get("EVENT_NAME", "")
    if event == "repository_dispatch":
        url = env.get("DISPATCH_URL", "")
        caption = env.get("DISPATCH_CAPTION", "")
        chat_id = env.get("DISPATCH_CHAT_ID", "")
        message_id = env.get("DISPATCH_STATUS_MESSAGE_ID", "")
        dry_run = "false"
    elif event == "workflow_dispatch":
        url = env.get("MANUAL_URL", "")
        caption = env.get("MANUAL_CAPTION", "")
        chat_id = env.get("FALLBACK_CHAT_ID", "")
        message_id = ""
        dry_run = "true" if env.get("MANUAL_DRY_RUN", "false").lower() == "true" else "false"
    else:
        raise ValueError("Unsupported workflow event")

    url = validate_url(url)
    if len(caption) > MAX_CAPTION_LENGTH or "\x00" in caption:
        raise ValueError("Caption must be at most 2200 characters and contain no NUL characters")
    chat_id = validate_id(chat_id, CHAT_ID_RE, "Telegram chat ID")
    message_id = validate_id(message_id, MESSAGE_ID_RE, "Telegram status message ID")
    return {
        "VIDEO_URL": url,
        "CAPTION": caption,
        "CHAT_ID": chat_id,
        "STATUS_MESSAGE_ID": message_id,
        "DRY_RUN": dry_run,
    }


def write_github_env(path: Path, values: dict[str, str]) -> None:
    # Single-line values have been validated. Captions can contain multiple lines.
    delimiter = "CAPTION_" + uuid.uuid4().hex
    with path.open("a", encoding="utf-8") as stream:
        for key in ("VIDEO_URL", "CHAT_ID", "STATUS_MESSAGE_ID", "DRY_RUN"):
            stream.write(f"{key}={values[key]}\n")
        stream.write(f"CAPTION<<{delimiter}\n{values['CAPTION']}\n{delimiter}\n")


def main() -> int:
    try:
        values = prepare(dict(os.environ))
        write_github_env(Path(os.environ["GITHUB_ENV"]), values)
        with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as stream:
            stream.write(f"dry_run={values['DRY_RUN']}\n")
        print("Input validated; dry-run=" + values["DRY_RUN"])
        return 0
    except (ValueError, KeyError, OSError) as exc:
        print("Request rejected: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
