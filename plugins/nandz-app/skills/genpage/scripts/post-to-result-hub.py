#!/usr/bin/env python3
"""
Post a Nandz Space bundle (folder of .tsx files + manifest.json) to the local
or remote Nandz hub.

Usage:
    python3 post-to-result-hub.py /path/to/space-<timestamp>/

The script reads `manifest.json` and every `.tsx`/`.ts` file in the folder,
packs them into a JSON envelope, and POSTs to `${NANDZ_HUB_URL}` (default
`http://127.0.0.1:5678/render`). The host bundles and mounts the entry
component inside its own ThemeProvider + Inter shell.

Prints 'ok' on success, 'CONNECTION_REFUSED' when the hub is not running,
or an error message otherwise.

The Space folder stays on disk after a successful POST so the user can
re-open or re-send it. A log entry is appended to `~/.nandz/nandz.log`.
"""
import json
import os
import sys
import datetime
import urllib.request
import urllib.error

NANDZ_URL = os.environ.get("NANDZ_HUB_URL", "http://127.0.0.1:5678/render")
TIMEOUT_SECONDS = 5
MAX_BYTES = 10 * 1024 * 1024  # 10 MB safety cap on the envelope
ALLOWED_EXTS = (".tsx", ".ts")
NANDZ_DIR = os.path.expanduser("~/.nandz")
SPACES_DIR = os.path.join(NANDZ_DIR, "spaces")
LOG_FILE = os.path.join(NANDZ_DIR, "nandz.log")


def ensure_nandz_dir() -> None:
    os.makedirs(NANDZ_DIR, exist_ok=True)
    os.makedirs(SPACES_DIR, exist_ok=True)


def log(message: str) -> None:
    ensure_nandz_dir()
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def fail(msg: str, code: int = 1) -> None:
    print(msg)
    log(msg)
    sys.exit(code)


def collect_files(space_dir: str) -> dict:
    files = {}
    for root, _dirs, names in os.walk(space_dir):
        for name in names:
            if not name.endswith(ALLOWED_EXTS):
                continue
            full = os.path.join(root, name)
            rel = os.path.relpath(full, space_dir).replace(os.sep, "/")
            with open(full, "r", encoding="utf-8") as fh:
                files[rel] = fh.read()
    return files


def main() -> None:
    ensure_nandz_dir()

    if len(sys.argv) < 2:
        fail("error: pass the Space folder path (e.g. ~/.nandz/spaces/space-<ts>/)")

    space_dir = os.path.expanduser(sys.argv[1].rstrip(os.sep) or sys.argv[1])
    if not os.path.isdir(space_dir):
        fail(f"error: not a directory \u2014 {space_dir}")

    manifest_path = os.path.join(space_dir, "manifest.json")
    if not os.path.isfile(manifest_path):
        fail(f"error: manifest.json missing in {space_dir}")

    try:
        with open(manifest_path, "r", encoding="utf-8") as fh:
            manifest = json.load(fh)
    except (OSError, json.JSONDecodeError) as e:
        fail(f"error: could not read manifest.json \u2014 {e}")

    entry = manifest.get("entry") or "index.tsx"
    if not os.path.isfile(os.path.join(space_dir, entry)):
        fail(f"error: entry file '{entry}' missing in {space_dir}")

    files = collect_files(space_dir)
    if entry not in files:
        fail(f"error: entry file '{entry}' is not a .tsx/.ts file")

    envelope = {
        "id": manifest.get("id") or os.path.basename(space_dir),
        "title": manifest.get("title", ""),
        "summary": manifest.get("summary", ""),
        "createdAt": manifest.get("createdAt", datetime.datetime.now().isoformat()),
        "entry": entry,
        "theme": manifest.get("theme", "zinc"),
        "files": files,
    }

    encoded = json.dumps(envelope).encode("utf-8")
    if len(encoded) > MAX_BYTES:
        fail(
            f"error: payload too large ({len(encoded)} bytes). "
            "Split the Space or reduce inline data."
        )

    req = urllib.request.Request(
        NANDZ_URL,
        data=encoded,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as r:
            result = json.loads(r.read().decode())
            if result.get("ok"):
                print("ok")
                log(f"ok \u2014 posted {len(encoded)} bytes to {NANDZ_URL}")
            else:
                fail(f"error: {result.get('error')}")
    except urllib.error.URLError as e:
        if isinstance(e.reason, ConnectionRefusedError):
            print("CONNECTION_REFUSED")
            print("Install or start the Nandz App: https://github.com/nandzz/genpage")
            log(f"CONNECTION_REFUSED on {NANDZ_URL}")
        else:
            fail(f"error: {e.reason}")


if __name__ == "__main__":
    main()
