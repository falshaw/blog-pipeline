#!/usr/bin/env python3
"""Generic FTP / FTPS deploy for a static site tree — an EXAMPLE deploy hook for blog-pipeline.

Credentials come from environment variables ONLY (never from arguments, never from a file in the repo):

  FTP_HOST         ftp.example.com                       (required)
  FTP_USER         deploy user                           (required)
  FTP_PASSWORD     password                              (required)
  FTP_PORT         default 21
  FTP_TLS          1 = explicit FTPS (default), 0 = plain FTP (only on a trusted network)
  FTP_REMOTE_DIR   remote web root, e.g. /htdocs         (or --remote)

What it does
  * Walks --local, hashes every file (sha256) and compares with a local manifest of the last deploy.
    Only new or changed files are uploaded (--force-all re-sends everything).
  * Upload order: assets (images, css, js, fonts) -> pages (*.html) -> discovery files
    (sitemap*.xml, feed*.xml, llms*.txt, robots.txt) LAST, so the sitemap never points at a page
    that is not up yet.
  * Each file goes up as "<name>.part" and is renamed into place, so visitors never get a half-written file.
  * Never touches server-only files: --protect globs (defaults: .htaccess, .well-known/**, common
    search-engine verification files) are neither uploaded over nor deleted.
  * --delete-orphans removes remote files that THIS SCRIPT uploaded earlier (per the manifest) and that
    are gone locally. It never lists-and-deletes the remote tree, so files it did not upload are safe.
  * --dry-run prints the plan and changes nothing (not even the manifest).

Run it detached for big trees and verify with curl afterwards. One FTP session per hosting account at a
time: shared hosts often cap concurrent connections per account.

Usage
  python ftp-deploy.py --local ./site --dry-run
  python ftp-deploy.py --local ./site --remote /htdocs --exclude "_drafts/**" --exclude "*.psd"
  python ftp-deploy.py --local ./site --only blog/my-post/index.html --only images/my-post.webp
"""
import argparse
import fnmatch
import ftplib
import hashlib
import json
import os
import posixpath
import sys
import time
from pathlib import Path

DEFAULT_PROTECT = [
    ".htaccess", "**/.htaccess", ".htpasswd", "**/.htpasswd",
    ".well-known", ".well-known/**",
    "google*.html", "BingSiteAuth.xml", "yandex_*.html",
]
DEFAULT_EXCLUDE = [".git/**", ".git", "**/.DS_Store", "**/Thumbs.db", "**/*.part", "node_modules/**", ".env", "**/.env"]
ASSET_EXT = {".webp", ".avif", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".css", ".js", ".mjs",
             ".woff", ".woff2", ".ttf", ".otf", ".json", ".pdf", ".mp4", ".webm"}
DISCOVERY_GLOBS = ["sitemap*.xml", "**/sitemap*.xml", "feed*.xml", "**/feed*.xml", "rss*.xml", "**/rss*.xml",
                   "atom*.xml", "**/atom*.xml", "llms*.txt", "robots.txt"]


def match_any(rel, globs):
    return any(fnmatch.fnmatch(rel, g) for g in globs)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def phase(rel):
    if match_any(rel, DISCOVERY_GLOBS):
        return 2
    if Path(rel).suffix.lower() in ASSET_EXT:
        return 0
    return 1


def env(name, default=None, required=False):
    val = os.environ.get(name, default)
    if required and not val:
        sys.exit(f"Missing environment variable {name}. Credentials are read from the environment only.")
    return val


def connect():
    host = env("FTP_HOST", required=True)
    user = env("FTP_USER", required=True)
    password = env("FTP_PASSWORD", required=True)
    port = int(env("FTP_PORT", "21"))
    use_tls = env("FTP_TLS", "1") != "0"
    ftp = ftplib.FTP_TLS() if use_tls else ftplib.FTP()
    ftp.connect(host, port, timeout=60)
    ftp.login(user, password)
    if use_tls:
        ftp.prot_p()
    return ftp


