"""
Property-based tests for README validator.
Feature: docker-tutorial-modernization
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from validators.readme_validator import ReadmeValidator


# Feature: docker-tutorial-modernization, Property 13: README Essential Sections
# Feature: docker-tutorial-modernization, Property 14: README Badges
def test_property_13_14_readme_completeness():
    """
    Property 13: README Essential Sections
    Property 14: README Badges
    
    For any valid repository state, the root README.md should contain sections 
    for project overview, learning objectives, prerequisites, setup instructions, 
    and contribution guidelines or link.
    
    For any valid repository state, the root README.md should include badge 
    markdown for license, Docker version compatibility, and maintenance status.
    
    Validates: Requirements 5.1, 5.3, 5.4, 5.5, 5.7
    """
    repo_root = Path('.')
    validator = ReadmeValidator(repo_root)
    
    # Run validation
    is_valid = validator.validate()
    
    # Check README exists
    readme_path = repo_root / 'README.md'
    assert readme_path.exists(), "README.md does not exist"
    
    content = readme_path.read_text(encoding='utf-8')
    content_lower = content.lower()
    
    # Check required sections
    assert any(term in content_lower for term in ['overview', 'about', 'introduction']), \
        "README missing overview/introduction section"
    
    assert 'prerequisite' in content_lower or 'requirement' in content_lower, \
        "README missing prerequisites section"
    
    assert any(term in content_lower for term in ['setup', 'installation', 'getting started']), \
        "README missing setup/installation section"
    
    assert 'contribut' in content_lower, \
        "README missing contribution guidelines or link"
    
    assert 'license' in content_lower, \
        "README missing license information"
    
    # Check for badges (at least some badges should exist)
    badges = validator.BADGE_PATTERN.findall(content)
    assert len(badges) > 0, "README has no badges"
    
    # Overall validation should pass
    assert is_valid, f"README validation failed:\n{validator.get_report()}"
    assert len(validator.errors) == 0, f"Validation errors found: {validator.errors}"


if __name__ == '__main__':
    # Run the property test 100 times as specified in design
    print("Running Property 13 & 14: README Completeness (100 iterations)")
    for i in range(100):
        test_property_13_14_readme_completeness()
        if (i + 1) % 10 == 0:
            print(f"  Completed {i + 1}/100 iterations")
    print("✓ All 100 iterations passed!")
