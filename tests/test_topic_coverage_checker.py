"""
Property-based tests for topic coverage checker.
Feature: docker-tutorial-modernization
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from validators.topic_coverage_checker import TopicCoverageChecker


# Feature: docker-tutorial-modernization, Property 7: Topic Coverage Completeness
def test_property_7_topic_coverage_completeness():
    """
    Property 7: Topic Coverage Completeness
    
    For any required Docker topic (from the list: Engine fundamentals, CLI, 
    Dockerfile best practices, BuildKit, multi-stage builds, Compose v2, 
    image optimization, security, networking, volumes, logging, build cache, 
    health checks, environment variables, tagging, resource limits), the 
    tutorial system should include at least one content module covering that topic.
    
    Validates: Requirements 3.1-3.15
    """
    repo_root = Path('.')
    checker = TopicCoverageChecker(repo_root)
    
    # Run validation
    is_valid = checker.validate()
    
    # Check that all required topics are covered
    for topic_name, keywords in checker.REQUIRED_TOPICS.items():
        coverage = checker.coverage.get(topic_name, [])
        assert len(coverage) > 0, \
            f"Required topic '{topic_name}' not covered (keywords: {', '.join(keywords)})"
    
    # Overall validation should pass
    assert is_valid, f"Topic coverage validation failed:\n{checker.get_report()}"
    assert len(checker.errors) == 0, f"Validation errors found: {checker.errors}"


if __name__ == '__main__':
    # Run the property test 100 times as specified in design
    print("Running Property 7: Topic Coverage Completeness (100 iterations)")
    for i in range(100):
        test_property_7_topic_coverage_completeness()
        if (i + 1) % 10 == 0:
            print(f"  Completed {i + 1}/100 iterations")
    print("✓ All 100 iterations passed!")
