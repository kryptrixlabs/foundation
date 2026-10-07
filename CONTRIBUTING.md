# Contributing to KryptrixLabs Foundation

KryptrixLabs Foundation is currently maintained as a focused security-engineering and publication project.

## Before Contributing

Please keep the project boundary in mind:

- **Foundation is complete.**
- Manual v1.0 is an immutable release baseline.
- New product ideas should become separate projects rather than reopening Foundation scope.
- KRYP-BOT-001, KRYP-001, lab provisioning, detection engineering, and AI-security work are tracked as future projects.

## Contribution Workflow

1. Open an issue describing the proposed change.
2. Keep changes small and scoped.
3. Do not commit secrets, credentials, tokens, private keys, or sensitive lab data.
4. For controller/config changes, run:

```bash
python -m unittest discover -s tests/unit -p 'test_*.py' -v
python software/cli/kryp_lab.py validate
python software/cli/kryp_lab.py doctor
```

5. If a change touches publication/release tooling, preserve the v1.0 checksum baseline and document why the change does not mutate the frozen release.

## What Not to Change Directly

Do not silently rewrite or replace:

- the v1.0 release artifacts;
- checksum manifests;
- baseline metadata;
- finalized Chapter 1–31 content;
- released Appendices A–J.

Corrections to the released publication require an explicit maintenance-release decision.
