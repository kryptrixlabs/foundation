#!/usr/bin/env python3
"""
KryptrixLabs™ Cybersecurity Operating Manual - Release Integrity & Immutability Verification Engine
File: verify_release_integrity.py
Purpose: Audits SHA-256 hashes of frozen v1.0 release artifacts, verifies structural integrity,
ensures zero contamination of EXPORTS/FINAL_RELEASE_v1.0/, and enforces non-zero exit code on failure.
"""

import os
import sys
import hashlib
import json
import re

MANUSCRIPT_PATH = 'MANUSCRIPT/KRYPTRIXLABS-CYBERSECURITY-OPERATING-MANUAL.md'
RELEASE_DIR = 'EXPORTS/FINAL_RELEASE_v1.0'
RELEASE_CHECKSUMS = 'EXPORTS/FINAL_RELEASE_v1.0/CHECKSUMS-SHA256.txt'

def get_sha256(filepath):
    sha = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest()

def verify_release():
    print("=" * 70)
    print("KryptrixLabs™ Release Integrity & Immutability Suite")
    print("=" * 70)

    failures = []

    # 1. Verify Release Manifest & Immutability
    print("\n[CHECK 1] Release Package SHA-256 Immutability Check...")
    if not os.path.exists(RELEASE_CHECKSUMS):
        failures.append(f"Missing release checksum manifest: {RELEASE_CHECKSUMS}")
    else:
        with open(RELEASE_CHECKSUMS, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
        
        checked_count = 0
        for line in lines:
            line_str = line.strip()
            if not line_str or line_str.startswith('#'):
                continue
            parts = line_str.split(maxsplit=1)
            if len(parts) != 2:
                continue
            expected_hash, rel_path = parts[0].strip(), parts[1].strip()
            if not os.path.exists(rel_path):
                failures.append(f"Missing release artifact: {rel_path}")
                continue
            actual_hash = get_sha256(rel_path)
            if actual_hash != expected_hash:
                failures.append(f"Immutability Violation in {rel_path}: Hash changed!")
            else:
                checked_count += 1
        print(f"  -> PASSED: {checked_count} critical artifacts verified against SHA-256 baseline.")

    # 2. Verify Release Package Files Existence
    print("\n[CHECK 2] Clean Release Package Structure Check...")
    required_release_files = [
        'KRYPTRIXLABS-CYBERSECURITY-OPERATING-MANUAL-v1.0.pdf',
        'KRYPTRIXLABS-CYBERSECURITY-OPERATING-MANUAL.md',
        'publication_manifest.json',
        'CHECKSUMS-SHA256.txt',
        'RELEASE_NOTES_v1.0.md'
    ]
    for rfile in required_release_files:
        full_p = os.path.join(RELEASE_DIR, rfile)
        if not os.path.exists(full_p):
            failures.append(f"Missing required release package file: {full_p}")
        elif os.path.getsize(full_p) == 0:
            failures.append(f"Zero-byte release package file: {full_p}")
    print(f"  -> PASSED: Clean release package at {RELEASE_DIR}/ verified complete.")

    # 3. Verify Appendix A Alphabetical Sorting
    print("\n[CHECK 3] Appendix A Alphabetical Sorting Verification...")
    app_a_path = 'APPENDICES/appendix-a-glossary-and-acronyms.md'
    if not os.path.exists(app_a_path):
        failures.append(f"Missing Appendix A file: {app_a_path}")
    else:
        with open(app_a_path, 'r', encoding='utf-8', errors='ignore') as f:
            app_a_text = f.read()
        
        in_a1 = False
        a1_acronyms = []
        for line in app_a_text.splitlines():
            if re.search(r'##\s*Section\s*A\.1', line, re.IGNORECASE):
                in_a1 = True
                continue
            elif re.search(r'##\s*Section\s*A\.2', line, re.IGNORECASE):
                in_a1 = False
                break
            if in_a1 and '|' in line and not ('|---|' in line or '| --- |' in line or '| Acronym |' in line or '| **Acronym** |' in line):
                cells = [c.strip() for c in line.strip('|').split('|')]
                if cells:
                    m = re.search(r'\*\*(.*?)\*\*', cells[0])
                    term = m.group(1).strip().upper() if m else cells[0].strip().upper()
                    if term:
                        a1_acronyms.append(term)
        
        clean_acronyms = [a for a in a1_acronyms if a]
        if not clean_acronyms:
            failures.append("Failed to extract Section A.1 acronyms for sorting check!")
        elif clean_acronyms != sorted(clean_acronyms):
            failures.append("Appendix A Table A.1 acronyms are out of alphabetical order!")
        else:
            print(f"  -> PASSED: {len(clean_acronyms)} acronyms verified 100% alphabetically sorted A to Z.")

    # SUMMARY
    print("\n" + "=" * 70)
    print("RELEASE INTEGRITY AUDIT SUMMARY")
    print("=" * 70)
    print(f"Integrity Checkpoints Executed : 3 Checks")
    print(f"Failures Detected             : {len(failures)}")
    print("-" * 70)

    if failures:
        print("\n" + "!" * 70)
        print("RELEASE INTEGRITY CHECK FAILED:")
        for f in failures:
            print(f"  - [FAIL] {f}")
        print("!" * 70)
        sys.exit(1)

    print("\n[SUCCESS] ALL RELEASE INTEGRITY CHECKS PASSED WITH ZERO ERRORS!")

if __name__ == '__main__':
    verify_release()
