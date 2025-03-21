#!/usr/bin/env python3
"""
Test runner for SimpleScript tests.
"""

import sys
import os
import unittest

# Add the parent directory to the Python path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_tests():
    """Run all tests for the SimpleScript project."""
    # Discover and load all tests
    loader = unittest.TestLoader()
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    test_suite = loader.discover(tests_dir, pattern="test_*.py")
    
    # Run the tests
    print("\n===== Running SimpleScript Tests =====\n")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n===== Test Summary =====")
    print(f"Ran {result.testsRun} tests")
    if result.wasSuccessful():
        print("All tests passed!")
    else:
        print(f"Failed tests: {len(result.failures)}")
        if result.failures:
            print("\nFailures:")
            for i, (test, error) in enumerate(result.failures, 1):
                print(f"{i}. {test}")
        
        if result.errors:
            print(f"\nErrors: {len(result.errors)}")
            for i, (test, error) in enumerate(result.errors, 1):
                print(f"{i}. {test}")
    
    print("\nNote: Some tests are currently skipped due to pending implementation.")
    print("Work on fixing the compiler and CPU implementations first.")
    
    # Return the result status
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 