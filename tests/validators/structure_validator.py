"""
Structure validator for Docker tutorial repository.
Validates directory structure and required files.
"""

import os
from pathlib import Path
from typing import List, Tuple


class StructureValidator:
    """Validates repository structure compliance."""
    
    REQUIRED_DIRS = [
        'docs',
        'docs/01-getting-started',
        'docs/02-fundamentals',
        'docs/03-dockerfiles',
        'docs/04-compose',
        'docs/05-networking',
        'docs/06-volumes',
        'docs/07-optimization',
        'docs/08-security',
        'docs/09-production',
        'examples',
        'examples/basic',
        'examples/multi-stage',
        'examples/compose',
        'examples/networking',
        'examples/production'
    ]
    
    REQUIRED_ROOT_FILES = [
        'README.md',
        'LICENSE',
        'CONTRIBUTING.md',
        '.gitignore'
    ]
    
    LEGACY_DIRS = [
        'Basic Intro',
        'DockerFiles',
        'HowItWorks',
        'OrganizingDocker',
        'PowerWithCompose'
    ]
    
    def __init__(self, repo_root: Path):
        """Initialize validator with repository root path."""
        self.repo_root = Path(repo_root)
        self.errors = []
        self.warnings = []
    
    def validate(self) -> bool:
        """Run all structure validations. Returns True if valid."""
        self.errors = []
        self.warnings = []
        
        self._check_required_directories()
        self._check_required_root_files()
        self._check_legacy_directories()
        
        return len(self.errors) == 0
    
    def _check_required_directories(self):
        """Check that all required directories exist."""
        for dir_path in self.REQUIRED_DIRS:
            full_path = self.repo_root / dir_path
            if not full_path.exists():
                self.errors.append(f"Missing required directory: {dir_path}")
            elif not full_path.is_dir():
                self.errors.append(f"Path exists but is not a directory: {dir_path}")
    
    def _check_required_root_files(self):
        """Check that all required root files exist."""
        for file_name in self.REQUIRED_ROOT_FILES:
            full_path = self.repo_root / file_name
            if not full_path.exists():
                self.errors.append(f"Missing required root file: {file_name}")
            elif not full_path.is_file():
                self.errors.append(f"Path exists but is not a file: {file_name}")
    
    def _check_legacy_directories(self):
        """Check that legacy directories have been removed."""
        for dir_name in self.LEGACY_DIRS:
            full_path = self.repo_root / dir_name
            if full_path.exists():
                self.errors.append(f"Legacy directory still exists: {dir_name}")
    
    def get_report(self) -> str:
        """Generate validation report."""
        report = ["=" * 60]
        report.append("STRUCTURE VALIDATION REPORT")
        report.append("=" * 60)
        
        if not self.errors and not self.warnings:
            report.append("\n✓ All structure validations passed!")
        else:
            if self.errors:
                report.append(f"\n✗ {len(self.errors)} error(s) found:")
                for error in self.errors:
                    report.append(f"  - {error}")
            
            if self.warnings:
                report.append(f"\n⚠ {len(self.warnings)} warning(s):")
                for warning in self.warnings:
                    report.append(f"  - {warning}")
        
        report.append("")
        return "\n".join(report)


def validate_structure(repo_root: Path = Path('.')) -> Tuple[bool, str]:
    """
    Validate repository structure.
    
    Args:
        repo_root: Path to repository root
        
    Returns:
        Tuple of (is_valid, report_string)
    """
    validator = StructureValidator(repo_root)
    is_valid = validator.validate()
    report = validator.get_report()
    return is_valid, report


if __name__ == '__main__':
    is_valid, report = validate_structure()
    print(report)
    exit(0 if is_valid else 1)
