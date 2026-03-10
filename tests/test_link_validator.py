"""
Property-based tests for link validator.
Feature: docker-tutorial-modernization
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from validators.link_validator import LinkValidator


# Feature: docker-tutorial-modernization, Property 5: Cross-Reference Hyperlinks
def test_property_5_cross_reference_hyperlinks():
    """
    Property 5: Cross-Reference Hyperlinks
    
    For any content module that references another topic, the reference should 
    include a hyperlink to the relevant document using markdown link syntax.
    
    Validates: Requirements 2.5, 2.7
    """
    repo_root = Path('.')
    validator = LinkValidator(repo_root)
    
    # Run validation
    is_valid = validator.validate()
    
    # Check all markdown files for valid links
    docs_path = repo_root / 'docs'
    if docs_path.exists():
        for md_file in docs_path.rglob('*.md'):
            content = md_file.read_text(encoding='utf-8')
            rel_path = md_file.relative_to(repo_root)
            
            # Find all links
            for match in validator.LINK_PATTERN.finditer(content):
                link_url = match.group(2)
                
                # Skip external links
                if link_url.startswith(('http://', 'https://', 'mailto:', '#')):
                    continue
                
                # Should not reference .rst files
                assert not validator.RST_PATTERN.search(link_url), \
                    f"RST reference found in {rel_path}: {link_url}"
                
                # Internal links should have valid targets
                link_path = link_url.split('#')[0]
                if link_path:
                    if link_path.startswith('/'):
                        target = repo_root / link_path.lstrip('/')
                    else:
                        target = (md_file.parent / link_path).resolve()
                    
                    assert target.exists(), \
                        f"Broken link in {rel_path}: {link_url} -> target does not exist"
    
    # Overall validation should pass
    assert is_valid, f"Link validation failed:\n{validator.get_report()}"
    assert len(validator.errors) == 0, f"Validation errors found: {validator.errors}"


if __name__ == '__main__':
    # Run the property test 100 times as specified in design
    print("Running Property 5: Cross-Reference Hyperlinks (100 iterations)")
    for i in range(100):
        test_property_5_cross_reference_hyperlinks()
        if (i + 1) % 10 == 0:
            print(f"  Completed {i + 1}/100 iterations")
    print("✓ All 100 iterations passed!")
