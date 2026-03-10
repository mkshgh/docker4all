"""
Markdown formatter validator for Docker tutorial repository.
Validates markdown formatting standards.
"""

import re
from pathlib import Path
from typing import List, Tuple


class MarkdownValidator:
    """Validates markdown formatting standards."""
    
    # Heading patterns
    HEADING_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    
    # Code block patterns
    FENCED_CODE_PATTERN = re.compile(r'^```(\w+)?\n', re.MULTILINE)
    INDENTED_CODE_PATTERN = re.compile(r'^    \w+', re.MULTILINE)
    
    # Admonition patterns
    ADMONITION_PATTERN = re.compile(r'^>\s*\*\*(Note|Warning|Tip|Important):\*\*', re.MULTILINE)
    
    # List patterns
    BULLET_LIST_PATTERN = re.compile(r'^(\s*)[-*+]\s+', re.MULTILINE)
    NUMBERED_LIST_PATTERN = re.compile(r'^(\s*)(\d+)\.\s+', re.MULTILINE)
    
    def __init__(self, repo_root: Path):
        """Initialize validator with repository root path."""
        self.repo_root = Path(repo_root)
        self.errors = []
        self.warnings = []
        self.files_checked = 0
    
    def validate(self) -> bool:
        """Run all markdown validations. Returns True if valid."""
        self.errors = []
        self.warnings = []
        self.files_checked = 0
        
        self._check_markdown_files()
        
        return len(self.errors) == 0
    
    def _check_markdown_files(self):
        """Check all markdown files."""
        docs_path = self.repo_root / 'docs'
        
        if not docs_path.exists():
            return
        
        for md_file in docs_path.rglob('*.md'):
            self.files_checked += 1
            self._check_file(md_file)
    
    def _check_file(self, file_path: Path):
        """Check a single markdown file."""
        content = file_path.read_text(encoding='utf-8')
        rel_path = file_path.relative_to(self.repo_root)
        
        # Remove code blocks before checking headings to avoid false positives
        # Remove fenced code blocks
        content_no_code = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        # Remove indented code blocks (4 spaces or tab)
        content_no_code = re.sub(r'^(    |\t).*$', '', content_no_code, flags=re.MULTILINE)
        
        self._check_heading_hierarchy(content_no_code, rel_path)
        self._check_code_blocks(content, rel_path)
        self._check_list_formatting(content, rel_path)
    
    def _check_heading_hierarchy(self, content: str, file_path: Path):
        """Check heading hierarchy (no level skipping)."""
        headings = self.HEADING_PATTERN.findall(content)
        
        if not headings:
            return
        
        # First heading should be level 1
        first_level = len(headings[0][0])
        if first_level != 1:
            self.warnings.append(
                f"First heading in {file_path} is level {first_level}, expected level 1"
            )
        
        # Check for level skipping - only when going deeper
        for i in range(1, len(headings)):
            prev_level = len(headings[i-1][0])
            current_level = len(headings[i][0])
            heading_text = headings[i][1]
            
            # Only check for skips when going deeper (increasing level number)
            if current_level > prev_level and current_level > prev_level + 1:
                self.errors.append(
                    f"Heading level skip in {file_path}: "
                    f"from level {prev_level} to {current_level} "
                    f"(heading: '{heading_text}')"
                )
    
    def _check_code_blocks(self, content: str, file_path: Path):
        """Check code block formatting."""
        # Check for indented code blocks (should use fenced)
        indented_blocks = self.INDENTED_CODE_PATTERN.findall(content)
        if indented_blocks:
            self.warnings.append(
                f"Indented code blocks found in {file_path}, "
                f"prefer fenced code blocks with language tags"
            )
        
        # Check fenced code blocks have language tags
        fenced_blocks = self.FENCED_CODE_PATTERN.findall(content)
        for lang in fenced_blocks:
            if not lang:
                self.warnings.append(
                    f"Fenced code block without language tag in {file_path}"
                )
    
    def _check_list_formatting(self, content: str, file_path: Path):
        """Check list formatting consistency."""
        # Check bullet list markers
        bullet_markers = self.BULLET_LIST_PATTERN.findall(content)
        if bullet_markers:
            # Extract just the marker characters
            markers = [m[1] if len(m) > 1 else m for m in bullet_markers]
            unique_markers = set(markers)
            if len(unique_markers) > 1:
                self.warnings.append(
                    f"Inconsistent bullet list markers in {file_path}: "
                    f"found {unique_markers}"
                )
        
        # Check numbered list sequencing
        numbered_items = self.NUMBERED_LIST_PATTERN.findall(content)
        if numbered_items:
            # Group by indentation level
            by_indent = {}
            for indent, number in numbered_items:
                indent_len = len(indent)
                if indent_len not in by_indent:
                    by_indent[indent_len] = []
                by_indent[indent_len].append(int(number))
            
            # Check each indentation level
            for indent_len, numbers in by_indent.items():
                expected = list(range(1, len(numbers) + 1))
                if numbers != expected:
                    self.warnings.append(
                        f"Non-sequential numbered list in {file_path} "
                        f"at indent {indent_len}: {numbers}"
                    )
    
    def get_report(self) -> str:
        """Generate validation report."""
        report = ["=" * 60]
        report.append("MARKDOWN FORMATTING REPORT")
        report.append("=" * 60)
        report.append(f"\nFiles checked: {self.files_checked}")
        
        if not self.errors and not self.warnings:
            report.append("\n✓ All markdown formatting validations passed!")
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


def validate_markdown(repo_root: Path = Path('.')) -> Tuple[bool, str]:
    """
    Validate markdown formatting.
    
    Args:
        repo_root: Path to repository root
        
    Returns:
        Tuple of (is_valid, report_string)
    """
    validator = MarkdownValidator(repo_root)
    is_valid = validator.validate()
    report = validator.get_report()
    return is_valid, report


if __name__ == '__main__':
    is_valid, report = validate_markdown()
    print(report)
    exit(0 if is_valid else 1)
