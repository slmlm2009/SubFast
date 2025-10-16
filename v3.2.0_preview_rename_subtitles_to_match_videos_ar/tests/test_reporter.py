"""
Module: test_reporter.py
Purpose: Comprehensive test report generator with bordered tables

Generates detailed, self-contained test reports with bordered table format
matching SubFast's console output style. Reports always generated automatically.
"""

import unittest
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
import time


class TestResult:
    """Container for individual test result data."""
    
    def __init__(self, test_id: str, status: str, duration: float, error_msg: str = ""):
        self.test_id = test_id  # Full test identifier
        self.status = status  # PASS, FAIL, SKIP
        self.duration = duration
        self.error_msg = error_msg
        
        # Parse test components from unittest format
        # Format: "test_method (tests.test_module.TestClass.test_method)"
        # or just "tests.test_module.TestClass.test_method"
        self.test_script = ""
        self.test_class = ""
        self.test_method = ""
        
        # Extract from parentheses format if present
        if '(' in test_id and ')' in test_id:
            # Format: "test_name (module.class.method)"
            paren_content = test_id.split('(')[1].split(')')[0]
            parts = paren_content.split('.')
            
            if len(parts) >= 4:  # tests.test_script.TestClass.test_method
                self.test_script = parts[1]  # test_config_loader
                self.test_class = parts[2]   # TestBooleanParsing
                self.test_method = parts[3]  # test_parse_boolean_false_values
            elif len(parts) >= 3:
                self.test_script = parts[0]  # test_config_loader
                self.test_class = parts[1]   # TestBooleanParsing
                self.test_method = parts[2]  # test_method
        else:
            # Direct format: module.class.method
            parts = test_id.split('.')
            if len(parts) >= 3:
                self.test_script = parts[0]
                self.test_class = parts[1]
                self.test_method = parts[2]
            else:
                self.test_method = test_id
        
        # Pattern test detection
        self.is_pattern_test = 'pattern' in test_id.lower()
        self.pattern_id = None
        self.pattern_name = None
        self.filename_variation = None
        
        if self.is_pattern_test:
            self._extract_pattern_info()
    
    def _extract_pattern_info(self):
        """Extract pattern-specific information from test ID."""
        # Pattern tests follow naming: test_pattern_##_name_variation
        # Example: test_pattern_01_s_e_format
        if 'test_pattern_' in self.test_method:
            try:
                parts = self.test_method.replace('test_pattern_', '').split('_')
                if parts and parts[0].isdigit():
                    self.pattern_id = int(parts[0])
                    # Pattern name from remaining parts
                    self.pattern_name = '_'.join(parts[1:]).replace('_', ' ').title()
            except:
                pass


