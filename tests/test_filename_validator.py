"""
Property-based tests for filename validator.
Feature: docker-tutorial-modernization
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from validators.filename_validator import FilenameValidator


# Feature: docker-tutorial-modernization, Property 3: Numbered Descriptive Filenames
def test_property_3_numbered_descriptive_filenames():
    """
    Property 3: Numbered Descriptive Filenames
    
    For any tutorial file in the docs/ directory, the filename should follow 
    the pattern NN-descriptive-name.md and not use step-based naming 
    (step1.md, step2.md).
    
    Validates: Requirements 2.2, 2.4
    """
    repo_root = Path('.')
    validator = FilenameValidator(repo_root)
    
    # Run validation
    is_valid = validator.validate()
    
    # Get all markdown files in docs/ subdirectories
    docs_path = repo_root / 'docs'
    if docs_path.exists():
        for md_file in docs_path.rglob('*.md'):
            # Skip files in root docs/ directory
            if md_file.parent == docs_path:
                continue
            
            filename = md_file.name
            
            # Check no step-based naming
            assert not validator.STEP_PATTERN.search(filename), \
                f"Step-based naming found: {md_file.relative_to(repo_root)}"
            
            # Check numbered descriptive pattern
            assert validator.NUMBERED_PATTERN.match(filename), \
                f"Invalid filename pattern: {md_file.relative_to(repo_root)} " \
                f"(expected NN-descriptive-name.md)"
    
    # Overall validation should pass
    assert is_valid, f"Filename validation failed:\n{validator.get_report()}"
    assert len(validator.errors) == 0, f"Validation errors found: {validator.errors}"


if __name__ == '__main__':
    # Run the property test 100 times as specified in design
    print("Running Property 3: Numbered Descriptive Filenames (100 iterations)")
    for i in range(100):
        test_property_3_numbered_descriptive_filenames()
        if (i + 1) % 10 == 0:
            print(f"  Completed {i + 1}/100 iterations")
    print("✓ All 100 iterations passed!")
