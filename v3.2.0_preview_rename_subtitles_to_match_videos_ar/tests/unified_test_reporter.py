"""
Module: unified_test_reporter.py
Purpose: Unified comprehensive test report generator

Combines unit test and integration test results into a single comprehensive report.
"""

from datetime import datetime
from pathlib import Path
from typing import List, Dict


class UnifiedTestReporter:
    """Generates comprehensive reports combining unit and integration tests."""
    
    def __init__(self):
        self.report_lines = []
        self.start_time = None
        self.total_duration = 0.0
        
        # Unit test data
        self.unit_test_results = []
        self.unit_total = 0
        self.unit_passed = 0
        self.unit_failed = 0
        self.unit_skipped = 0
        self.unit_duration = 0.0
        
        # Integration test data
        self.integration_total_variations = 0
        self.integration_passed = 0
        self.integration_failed = 0
        self.integration_failed_details = []
        self.integration_output = []
        self.integration_duration = 0.0
    
    def set_unit_test_data(self, test_results, total, passed, failed, skipped, duration):
        """Set unit test results data."""
        self.unit_test_results = test_results
        self.unit_total = total
        self.unit_passed = passed
        self.unit_failed = failed
        self.unit_skipped = skipped
        self.unit_duration = duration
    
    def set_integration_test_data(self, total_variations, passed, failed, failed_details, output_lines, duration):
        """Set integration test results data."""
        self.integration_total_variations = total_variations
        self.integration_passed = passed
        self.integration_failed = failed
        self.integration_failed_details = failed_details
        self.integration_output = output_lines
        self.integration_duration = duration
    
    def generate_report(self) -> List[str]:
        """Generate comprehensive unified report."""
        self.report_lines = []
        
        # Calculate totals
        total_tests = self.unit_total + self.integration_total_variations
        total_passed = self.unit_passed + self.integration_passed
        total_failed = self.unit_failed + self.integration_failed
        total_skipped = self.unit_skipped  # Integration tests don't skip
        self.total_duration = self.unit_duration + self.integration_duration
        
        # Header
        self._add_header()
        
        # Summary Statistics
        self._add_summary_statistics(total_tests, total_passed, total_failed, total_skipped)
        
        # Unit Test Summary
        self._add_unit_test_summary()
        
        # Integration Test Summary
        self._add_integration_test_summary()
        
        # Detailed Unit Test Results
        self._add_detailed_unit_test_results()
        
        # Detailed Integration Test Results
        self._add_detailed_integration_test_results()
        
        return self.report_lines
    
    def _add_header(self):
        """Add report header."""
        self.report_lines.append("=" * 100)
        self.report_lines.append("SUBFAST TEST EXECUTION REPORT".center(100))
        self.report_lines.append("=" * 100)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.report_lines.append(f"Test Run: {timestamp}")
        self.report_lines.append(f"Total Duration: {self.total_duration:.2f} seconds")
        self.report_lines.append("")
    
    def _add_summary_statistics(self, total, passed, failed, skipped):
        """Add overall summary statistics."""
        self.report_lines.append("-" * 100)
        self.report_lines.append("OVERALL SUMMARY STATISTICS".center(100))
        self.report_lines.append("-" * 100)
        
        pass_pct = (passed / total * 100) if total > 0 else 0
        fail_pct = (failed / total * 100) if total > 0 else 0
        skip_pct = (skipped / total * 100) if total > 0 else 0
        
        self.report_lines.append("| Metric                       | Count  | Percentage |")
        self.report_lines.append("|------------------------------|--------|------------|")
        self.report_lines.append(f"| Total Tests Run              | {total:<6} | {100.00:>9.2f}% |")
        self.report_lines.append(f"| Tests Passed                 | {passed:<6} | {pass_pct:>9.2f}% |")
        self.report_lines.append(f"| Tests Failed                 | {failed:<6} | {fail_pct:>9.2f}% |")
        self.report_lines.append(f"| Tests Skipped                | {skipped:<6} | {skip_pct:>9.2f}% |")
        self.report_lines.append(f"| Total Execution Time         | {self.total_duration:.2f}s |            |")
        self.report_lines.append("-" * 100)
        self.report_lines.append("")
    
    def _add_unit_test_summary(self):
        """Add unit test summary section."""
        self.report_lines.append("-" * 100)
        self.report_lines.append("UNIT TEST SUMMARY".center(100))
        self.report_lines.append("=" * 100)
        
        # Group by test script
        script_stats = {}
        failed_tests = []
        skipped_tests = []
        
        for result in self.unit_test_results:
            # Parse test_id to extract script name
            test_id = result.get('test_id', '')
            script = 'unknown'
            
            # Format: "test_method (tests.test_module.TestClass)"
            if '(' in test_id and ')' in test_id:
                module_part = test_id.split('(')[1].split(')')[0]
                parts = module_part.split('.')
                if len(parts) >= 2:
                    script = parts[1]  # test_config_loader
            
            if script not in script_stats:
                script_stats[script] = {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0}
            
            script_stats[script]['total'] += 1
            if result.get('status') == 'PASS':
                script_stats[script]['passed'] += 1
            elif result.get('status') in ['FAIL', 'ERROR']:
                script_stats[script]['failed'] += 1
                failed_tests.append(test_id)
            elif result.get('status') == 'SKIP':
                script_stats[script]['skipped'] += 1
                skipped_tests.append(test_id)
        
        # Table
        self.report_lines.append("-" * 100)
        self.report_lines.append("| Test Script               | Total  | Passed | Failed | Skipped | Pass %   |")
        self.report_lines.append("|---------------------------|--------|--------|--------|---------|----------|")
        
        for script in sorted(script_stats.keys()):
            stats = script_stats[script]
            pass_pct = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            self.report_lines.append(
                f"| {script:<25} | {stats['total']:<6} | {stats['passed']:<6} | "
                f"{stats['failed']:<6} | {stats['skipped']:<7} | {pass_pct:>7.2f}% |"
            )
        
        self.report_lines.append("-" * 100)
        
        # Failed and skipped tests
        if failed_tests:
            self.report_lines.append("FAILED TESTS:")
            for test in failed_tests:
                self.report_lines.append(f"  - {test}")
        
        if skipped_tests:
            self.report_lines.append("SKIPPED TESTS:")
            for test in skipped_tests:
                self.report_lines.append(f"  - {test}")
        
        self.report_lines.append("-" * 100)
        self.report_lines.append("")
    
    def _add_integration_test_summary(self):
        """Add integration test summary section."""
        self.report_lines.append("-" * 100)
        self.report_lines.append("INTEGRATION TEST SUMMARY".center(100))
        self.report_lines.append("=" * 100)
        
        pass_pct = (self.integration_passed / self.integration_total_variations * 100) if self.integration_total_variations > 0 else 0
        fail_pct = (self.integration_failed / self.integration_total_variations * 100) if self.integration_total_variations > 0 else 0
        
        self.report_lines.append(f"Total Patterns Tested:  25")
        self.report_lines.append(f"Total Variations:       {self.integration_total_variations}")
        self.report_lines.append(f"Passed:                 {self.integration_passed} ({pass_pct:.1f}%)")
        self.report_lines.append(f"Failed:                 {self.integration_failed} ({fail_pct:.1f}%)")
        self.report_lines.append("")
        
        if self.integration_failed_details:
            self.report_lines.append("FAILED VARIATIONS:")
            for detail in self.integration_failed_details:
                self.report_lines.append(f"  - {detail}")
        
        self.report_lines.append("=" * 100)
        self.report_lines.append("")
    
    def _add_detailed_unit_test_results(self):
        """Add detailed unit test results table."""
        self.report_lines.append("-" * 100)
        self.report_lines.append("DETAILED UNIT TEST RESULTS".center(100))
        self.report_lines.append("=" * 100)
        
        self.report_lines.append("| Test Script        | Test Class           | Test Name                      | Status | Duration |")
        self.report_lines.append("|--------------------|----------------------|--------------------------------|--------|----------|")
        
        for result in self.unit_test_results:
            # Parse test_id to get components
            test_id = result.get('test_id', '')
            
            # Format: "test_method (tests.test_module.TestClass)"
            if '(' in test_id and ')' in test_id:
                method_part = test_id.split('(')[0].strip()
                module_part = test_id.split('(')[1].split(')')[0]
                parts = module_part.split('.')
                
                if len(parts) >= 3:
                    script = parts[1][:18]  # test_config_loader
                    test_class = parts[2][:20]  # TestBooleanParsing
                    test_name = method_part[:30]  # test_method
                else:
                    script = 'unknown'[:18]
                    test_class = ''[:20]
                    test_name = test_id[:30]
            else:
                script = 'unknown'[:18]
                test_class = ''[:20]
                test_name = test_id[:30]
            
            status = result.get('status', 'UNKNOWN')
            duration = f"{result.get('duration', 0.0):.3f}s"
            
            self.report_lines.append(
                f"| {script:<18} | {test_class:<20} | {test_name:<30} | {status:<6} | {duration:>8} |"
            )
        
        self.report_lines.append("-" * 100)
        self.report_lines.append("")
    
    def _add_detailed_integration_test_results(self):
        """Add detailed integration test results."""
        self.report_lines.append("-" * 100)
        self.report_lines.append("DETAILED INTEGRATION TEST RESULTS".center(100))
        self.report_lines.append("=" * 100)
        self.report_lines.append("")
        
        # Add all integration test output
        self.report_lines.extend(self.integration_output)
    
    def save_report(self, output_dir: Path):
        """Save unified report to file."""
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        report_path = output_dir / f"test-results-{timestamp}.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.report_lines))
        
        return report_path