class ComprehensiveTestReporter:
    """
    Generates comprehensive bordered table reports for test execution.
    
    Features:
    - Summary statistics with percentages
    - Pattern-specific test breakdown
    - Detailed failure information
    - Complete test listing
    - Bordered table format (like SubFast console)
    """
    
    def __init__(self):
        self.test_results: List[TestResult] = []
        self.start_time = None
        self.end_time = None
    
    def start_run(self):
        """Mark test run start time."""
        self.start_time = time.time()
    
    def end_run(self):
        """Mark test run end time."""
        self.end_time = time.time()
    
    def add_result(self, test_id: str, status: str, duration: float, error_msg: str = ""):
        """Add a test result to the report."""
        result = TestResult(test_id, status, duration, error_msg)
        self.test_results.append(result)
    
    def get_statistics(self) -> Dict[str, any]:
        """Calculate test execution statistics."""
        total = len(self.test_results)
        if total == 0:
            return {
                'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0,
                'pass_pct': 0.0, 'fail_pct': 0.0, 'skip_pct': 0.0,
                'duration': 0.0
            }
        
        passed = sum(1 for r in self.test_results if r.status == 'PASS')
        failed = sum(1 for r in self.test_results if r.status == 'FAIL')
        skipped = sum(1 for r in self.test_results if r.status == 'SKIP')
        
        duration = self.end_time - self.start_time if self.end_time and self.start_time else 0.0
        
        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'skipped': skipped,
            'pass_pct': (passed / total * 100) if total > 0 else 0.0,
            'fail_pct': (failed / total * 100) if total > 0 else 0.0,
            'skip_pct': (skipped / total * 100) if total > 0 else 0.0,
            'duration': duration
        }
    
    def get_test_script_statistics(self) -> List[Dict]:
        """Get statistics grouped by test script (test file)."""
        # Group by test script
        scripts = {}
        for result in self.test_results:
            script = result.test_script or 'unknown'
            if script not in scripts:
                scripts[script] = {
                    'script': script,
                    'total': 0,
                    'passed': 0,
                    'failed': 0,
                    'skipped': 0
                }
            
            scripts[script]['total'] += 1
            if result.status == 'PASS':
                scripts[script]['passed'] += 1
            elif result.status == 'FAIL':
                scripts[script]['failed'] += 1
            elif result.status == 'SKIP':
                scripts[script]['skipped'] += 1
        
        # Convert to sorted list and add percentages
        script_list = list(scripts.values())
        script_list.sort(key=lambda s: s['script'])
        
        # Add pass percentage and status
        for s in script_list:
            if s['total'] > 0:
                s['pass_pct'] = (s['passed'] / s['total'] * 100)
            else:
                s['pass_pct'] = 0.0
            s['status'] = 'PASS' if s['failed'] == 0 else 'FAIL'
        
        return script_list
    
    def get_pattern_statistics(self) -> List[Dict]:
        """Get statistics for pattern tests grouped by pattern ID."""
        pattern_tests = [r for r in self.test_results if r.is_pattern_test and r.pattern_id]
        
        # Group by pattern ID
        patterns = {}
        for result in pattern_tests:
            pid = result.pattern_id
            if pid not in patterns:
                patterns[pid] = {
                    'id': pid,
                    'name': result.pattern_name or f"Pattern {pid}",
                    'total': 0,
                    'passed': 0,
                    'failed': 0
                }
            
            patterns[pid]['total'] += 1
            if result.status == 'PASS':
                patterns[pid]['passed'] += 1
            elif result.status == 'FAIL':
                patterns[pid]['failed'] += 1
        
        # Convert to sorted list
        pattern_list = list(patterns.values())
        pattern_list.sort(key=lambda p: p['id'])
        
        # Add status
        for p in pattern_list:
            p['status'] = 'PASS' if p['failed'] == 0 else 'FAIL'
        
        return pattern_list
    
    def generate_report(self, output_path: Path = None) -> str:
        """
        Generate comprehensive bordered table report.
        
        Args:
            output_path: Optional file path to save report
        
        Returns:
            Complete report as string
        """
        lines = []
        stats = self.get_statistics()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Header
        lines.append("=" * 95)
        lines.append("TEST EXECUTION REPORT".center(95))
        lines.append("=" * 95)
        lines.append(f"Test Run: {timestamp}")
        lines.append(f"Total Duration: {stats['duration']:.2f} seconds")
        lines.append("")
        
        # Summary Statistics
        lines.append("-" * 95)
        lines.append("SUMMARY STATISTICS".center(80))
        lines.append("-" * 95)
        lines.append(f"| {'Metric':<28} | {'Count':<6} | {'Percentage':<10} |")
        lines.append(f"|{'-' * 30}|{'-' * 8}|{'-' * 12}|")
        lines.append(f"| {'Total Tests Run':<28} | {stats['total']:<6} | {'100.00%':<10} |")
        lines.append(f"| {'Tests Passed':<28} | {stats['passed']:<6} | {stats['pass_pct']:<10.2f}% |")
        lines.append(f"| {'Tests Failed':<28} | {stats['failed']:<6} | {stats['fail_pct']:<10.2f}% |")
        lines.append(f"| {'Tests Skipped':<28} | {stats['skipped']:<6} | {stats['skip_pct']:<10.2f}% |")
        lines.append(f"| {'Total Execution Time':<28} | {stats['duration']:.2f}s | {'':<10} |")
        lines.append("-" * 95)
        lines.append("")
        
        # Test Script Summary
        script_stats = self.get_test_script_statistics()
        if script_stats:
            lines.append("-" * 95)
            lines.append("TEST SCRIPT SUMMARY".center(95))
            lines.append("-" * 95)
            lines.append(f"| {'Test Script':<25} | {'Total':<6} | {'Passed':<6} | {'Failed':<6} | {'Skipped':<7} | {'Pass %':<8} | {'Status':<6} |")
            lines.append(f"|{'-' * 27}|{'-' * 8}|{'-' * 8}|{'-' * 8}|{'-' * 9}|{'-' * 10}|{'-' * 8}|")
            
            for s in script_stats:
                lines.append(
                    f"| {s['script']:<25} | {s['total']:<6} | {s['passed']:<6} | "
                    f"{s['failed']:<6} | {s['skipped']:<7} | {s['pass_pct']:<8.2f}% | {s['status']:<6} |"
                )
            
            lines.append("-" * 95)
            lines.append("")
        
        # Pattern Matching Tests (if any)
        pattern_stats = self.get_pattern_statistics()
        if pattern_stats:
            lines.append("-" * 95)
            lines.append("PATTERN MATCHING TESTS".center(80))
            lines.append("-" * 95)
            lines.append(f"| {'ID':<4} | {'Pattern Name':<20} | {'Variations':<10} | {'Passed':<6} | {'Failed':<6} | {'Status':<6} |")
            lines.append(f"|{'-' * 6}|{'-' * 22}|{'-' * 12}|{'-' * 8}|{'-' * 8}|{'-' * 8}|")
            
            for p in pattern_stats:
                lines.append(
                    f"| {p['id']:<4} | {p['name']:<20} | {p['total']:<10} | "
                    f"{p['passed']:<6} | {p['failed']:<6} | {p['status']:<6} |"
                )
            
            lines.append("-" * 95)
            lines.append("")
        
        # Failed Tests
        failed_tests = [r for r in self.test_results if r.status == 'FAIL']
        if failed_tests:
            lines.append("-" * 95)
            lines.append("FAILED TESTS".center(80))
            lines.append("-" * 95)
            
            for result in failed_tests:
                lines.append(f"[FAIL] {result.test_id}")
                
                if result.is_pattern_test and result.pattern_id:
                    lines.append(f"  Pattern: Pattern {result.pattern_id} ({result.pattern_name})")
                
                if result.error_msg:
                    # Truncate long error messages
                    error_lines = result.error_msg.split('\n')
                    for eline in error_lines[:5]:  # First 5 lines
                        lines.append(f"  {eline}")
                
                lines.append(f"  Duration: {result.duration:.3f}s")
                lines.append("")
            
            lines.append("-" * 95)
            lines.append("")
        
        # Detailed Test Results
        lines.append("-" * 95)
        lines.append("DETAILED TEST RESULTS".center(95))
        lines.append("-" * 95)
        lines.append(f"| {'Test Script':<18} | {'Test Class':<20} | {'Test Name':<30} | {'Status':<6} | {'Duration':<8} |")
        lines.append(f"|{'-' * 20}|{'-' * 22}|{'-' * 32}|{'-' * 8}|{'-' * 10}|")
        
        for result in self.test_results:
            script = result.test_script[:17] if result.test_script else ""
            test_class = result.test_class[:19] if result.test_class else ""
            method = result.test_method[:29] if result.test_method else ""
            lines.append(
                f"| {script:<18} | {test_class:<20} | {method:<30} | {result.status:<6} | {result.duration:.3f}s |"
            )
        
        lines.append("-" * 95)
        lines.append("")
        
        # Footer
        if output_path:
            lines.append(f"Report saved to: {output_path}")
        lines.append("=" * 95)
        
        report = '\n'.join(lines)
        
        # Save to file if path provided
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(report, encoding='utf-8')
        
        return report


# Singleton instance for use by test runner
_global_reporter = ComprehensiveTestReporter()


def get_reporter() -> ComprehensiveTestReporter:
    """Get the global test reporter instance."""
    return _global_reporter
