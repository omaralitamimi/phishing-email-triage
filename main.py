"""Offline triage helper for saved RFC 822 email files."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from email import policy
from email.parser import BytesParser
from email.utils import parseaddr
from pathlib import Path
from urllib.parse import urlparse

URL_RE = re.compile(r"https?://[^\s<>\"']+")


def domain(address: str) -> str:
    parsed = parseaddr(address)[1]
    return parsed.rsplit("@", 1)[-1].lower() if "@" in parsed else ""


def analyze(raw: bytes) -> dict:
    message = BytesParser(policy=policy.default).parsebytes(raw)
    body_parts = []
    attachments = []
    for part in message.walk():
        if part.get_content_disposition() == "attachment":
            payload = part.get_payload(decode=True) or b""
            attachments.append({"filename": part.get_filename(), "sha256": hashlib.sha256(payload).hexdigest(), "size": len(payload)})
        elif part.get_content_type() in {"text/plain", "text/html"}:
            try:
                body_parts.append(part.get_content())
            except Exception:
                pass
    urls = sorted(set(URL_RE.findall("\n".join(body_parts))))
    return {"subject": message.get("subject", ""), "from_domain": domain(message.get("from", "")), "reply_to_domain": domain(message.get("reply-to", "")), "url_hosts": sorted({urlparse(url).hostname or "" for url in urls}), "attachments": attachments}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("email", type=Path)
    args = parser.parse_args()
    print(json.dumps(analyze(args.email.read_bytes()), indent=2))


if __name__ == "__main__":
    main()
