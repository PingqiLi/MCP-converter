#!/usr/bin/env python3
"""
Test Runner for API-to-MCP Transformation Tool
Runs all test suites with proper organization and reporting
"""
import sys
import os
import unittest
import argparse
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))


def discover_and_run_tests(test_type="all", verbosity=2):
    """Discover and run tests based on type"""
    
    print("🧪 API-to-MCP Tool Test Suite")
    print("=" * 50)
    
    # Check LLM availability for system tests
    llm_available = any(os.getenv(key) for key in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"])
    if test_type in ["system", "st", "all"] and not llm_available:
        print("⚠️  Warning: No LLM API key found")
        print("💡 System tests require one of:")
        print("   - OPENAI_API_KEY")
        print("   - ANTHROPIC_API_KEY")
        print()
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    if test_type == "all":
        # Run all tests (both unit and system)
        print("📋 Running all test suites...")
        print("🔧 Discovering unit tests...")
        ut_tests = loader.discover(str(project_root / "tests" / "ut"), pattern="test_*.py")
        suite.addTests(ut_tests)
        print("🔗 Discovering system tests...")
        st_tests = loader.discover(str(project_root / "tests" / "st"), pattern="test_*.py")
        suite.addTests(st_tests)
    
    elif test_type in ["unit", "ut"]:
        # Run only unit tests
        print("🔧 Running unit tests...")
        discovered = loader.discover(str(project_root / "tests" / "ut"), pattern="test_*.py")
        suite.addTests(discovered)
    
    elif test_type in ["system", "st"]:
        # Run only system tests
        print("🔗 Running system tests...")
        discovered = loader.discover(str(project_root / "tests" / "st"), pattern="test_*.py")
        suite.addTests(discovered)
    
    elif test_type == "integration":
        # Legacy support - run integration test specifically
        print("🔗 Running integration tests...")
        suite.addTests(loader.loadTestsFromName("tests.st.test_integration"))
    
    elif test_type == "simplified":
        # Legacy support - run simplified workflow test specifically
        print("🚀 Running simplified workflow tests...")
        suite.addTests(loader.loadTestsFromName("tests.st.test_simplified_workflow"))
    
    else:
        print(f"❌ Unknown test type: {test_type}")
        return False
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=verbosity, buffer=True)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    if success:
        print("\n✅ All tests passed!")
    else:
        print(f"\n❌ {len(result.failures + result.errors)} test(s) failed")
    
    return success


def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(
        description="Test runner for API-to-MCP Transformation Tool"
    )
    parser.add_argument(
        "--type", 
        choices=["all", "unit", "ut", "system", "st", "integration", "simplified"],
        default="all",
        help="Type of tests to run (default: all)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="count",
        default=2,
        help="Increase verbosity (use -v, -vv, or -vvv)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available test types"
    )
    
    args = parser.parse_args()
    
    if args.list:
        print("📋 Available test types:")
        print("  all         - Run all test suites (unit + system)")
        print("  unit, ut    - Run unit tests only (tests/ut/)")
        print("  system, st  - Run system tests only (tests/st/) - requires LLM API key")
        print("  integration - Run integration tests specifically (legacy)")
        print("  simplified  - Run simplified workflow tests specifically (legacy)")
        return 0
    
    success = discover_and_run_tests(args.type, args.verbose)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main()) 