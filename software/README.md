# KryptrixLabs™ Software Engineering Workspace (`software/`)

## Overview
This directory contains the Python core controller engine, command-line interface, agents, and integration components for KryptrixLabs software projects.

## Directory Structure
- `core/`: Core business logic engines (`lab_controller.py`) (`IMPLEMENTED`).
- `cli/`: Command-line entry points (`kryp_lab.py`) (`IMPLEMENTED`).
- `agents/`: Telemetry & monitoring agent prototypes (`PLANNED`).
- `integrations/`: Third-party integration adapters (`PLANNED`).

## CLI Interface Usage
```bash
# Check environment health
python software/cli/kryp_lab.py status

# Run dependency diagnosis
python software/cli/kryp_lab.py doctor

# Display configured inventory
python software/cli/kryp_lab.py inventory

# Validate schema and safety rules
python software/cli/kryp_lab.py validate
```
