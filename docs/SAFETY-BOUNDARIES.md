# KryptrixLabs™ Virtual Cybersecurity Laboratory v0.1 — Safety Boundaries & Ethics Policy

| Field | Value |
|---|---|
| **Document ID** | KRYP-DOC-SAFETY-v0.1 |
| **Title** | Laboratory Safety Boundaries, Isolation Policy & Operational Limits |
| **Status** | APPROVED SAFETY SPECIFICATION |
| **Author** | KryptrixLabs™ Security Engineering |

---

## 1. Core Safety Imperatives

The KryptrixLabs Virtual Cybersecurity Laboratory v0.1 is designed exclusively for **educational, defensive, and authorized cybersecurity research**. All operations must strictly adhere to the following 5 safety rules:

1. **Rule 1 — Controlled Isolation**: All experimental virtual machines must operate within designated internal subnets (`MGMT-NET` 192.168.10.0/24 or `TEST-NET` 10.0.20.0/24). Direct routing to external internet networks is `DISABLED_BY_DEFAULT`.
2. **Rule 2 — Zero External Attack Activity**: No script, tool, or process authored within KryptrixLabs may transmit unauthorized network traffic, port scans, or payloads to external IP addresses, domains, or infrastructure.
3. **Rule 3 — Zero Hardcoded Credentials**: No production API keys, passwords, private keys, or tokens may be hardcoded in laboratory configuration files or source code.
4. **Rule 4 — Immutable Baseline Protection**: No laboratory operation, script, or build tool may alter, delete, or overwrite the frozen *KryptrixLabs Cybersecurity Operating Manual v1.0* baseline artifacts (`MANUSCRIPT/`, `APPENDICES/`, `EXPORTS/FINAL_RELEASE_v1.0/`).
5. **Rule 5 — Non-Destructive Default Execution**: Lab control software (`kryp-lab`) must operate in a non-destructive, read-only mode by default. Destructive operations (reset, wipe, destroy) require explicit safety confirmations.

---

## 2. Technical Controls & Verification

| Control Point | Technical Implementation | Verification Method | Status |
|---|---|---|---|
| **Host Isolation** | VMware VMnet1 (Host-Only) & VMnet8 adapter isolation | Network interface audit (`Get-NetAdapter`) | `IMPLEMENTED` |
| **Schema Safety Guard** | `strict_host_isolation: true` required in `lab.yaml` | `python software/cli/kryp_lab.py validate` | `IMPLEMENTED` |
| **Secret Scanning** | Automated regex pattern scan for plain-text keys/passwords | `LabController.validate_config()` check | `IMPLEMENTED` |
| **v1.0 Baseline Lock** | SHA-256 baseline verification script | `python verify_release_integrity.py` | `IMPLEMENTED` |
