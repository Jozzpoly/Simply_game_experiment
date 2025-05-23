#!/usr/bin/env python3
"""
Test runner script for the Simple Roguelike game.

This script runs all unit tests and provides a summary of the results.
"""

import unittest
import sys
import os

# Add the current directory to the path so we can import the game modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def run_all_tests():
    """Run all unit tests in the tests directory"""
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\nAll tests passed! ✅")
        return 0
    else:
        print("\nSome tests failed! ❌")
        return 1

if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)
