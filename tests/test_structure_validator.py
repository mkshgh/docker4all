"""
Property-based tests for structure validator.
Feature: docker-tutorial-modernization
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from validators.structure_validator import StructureValidator


# Feature: docker-tutorial-modernization, Property 2: Repository Structure Compliance
def test_property_2_repository_structure_compliance():
    """
    Property 2: Repository Structure Compliance
    
    For any valid tutorial repository state, the required directory structure 
    (docs/ with subdirectories, examples/ with subdirectories, root files) 
    should exist and legacy directories should not exist.
    
    Validates: Requirements 2.1, 4.1, 9.1, 9.2, 9.8
    """
    repo_root = Path('.')
    validator = StructureValidator(repo_root)
    
    # Run validation
    is_valid = validator.validate()
    
    # Check required directories exist
    for dir_path in validator.REQUIRED_DIRS:
        full_path = repo_root / dir_path
        assert full_path.exists(), f"Required directory missing: {dir_path}"
        assert full_path.is_dir(), f"Path is not a directory: {dir_path}"
    
    # Check required root files exist
    for file_name in validator.REQUIRED_ROOT_FILES:
        full_path = repo_root / file_name
        assert full_path.exists(), f"Required root file missing: {file_name}"
        assert full_path.is_file(), f"Path is not a file: {file_name}"
    
    # Check legacy directories do not exist
    for dir_name in validator.LEGACY_DIRS:
        full_path = repo_root / dir_name
        assert not full_path.exists(), f"Legacy directory still exists: {dir_name}"
    
    # Overall validation should pass
    assert is_valid, f"Structure validation failed:\n{validator.get_report()}"
    assert len(validator.errors) == 0, f"Validation errors found: {validator.errors}"


if __name__ == '__main__':
    # Run the property test 100 times as specified in design
    print("Running Property 2: Repository Structure Compliance (100 iterations)")
    for i in range(100):
        test_property_2_repository_structure_compliance()
        if (i + 1) % 10 == 0:
            print(f"  Completed {i + 1}/100 iterations")
    print("✓ All 100 iterations passed!")
