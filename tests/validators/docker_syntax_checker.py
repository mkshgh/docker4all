"""
Docker syntax checker for Docker tutorial repository.
Validates modern Docker syntax usage and detects legacy patterns.
"""

import re
from pathlib import Path
from typing import List, Tuple, Dict


class DockerSyntaxChecker:
    """Validates modern Docker syntax in documentation and examples."""
    
    # Legacy patterns to detect
    LEGACY_PATTERNS = {
        'docker-compose command': re.compile(r'`docker-compose\s'),  # Command usage in backticks
        'docker-compose standalone': re.compile(r'\bdocker-compose\b(?!-plugin)'),  # Standalone, not plugin
        '-v flag': re.compile(r'\s-v\s+[^\s]+:[^\s]+'),
        'version in compose': re.compile(r'^version:\s*["\']?\d+', re.MULTILINE),
    }
    
    # Deprecated commands
    DEPRECATED_COMMANDS = [
        'docker-compose',
        'docker rm -f',  # Should use docker rm with proper cleanup
    ]
    
    def __init__(self, repo_root: Path):
        """Initialize checker with repository root path."""
        self.repo_root = Path(repo_root)
        self.errors = []
        self.warnings = []
        self.files_checked = 0
    
    def validate(self) -> bool:
        """Run all syntax checks. Returns True if valid."""
        self.errors = []
        self.warnings = []
        self.files_checked = 0
        
        self._check_markdown_files()
        self._check_yaml_files()
        self._check_dockerfile_files()
        
        return len(self.errors) == 0
    
    def _check_markdown_files(self):
        """Check Docker syntax in markdown documentation."""
        docs_path = self.repo_root / 'docs'
        
        if not docs_path.exists():
            return
        
        for md_file in docs_path.rglob('*.md'):
            self.files_checked += 1
            content = md_file.read_text(encoding='utf-8')
            rel_path = md_file.relative_to(self.repo_root)
            
            self._check_content(content, rel_path)
    
    def _check_yaml_files(self):
        """Check Docker syntax in compose files."""
        examples_path = self.repo_root / 'examples'
        
        if not examples_path.exists():
            return
        
        for yaml_file in examples_path.rglob('*.yaml'):
            self.files_checked += 1
            content = yaml_file.read_text(encoding='utf-8')
            rel_path = yaml_file.relative_to(self.repo_root)
            
            self._check_content(content, rel_path)
        
        for yml_file in examples_path.rglob('*.yml'):
            self.files_checked += 1
            content = yml_file.read_text(encoding='utf-8')
            rel_path = yml_file.relative_to(self.repo_root)
            
            self._check_content(content, rel_path)
    
    def _check_dockerfile_files(self):
        """Check Docker syntax in Dockerfiles."""
        examples_path = self.repo_root / 'examples'
        
        if not examples_path.exists():
            return
        
        for dockerfile in examples_path.rglob('Dockerfile*'):
            if dockerfile.is_file():
                self.files_checked += 1
                content = dockerfile.read_text(encoding='utf-8')
                rel_path = dockerfile.relative_to(self.repo_root)
                
                self._check_content(content, rel_path)
    
    def _check_content(self, content: str, file_path: Path):
        """Check content for legacy Docker syntax."""
        # Check for docker-compose command (should be docker compose)
        if self.LEGACY_PATTERNS['docker-compose command'].search(content):
            self.errors.append(
                f"Legacy 'docker-compose' command found in {file_path} "
                f"(use 'docker compose' instead)"
            )
        
        # Check for standalone docker-compose (not plugin)
        if self.LEGACY_PATTERNS['docker-compose standalone'].search(content):
            # Additional check: make sure it's not in a note explaining the difference
            if '(not `docker-compose`)' not in content and 'not docker-compose' not in content.lower():
                self.errors.append(
                    f"Legacy 'docker-compose' found in {file_path} "
                    f"(use 'docker compose' instead)"
                )
        
        # Check for -v flag (should use --mount)
        if self.LEGACY_PATTERNS['-v flag'].search(content):
            self.errors.append(
                f"Legacy '-v' flag found in {file_path} "
                f"(use '--mount' syntax instead)"
            )
        
        # Check for version field in compose files
        if str(file_path).endswith(('.yaml', '.yml')):
            if self.LEGACY_PATTERNS['version in compose'].search(content):
                self.errors.append(
                    f"Legacy 'version:' field found in {file_path} "
                    f"(Compose v2 doesn't require version field)"
                )
    
    def get_report(self) -> str:
        """Generate validation report."""
        report = ["=" * 60]
        report.append("DOCKER SYNTAX VALIDATION REPORT")
        report.append("=" * 60)
        report.append(f"\nFiles checked: {self.files_checked}")
        
        if not self.errors and not self.warnings:
            report.append("\n✓ All Docker syntax validations passed!")
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


def validate_docker_syntax(repo_root: Path = Path('.')) -> Tuple[bool, str]:
    """
    Validate Docker syntax in repository.
    
    Args:
        repo_root: Path to repository root
        
    Returns:
        Tuple of (is_valid, report_string)
    """
    checker = DockerSyntaxChecker(repo_root)
    is_valid = checker.validate()
    report = checker.get_report()
    return is_valid, report


if __name__ == '__main__':
    is_valid, report = validate_docker_syntax()
    print(report)
    exit(0 if is_valid else 1)
