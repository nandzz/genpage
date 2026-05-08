#!/usr/bin/env python3
"""
Post a self-contained HTML report to the local GenPage App.

Usage:
    python3 post-to-result-hub.py /path/to/report.html
    # or
    python3 post-to-result-hub.py << 'HTML_EOF'
    ...html...
    HTML_EOF

Reads HTML from a file path (preferred) or stdin and POSTs it to the genpage
render endpoint.
Prints 'ok' on success, 'CONNECTION_REFUSED' when the app is not running,
or an error message otherwise.

Temp files are stored in ~/.genpage/ and deleted after a successful POST.
A log entry is appended to ~/.genpage/genpage.log for every run.
"""
import json
import os
import sys
import datetime
import urllib.request
import urllib.error

GENPAGE_URL = "http://127.0.0.1:5678/render"
TIMEOUT_SECONDS = 5
MAX_BYTES = 10 * 1024 * 1024  # 10 MB safety cap
GENPAGE_DIR = os.path.expanduser("~/.genpage")
LOG_FILE = os.path.join(GENPAGE_DIR, "genpage.log")


def ensure_genpage_dir() -> None:
    os.makedirs(GENPAGE_DIR, exist_ok=True)


def log(message: str) -> None:
    ensure_genpage_dir()
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def main() -> None:
    ensure_genpage_dir()
    html = ""
    html_path = None
    owned_file = False  # True if we should delete the file after posting

    # Prefer explicit file path input to avoid huge inline shell commands.
    if len(sys.argv) > 1:
        html_path = sys.argv[1]
        try:
            with open(html_path, "r", encoding="utf-8") as f:
                html = f.read()
        except OSError as e:
            msg = f"error: could not read file — {e}"
            print(msg)
            log(msg)
            sys.exit(1)
        # Only delete files that live inside ~/.genpage/ (written by the agent)
        owned_file = os.path.abspath(html_path).startswith(os.path.abspath(GENPAGE_DIR))
    else:
        try:
            html = sys.stdin.read()
        except OSError as e:
            msg = f"error: could not read stdin — {e}"
            print(msg)
            log(msg)
            sys.exit(1)

    if not html.strip():
        msg = "error: no HTML content provided"
        print(msg)
        log(msg)
        sys.exit(1)

    encoded = json.dumps({"html": html}).encode("utf-8")

    if len(encoded) > MAX_BYTES:
        msg = (
            f"error: payload too large ({len(encoded)} bytes). "
            "Reduce report size or split into sections."
        )
        print(msg)
        log(msg)
        sys.exit(1)

    req = urllib.request.Request(
        GENPAGE_URL,
        data=encoded,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as r:
            result = json.loads(r.read().decode())
            if result.get("ok"):
                print("ok")
                log(f"ok — posted {len(encoded)} bytes")
                if owned_file and html_path:
                    try:
                        os.remove(html_path)
                    except OSError:
                        pass
            else:
                msg = f"error: {result.get('error')}"
                print(msg)
                log(msg)
    except urllib.error.URLError as e:
        if isinstance(e.reason, ConnectionRefusedError):
            msg = "CONNECTION_REFUSED"
            print(msg)
            print("Install or start the GenPage App: https://github.com/nandzz/genpage")
            log(msg)
        else:
            msg = f"error: {e.reason}"
            print(msg)
            log(msg)


if __name__ == "__main__":
    main()
