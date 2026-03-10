"""
Topic coverage checker for Docker tutorial repository.
Validates that all required Docker topics are covered.
"""

from pathlib import Path
from typing import List, Tuple, Dict, Set


class TopicCoverageChecker:
    """Validates topic coverage completeness."""
    
    # Required topics from Requirements 3.1-3.15
    REQUIRED_TOPICS = {
        'docker-engine': ['engine', 'daemon', 'cli', 'architecture'],
        'dockerfile-basics': ['dockerfile', 'instruction', 'layer', 'optimization'],
        'buildkit': ['buildkit', 'build cache', 'cache mount'],
        'multi-stage': ['multi-stage', 'multi stage', 'multiple from'],
        'compose': ['compose', 'service', 'docker compose'],
        'image-optimization': ['optimization', 'image size', '.dockerignore'],
        'security': ['security', 'rootless', 'user directive', 'secrets'],
        'networking': ['network', 'bridge', 'host', 'overlay'],
        'volumes': ['volume', 'mount', 'persistence', 'data'],
        'logging': ['log', 'debug', 'troubleshoot'],
        'build-cache': ['cache', 'build cache', 'layer cache'],
        'health-checks': ['health', 'healthcheck', 'lifecycle'],
        'environment': ['environment', 'env', 'secrets'],
        'tagging': ['tag', 'registry', 'push', 'pull'],
        'resources': ['resource', 'cpu', 'memory', 'limit']
    }
    
    def __init__(self, repo_root: Path):
        """Initialize checker with repository root path."""
        self.repo_root = Path(repo_root)
        self.errors = []
        self.warnings = []
        self.coverage = {}
    
    def validate(self) -> bool:
        """Run topic coverage check. Returns True if valid."""
        self.errors = []
        self.warnings = []
        self.coverage = {}
        
        self._check_topic_coverage()
        
        return len(self.errors) == 0
    
    def _check_topic_coverage(self):
        """Check that all required topics are covered."""
        docs_path = self.repo_root / 'docs'
        
        if not docs_path.exists():
            self.errors.append("docs/ directory does not exist")
            return
        
        # Read all markdown files
        all_content = {}
        for md_file in docs_path.rglob('*.md'):
            content = md_file.read_text(encoding='utf-8').lower()
            rel_path = md_file.relative_to(self.repo_root)
            all_content[rel_path] = content
        
        # Check each required topic
        for topic_name, keywords in self.REQUIRED_TOPICS.items():
            found_in = []
            
            for file_path, content in all_content.items():
                # Check if any keyword appears in content
                if any(keyword.lower() in content for keyword in keywords):
                    found_in.append(str(file_path))
            
            self.coverage[topic_name] = found_in
            
            if not found_in:
                self.errors.append(
                    f"Required topic '{topic_name}' not covered "
                    f"(keywords: {', '.join(keywords)})"
                )
    
    def get_report(self) -> str:
        """Generate validation report."""
        report = ["=" * 60]
        report.append("TOPIC COVERAGE REPORT")
        report.append("=" * 60)
        
        if self.coverage:
            report.append(f"\nTopics checked: {len(self.REQUIRED_TOPICS)}")
            covered = sum(1 for files in self.coverage.values() if files)
            report.append(f"Topics covered: {covered}/{len(self.REQUIRED_TOPICS)}")
        
        if not self.errors and not self.warnings:
            report.append("\n✓ All required topics are covered!")
        else:
            if self.errors:
                report.append(f"\n✗ {len(self.errors)} error(s) found:")
                for error in self.errors:
                    report.append(f"  - {error}")
            
            if self.warnings:
                report.append(f"\n⚠ {len(self.warnings)} warning(s):")
                for warning in self.warnings:
                    report.append(f"  - {warning}")
        
        # Show coverage details
        if self.coverage:
            report.append("\nCoverage details:")
            for topic, files in sorted(self.coverage.items()):
                if files:
                    report.append(f"  ✓ {topic}: {len(files)} file(s)")
                else:
                    report.append(f"  ✗ {topic}: NOT COVERED")
        
        report.append("")
        return "\n".join(report)


def validate_topic_coverage(repo_root: Path = Path('.')) -> Tuple[bool, str]:
    """
    Validate topic coverage.
    
    Args:
        repo_root: Path to repository root
        
    Returns:
        Tuple of (is_valid, report_string)
    """
    checker = TopicCoverageChecker(repo_root)
    is_valid = checker.validate()
    report = checker.get_report()
    return is_valid, report


if __name__ == '__main__':
    is_valid, report = validate_topic_coverage()
    print(report)
    exit(0 if is_valid else 1)
