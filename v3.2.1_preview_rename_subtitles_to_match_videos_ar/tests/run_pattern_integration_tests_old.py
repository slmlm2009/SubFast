"""
Pattern Integration Test Runner

Runs comprehensive integration tests on all 25 patterns with detailed,
formatted output showing extraction results and pairing status.

Usage:
    python tests/run_pattern_integration_tests.py
    python tests/run_pattern_integration_tests.py --pattern 21
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import json
import shutil
import subprocess
import tempfile
import argparse
from datetime import datetime
from typing import Dict, List, Tuple

from tests.csv_report_parser import CSVReportParser, extract_var_tag


class IntegrationTestRunner:
    """Runs pattern integration tests with formatted output."""
    
    def __init__(self):
        """Initialize test runner."""
        self.patterns = self._load_patterns()
        self.fixtures_dir = Path(__file__).parent / 'fixtures' / 'pattern_files'
        self.total_variations = 0
        self.passed_variations = 0
        self.failed_variations = 0
        self.failed_details = []
    
    def _load_patterns(self) -> Dict:
        """Load pattern definitions."""
        pattern_file = Path(__file__).parent / 'fixtures' / 'pattern_definitions.json'
        with open(pattern_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {p['id']: p for p in data['patterns']}
    
    def run_rename_on_pattern(self, pattern_id: int) -> Path:
        """Run subfast_rename.py on a pattern directory."""
        pattern = self.patterns[pattern_id]
        pattern_name_clean = pattern['name'].replace('##', '').replace('#', '').replace(' ', '_').strip('_')
        pattern_dir = self.fixtures_dir / f"pattern_{pattern_id:02d}_{pattern_name_clean}"
        
        # Create temporary directory
        temp_dir = Path(tempfile.mkdtemp(prefix=f"subfast_test_pattern_{pattern_id:02d}_"))
        
        # Copy files to temp directory
        temp_pattern_dir = temp_dir / pattern_dir.name
        shutil.copytree(pattern_dir, temp_pattern_dir)
        
        # Copy real config
        real_config = project_root / 'subfast' / 'config.ini'
        temp_config = temp_pattern_dir / 'config.ini'
        shutil.copy(real_config, temp_config)
        
        # Run script
        rename_script = project_root / 'subfast' / 'scripts' / 'subfast_rename.py'
        
        try:
            result = subprocess.run(
                [sys.executable, str(rename_script)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(temp_pattern_dir)
            )
            
            csv_report = temp_pattern_dir / 'renaming_report.csv'
            
            if not csv_report.exists():
                raise FileNotFoundError(
                    f"CSV report not generated!\n"
                    f"Exit Code: {result.returncode}\n"
                    f"STDOUT:\n{result.stdout}\n"
                    f"STDERR:\n{result.stderr}"
                )
            
            return csv_report
            
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"Renaming script timed out for pattern {pattern_id}")
    
    def test_pattern(self, pattern_id: int) -> Tuple[int, int]:
        """
        Test a single pattern and return (passed, failed) counts.
        
        Args:
            pattern_id: Pattern ID to test
        
        Returns:
            Tuple of (passed_count, failed_count)
        """
        pattern = self.patterns[pattern_id]
        variations = pattern['variations']
        
        print("=" * 100)
        print(f"Pattern {pattern_id:02d}: {pattern['name']}")
        print("=" * 100)
        print()
        
        # Run renaming script
        try:
            csv_path = self.run_rename_on_pattern(pattern_id)
            parser = CSVReportParser(csv_path)
        except Exception as e:
            print(f"[ERROR] Failed to run renaming script: {e}")
            print()
            for variation in variations:
                self.failed_variations += 1
                self.failed_details.append(f"Pattern {pattern_id:02d} [{variation['var_id']}] - Script execution failed")
            return (0, len(variations))
        
        passed = 0
        failed = 0
        
        # Test each variation
        for variation in variations:
            var_id = variation['var_id']
            expected = variation['expected']
            
            # Find entry in CSV
            entry = parser.find_by_var_tag(var_id)
            
            print(f"[{var_id}] Expected: {expected}")
            
            if not entry:
                # Entry not found
                print(f"  [FAIL] No entry found in CSV report!")
                print(f"  Video:    NOT FOUND")
                print(f"  Subtitle: NOT FOUND")
                print()
                failed += 1
                self.failed_details.append(f"Pattern {pattern_id:02d} [{var_id}] - No CSV entry")
                continue
            
            # Check video extraction
            video_match = entry.extracted_episode == expected
            video_status = "[MATCH]" if video_match else "[MISMATCH]"
            
            # Check subtitle extraction (should be same as video)
            subtitle_match = entry.extracted_episode == expected
            subtitle_status = "[MATCH]" if subtitle_match else "[MISMATCH]"
            
            # Check pairing
            paired = bool(entry.original_video and entry.original_subtitle)
            pairing_status = "PAIRED" if paired else "NOT PAIRED"
            
            # Overall status
            overall_pass = video_match and subtitle_match and paired
            overall_status = "PASS" if overall_pass else "FAIL"
            
            # Display results
            print(f"  Video:    {entry.original_video:<50} -> Extracted: {entry.extracted_episode:<8} | {video_status}")
            print(f"  Subtitle: {entry.original_subtitle:<50} -> Extracted: {entry.extracted_episode:<8} | {subtitle_status}")
            print(f"  Pairing:  Video <-> Subtitle {pairing_status:<20} | Status: {overall_status}")
            
            if not overall_pass:
                # Show error details
                if not video_match or not subtitle_match:
                    print(f"  [ERROR] Extraction mismatch! Expected '{expected}', got '{entry.extracted_episode}'")
                if not paired:
                    print(f"  [ERROR] Video and subtitle not paired!")
                failed += 1
                self.failed_details.append(
                    f"Pattern {pattern_id:02d} [{var_id}] - Expected {expected}, got {entry.extracted_episode}, paired={paired}"
                )
            else:
                passed += 1
            
            print("  " + "-" * 94)
            print()
        
        return (passed, failed)
    
    def run_all_patterns(self, pattern_filter=None):
        """Run tests on all patterns or filtered patterns."""
        print()
        print("=" * 100)
        print("SUBFAST PATTERN INTEGRATION TESTS")
        print("=" * 100)
        print(f"Test Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Determine which patterns to test
        if pattern_filter:
            pattern_ids = [pattern_filter] if pattern_filter in self.patterns else []
            if not pattern_ids:
                print(f"[ERROR] Pattern {pattern_filter} not found!")
                return
        else:
            pattern_ids = sorted(self.patterns.keys())
        
        # Run tests
        for pattern_id in pattern_ids:
            passed, failed = self.test_pattern(pattern_id)
            self.passed_variations += passed
            self.failed_variations += failed
            self.total_variations += (passed + failed)
            
            # Pattern summary
            total = passed + failed
            pass_rate = (passed / total * 100) if total > 0 else 0
            print(f"Pattern {pattern_id:02d} Summary: {passed}/{total} PASSED ({pass_rate:.1f}%)")
            if failed > 0:
                print(f"                  {failed} FAILED")
            print("=" * 100)
            print()
        
        # Final summary
        self.print_final_summary()
    
    def print_final_summary(self):
        """Print final test summary."""
        print()
        print("=" * 100)
        print("FINAL SUMMARY")
        print("=" * 100)
        print(f"Total Patterns Tested:  {len(self.patterns)}")
        print(f"Total Variations:       {self.total_variations}")
        print(f"Passed:                 {self.passed_variations} ({self.passed_variations/self.total_variations*100:.1f}%)" if self.total_variations > 0 else "Passed: 0")
        print(f"Failed:                 {self.failed_variations} ({self.failed_variations/self.total_variations*100:.1f}%)" if self.total_variations > 0 else "Failed: 0")
        print()
        
        if self.failed_variations > 0:
            print("FAILED VARIATIONS:")
            for detail in self.failed_details:
                print(f"  - {detail}")
            print()
        
        print("=" * 100)
        
        # Exit code
        return 0 if self.failed_variations == 0 else 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Run SubFast pattern integration tests',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--pattern',
        type=int,
        help='Test specific pattern only (1-25)'
    )
    
    args = parser.parse_args()
    
    runner = IntegrationTestRunner()
    exit_code = runner.run_all_patterns(args.pattern)
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
