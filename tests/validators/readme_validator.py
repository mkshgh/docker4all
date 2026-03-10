"""
README validator for Docker tutorial repository.
Validates README.md completeness and structure.
"""

import re
from pathlib import Path
from typing import List, Tuple, Set


class ReadmeValidator:
    """Validates README.md structure and content."""
    
    # Required sections (case-insensitive)
    REQUIRED_SECTIONS = [
        'overview',
        'objective',
        'prerequisite',
        'setup',
        'contribution',
        'contributing',
        'license'
    ]
    
    # Badge patterns
    BADGE_PATTERN = re.compile(r'!\[([^\]]*)\]\(([^\)]+)\)')
    
    def __init__(self, repo_root: Path):
        """Initialize validator with repository root path."""
        self.repo_root = Path(repo_root)
        self.errors = []
        self.warnings = []
    
    def validate(self) -> bool:
        """Run all README validations. Returns True if valid."""
        self.errors = []
        self.warnings = []
        
        readme_path = self.repo_root / 'README.md'
        
        if not readme_path.exists():
            self.errors.append("README.md does not exist")
            return False
        
        content = readme_path.read_text(encoding='utf-8')
        
        self._check_required_sections(content)
        self._check_badges(content)
        self._check_table_of_contents(content)
        
        return len(self.errors) == 0
    
    def _check_required_sections(self, content: str):
        """Check that required sections are present."""
        content_lower = content.lower()
        
        # Check for overview/objectives
        has_overview = any(term in content_lower for term in ['overview', 'about', 'introduction'])
        if not has_overview:
            self.errors.append("README missing overview/introduction section")
        
        has_objectives = 'objective' in content_lower or 'goal' in content_lower
        if not has_objectives:
            self.warnings.append("README missing learning objectives section")
        
        # Check for prerequisites
        has_prerequisites = 'prerequisite' in content_lower or 'requirement' in content_lower
        if not has_prerequisites:
            self.errors.append("README missing prerequisites section")
        
        # Check for setup/installation
        has_setup = any(term in content_lower for term in ['setup', 'installation', 'getting started'])
        if not has_setup:
            self.errors.append("README missing setup/installation section")
        
        # Check for contribution guidelines
        has_contributing = 'contribut' in content_lower
        if not has_contributing:
            self.errors.append("README missing contribution guidelines or link")
        
        # Check for license
        has_license = 'license' in content_lower
        if not has_license:
            self.errors.append("README missing license information")
    
    def _check_badges(self, content: str):
        """Check for badges."""
        badges = self.BADGE_PATTERN.findall(content)
        
        if not badges:
            self.warnings.append("README has no badges")
            return
        
        badge_texts = [text.lower() for text, url in badges]
        
        # Check for license badge
        has_license_badge = any('license' in text for text in badge_texts)
        if not has_license_badge:
            self.warnings.append("README missing license badge")
        
        # Check for version/compatibility badge
        has_version_badge = any(
            term in text 
            for text in badge_texts 
            for term in ['docker', 'version', 'compatibility']
        )
        if not has_version_badge:
            self.warnings.append("README missing Docker version compatibility badge")
    
    def _check_table_of_contents(self, content: str):
        """Check for table of contents with links."""
        content_lower = content.lower()
        
        # Check for TOC section
        has_toc = any(term in content_lower for term in [
            'table of contents',
            'contents',
            '## topics',
            '## modules',
            '## tutorials'
        ])
        
        if not has_toc:
            self.warnings.append("README missing table of contents")
            return
        
        # Check for links to docs/
        has_doc_links = 'docs/' in content or '../docs/' in content
        if not has_doc_links:
            self.warnings.append("README table of contents missing links to documentation")
    
    def get_report(self) -> str:
        """Generate validation report."""
        report = ["=" * 60]
        report.append("README VALIDATION REPORT")
        report.append("=" * 60)
        
        if not self.errors and not self.warnings:
            report.append("\n✓ All README validations passed!")
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


def validate_readme(repo_root: Path = Path('.')) -> Tuple[bool, str]:
    """
    Validate README.md.
    
    Args:
        repo_root: Path to repository root
        
    Returns:
        Tuple of (is_valid, report_string)
    """
    validator = ReadmeValidator(repo_root)
    is_valid = validator.validate()
    report = validator.get_report()
    return is_valid, report


if __name__ == '__main__':
    is_valid, report = validate_readme()
    print(report)
    exit(0 if is_valid else 1)
