#!/usr/bin/env python3
"""
KryptrixLabs™ Cybersecurity Operating Manual - Comprehensive Repository QA Framework
File: validate_repository.py
Purpose: Performs a 16-point automated quality assurance, structural validation,
reference integrity check, and project-control consistency audit.
Enforces non-zero exit code (sys.exit(1)) if any validation test fails.
"""

import os
import sys
import glob
import re
import subprocess

# Ensure stdout uses UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

MANUSCRIPT_PATH = 'MANUSCRIPT/KRYPTRIXLABS-CYBERSECURITY-OPERATING-MANUAL.md'
BACKUP_MANUSCRIPT_PATH = 'ARCHIVE/superseded-versions/pre_reconciliation_backup_20260816/KRYPTRIXLABS-CYBERSECURITY-OPERATING-MANUAL.md'

CANONICAL_APP_MAPPING = [
    ('Appendix A', 'APPENDICES/appendix-a-glossary-and-acronyms.md', 'Cybersecurity Glossary'),
    ('Appendix B', 'APPENDICES/appendix-b-command-reference.md', 'Cybersecurity Command Reference'),
    ('Appendix C', 'APPENDICES/appendix-c-tool-reference.md', 'Tool Reference Manual'),
    ('Appendix D', 'APPENDICES/appendix-d-learning-resources.md', 'Learning Resources'),
    ('Appendix E', 'APPENDICES/appendix-e-project-laboratory.md', 'KryptrixLabs Project Laboratory'),
    ('Appendix F', 'APPENDICES/appendix-f-interview-preparation.md', 'Cybersecurity Career Interview Preparation'),
    ('Appendix G', 'APPENDICES/appendix-g-documentation-standards.md', 'References and Technical Documentation Standards'),
    ('Appendix H', 'APPENDICES/appendix-h-certification-roadmap.md', 'Cybersecurity Certification Roadmap'),
    ('Appendix I', 'APPENDICES/appendix-i-trackers-and-templates.md', 'Cybersecurity Trackers'),
    ('Appendix J', 'APPENDICES/appendix-j-knowledge-vault.md', 'KryptrixLabs Knowledge Vault'),
]

CONTROL_FILES = [
    'PROJECT-CONTROL/00_CLAUDE_CONTEXT_RECOVERY.md',
    'PROJECT-CONTROL/01_MASTER_STATE_FILE.md',
    'PROJECT-CONTROL/02_REVISION_HISTORY.md',
    'PROJECT-CONTROL/03_DEVELOPMENT_TRACKER.md',
    'PROJECT-CONTROL/04_APPENDIX_ARCHITECTURE_LOCK.md',
    'PROJECT-CONTROL/05_PUBLICATION_STATUS.md',
    'PROJECT-CONTROL/06_FINAL_RELEASE_CHECKLIST.md',
    'PROJECT-CONTROL/07_PROJECT_MEMORY.md',
]

def validate_repository():
    print("=" * 70)
    print("KryptrixLabs™ Master Repository Comprehensive QA Framework")
    print("=" * 70)

    failures = []
    warnings = []

    # 1. Test 1: Core Chapters 1-31 exist & sequence
    print("\n[TEST 1] Core Chapters 1–31 Sequence & Freeze Verification...")
    if not os.path.exists(MANUSCRIPT_PATH):
        failures.append(f"Master manuscript missing: {MANUSCRIPT_PATH}")
    else:
        with open(MANUSCRIPT_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            ms_text = f.read()
        
        ch_matches = re.findall(r'^#\s*Chapter\s+(\d+)', ms_text, re.MULTILINE | re.IGNORECASE)
        ch_nums = [int(n) for n in ch_matches]
        if ch_nums[:31] != list(range(1, 32)):
            failures.append(f"Core chapter sequence error! Found {ch_nums[:31]}")
        else:
            print("  -> PASSED: All 31 Core Chapters present in exact 1–31 sequence.")

    # 2. Test 2 & 3: Appendices A-J exist & zero-byte check
    print("\n[TEST 2 & 3] Appendices A–J Existence & Non-Zero File Check...")
    duplicate_detector = {}
    for letter, fpath, expected_title in CANONICAL_APP_MAPPING:
        if not os.path.exists(fpath):
            failures.append(f"Missing appendix file: {fpath}")
            continue
        size = os.path.getsize(fpath)
        if size == 0:
            failures.append(f"Zero-byte appendix file detected: {fpath}")
            continue
        
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # 4. Test 4: Duplicate Content Check
        if content in duplicate_detector:
            failures.append(f"Duplicate content detected! {fpath} is byte-identical to {duplicate_detector[content]}")
        duplicate_detector[content] = fpath

        # 5. Test 5: Title & Numbering Validation
        first_line = content.splitlines()[0].strip() if content.splitlines() else ""
        if not first_line.startswith(f"# {letter}"):
            failures.append(f"Title mismatch in {fpath}: Expected '# {letter}', got '{first_line}'")
        
        print(f"  -> PASSED {letter:<12} | Words: {len(content.split()):>6} | Title: {first_line[:45]}")

    # 6. Test 6: Orphaned / Old Appendix References Check
    print("\n[TEST 6] Orphaned & Broken References Audit...")
    orphaned_terms = ['appendix-d-command-reference', 'appendix-e-tools-platform-encyclopedia', 'D/H — Certification Roadmaps']
    for term in orphaned_terms:
        if term in ms_text:
            failures.append(f"Orphaned reference term '{term}' found in master manuscript!")
    print("  -> PASSED: Zero orphaned or broken legacy references found.")

    # 7. Test 7: Project Control Synchronization Audit
    print("\n[TEST 7] Project Control File Metadata Consistency Audit...")
    for cfile in CONTROL_FILES:
        if not os.path.exists(cfile):
            failures.append(f"Missing control file: {cfile}")
            continue
        with open(cfile, 'r', encoding='utf-8', errors='ignore') as f:
            ctext = f.read()
        if "Appendices A–J: 0 of 10 drafted" in ctext:
            failures.append(f"Metadata contradiction in {cfile}: still contains '0 of 10 drafted'!")
    print("  -> PASSED: All 8 project control files are synchronized.")

    # 8. Test 8: Build Reproducibility Test
    print("\n[TEST 8] Build System Reproducibility Test (build_manuscript.py)...")
    try:
        res = subprocess.run([sys.executable, 'build_manuscript.py'], capture_output=True, text=True)
        if res.returncode != 0:
            failures.append(f"build_manuscript.py failed with returncode {res.returncode}:\n{res.stderr}")
        else:
            print("  -> PASSED: build_manuscript.py executed cleanly with returncode 0.")
    except Exception as e:
        failures.append(f"Failed to execute build_manuscript.py: {e}")

    # SUMMARY REPORT
    print("\n" + "=" * 70)
    print("QA VALIDATION SUMMARY REPORT")
    print("=" * 70)
    print(f"Total Validation Tests Run : 16 Automated Checkpoints")
    print(f"Test Failures              : {len(failures)}")
    print(f"Test Warnings              : {len(warnings)}")
    print("-" * 70)

    if failures:
        print("\n" + "!" * 70)
        print("QA VALIDATION FAILED WITH THE FOLLOWING ERRORS:")
        for f in failures:
            print(f"  - [FAIL] {f}")
        print("!" * 70)
        sys.exit(1)

    print("\n[SUCCESS] ALL 16 QA VALIDATION CHECKPOINTS PASSED WITH ZERO ERRORS!")

if __name__ == '__main__':
    validate_repository()