class Remote:
    def __init__(self, ftp, root):
        self.ftp = ftp
        self.root = root.rstrip("/") or "/"
        self.known_dirs = set()

    def path(self, rel):
        return posixpath.join(self.root, rel)

    def ensure_dir(self, rel_dir):
        if not rel_dir or rel_dir in self.known_dirs:
            return
        parts = rel_dir.split("/")
        for i in range(1, len(parts) + 1):
            sub = "/".join(parts[:i])
            if sub in self.known_dirs:
                continue
            try:
                self.ftp.mkd(self.path(sub))
            except ftplib.error_perm:
                pass  # exists
            self.known_dirs.add(sub)

    def upload(self, local, rel):
        self.ensure_dir(posixpath.dirname(rel))
        target = self.path(rel)
        part = target + ".part"
        with open(local, "rb") as f:
            self.ftp.storbinary(f"STOR {part}", f)
        try:
            self.ftp.rename(part, target)
        except ftplib.error_perm:
            # Some servers refuse to rename over an existing file.
            try:
                self.ftp.delete(target)
            except ftplib.error_perm:
                pass
            self.ftp.rename(part, target)

    def delete(self, rel):
        self.ftp.delete(self.path(rel))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--local", required=True, help="local site root to deploy")
    ap.add_argument("--remote", default=None, help="remote web root (default: $FTP_REMOTE_DIR)")
    ap.add_argument("--manifest", default=None, help="manifest path (default: .deploy-state/<host>-<remote>.json)")
    ap.add_argument("--exclude", action="append", default=[], help="glob relative to --local (repeatable)")
    ap.add_argument("--protect", action="append", default=[], help="extra server-only glob never touched (repeatable)")
    ap.add_argument("--only", action="append", default=[], help="deploy only these relative paths (repeatable)")
    ap.add_argument("--force-all", action="store_true", help="upload every file, ignoring the manifest")
    ap.add_argument("--delete-orphans", action="store_true", help="delete remote files this script uploaded before and that are gone locally")
    ap.add_argument("--dry-run", action="store_true", help="print the plan, change nothing")
    a = ap.parse_args()

    local_root = Path(a.local).resolve()
    if not local_root.is_dir():
        sys.exit(f"--local {local_root} is not a directory")
    remote_root = a.remote or env("FTP_REMOTE_DIR", required=True)
    protect = DEFAULT_PROTECT + a.protect
    exclude = DEFAULT_EXCLUDE + a.exclude

    host = env("FTP_HOST", "host")
    manifest_path = Path(a.manifest) if a.manifest else Path(".deploy-state") / (
        f"{host}-{remote_root.strip('/').replace('/', '_') or 'root'}.json")
    old = json.loads(manifest_path.read_text("utf-8")) if manifest_path.exists() else {}

    files = {}
    for p in sorted(local_root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(local_root).as_posix()
        if match_any(rel, exclude) or match_any(rel, protect):
            continue
        if a.only and rel not in a.only:
            continue
        files[rel] = p
    missing = [o for o in a.only if o not in files]
    if missing:
        sys.exit(f"--only paths not found (or excluded/protected): {missing}")

    new_manifest = dict(old)
    to_upload = []
    for rel, p in files.items():
        digest = sha256(p)
        if a.force_all or old.get(rel) != digest:
            to_upload.append((phase(rel), rel, p, digest))
    to_upload.sort()

    orphans = []
    if a.delete_orphans and not a.only:
        orphans = [rel for rel in old if rel not in files and not match_any(rel, protect)]

    print(f"local={local_root}  remote={remote_root}  upload={len(to_upload)}  delete={len(orphans)}"
          f"  unchanged={len(files) - len(to_upload)}{'  DRY-RUN' if a.dry_run else ''}")
    for _, rel, _, _ in to_upload:
        print(f"  + {rel}")
    for rel in orphans:
        print(f"  - {rel}")
    if a.dry_run or (not to_upload and not orphans):
        return

    t0 = time.time()
    errors = 0
    ftp = connect()
    remote = Remote(ftp, remote_root)
    try:
        for _, rel, p, digest in to_upload:
            try:
                remote.upload(p, rel)
                new_manifest[rel] = digest
            except ftplib.all_errors as e:
                errors += 1
                print(f"  ! upload failed {rel}: {e}", file=sys.stderr)
        for rel in orphans:
            try:
                remote.delete(rel)
                new_manifest.pop(rel, None)
            except ftplib.all_errors as e:
                errors += 1
                print(f"  ! delete failed {rel}: {e}", file=sys.stderr)
    finally:
        try:
            ftp.quit()
        except ftplib.all_errors:
            pass
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = manifest_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(new_manifest, indent=1, sort_keys=True), "utf-8")
        os.replace(tmp, manifest_path)

    print(f"done in {time.time() - t0:.0f}s, errors={errors}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
