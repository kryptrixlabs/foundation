# Publication Migration Note

During final GitHub publication preparation, one state mismatch was found in the packaged working tree:

- The immutable release copy at `EXPORTS/FINAL_RELEASE_v1.0/KRYPTRIXLABS-CYBERSECURITY-OPERATING-MANUAL.md` retained the correct v1.0 SHA-256 baseline.
- The working `MANUSCRIPT/KRYPTRIXLABS-CYBERSECURITY-OPERATING-MANUAL.md` had been rewritten by the repository QA build step.

No immutable release artifact was corrupted.

The publication procedure therefore restores the working `MANUSCRIPT/` copy from the immutable release copy before final verification. After restoration, the repository passes:

- release integrity: **3/3**
- repository QA: **16/16**
- controller tests: **7/7**
- lab configuration validation: **PASS**

The original `validate_repository.py` intentionally invokes `build_manuscript.py`, which rewrites the working manuscript. The publishing helper preserves and restores the canonical manuscript around that QA execution so the final repository remains byte-identical to the v1.0 baseline.
