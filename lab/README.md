# KryptrixLabs™ Virtual Cybersecurity Laboratory Workspace (`lab/`)

## Overview
This directory contains the declarative architecture, network topologies, machine specifications, configuration files, evidence storage, and snapshot manifests for the KryptrixLabs Virtual Cybersecurity Laboratory v0.1.

## Directory Structure
- `architecture/`: High-level topology diagrams and network design specifications (`IMPLEMENTED`).
- `configs/`: Machine-readable lab configuration manifests (`lab.yaml`, `lab.example.yaml`) (`IMPLEMENTED`).
- `infrastructure/`: Hypervisor provisioning templates (`PLANNED`).
- `networks/`: Subnet and virtual adapter definitions (`PLANNED`).
- `machines/`: VM definitions and hardware allocation profiles (`PLANNED`).
- `services/`: Lab service definitions (Syslog, KRYP-001 SyncBridge) (`PLANNED`).
- `evidence/`: Telemetry log captures and experiment evidence (`PLANNED`).
- `snapshots/`: Machine snapshot manifests and restore points (`PLANNED`).

## Quick Usage
Validate the lab configuration:
```bash
python ../software/cli/kryp_lab.py validate
```
