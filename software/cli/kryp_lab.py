#!/usr/bin/env python3
"""
KryptrixLabs™ Virtual Cybersecurity Laboratory v0.1 — CLI Entry Point
File: software/cli/kryp_lab.py
Purpose: Command-line interface for Kryptrix Lab Controller supporting status, doctor, inventory, and validate commands.
"""

import os
import sys
import argparse
import json

# Add software root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.lab_controller import LabController

def main():
    parser = argparse.ArgumentParser(
        prog="kryp-lab",
        description="KryptrixLabs™ Virtual Cybersecurity Laboratory Controller v0.1 CLI"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: status
    parser_status = subparsers.add_parser("status", help="Display environment health and hypervisor status")
    parser_status.add_argument("--json", action="store_true", help="Output status as JSON")

    # Command: doctor
    parser_doctor = subparsers.add_parser("doctor", help="Run health check and dependency diagnosis")
    parser_doctor.add_argument("--json", action="store_true", help="Output doctor report as JSON")

    # Command: inventory
    parser_inventory = subparsers.add_parser("inventory", help="List configured networks, machines, and services")
    parser_inventory.add_argument("--json", action="store_true", help="Output inventory as JSON")

    # Command: validate
    parser_validate = subparsers.add_parser("validate", help="Validate lab.yaml configuration and safety boundaries")
    parser_validate.add_argument("--json", action="store_true", help="Output validation results as JSON")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    controller = LabController()

    if args.command == "status":
        res = controller.get_status()
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print("=" * 60)
            print("KryptrixLabs™ Lab Controller v0.1 — Status Report")
            print("=" * 60)
            print(f"Lab Name       : {res['lab_name']}")
            print(f"Controller Ver : {res['version']}")
            print(f"Python Engine  : {res['python_version']}")
            print(f"Host OS        : {res['operating_system']}")
            print("\nHypervisor Availability:")
            for hyp, st in res['hypervisor_availability'].items():
                print(f"  - {hyp:<20}: {st}")
            print(f"\nConfig File Present : {res['config_file_present']}")
            print("=" * 60)

    elif args.command == "doctor":
        res = controller.get_doctor_report()
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print("=" * 60)
            print("KryptrixLabs™ Lab Controller v0.1 — Doctor Report")
            print("=" * 60)
            print(f"System Health Status : {res['doctor_status']}\n")
            for c in res['checks']:
                symbol = "[PASS]" if c['status'] == "PASS" else f"[{c['status']}]"
                print(f"  {symbol:<8} {c['item']:<30} : {c['details']}")
            print("=" * 60)

    elif args.command == "inventory":
        res = controller.get_inventory()
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print("=" * 60)
            print("KryptrixLabs™ Lab Controller v0.1 — Lab Inventory")
            print("=" * 60)
            print(f"Lab Title : {res['lab'].get('name', 'N/A')} (v{res['lab'].get('version', '0.1.0')})")
            print("\nConfigured Networks:")
            for net in res['networks']:
                print(f"  - [{net.get('name')}] Subnet: {net.get('subnet')} ({net.get('adapter_type')})")
            print("\nConfigured Machines:")
            for vm in res['machines']:
                print(f"  - [{vm.get('id')}] {vm.get('name'):<32} IP: {vm.get('ip_address'):<15} Role: {vm.get('role')}")
            print("\nConfigured Services:")
            for svc in res['services']:
                print(f"  - [{svc.get('name')}] Target: {svc.get('machine')} Port: {svc.get('port')}/{svc.get('protocol')}")
            print("=" * 60)

    elif args.command == "validate":
        res = controller.validate_config()
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print("=" * 60)
            print("KryptrixLabs™ Lab Controller v0.1 — Configuration Validation")
            print("=" * 60)
            print(f"Validation Result : {'PASSED (VALID)' if res['valid'] else 'FAILED (INVALID)'}")
            print(f"Networks Verified : {res['network_count']}")
            print(f"Machines Verified : {res['machine_count']}")
            print(f"Services Verified : {res['service_count']}")
            if res['warnings']:
                print("\nWarnings:")
                for w in res['warnings']:
                    print(f"  - [WARN] {w}")
            if res['errors']:
                print("\nErrors:")
                for e in res['errors']:
                    print(f"  - [ERROR] {e}")
                sys.exit(1)
            else:
                print("\n[SUCCESS] Lab configuration adheres strictly to safety and schema rules.")
            print("=" * 60)

if __name__ == '__main__':
    main()
