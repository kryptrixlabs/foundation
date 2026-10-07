#!/usr/bin/env python3
"""
KryptrixLabs™ Virtual Cybersecurity Laboratory v0.1 — Unit Test Suite
File: tests/unit/test_kryp_lab.py
Purpose: Automated unit testing for LabController, configuration validation, dependency detection, CLI interface, and safe failure modes.
"""

import os
import sys
import unittest
import tempfile
import shutil
import json

# Ensure software directory is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from software.core.lab_controller import LabController

class TestKrypLabController(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.default_config_path = os.path.join(self.base_dir, 'lab', 'configs', 'lab.yaml')
        self.controller = LabController(self.default_config_path)

    def test_01_configuration_parsing(self):
        """Verify clean loading and parsing of lab.yaml."""
        data = self.controller.load_config()
        self.assertIsInstance(data, dict)
        self.assertIn("lab", data)
        self.assertIn("networks", data)
        self.assertIn("machines", data)
        self.assertEqual(data["lab"]["version"], "0.1.0")

    def test_02_configuration_validation_success(self):
        """Verify that default lab.yaml passes validation."""
        val_res = self.controller.validate_config()
        self.assertTrue(val_res["valid"], f"Validation failed with errors: {val_res['errors']}")
        self.assertGreaterEqual(val_res["network_count"], 1)
        self.assertGreaterEqual(val_res["machine_count"], 1)

    def test_03_status_reporting(self):
        """Verify non-destructive status reporting."""
        status = self.controller.get_status()
        self.assertEqual(status["version"], "0.1.0")
        self.assertIn("python_version", status)
        self.assertIn("operating_system", status)
        self.assertIn("hypervisor_availability", status)
        self.assertTrue(status["config_file_present"])

    def test_04_doctor_check(self):
        """Verify system health doctor report generation."""
        doc_report = self.controller.get_doctor_report()
        self.assertIn("doctor_status", doc_report)
        self.assertIsInstance(doc_report["checks"], list)
        self.assertGreaterEqual(len(doc_report["checks"]), 3)

    def test_05_inventory_generation(self):
        """Verify structured inventory payload."""
        inv = self.controller.get_inventory()
        self.assertIn("lab", inv)
        self.assertIn("networks", inv)
        self.assertIn("machines", inv)
        self.assertIn("services", inv)
        self.assertIn("safety_policy", inv)

    def test_06_invalid_configuration_handling(self):
        """Verify failure behavior on invalid configuration schema."""
        temp_dir = tempfile.mkdtemp()
        try:
            bad_config_path = os.path.join(temp_dir, 'bad_lab.yaml')
            with open(bad_config_path, 'w', encoding='utf-8') as f:
                f.write("""
lab:
  name: "Bad Config Lab"
# Missing version
safety:
  strict_host_isolation: false # Violation!
networks:
  - name: "MGMT"
machines:
  - id: "VM-1"
    network: "NON_EXISTENT_NET" # Discrepancy!
""")
            bad_controller = LabController(bad_config_path)
            val_res = bad_controller.validate_config()
            self.assertFalse(val_res["valid"])
            self.assertGreaterEqual(len(val_res["errors"]), 1)
        finally:
            shutil.rmtree(temp_dir)

    def test_07_missing_file_failure(self):
        """Verify safe handling of missing configuration file."""
        bad_controller = LabController("/non/existent/path/lab.yaml")
        with self.assertRaises(FileNotFoundError):
            bad_controller.load_config()

if __name__ == '__main__':
    unittest.main()
