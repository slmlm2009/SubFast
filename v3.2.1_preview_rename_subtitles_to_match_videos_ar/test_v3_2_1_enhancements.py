#!/usr/bin/env python3
"""
Comprehensive Test Suite for SubFast v3.2.1 Pattern Enhancements

Tests the enhanced patterns 26-29 with:
1. Zero padding support (up to 3 zeros)
2. Versioning support (V1, v2, etc.)
3. Pattern 26 number handling improvements
"""

import sys
import os
import json
from typing import List, Tuple, Dict

# Add the subfast module to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'subfast'))

from subfast.scripts.common.pattern_engine import (
    extract_episode_info, 
    normalize_episode_number,
    EPISODE_PATTERNS
)

class TestResult:
    """Container for test results"""
    def __init__(self, pattern_id: int, pattern_name: str, test_input: str, 
                 expected: Tuple[int, int], actual: Tuple[int, int], 
                 passed: bool, notes: str = ""):
        self.pattern_id = pattern_id
        self.pattern_name = pattern_name
        self.test_input = test_input
        self.expected = expected
        self.actual = actual
        self.passed = passed
        self.notes = notes

class PatternTester:
    """Test harness for v3.2.1 pattern enhancements"""
    
    def __init__(self):
        self.test_results: List[TestResult] = []
        
    def test_pattern_26_enhancements(self):
        """Test Pattern 26: ## - ## with versioning and improved number handling"""
        print("=" * 70)
        print("Testing Pattern 26: ## - ## enhancements")
        print("=" * 70)
        
        test_cases = [
            # Basic functionality (should still work)
            ("Show 3 - 04.mkv", (3, 4), "Basic season-episode with dash"),
            ("Series 2-10.720p.mkv", (2, 10), "No spaces around dash"),
            ("Example 1 - 25.BluRay.mkv", (1, 25), "Standard format"),
            
            # Versioning support
            ("Show 3 - 04v2.mkv", (3, 4), "Versioning with v2"),
            ("Series 2-10V1.720p.mkv", (2, 10), "Versioning with V1"),
            ("Example 1 - 25v3.BluRay.mkv", (1, 25), "Versioning with v3"),
            
            # Prevent false positives (numbers before pattern)
            ("Movie.2023.Show 3 - 04.mkv", (3, 4), "Should still work with proper start"),
            ("Show 123.Movie 3 - 04.mkv", (3, 4), "Numbers before should not trigger"),
        ]
        
        for filename, expected, notes in test_cases:
            result = extract_episode_info(filename)
            passed = result == expected
            actual = result if result else None
            
            test_result = TestResult(
                26, "## - ##", filename, expected, actual, passed, notes
            )
            self.test_results.append(test_result)
            
            status = "[PASS]" if passed else "[FAIL]"
            print(f"{status} Pattern 26: {filename}")
            print(f"   Expected: {expected}, Got: {actual}")
            print(f"   Notes: {notes}")
            print()
    
    def test_pattern_27_enhancements(self):
        """Test Pattern 27: - ## with zero padding and versioning"""
        print("=" * 70)
        print("Testing Pattern 27: - ## enhancements")
        print("=" * 70)
        
        test_cases = [
            # Basic functionality
            ("Show - 15.mkv", (1, 15), "Basic single episode"),
            ("Series - 10.720p.mkv", (1, 10), "With quality tag"),
            
            # Zero padding support
            ("Show - 0005.mkv", (1, 5), "Three zero padding"),
            ("Show - 0010.mkv", (1, 10), "Two zero padding"),  
            ("Show - 0150.mkv", (1, 150), "One zero padding"),
            
            # Versioning support
            ("Show - 15v2.mkv", (1, 15), "Versioning with v2"),
            ("Series - 10V1.720p.mkv", (1, 10), "Versioning with V1"),
            ("Example - 05v3.BluRay.mkv", (1, 5), "Zero padding + versioning"),
            
            # Edge cases within range
            ("Show - 1.mkv", (1, 1), "Single digit episode"),
            ("Show - 1899.mkv", (1, 1899), "Maximum supported range"),
            
            # Should NOT match (outside range or invalid)
            ("Show - 1900.mkv", None, "Year value should not match"),
            ("Show - 2023.mkv", None, "Year value should not match"),
            ("Show - 1080p.mkv", None, "Quality tag should not match"),
            ("Show - x264.mkv", None, "Codec should not match"),
        ]
        
        for filename, expected, notes in test_cases:
            result = extract_episode_info(filename)
            passed = result == expected
            actual = result if result else None
            
            test_result = TestResult(
                27, "- ##", filename, expected, actual, passed, notes
            )
            self.test_results.append(test_result)
            
            status = "[PASS]" if passed else "[FAIL]"
            print(f"{status} Pattern 27: {filename}")
            print(f"   Expected: {expected}, Got: {actual}")
            print(f"   Notes: {notes}")
            print()
    
    def test_pattern_28_enhancements(self):
        """Test Pattern 28: [##] with zero padding and versioning"""
        print("=" * 70)
        print("Testing Pattern 28: [##] enhancements")
        print("=" * 70)
        
        test_cases = [
            # Basic functionality
            ("Show.[07].mkv", (1, 7), "Basic bracketed episode"),
            ("Series.[12].720p.mkv", (1, 12), "With quality tag"),
            
            # Zero padding support
            ("Show.[0005].mkv", (1, 5), "Three zero padding"),
            ("Show.[0010].mkv", (1, 10), "Two zero padding"),
            ("Show.[0150].mkv", (1, 150), "One zero padding"),
            
            # Versioning support
            ("Show.[07]v2.mkv", (1, 7), "Versioning with v2"),
            ("Series.[12]V1.720p.mkv", (1, 12), "Versioning with V1"),
            ("Example.[0005]v3.mkv", (1, 5), "Zero padding + versioning"),
            
            # Edge cases within range
            ("Show.[1].mkv", (1, 1), "Single digit episode"),
            ("Show.[1899].mkv", (1, 1899), "Maximum supported range"),
            
            # Should NOT match (outside range or technical tags)
            ("Show.[1080p].mkv", None, "Quality tag should not match"),
            ("Show.[10bit].mkv", None, "Bit depth should not match"),
            ("Show.[x265].mkv", None, "Codec should not match"),
            ("Show.[2023].mkv", None, "Year value should not match"),
        ]
        
        for filename, expected, notes in test_cases:
            result = extract_episode_info(filename)
            passed = result == expected
            actual = result if result else None
            
            test_result = TestResult(
                28, "[##]", filename, expected, actual, passed, notes
            )
            self.test_results.append(test_result)
            
            status = "[PASS]" if passed else "[FAIL]"
            print(f"{status} Pattern 28: {filename}")
            print(f"   Expected: {expected}, Got: {actual}")
            print(f"   Notes: {notes}")
            print()
    
    def test_pattern_29_enhancements(self):
        """Test Pattern 29: _## with zero padding and versioning"""
        print("=" * 70)
        print("Testing Pattern 29: _## enhancements")
        print("=" * 70)
        
        test_cases = [
            # Basic functionality
            ("Show_09.mkv", (1, 9), "Basic underscore episode"),
            ("Series_15.720p.mkv", (1, 15), "With quality tag"),
            
            # Zero padding support
            ("Show_0005.mkv", (1, 5), "Three zero padding"),
            ("Show_0010.mkv", (1, 10), "Two zero padding"),
            ("Show_0150.mkv", (1, 150), "One zero padding"),
            
            # Versioning support
            ("Show_09v2.mkv", (1, 9), "Versioning with v2"),
            ("Series_15V1.720p.mkv", (1, 15), "Versioning with V1"),
            ("Example_0005v3.mkv", (1, 5), "Zero padding + versioning"),
            
            # Edge cases within range
            ("Show_1.mkv", (1, 1), "Single digit episode"),
            ("Show_1899.mkv", (1, 1899), "Maximum supported range"),
            
            # Should NOT match (technical tags)
            ("Show_1080p.mkv", None, "Quality tag should not match"),
            ("Show_10bit.mkv", None, "Bit depth should not match"),
            ("Show_x264.mkv", None, "Codec should not match"),
            ("Show_2023.mkv", None, "Year value should not match"),
        ]
        
        for filename, expected, notes in test_cases:
            result = extract_episode_info(filename)
            passed = result == expected
            actual = result if result else None
            
            test_result = TestResult(
                29, "_##", filename, expected, actual, passed, notes
            )
            self.test_results.append(test_result)
            
            status = "[PASS]" if passed else "[FAIL]"
            print(f"{status} Pattern 29: {filename}")
            print(f"   Expected: {expected}, Got: {actual}")
            print(f"   Notes: {notes}")
            print()
    
    def test_compatibility_with_existing_tests(self):
        """Verify that existing test cases still pass with enhanced patterns"""
        print("=" * 70)
        print("Testing compatibility with existing pattern definitions")
        print("=" * 70)
        
        # Load existing pattern definitions
        pattern_file = os.path.join("tests", "fixtures", "pattern_definitions.json")
        
        if not os.path.exists(pattern_file):
            print("WARNING: Could not find pattern_definitions.json for compatibility testing")
            return
        
        with open(pattern_file, 'r', encoding='utf-8') as f:
            pattern_data = json.load(f)
        
        # Test patterns 26-29 from the existing definitions
        for pattern in pattern_data.get("patterns", []):
            pattern_id = pattern.get("id")
            if pattern_id not in [26, 27, 28, 29]:
                continue
                
            pattern_name = pattern.get("name", f"Pattern {pattern_id}")
            print(f"\nTesting {pattern_name} (ID: {pattern_id}):")
            
            for variation in pattern.get("variations", []):
                video_template = variation.get("video_template", "")
                expected_str = variation.get("expected", "")
                
                if not video_template or not expected_str:
                    continue
                
                # Extract expected values from normalized string
                match = re.match(r'S(\d+)E(\d+)', expected_str)
                if not match:
                    continue
                
                expected = (int(match.group(1)), int(match.group(2)))
                
                # Remove VAR prefixes for testing
                clean_filename = re.sub(r'\[VAR\d+\]-?', '', video_template)
                
                result = extract_episode_info(clean_filename)
                passed = result == expected
                
                status = "[PASS]" if passed else "[FAIL]"
                print(f"  {status} {pattern_name}: {clean_filename}")
                print(f"       Expected: {expected}, Got: {result}")
                
                if not passed:
                    print(f"       ERROR: Existing test case failed!")
    
    def generate_test_report(self) -> Dict:
        """Generate comprehensive test report"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r.passed)
        failed_tests = total_tests - passed_tests
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "pass_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0
            },
            "by_pattern": {}
        }
        
        # Group results by pattern
        for result in self.test_results:
            pattern_key = f"Pattern {result.pattern_id}: {result.pattern_name}"
            if pattern_key not in report["by_pattern"]:
                report["by_pattern"][pattern_key] = {
                    "total": 0,
                    "passed": 0,
                    "failed": 0,
                    "failures": []
                }
            
            report["by_pattern"][pattern_key]["total"] += 1
            if result.passed:
                report["by_pattern"][pattern_key]["passed"] += 1
            else:
                report["by_pattern"][pattern_key]["failed"] += 1
                report["by_pattern"][pattern_key]["failures"].append({
                    "input": result.test_input,
                    "expected": result.expected,
                    "actual": result.actual,
                    "notes": result.notes
                })
        
        return report
    
    def print_final_summary(self):
        """Print comprehensive test summary"""
        report = self.generate_test_report()
        summary = report["summary"]
        
        print("=" * 70)
        print("V3.2.1 PATTERN ENHANCEMENTS TEST SUMMARY")
        print("=" * 70)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Pass Rate: {summary['pass_rate']:.1f}%")
        print()
        
        # Print pattern-by-pattern breakdown
        for pattern_name, results in report["by_pattern"].items():
            print(f"{pattern_name}:")
            print(f"  Total: {results['total']}, Passed: {results['passed']}, Failed: {results['failed']}")
            
            if results["failures"]:
                print("  Failures:")
                for failure in results["failures"]:
                    print(f"    - {failure['input']}")
                    print(f"      Expected: {failure['expected']}, Got: {failure['actual']}")
                    print(f"      Notes: {failure['notes']}")
            print()
        
        # Overall result
        if summary['failed'] == 0:
            print("🎉 ALL TESTS PASSED! v3.2.1 enhancements are working correctly.")
        else:
            print(f"❌ {summary['failed']} TESTS FAILED. Please review the issues above.")
        
        print("=" * 70)
        
        return summary['failed'] == 0

def main():
    """Main test execution"""
    print("SubFast v3.2.1 Pattern Enhancement Test Suite")
    print("Testing zero padding and versioning support for patterns 26-29")
    print()
    
    tester = PatternTester()
    
    # Test each enhanced pattern
    tester.test_pattern_26_enhancements()
    tester.test_pattern_27_enhancements() 
    tester.test_pattern_28_enhancements()
    tester.test_pattern_29_enhancements()
    
    # Test compatibility with existing tests
    tester.test_compatibility_with_existing_tests()
    
    # Generate final report
    all_passed = tester.print_final_summary()
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    # Import regex for pattern cleanup
    import re
    exit(main())
