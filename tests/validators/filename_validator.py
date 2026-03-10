"""
Filename validator for Docker tutorial repository.
Validates that filenames follow the NN-descriptive-name.md pattern.
"""

import re
from pathlib import Path
from typing import List, Tuple


class FilenameValidator:
    """Validates filename patterns in documentation."""
    
    # Pattern: NN-descriptive-name.md (e.g., 01-installation-setup.md)
    NUMBERED_PATTERN = re.compile(r'^\d{2}-[a-z0-9]+(-[a-z0-9]+)*\.md$')
    
    # Step-based naming violations (e.g., step1.md, step-1.md)
    STEP_PATTERN = re.compile(r'step[-_]?\d+', re.IGNORECASE)
    
    def __init__(self, repo_root: Path):
        """Initialize validator with repository root path."""
        self.repo_root = Path(repo_root)
        self.errors = []
        self.warnings = []
    
    def validate(self) -> bool:
        """Run all filename validations. Returns True if valid."""
        self.errors = []
        self.warnings = []
        
        self._check_docs_filenames()
        
        return len(self.errors) == 0
    
    def _check_docs_filenames(self):
        """Check all markdown files in docs/ directory."""
        docs_path = self.repo_root / 'docs'
        
        if not docs_path.exists():
            self.errors.append("docs/ directory does not exist")
            return
        
        # Find all .md files in docs/ subdirectories
        for md_file in docs_path.rglob('*.md'):
            # Skip files in root docs/ directory (like CONTENT_AUDIT.md)
            if md_file.parent == docs_path:
                continue
            
            filename = md_file.name
            
            # Check for step-based naming
            if self.STEP_PATTERN.search(filename):
                rel_path = md_file.relative_to(self.repo_root)
                self.errors.append(
                    f"Step-based naming violation: {rel_path}"
                )
            
            # Check for numbered descriptive pattern
            elif not self.NUMBERED_PATTERN.match(filename):
                rel_path = md_file.relative_to(self.repo_root)
                self.errors.append(
                    f"Invalid filename pattern (expected NN-descriptive-name.md): {rel_path}"
                )
    
    def get_report(self) -> str:
        """Generate validation report."""
        report = ["=" * 60]
        report.append("FILENAME VALIDATION REPORT")
        report.append("=" * 60)
        
        if not self.errors and not self.warnings:
            report.append("\n✓ All filename validations passed!")
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


def validate_filenames(repo_root: Path = Path('.')) -> Tuple[bool, str]:
    """
    Validate filename patterns.
    
    Args:
        repo_root: Path to repository root
        
    Returns:
        Tuple of (is_valid, report_string)
    """
    validator = FilenameValidator(repo_root)
    is_valid = validator.validate()
    report = validator.get_report()
    return is_valid, report


if __name__ == '__main__':
    is_valid, report = validate_filenames()
    print(report)
    exit(0 if is_valid else 1)
