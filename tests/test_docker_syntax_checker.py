"""
Property-based tests for Docker syntax checker.
Feature: docker-tutorial-modernization
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from validators.docker_syntax_checker import DockerSyntaxChecker


# Feature: docker-tutorial-modernization, Property 1: Modern Docker Syntax Consistency
def test_property_1_modern_docker_syntax_consistency():
    """
    Property 1: Modern Docker Syntax Consistency
    
    For any markdown file in the tutorial system, all Docker commands and syntax 
    should use modern equivalents (docker compose not docker-compose, --mount not -v) 
    and contain no deprecated features or commands.
    
    Validates: Requirements 1.1, 1.6, 6.5, 10.6
    """
    repo_root = Path('.')
    checker = DockerSyntaxChecker(repo_root)
    
    # Run validation
    is_valid = checker.validate()
    
    # Check all markdown files in docs/
    docs_path = repo_root / 'docs'
    if docs_path.exists():
        for md_file in docs_path.rglob('*.md'):
            content = md_file.read_text(encoding='utf-8')
            rel_path = md_file.relative_to(repo_root)
            
            # Should not contain legacy docker-compose command
            assert not checker.LEGACY_PATTERNS['docker-compose command'].search(content), \
                f"Legacy 'docker-compose' command found in {rel_path}"
            
            # Should not contain standalone docker-compose (except in explanatory notes)
            if checker.LEGACY_PATTERNS['docker-compose standalone'].search(content):
                # Allow if it's explaining the difference
                assert '(not `docker-compose`)' in content or 'not docker-compose' in content.lower(), \
                    f"Legacy 'docker-compose' found in {rel_path}"
            
            # Should not contain legacy -v flag
            assert not checker.LEGACY_PATTERNS['-v flag'].search(content), \
                f"Legacy '-v' flag found in {rel_path}"
    
    # Check all YAML files in examples/
    examples_path = repo_root / 'examples'
    if examples_path.exists():
        for yaml_file in list(examples_path.rglob('*.yaml')) + list(examples_path.rglob('*.yml')):
            content = yaml_file.read_text(encoding='utf-8')
            rel_path = yaml_file.relative_to(repo_root)
            
            # Should not contain version field (Compose v2)
            assert not checker.LEGACY_PATTERNS['version in compose'].search(content), \
                f"Legacy 'version:' field found in {rel_path}"
    
    # Overall validation should pass
    assert is_valid, f"Docker syntax validation failed:\n{checker.get_report()}"
    assert len(checker.errors) == 0, f"Validation errors found: {checker.errors}"


if __name__ == '__main__':
    # Run the property test 100 times as specified in design
    print("Running Property 1: Modern Docker Syntax Consistency (100 iterations)")
    for i in range(100):
        test_property_1_modern_docker_syntax_consistency()
        if (i + 1) % 10 == 0:
            print(f"  Completed {i + 1}/100 iterations")
    print("✓ All 100 iterations passed!")
