# KryptrixLabs™ Virtual Cybersecurity Laboratory v0.1 — Development Workflow

| Field | Value |
|---|---|
| **Document ID** | KRYP-DOC-DEV-WORKFLOW-v0.1 |
| **Title** | Laboratory Engineering Development & QA Workflow |
| **Status** | APPROVED WORKFLOW SPECIFICATION |
| **Author** | KryptrixLabs™ Security Engineering |

---

## 1. Controlled Development Lifecycle

All software, automation scripts, and lab configurations must follow a strict, reproducible engineering lifecycle:

```text
[ Step 1: Feature / Lab Design ] ──> [ Step 2: Local Code / Manifest Authoring ]
                                                       │
[ Step 4: System QA Suite ] <── [ Step 3: Automated Unit Testing (kryp-lab) ]
          │
          ▼
[ Step 5: Version Control Verification ] ──> [ Step 6: Baseline Immutability Audit ]
```

---

## 2. Step-by-Step Engineering Protocol

### Step 1: Architecture & Schema Design
- All new virtual machines, subnets, or services must first be defined in `lab/configs/lab.yaml`.
- Ensure strict compliance with trust boundaries (`strict_host_isolation: true`).

### Step 2: Local Code & Configuration Authoring
- Place core controller components in `software/core/`.
- Place CLI commands in `software/cli/`.
- Place configuration files in `lab/configs/`.
- **Zero Secrets Rule**: Use `${ENVIRONMENT_VARIABLE}` syntax; never hardcode passwords, API keys, or private tokens.

### Step 3: Local Unit Testing & Validation
Before submitting any changes, execute the lab controller validation suite:

```bash
python software/cli/kryp_lab.py validate
python software/cli/kryp_lab.py doctor
python tests/unit/test_kryp_lab.py
```

### Step 4: Repository Quality & Immutability Verification
Ensure that v1.0 release baseline artifacts have not been touched or altered:

```bash
python validate_repository.py
python verify_release_integrity.py
```

---

## 3. Implementation Status Summary

* **Lab Controller CLI**: `IMPLEMENTED` (`kryp-lab status`, `doctor`, `inventory`, `validate`)
* **Unit Testing Suite**: `IMPLEMENTED` (`tests/unit/test_kryp_lab.py`)
* **v1.0 Immutability Protection**: `IMPLEMENTED` (Verified by `verify_release_integrity.py`)
* **Automated VM Provisioning**: `PLANNED` (Targeted for v0.2)
