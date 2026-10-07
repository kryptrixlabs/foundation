#!/usr/bin/env python3
"""Publish the verified KryptrixLabs Foundation v1.0 corpus to kryptrixlabs/foundation.

This script preserves the immutable release baseline, repairs the working MANUSCRIPT
copy from the frozen release copy, runs QA with automatic restoration after the
build validator, pushes the publication corpus, and optionally creates the GitHub
v1.0 release with the production PDF.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

REPO = "kryptrixlabs/foundation"
PREFIX = "KRYPTRIXLABS-HANDBOOK/"
FINAL = "EXPORTS/FINAL_RELEASE_v1.0"
MANUAL_MD = "KRYPTRIXLABS-CYBERSECURITY-OPERATING-MANUAL.md"
MANUAL_PDF = "KRYPTRIXLABS-CYBERSECURITY-OPERATING-MANUAL-v1.0.pdf"

ROOT_FILES = [
    "build_manuscript.py",
    "create_release_package.py",
    "generate_pdf.py",
    "publication_prep.py",
    "inspect_pdf_rc.py",
    "update_governance_final.py",
    "validate_repository.py",
    "verify_release_integrity.py",
]

def run(cmd, cwd: Path, check=True):
    print("+", " ".join(map(str, cmd)))
    return subprocess.run(cmd, cwd=cwd, check=check, text=True)

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def zip_bytes(z: zipfile.ZipFile, rel: str) -> bytes:
    return z.read(PREFIX + rel)

def copy_member(z: zipfile.ZipFile, rel: str, repo: Path):
    dst = repo / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(zip_bytes(z, rel))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-zip", required=True, type=Path, help="KryptrixLabs Foundation Final ZIP")
    ap.add_argument("--repo-dir", type=Path, default=Path.cwd(), help="local clone of kryptrixlabs/foundation")
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--no-release", action="store_true")
    args = ap.parse_args()

    source = args.source_zip.resolve()
    repo = args.repo_dir.resolve()
    if not source.exists():
        raise SystemExit(f"Source ZIP not found: {source}")
    if not (repo / ".git").exists():
        raise SystemExit(f"Not a git repository: {repo}")

    with zipfile.ZipFile(source) as z:
        names = set(z.namelist())
        for n in sorted(names):
            if not n.startswith(PREFIX) or n.endswith("/"):
                continue
            rel = n[len(PREFIX):]
            if rel.startswith("APPENDICES/") or rel.startswith("PROJECT-CONTROL/") or rel.startswith("V1.1-"):
                copy_member(z, rel, repo)

        for rel in ROOT_FILES:
            if PREFIX + rel in names:
                copy_member(z, rel, repo)

        for n in sorted(names):
            if n.startswith(PREFIX + FINAL + "/") and not n.endswith("/"):
                copy_member(z, n[len(PREFIX):], repo)

        for rel in [
            f"EXPORTS/print-ready/{MANUAL_PDF}",
            "EXPORTS/print-ready/publication_manifest.json",
        ]:
            if PREFIX + rel in names:
                copy_member(z, rel, repo)

        canonical = zip_bytes(z, f"{FINAL}/{MANUAL_MD}")
        manuscript = repo / "MANUSCRIPT" / MANUAL_MD
        manuscript.parent.mkdir(parents=True, exist_ok=True)
        manuscript.write_bytes(canonical)

    baseline = json.loads((repo / "PROJECT-CONTROL/v1_0_baseline.json").read_text(encoding="utf-8"))
    expected_md = baseline["hashes"]["master_manuscript"]
    expected_pdf = baseline["hashes"]["production_pdf"]
    actual_md = sha256(repo / "MANUSCRIPT" / MANUAL_MD)
    actual_pdf = sha256(repo / FINAL / MANUAL_PDF)
    if actual_md != expected_md:
        raise SystemExit(f"Manuscript SHA mismatch: {actual_md} != {expected_md}")
    if actual_pdf != expected_pdf:
        raise SystemExit(f"PDF SHA mismatch: {actual_pdf} != {expected_pdf}")
    print(f"[PASS] Manuscript SHA-256: {actual_md}")
    print(f"[PASS] PDF SHA-256:        {actual_pdf}")

    run([sys.executable, "verify_release_integrity.py"], repo)

    canonical_bytes = (repo / "MANUSCRIPT" / MANUAL_MD).read_bytes()
    try:
        run([sys.executable, "validate_repository.py"], repo)
    finally:
        (repo / "MANUSCRIPT" / MANUAL_MD).write_bytes(canonical_bytes)

    run([sys.executable, "verify_release_integrity.py"], repo)
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests/unit", "-p", "test_*.py", "-v"], repo)
    run([sys.executable, "software/cli/kryp_lab.py", "validate"], repo)

    run(["git", "add", "APPENDICES", "MANUSCRIPT", "PROJECT-CONTROL", "EXPORTS", *ROOT_FILES], repo)
    for p in repo.glob("V1.1-*.md"):
        run(["git", "add", p.name], repo)

    status = subprocess.run(["git", "status", "--porcelain"], cwd=repo, capture_output=True, text=True, check=True).stdout
    if status.strip():
        run(["git", "commit", "-m", "release: publish verified Foundation v1.0 corpus"], repo)
    else:
        print("[INFO] No publication changes to commit.")

    if not args.no_push:
        run(["git", "push", "origin", "main"], repo)

    if not args.no_release:
        gh = shutil.which("gh")
        pdf = repo / FINAL / MANUAL_PDF
        notes = repo / FINAL / "RELEASE_NOTES_v1.0.md"
        if gh:
            auth = subprocess.run([gh, "auth", "status"], cwd=repo, capture_output=True, text=True)
            if auth.returncode == 0:
                exists = subprocess.run([gh, "release", "view", "v1.0", "--repo", REPO], cwd=repo, capture_output=True)
                if exists.returncode == 0:
                    run([gh, "release", "upload", "v1.0", str(pdf), "--clobber", "--repo", REPO], repo)
                else:
                    run([
                        gh, "release", "create", "v1.0", str(pdf),
                        "--repo", REPO,
                        "--target", "main",
                        "--title", "KryptrixLabs Foundation v1.0",
                        "--notes-file", str(notes),
                        "--latest",
                    ], repo)
            else:
                print("[WARN] gh is installed but not authenticated; GitHub Release step skipped.")
        else:
            print("[WARN] GitHub CLI (gh) not found; GitHub Release step skipped.")

    print("\n[DONE] KryptrixLabs Foundation publication corpus is verified and published.")

if __name__ == "__main__":
    main()
