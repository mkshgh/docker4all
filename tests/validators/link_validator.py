"""
Link validator for Docker tutorial repository.
Validates internal links and checks for .rst references.
"""

import re
from pathlib import Path
from typing import List, Tuple, Set


class LinkValidator:
    """Validates links in markdown documentation."""
    
    # Markdown link pattern: [text](url)
    LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')
    
    # RST file reference pattern
    RST_PATTERN = re.compile(r'\.rst\b')
    
    def __init__(self, repo_root: Path):
        """Initialize validator with repository root path."""
        self.repo_root = Path(repo_root)
        self.errors = []
        self.warnings = []
        self.files_checked = 0
        self.links_checked = 0
    
    def validate(self) -> bool:
        """Run all link validations. Returns True if valid."""
        self.errors = []
        self.warnings = []
        self.files_checked = 0
        self.links_checked = 0
        
        self._check_markdown_links()
        
        return len(self.errors) == 0
    
    def _check_markdown_links(self):
        """Check all links in markdown files."""
        # Check docs/
        docs_path = self.repo_root / 'docs'
        if docs_path.exists():
            for md_file in docs_path.rglob('*.md'):
                self._check_file_links(md_file)
        
        # Check root README.md
        readme = self.repo_root / 'README.md'
        if readme.exists():
            self._check_file_links(readme)
        
        # Check CONTRIBUTING.md
        contributing = self.repo_root / 'CONTRIBUTING.md'
        if contributing.exists():
            self._check_file_links(contributing)
    
    def _check_file_links(self, file_path: Path):
        """Check links in a single markdown file."""
        self.files_checked += 1
        content = file_path.read_text(encoding='utf-8')
        rel_path = file_path.relative_to(self.repo_root)
        
        # Find all markdown links
        for match in self.LINK_PATTERN.finditer(content):
            link_text = match.group(1)
            link_url = match.group(2)
            self.links_checked += 1
            
            # Skip external links (http://, https://, mailto:)
            if link_url.startswith(('http://', 'https://', 'mailto:', '#')):
                continue
            
            # Check for .rst references
            if self.RST_PATTERN.search(link_url):
                self.errors.append(
                    f"RST reference found in {rel_path}: [{link_text}]({link_url})"
                )
                continue
            
            # Check internal link target exists
            self._check_internal_link(file_path, link_url, link_text, rel_path)
    
    def _check_internal_link(self, source_file: Path, link_url: str, 
                            link_text: str, source_rel_path: Path):
        """Check if internal link target exists."""
        # Remove anchor if present
        link_path = link_url.split('#')[0]
        
        if not link_path:
            # Just an anchor link, skip
            return
        
        # Resolve relative to source file's directory
        if link_path.startswith('/'):
            # Absolute path from repo root
            target = self.repo_root / link_path.lstrip('/')
        else:
            # Relative path
            target = (source_file.parent / link_path).resolve()
        
        # Check if target exists
        if not target.exists():
            self.errors.append(
                f"Broken link in {source_rel_path}: [{link_text}]({link_url}) "
                f"-> target does not exist"
            )
    
    def get_report(self) -> str:
        """Generate validation report."""
        report = ["=" * 60]
        report.append("LINK VALIDATION REPORT")
        report.append("=" * 60)
        report.append(f"\nFiles checked: {self.files_checked}")
        report.append(f"Links checked: {self.links_checked}")
        
        if not self.errors and not self.warnings:
            report.append("\n✓ All link validations passed!")
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


def validate_links(repo_root: Path = Path('.')) -> Tuple[bool, str]:
    """
    Validate links in repository.
    
    Args:
        repo_root: Path to repository root
        
    Returns:
        Tuple of (is_valid, report_string)
    """
    validator = LinkValidator(repo_root)
    is_valid = validator.validate()
    report = validator.get_report()
    return is_valid, report


if __name__ == '__main__':
    is_valid, report = validate_links()
    print(report)
    exit(0 if is_valid else 1)
