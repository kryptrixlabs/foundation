# KryptrixLabs™ Virtual Cybersecurity Laboratory v0.1 — Architecture Specification

| Field | Value |
|---|---|
| **Document ID** | KRYP-DOC-LAB-ARCH-v0.1 |
| **Title** | Virtual Cybersecurity Laboratory v0.1 Architecture Specification |
| **Status** | APPROVED ARCHITECTURE SPECIFICATION |
| **Implementation State** | `IMPLEMENTED` (Config Schema, Controller Engine, Validation CLI) / `PLANNED` (VMware VM Provisioning) |
| **Target Hypervisor** | VMware Workstation Pro (Host VMnet Adapters VMnet1 & VMnet8) |
| **Author** | KryptrixLabs™ Security Engineering |

---

## 1. Laboratory Purpose & Objectives

The KryptrixLabs Virtual Cybersecurity Laboratory v0.1 provides a controlled, reproducible, host-isolated virtualization environment for developing, testing, observing, and validating defensive security tools, telemetry collectors, and architectural patterns.

It establishes:
1. A safe, deterministic sandbox for testing security code without external network exposure.
2. A two-tier isolated network model separating management traffic from experimental sensor and target traffic.
3. Machine-readable, declarative configuration (`lab/configs/lab.yaml`) governed by automated CLI validation (`kryp-lab validate`).

---

## 2. Trust Boundaries & Safety Model

```text
                                HOST WORKSTATION (Windows 11 Pro)
                                                |
        ================================================================================
        [TRUST BOUNDARY 1: HOST ISOLATION]
        ================================================================================
                                                |
                                KRYPTRIXLABS LAB ENVIRONMENT
                                                |
              +---------------------------------+---------------------------------+
              |                                                                   |
     MANAGEMENT NETWORK                                                   TEST NETWORK
    (VMnet1 / Host-Only)                                             (VMnet8 / Host-Isolated NAT)
    192.168.10.0/24                                                   10.0.20.0/24
    Trust Level: HIGH                                                 Trust Level: ISOLATED
              |                                                                   |
     +-----------------+                                         +----------------+----------------+
     |                 |                                         |                |                |
 VM-MGMT-01       Lab Controller                               VM-TGT-01        VM-SNS-01        Service
 Controller       (Python Engine)                              Target System    Telemetry Sensor  Target
 (192.168.10.10)  (Host/Guest CLI)                             (10.0.20.50)     (10.0.20.100)     (10.0.20.x)
```

### Trust Boundary Rules:
- **Host Isolation**: The virtual laboratory is completely isolated from the primary host operating system. No guest VM has administrative privileges or raw hypervisor access to the Windows host.
- **Air-Gapped Management Network (VMnet1)**: `MGMT-NET` (192.168.10.0/24) is strictly host-only. It has zero routing or gateway connectivity to the external internet.
- **Isolated Test Network (VMnet8)**: `TEST-NET` (10.0.20.0/24) is restricted to inter-VM communication and local telemetry logging. Outbound internet access is `DISABLED_BY_DEFAULT`.
- **Zero Live Attack Activity**: The laboratory operates strictly on authorized, internal test systems controlled by KryptrixLabs.

---

## 3. Network Segmentation & Architecture

| Network Name | Subnet | Adapter Type | Trust Level | DHCP | Purpose | Implementation State |
|---|---|---|---|---|---|---|
| **MGMT-NET** | `192.168.10.0/24` | VMware VMnet1 (Host-Only) | **HIGH** | Disabled | Controller node management & secure daemon interface | `IMPLEMENTED` (Schema) / `PLANNED` (VM) |
| **TEST-NET** | `10.0.20.0/24` | VMware VMnet8 (NAT / Host Isolated) | **ISOLATED** | Enabled | Defensive target testing & sensor log collection | `IMPLEMENTED` (Schema) / `PLANNED` (VM) |

---

## 4. Node & Virtual Machine Responsibilities

| Machine ID | Name | Subnet / IP | OS Target | vCPU / RAM / Disk | Role & Responsibility | Status |
|---|---|---|---|---|---|---|
| **VM-MGMT-01** | Kryptrix Controller Node | `192.168.10.10` | Ubuntu Server 24.04 LTS | 2 vCPU / 2048 MB / 10 GB | Orchestrates lab health, state reporting, and secure KRYP-001 daemon hosting | `PLANNED` |
| **VM-TGT-01** | Defensive Target Workstation | `10.0.20.50` | Alpine Linux 3.20 | 1 vCPU / 1024 MB / 5 GB | Defensive application target and benign artifact system | `PLANNED` |
| **VM-SNS-01** | Telemetry Sensor Node | `10.0.20.100` | Ubuntu Server 24.04 LTS | 1 vCPU / 1024 MB / 5 GB | Centralized Syslog collector and log ingestion endpoint | `PLANNED` |

---

## 5. Logging, Telemetry & Reset Strategy

1. **Logging Architecture**:
   - Centralized UDP/514 Syslog collector on `VM-SNS-01` (`10.0.20.100`).
   - Local CLI log aggregation stored in `lab/evidence/`.
2. **Snapshot & State Reset Strategy**:
   - Clean baseline snapshots created immediately following initial VM installation.
   - Experiments must return VMs to baseline snapshot prior to committing results.
3. **Secrets & Credentials Policy**:
   - Zero hardcoded passwords or API keys in configuration manifests (`lab/configs/lab.yaml`).
   - Automated CLI secret checks enforce placeholder syntax (`${ENV_VAR}`).

---

## 6. Implementation Matrix

| Component | Status | Description |
|---|---|---|
| Declarative Schema (`lab/configs/lab.yaml`) | `IMPLEMENTED` | Machine-readable topology and machine specification. |
| Lab Controller Engine (`software/core/lab_controller.py`) | `IMPLEMENTED` | Python management class with validation, status, doctor, and inventory functions. |
| CLI Tooling (`software/cli/kryp_lab.py`) | `IMPLEMENTED` | Executable CLI supporting `status`, `doctor`, `inventory`, `validate`. |
| Unit Test Suite (`tests/unit/test_kryp_lab.py`) | `IMPLEMENTED` | 7 automated unit tests covering parser, schema validator, and error handling. |
| VMware Hypervisor Environment | `PROPOSED` / `PLANNED` | VMware Workstation VMnet1/VMnet8 hypervisor integration. |
