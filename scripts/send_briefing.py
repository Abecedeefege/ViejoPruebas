#!/usr/bin/env python3
"""Send the AI radar briefing via Gmail SMTP.

Usage:
    python3 scripts/send_briefing.py                        # sends today's HTML
    python3 scripts/send_briefing.py --date 2026-04-24      # specific date
    python3 scripts/send_briefing.py --html-file path.html  # explicit file

Env (read from .env in repo root, or process env):
    GMAIL_USER             Sender address (must own the app password)
    GMAIL_APP_PASSWORD     16-char app password from myaccount.google.com/apppasswords
    AI_RADAR_TO            Destination (defaults to airadar@itamoa.com)
"""
from __future__ import annotations

import argparse
import os
import smtplib
import ssl
import sys
from datetime import date
from email.message import EmailMessage
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SESSIONS_DIR = REPO_ROOT / "docs" / "sessions"
DEFAULT_TO = "airadar@itamoa.com"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def find_html_for_date(d: date) -> Path:
    candidate = SESSIONS_DIR / f"{d.isoformat()}-ai-radar-email.html"
    if not candidate.exists():
        raise FileNotFoundError(f"No briefing HTML found at {candidate}")
    return candidate


def html_to_plain(html: str) -> str:
    import re

    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    text = re.sub(r"</p>", "\n\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</li>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</h[1-6]>", "\n\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def send(html_path: Path, subject: str, to_addr: str) -> None:
    user = os.environ.get("GMAIL_USER")
    password = os.environ.get("GMAIL_APP_PASSWORD")
    if not user or not password:
        print(
            "ERROR: set GMAIL_USER and GMAIL_APP_PASSWORD in .env or environment.",
            file=sys.stderr,
        )
        sys.exit(1)

    html_body = html_path.read_text(encoding="utf-8")
    plain_body = html_to_plain(html_body)

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to_addr
    msg.set_content(plain_body)
    msg.add_alternative(html_body, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(user, password)
        server.send_message(msg)

    print(f"Sent '{subject}' to {to_addr} from {user}")


def main() -> None:
    load_dotenv(REPO_ROOT / ".env")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", help="YYYY-MM-DD; defaults to today", default=None)
    parser.add_argument("--html-file", help="Path to HTML body", default=None)
    parser.add_argument("--subject", default=None)
    parser.add_argument("--to", default=os.environ.get("AI_RADAR_TO", DEFAULT_TO))
    args = parser.parse_args()

    if args.html_file:
        html_path = Path(args.html_file).resolve()
        d = date.today()
    else:
        d = date.fromisoformat(args.date) if args.date else date.today()
        html_path = find_html_for_date(d)

    subject = args.subject or f"AI radar — {d.strftime('%d/%m')}"
    send(html_path, subject, args.to)


if __name__ == "__main__":
    main()
