"""
Module: run_tests.py
Purpose: Test runner with comprehensive reporting

Executes SubFast test suite and generates detailed bordered table reports.
Reports are ALWAYS generated automatically (no flag required).
"""

import unittest
import sys
import argparse
from pathlib import Path
from datetime import datetime
import time

# CRITICAL: Add project root to Python path for imports
# This allows running tests directly without setting PYTHONPATH manually
project_root = Path(__file__).parent.parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


class ReportingTestResult(unittest.TextTestResult):
    """Enhanced test result that captures detailed information for reporting."""
    
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.test_times = {}
        self.test_details = []
    
    def startTest(self, test):
        """Record test start time."""
        super().startTest(test)
        self.test_times[test] = time.time()
    
    def addSuccess(self, test):
        """Record successful test."""
        super().addSuccess(test)
        duration = time.time() - self.test_times.get(test, time.time())
        self.test_details.append({
            'test_id': str(test),
            'status': 'PASS',
            'duration': duration,
            'error': ''
        })
    
    def addError(self, test, err):
        """Record test error."""
        super().addError(test, err)
        duration = time.time() - self.test_times.get(test, time.time())
        self.test_details.append({
            'test_id': str(test),
            'status': 'FAIL',
            'duration': duration,
            'error': self._exc_info_to_string(err, test)
        })
    
    def addFailure(self, test, err):
        """Record test failure."""
        super().addFailure(test, err)
        duration = time.time() - self.test_times.get(test, time.time())
        self.test_details.append({
            'test_id': str(test),
            'status': 'FAIL',
            'duration': duration,
            'error': self._exc_info_to_string(err, test)
        })
    
    def addSkip(self, test, reason):
        """Record skipped test."""
        super().addSkip(test, reason)
        self.test_details.append({
            'test_id': str(test),
            'status': 'SKIP',
            'duration': 0.0,
            'error': reason
        })


class ReportingTestRunner(unittest.TextTestRunner):
    """Test runner that generates comprehensive reports."""
    
    resultclass = ReportingTestResult
    
    def __init__(self, *args, generate_report=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_report = generate_report
    
    def run(self, test):
        """Run tests and optionally generate comprehensive report."""
        # Run tests with enhanced result
        result = super().run(test)
        
        # Generate comprehensive report only if requested
        if self.generate_report:
            self._generate_report(result)
        
        return result
    
    def _generate_report(self, result):
        """Generate and save comprehensive bordered table report."""
        from tests.test_reporter import ComprehensiveTestReporter
        
        reporter = ComprehensiveTestReporter()
        reporter.start_time = getattr(result, 'start_time', time.time())
        reporter.end_time = time.time()
        
        # Add all test results
        for detail in result.test_details:
            reporter.add_result(
                detail['test_id'],
                detail['status'],
                detail['duration'],
                detail['error']
            )
        
        # Generate report
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        report_dir = Path(__file__).parent / 'reports'
        report_path = report_dir / f'test-results-{timestamp}.txt'
        
        report_text = reporter.generate_report(report_path)
        
        # Print report to terminal
        print("\n")
        print(report_text)


def main():
    """Run SubFast test suite with optional filtering."""
    parser = argparse.ArgumentParser(
        description='SubFast Test Runner with Comprehensive Reporting',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python run_tests.py              # Run all tests (report auto-generated)
  python run_tests.py test_config  # Run specific module
  python run_tests.py -v           # Verbose output
  
Reports are ALWAYS generated automatically in tests/reports/
        '''
    )
    
    parser.add_argument(
        'module',
        nargs='?',
        help='Specific test module to run (e.g., test_config_loader)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose test output'
    )
    
    args = parser.parse_args()
    
    unittest_exit_code = 0
    
    # Set up test discovery (excluding test_pattern_matching - replaced by integration tests)
    tests_dir = Path(__file__).parent
    
    if args.module:
        # Run specific module
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromName(f'tests.{args.module}')
    else:
        # Discover all tests EXCEPT test_pattern_matching (replaced by integration tests)
        loader = unittest.TestLoader()
        all_tests = loader.discover(str(tests_dir), pattern='test_*.py')
        
        # Filter out test_pattern_matching
        suite = unittest.TestSuite()
        for test_group in all_tests:
            for test_case in test_group:
                if 'test_pattern_matching' not in str(test_case):
                    suite.addTest(test_case)
    
    # Run unit tests (without report generation - will be unified)
    verbosity = 2 if args.verbose else 1
    runner = ReportingTestRunner(verbosity=verbosity, generate_report=False)
    result = runner.run(suite)
    
    unittest_exit_code = 0 if result.wasSuccessful() else 1
    
    # Run pattern integration tests (replaces old test_pattern_matching.py)
    print("\n")
    print("=" * 100)
    print("PATTERN INTEGRATION TESTS")
    print("=" * 100)
    print()
    
    from run_pattern_integration_tests import IntegrationTestRunner
    integration_runner = IntegrationTestRunner()
    integration_exit_code = integration_runner.run_all_patterns(save_report=False)  # Don't save separate report
    
    # Generate unified comprehensive report
    from unified_test_reporter import UnifiedTestReporter
    unified_reporter = UnifiedTestReporter()
    
    # Set unit test data
    unified_reporter.set_unit_test_data(
        test_results=result.test_details,
        total=result.testsRun,
        passed=result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped),
        failed=len(result.failures) + len(result.errors),
        skipped=len(result.skipped),
        duration=sum(d['duration'] for d in result.test_details)
    )
    
    # Set integration test data
    unified_reporter.set_integration_test_data(
        total_variations=integration_runner.total_variations,
        passed=integration_runner.passed_variations,
        failed=integration_runner.failed_variations,
        failed_details=integration_runner.failed_details,
        output_lines=integration_runner.report_lines,
        duration=getattr(integration_runner, 'test_duration', 0.0)
    )
    
    # Extract embedding test data (if embedding test ran and created output)
    embedding_output_dir = Path(__file__).parent / '2- Embedding' / 'test_output'
    embedded_files = list(embedding_output_dir.glob('embedded_*.mkv')) if embedding_output_dir.exists() else []
    
    if embedded_files:
        # Read config to get settings
        from common import config_loader
        config = config_loader.load_config()
        lang_code = config.get('embedding_language_code', 'ar')
        default_flag = config.get('default_flag', True)
        
        # Get the first embedded file (there should only be one from the test)
        output_file = embedded_files[0]
        
        # Get track info using mkvmerge
        mkvmerge_path = Path(__file__).parent.parent / 'subfast' / 'bin' / 'mkvmerge.exe'
        if mkvmerge_path.exists():
            import subprocess
            result = subprocess.run(
                [str(mkvmerge_path), '-i', str(output_file)],
                capture_output=True,
                text=True,
                timeout=5
            )
            tracks_output = result.stdout
        else:
            tracks_output = "Track information not available"
        
        unified_reporter.set_embedding_test_data(
            output_file=str(output_file.relative_to(Path(__file__).parent.parent)),
            file_size=output_file.stat().st_size / (1024**2),
            lang_code=lang_code,
            default_flag=default_flag,
            tracks=tracks_output
        )
    
    # Generate and save unified report
    unified_report_lines = unified_reporter.generate_report()
    reports_dir = Path(__file__).parent / 'reports'
    report_path = unified_reporter.save_report(reports_dir)
    
    print(f"\nUnified comprehensive report saved to: {report_path}\n")
    
    # Exit with combined code (fail if either failed)
    sys.exit(max(unittest_exit_code, integration_exit_code))


if __name__ == '__main__':
    main()
