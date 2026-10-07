# POST-RELEASE OPERATIONS & GOVERNANCE GUIDE

## KryptrixLabs™ Cybersecurity Operating Manual — Version 1.0 Baseline

| Field | Value |
|---|---|
| **Release Identifier** | `KRYP-MANUAL-v1.0-FINAL` |
| **Release Version** | **v1.0 Final Release — VERIFIED** |
| **Release Date** | **2026-08-16** |
| **Author & Maintainer** | Christopher / KryptrixLabs™ |
| **Authoritative Package Location** | `EXPORTS/FINAL_RELEASE_v1.0/` |
| **Machine-Readable Baseline** | `PROJECT-CONTROL/v1_0_baseline.json` |

---

## 1. Release Immutability Policy

1. **v1.0 Immutability Guarantee**: The artifacts residing in `EXPORTS/FINAL_RELEASE_v1.0/` form the immutable baseline of the KryptrixLabs™ Cybersecurity Operating Manual v1.0.
2. **Build Protection**: Build scripts (`build_manuscript.py`, `generate_pdf.py`, `create_release_package.py`) are strictly prohibited from overwriting files inside `EXPORTS/FINAL_RELEASE_v1.0/`.
3. **Cryptographic Integrity**: All production files are indexed by SHA-256 checksums recorded in `EXPORTS/FINAL_RELEASE_v1.0/CHECKSUMS-SHA256.txt`.

## 2. Integrity Verification & QA Commands

```bash
python validate_repository.py
python verify_release_integrity.py
python publication_prep.py
python inspect_pdf_rc.py
```

## 3. Semantic Versioning & Change Taxonomy

* **`v1.0` (Released Baseline)**: The current immutable production release.
* **`v1.0.x` (Maintenance Release)**: Reserved exclusively for critical errata, typo corrections, or security bug fixes that do not alter core chapter structure or renumber sections.
* **`v1.1` (Substantive Content Release)**: Reserved for planned expansion of specialized topics, updated tool profiles (Appendix C), or new laboratory exercises (Appendix E).
* **`v2.0` (Major Revision)**: Reserved for fundamental architectural shifts or major re-structuring of core chapters.

## 4. Change Control & Submission Protocol

1. **Submit Change Request**: Log a new Change Request entry in `V1.1-BACKLOG.md`.
2. **Impact Assessment**: Evaluate affected chapters/appendices, security implications, and QA validation requirements.
3. **Approval Requirement**: No development work may begin on `v1.1` items without explicit approval from project governance.
4. **Maintenance of History**: All changes must be logged in `PROJECT-CONTROL/02_REVISION_HISTORY.md`.

## 5. What Must Never Be Modified

* **Core Chapters 1–31**: The substantive text of Chapters 1 through 31 is **FROZEN** and must not be renumbered, rewritten, or deleted.
* **v1.0 Checksum Baseline**: `EXPORTS/FINAL_RELEASE_v1.0/CHECKSUMS-SHA256.txt` must not be overwritten or modified.

## 6. Document Control & Revision Record

| Version | Date | Description | Author |
|---|---|---|---|
| v1.0 | 2026-08-16 | Initial complete release of Post-Release Operations Guide | KryptrixLabs Security Engineering |
