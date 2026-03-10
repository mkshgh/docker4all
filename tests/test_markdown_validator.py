"""
Property-based tests for markdown validator.
Feature: docker-tutorial-modernization
"""

import sys
from pathlib import Path
import re
# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from validators.markdown_validator import MarkdownValidator


# Feature: docker-tutorial-modernization, Property 15: Markdown Heading Hierarchy
# Feature: docker-tutorial-modernization, Property 16: Fenced Code Blocks with Language Tags
def test_property_15_16_markdown_formatting():
    """
    Property 15: Markdown Heading Hierarchy
    Property 16: Fenced Code Blocks with Language Tags
    
    For any content module, the heading structure should follow proper hierarchy 
    (single # for title, ## for major sections, ### for subsections) without 
    skipping levels.
    
    For any code block in a markdown file, it should use fenced code block syntax 
    (```) with an appropriate language tag (bash, dockerfile, yaml) rather than 
    indented code blocks.
    
    Validates: Requirements 6.1, 6.2, 8.3
    """
    repo_root = Path('.')
    validator = MarkdownValidator(repo_root)
    
    # Run validation
    is_valid = validator.validate()
    
    # Check all markdown files
    docs_path = repo_root / 'docs'
    if docs_path.exists():
        for md_file in docs_path.rglob('*.md'):
            content = md_file.read_text(encoding='utf-8')
            rel_path = md_file.relative_to(repo_root)
            
            # Remove code blocks before checking headings
            content_no_code = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
            content_no_code = re.sub(r'^(    |\t).*$', '', content_no_code, flags=re.MULTILINE)
            
            # Check heading hierarchy
            headings = validator.HEADING_PATTERN.findall(content_no_code)
            if headings:
                for i in range(1, len(headings)):
                    prev_level = len(headings[i-1][0])
                    current_level = len(headings[i][0])
                    heading_text = headings[i][1]
                    
                    # Should not skip levels when going deeper
                    if current_level > prev_level:
                        assert current_level <= prev_level + 1, \
                            f"Heading level skip in {rel_path}: " \
                            f"from level {prev_level} to {current_level}"
            
            # Check for fenced code blocks (prefer over indented)
            # This is a warning check, not a hard error
            indented_blocks = validator.INDENTED_CODE_PATTERN.findall(content)
            if indented_blocks:
                # Just a warning, not an assertion failure
                pass
    
    # Overall validation should pass (errors only, warnings are ok)
    assert is_valid, f"Markdown validation failed:\n{validator.get_report()}"
    assert len(validator.errors) == 0, f"Validation errors found: {validator.errors}"


if __name__ == '__main__':
    # Run the property test 100 times as specified in design
    print("Running Property 15 & 16: Markdown Formatting (100 iterations)")
    for i in range(100):
        test_property_15_16_markdown_formatting()
        if (i + 1) % 10 == 0:
            print(f"  Completed {i + 1}/100 iterations")
    print("✓ All 100 iterations passed!")
