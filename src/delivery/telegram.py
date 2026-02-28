"""
Telegram delivery module — sends bot output via Telegram.
For educational purposes only.
"""

import os
import json
import logging
from urllib.request import urlopen, Request
from urllib.error import URLError

log = logging.getLogger("delivery-telegram")

MAX_MESSAGE_LENGTH = 4096


def send_message(
    chat_id: str,
    text: str,
    token: str = "",
    parse_mode: str = "Markdown",
) -> bool:
    """Send a message via Telegram Bot API."""
    token = token or os.getenv("TELEGRAM_BOT_TOKEN", "")
    if not token:
        log.error("No Telegram bot token configured")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    # Split long messages
    chunks = [text[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(text), MAX_MESSAGE_LENGTH)]

    for chunk in chunks:
        payload = json.dumps({
            "chat_id": chat_id,
            "text": chunk,
            "parse_mode": parse_mode,
        }).encode()

        req = Request(url, data=payload, method="POST")
        req.add_header("Content-Type", "application/json")

        try:
            with urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
                if not data.get("ok"):
                    log.error("Telegram send failed: %s", data)
                    return False
        except URLError as e:
            log.error("Telegram API error: %s", e)
            return False

    return True


def format_report(title: str, body: str, footer: str = "") -> str:
    """Format a bot report for Telegram delivery."""
    parts = [f"*{title}*", "", body]
    if footer:
        parts.extend(["", f"_{footer}_"])
    return "\n".join(parts)
