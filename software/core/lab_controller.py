#!/usr/bin/env python3
"""
KryptrixLabs™ Virtual Cybersecurity Laboratory v0.1 — Core Controller Engine
File: software/core/lab_controller.py
Purpose: Provides configuration parsing, environment diagnostics, dependency verification,
         inventory generation, and safety validation for KryptrixLabs Lab v0.1.
"""

import os
import sys
import platform
import shutil
import json
import re

class LabController:
    """Core management class for KryptrixLabs Lab v0.1."""

    def __init__(self, config_path=None):
        if config_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            config_path = os.path.join(base_dir, 'lab', 'configs', 'lab.yaml')
        self.config_path = config_path
        self.raw_config_text = ""
        self.config_data = {}

    def load_config(self):
        """Loads and parses the lab configuration file safely."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Lab configuration file not found at: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.raw_config_text = f.read()

        # Parse key structural blocks using lightweight regex/dict parsing
        self.config_data = self._parse_simple_yaml(self.raw_config_text)
        return self.config_data

    def _parse_simple_yaml(self, text):
        """Minimal dependency-free parser for lab.yaml structure."""
        data = {
            "lab": {},
            "environment": {},
            "networks": [],
            "machines": [],
            "services": [],
            "monitoring": {},
            "safety": {}
        }
        
        current_section = None
        current_item = None
        
        for line in text.splitlines():
            line_str = line.strip()
            if not line_str or line_str.startswith("#"):
                continue
            
            # Check section header
            if line.endswith(":") and not line_str.startswith("-"):
                sec_name = line_str.rstrip(":").strip()
                if sec_name in data:
                    current_section = sec_name
                    current_item = None
                continue
            
            if current_section in ["lab", "environment", "monitoring", "safety"]:
                if ":" in line_str:
                    k, v = line_str.split(":", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if v.lower() == 'true': v = True
                    elif v.lower() == 'false': v = False
                    elif v.isdigit(): v = int(v)
                    data[current_section][k] = v

            elif current_section in ["networks", "machines", "services"]:
                if line_str.startswith("- "):
                    current_item = {}
                    data[current_section].append(current_item)
                    line_str = line_str[2:].strip()
                
                if current_item is not None and ":" in line_str:
                    k, v = line_str.split(":", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if v.lower() == 'true': v = True
                    elif v.lower() == 'false': v = False
                    elif v.isdigit(): v = int(v)
                    current_item[k] = v

        return data

    def validate_config(self):
        """Validates configuration rules, safety boundaries, and IP structures."""
        if not self.config_data:
            self.load_config()

        errors = []
        warnings = []

        # 1. Validate mandatory lab metadata
        lab_meta = self.config_data.get("lab", {})
        if not lab_meta.get("name"):
            errors.append("Missing required field 'lab.name'")
        if not lab_meta.get("version"):
            errors.append("Missing required field 'lab.version'")

        # 2. Validate safety policy
        safety = self.config_data.get("safety", {})
        if safety.get("internet_access") != "DISABLED_BY_DEFAULT":
            warnings.append("Safety Policy Warning: 'internet_access' should be 'DISABLED_BY_DEFAULT'")
        if not safety.get("strict_host_isolation"):
            errors.append("Safety Boundary Violation: 'strict_host_isolation' must be enabled (true)")

        # 3. Check for hardcoded credentials
        secret_patterns = [r'password\s*:\s*["\']?(?![${\s])[^\s"\']+', r'api_key\s*:\s*["\']?(?![${\s])[^\s"\']+']
        for pattern in secret_patterns:
            if re.search(pattern, self.raw_config_text, re.IGNORECASE):
                errors.append("Security Violation: Hardcoded password or API key detected in lab.yaml!")

        # 4. Validate network definitions
        networks = self.config_data.get("networks", [])
        if not networks:
            errors.append("No networks defined under 'networks'")

        # 5. Validate machine network assignments
        net_names = {n.get("name") for n in networks if n.get("name")}
        for vm in self.config_data.get("machines", []):
            if vm.get("network") and vm.get("network") not in net_names:
                errors.append(f"Machine '{vm.get('id')}' assigned to non-existent network '{vm.get('network')}'")

        is_valid = len(errors) == 0
        return {
            "valid": is_valid,
            "errors": errors,
            "warnings": warnings,
            "network_count": len(networks),
            "machine_count": len(self.config_data.get("machines", [])),
            "service_count": len(self.config_data.get("services", []))
        }

    def get_status(self):
        """Returns non-destructive environment health status."""
        python_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        os_info = f"{platform.system()} {platform.release()} ({platform.machine()})"

        # Check hypervisor commands
        vbox_path = shutil.which("VBoxManage")
        vmware_path = shutil.which("vmware")
        wsl_path = shutil.which("wsl")
        docker_path = shutil.which("docker")
        git_path = shutil.which("git")

        return {
            "lab_name": "KryptrixLabs Virtual Cybersecurity Laboratory",
            "version": "0.1.0",
            "python_version": python_ver,
            "operating_system": os_info,
            "hypervisor_availability": {
                "vmware_workstation": "INSTALLED (Adapters Active)" if (vmware_path or os.path.exists("C:\\Program Files (x86)\\VMware\\VMware Workstation")) else "NOT_FOUND",
                "virtualbox": "INSTALLED" if vbox_path else "NOT_INSTALLED",
                "wsl2": "AVAILABLE" if wsl_path else "NOT_INSTALLED",
                "docker": "AVAILABLE" if docker_path else "NOT_INSTALLED"
            },
            "toolchain": {
                "git": "INSTALLED" if git_path else "NOT_INSTALLED",
                "python": f"INSTALLED ({python_ver})"
            },
            "config_file_present": os.path.exists(self.config_path)
        }

    def get_doctor_report(self):
        """Performs safe health check and returns dependency diagnosis."""
        status = self.get_status()
        checks = []

        # Check Python version >= 3.10
        if sys.version_info >= (3, 10):
            checks.append({"item": "Python Version", "status": "PASS", "details": status["python_version"]})
        else:
            checks.append({"item": "Python Version", "status": "WARN", "details": f"Python {status['python_version']} (Recommend >= 3.10)"})

        # Check Git
        if status["toolchain"]["git"].startswith("INSTALLED"):
            checks.append({"item": "Git Version Control", "status": "PASS", "details": "Git executable detected in PATH"})
        else:
            checks.append({"item": "Git Version Control", "status": "FAIL", "details": "Git not found in PATH"})

        # Check Hypervisor Target
        if status["hypervisor_availability"]["vmware_workstation"] != "NOT_FOUND":
            checks.append({"item": "Virtualization Hypervisor", "status": "PASS", "details": "VMware Workstation environment detected"})
        else:
            checks.append({"item": "Virtualization Hypervisor", "status": "WARN", "details": "VMware / VirtualBox executable not in PATH"})

        # Check Lab Configuration
        val_res = self.validate_config()
        if val_res["valid"]:
            checks.append({"item": "Lab Configuration Integrity", "status": "PASS", "details": f"lab.yaml valid ({val_res['machine_count']} machines, {val_res['network_count']} networks)"})
        else:
            checks.append({"item": "Lab Configuration Integrity", "status": "FAIL", "details": f"Errors: {', '.join(val_res['errors'])}"})

        return {
            "doctor_status": "HEALTHY" if all(c["status"] in ["PASS", "WARN"] for c in checks) else "DEGRADED",
            "checks": checks
        }

    def get_inventory(self):
        """Returns structured inventory of networks, machines, and services."""
        if not self.config_data:
            self.load_config()

        return {
            "lab": self.config_data.get("lab", {}),
            "networks": self.config_data.get("networks", []),
            "machines": self.config_data.get("machines", []),
            "services": self.config_data.get("services", []),
            "safety_policy": self.config_data.get("safety", {})
        }
