# Security Policy

## Supported Scope

KryptrixLabs Foundation is a defensive cybersecurity education and engineering project. Security reports are welcome for defects in the repository's software, configuration validation, build/release tooling, or documentation that could create unsafe behavior.

The immutable manual v1.0 release is a frozen publication baseline. Substantive content expansion belongs in future projects rather than silent edits to the released baseline.

## Reporting a Vulnerability

Please do **not** publish sensitive vulnerability details in a public issue if exploitation could put users or systems at risk.

For now, contact the project maintainer through the KryptrixLabs GitHub account and provide:

- affected file/component;
- reproducible steps;
- expected versus actual behavior;
- impact assessment;
- any safe proof-of-concept details.

A private security-reporting channel may be enabled later.

## Laboratory Safety Boundaries

Contributions and reports must respect these boundaries:

- authorized systems only;
- no external attack activity;
- no hardcoded credentials or secrets;
- internet access disabled by default for experimental systems;
- non-destructive behavior by default;
- no modification of the frozen v1.0 release baseline without an explicit maintenance-release process.

See `docs/SAFETY-BOUNDARIES.md` for the full policy.
