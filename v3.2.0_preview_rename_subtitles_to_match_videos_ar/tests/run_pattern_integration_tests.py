"""
Pattern Integration Test Runner - FIXED DESIGN

Runs comprehensive integration tests on ACTUAL fixture files (not copies).
Tests validate real renaming behavior and generate reports in tests/reports/.

DESIGN:
1. Backup fixture files to pattern_folder/backup/ before testing
2. Run renaming on ACTUAL fixtures (you see the renames!)
3. Verify renamed files and generate comprehensive .txt report
4. User restores manually using reset script
5. Reset script preserves tests/reports/

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
import argparse
from datetime import datetime
from typing import Dict, List, Tuple

from tests.csv_report_parser import CSVReportParser, extract_var_tag


class IntegrationTestRunner:
    """Runs pattern integration tests on ACTUAL fixture files."""
    
    def __init__(self):
        """Initialize test runner."""
        self.patterns = self._load_patterns()
        self.fixtures_dir = Path(__file__).parent / 'fixtures' / 'pattern_files'
        self.reports_dir = Path(__file__).parent / 'reports'
        self.reports_dir.mkdir(exist_ok=True)
        
        self.total_variations = 0
        self.passed_variations = 0
        self.failed_variations = 0
        self.failed_details = []  # Store failed variation details
        self.test_results = []  # Store for comprehensive report
        
        # Initialize report
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        self.report_file = self.reports_dir / f'integration-test-{timestamp}.txt'
        self.report_lines = []
    
    def _load_patterns(self) -> Dict:
        """Load pattern definitions."""
        pattern_file = Path(__file__).parent / 'fixtures' / 'pattern_definitions.json'
        with open(pattern_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {p['id']: p for p in data['patterns']}
    
    def _backup_pattern_files(self, pattern_dir: Path):
        """Backup all files in pattern directory to backup/ subdirectory."""
        backup_dir = pattern_dir / 'backup'
        backup_dir.mkdir(exist_ok=True)
        
        # Backup all files (except backup dir itself and csv reports)
        for file in pattern_dir.iterdir():
            if file.is_file() and not file.name.endswith('.csv'):
                shutil.copy2(file, backup_dir / file.name)
    
    def _restore_from_backup(self, pattern_dir: Path):
        """Restore files from backup directory."""
        backup_dir = pattern_dir / 'backup'
        if not backup_dir.exists():
            return
        
        # Restore all files from backup
        for file in backup_dir.iterdir():
            if file.is_file():
                shutil.copy2(file, pattern_dir / file.name)
    
    def run_rename_on_pattern(self, pattern_id: int) -> Path:
        """
        Run REAL subfast_rename.py on ACTUAL fixture files.
        
        Args:
            pattern_id: Pattern ID to test
        
        Returns:
            Path to generated renaming_report.csv
        """
        pattern = self.patterns[pattern_id]
        pattern_name_clean = pattern['name'].replace('##', '').replace('#', '').replace(' ', '_').strip('_')
        pattern_dir = self.fixtures_dir / f"pattern_{pattern_id:02d}_{pattern_name_clean}"
        
        # Backup files before testing
        self._backup_pattern_files(pattern_dir)
        
        # Run script from original location, passing pattern folder path as argument
        rename_script = project_root / 'subfast' / 'scripts' / 'subfast_rename.py'
        
        try:
            # Run script from original location with pattern folder as CWD
            # Script reads files from current working directory
            result = subprocess.run(
                [sys.executable, str(rename_script)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(pattern_dir)  # Run IN the pattern directory
            )
            
            # Find generated CSV report in pattern directory
            csv_report = pattern_dir / 'renaming_report.csv'
            
            if not csv_report.exists():
                raise FileNotFoundError(
                    f"CSV report not generated!\n"
                    f"Script: {rename_script}\n"
                    f"Pattern Directory: {pattern_dir}\n"
                    f"Exit Code: {result.returncode}\n"
                    f"STDOUT:\n{result.stdout}\n"
                    f"STDERR:\n{result.stderr}"
                )
            
            return csv_report
            
        except subprocess.TimeoutExpired:
            # Restore from backup on timeout
            self._restore_from_backup(pattern_dir)
            raise RuntimeError(f"Renaming script timed out for pattern {pattern_id}")
        except Exception as e:
            # Restore from backup on error
            self._restore_from_backup(pattern_dir)
            raise
    
    def verify_renamed_files(self, pattern_id: int, pattern_dir: Path) -> List[str]:
        """
        Verify that files were actually renamed in the pattern directory.
        
        Returns:
            List of verification notes
        """
        notes = []
        
        # Check for renamed subtitle files (should have .ar.srt extension based on config)
        renamed_subtitles = list(pattern_dir.glob('*.ar.srt'))
        original_subtitles = list(pattern_dir.glob('[[]VAR*[]].srt'))
        
        if renamed_subtitles:
            notes.append(f"Found {len(renamed_subtitles)} renamed subtitle files")
        else:
            notes.append("WARNING: No renamed subtitle files found (.ar.srt)")
        
        return notes
    
    def test_pattern(self, pattern_id: int) -> Tuple[int, int]:
        """
        Test a single pattern and return (passed, failed) counts.
        
        Args:
            pattern_id: Pattern ID to test
        
        Returns:
            Tuple of (passed_count, failed_count)
        """
        pattern = self.patterns[pattern_id]
        pattern_name_clean = pattern['name'].replace('##', '').replace('#', '').replace(' ', '_').strip('_')
        pattern_dir = self.fixtures_dir / f"pattern_{pattern_id:02d}_{pattern_name_clean}"
        variations = pattern['variations']
        
        section_header = "=" * 100
        pattern_header = f"Pattern {pattern_id:02d}: {pattern['name']}"
        
        print(section_header)
        print(pattern_header)
        print(section_header)
        print()
        
        self.report_lines.append(section_header)
        self.report_lines.append(pattern_header)
        self.report_lines.append(section_header)
        self.report_lines.append("")
        
        # Run renaming script
        try:
            csv_path = self.run_rename_on_pattern(pattern_id)
            parser = CSVReportParser(csv_path)
            
            # Verify files were renamed
            verify_notes = self.verify_renamed_files(pattern_id, pattern_dir)
            for note in verify_notes:
                print(f"  {note}")
                self.report_lines.append(f"  {note}")
            print()
            self.report_lines.append("")
            
        except Exception as e:
            error_msg = f"[ERROR] Failed to run renaming script: {e}"
            print(error_msg)
            print()
            self.report_lines.append(error_msg)
            self.report_lines.append("")
            
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
            
            var_header = f"[{var_id}] Expected: {expected}"
            print(var_header)
            self.report_lines.append(var_header)
            
            if not entry:
                # Entry not found in CSV - extract patterns from actual files on disk
                from subfast.scripts.common import pattern_engine
                
                # Find actual files on disk with this VAR tag
                # Use rglob with prefix to avoid bracket issues in glob patterns
                all_videos = list(pattern_dir.glob("*.mkv")) + list(pattern_dir.glob("*.mp4"))
                all_subtitles = list(pattern_dir.glob("*.srt")) + list(pattern_dir.glob("*.ass"))
                
                video_files = [f for f in all_videos if f.name.startswith(f"[{var_id}]-")]
                subtitle_files = [f for f in all_subtitles if f.name.startswith(f"[{var_id}]-")]
                
                video_file = video_files[0] if video_files else None
                subtitle_file = subtitle_files[0] if subtitle_files else None
                
                # Extract patterns from the actual files
                video_extracted = pattern_engine.get_episode_number_cached(video_file.name) if video_file else None
                subtitle_extracted = pattern_engine.get_episode_number_cached(subtitle_file.name) if subtitle_file else None
                
                # Determine match status
                video_match = (video_extracted == expected) if video_extracted else False
                subtitle_match = (subtitle_extracted == expected) if subtitle_extracted else False
                
                # Overall status
                both_exist = (video_file and subtitle_file)
                both_match = (video_match and subtitle_match)
                overall_status = "PASS" if both_match else "FAIL"
                
                fail_msg = f"  [FAIL] No match pair for {expected} [X]"
                print(fail_msg)
                self.report_lines.append(fail_msg)
                
                # Show video extraction
                if video_file:
                    video_status = "[MATCH]" if video_match else "[NO MATCH]"
                    video_line = f"  Video:    {video_file.name:<50} -> Extracted: {video_extracted or 'None':<8} | {video_status}"
                    print(video_line)
                    self.report_lines.append(video_line)
                else:
                    video_line = f"  Video:    FILE NOT FOUND on disk"
                    print(video_line)
                    self.report_lines.append(video_line)
                
                # Show subtitle extraction
                if subtitle_file:
                    subtitle_status = "[MATCH]" if subtitle_match else "[NO MATCH]"
                    subtitle_line = f"  Subtitle: {subtitle_file.name:<50} -> Extracted: {subtitle_extracted or 'None':<8} | {subtitle_status}"
                    print(subtitle_line)
                    self.report_lines.append(subtitle_line)
                else:
                    subtitle_line = f"  Subtitle: FILE NOT FOUND on disk"
                    print(subtitle_line)
                    self.report_lines.append(subtitle_line)
                
                # Show pairing status
                # Files are PAIRED only if both exist AND both patterns match
                pairing_status = "PAIRED" if (both_exist and both_match) else "NOT PAIRED [X]"
                pairing_line = f"  Pairing:  Video <-> Subtitle {pairing_status:<25} | Status: {overall_status}"
                print(pairing_line)
                self.report_lines.append(pairing_line)
                
                separator = "  " + "-" * 94
                print(separator)
                print()
                self.report_lines.append(separator)
                self.report_lines.append("")
                
                failed += 1
                
                # Add detailed failure info
                if video_file and subtitle_file:
                    if not video_match and not subtitle_match:
                        self.failed_details.append(f"Pattern {pattern_id:02d} [{var_id}] - Both video and subtitle pattern mismatch (expected {expected}, got video={video_extracted}, subtitle={subtitle_extracted})")
                    elif not video_match:
                        self.failed_details.append(f"Pattern {pattern_id:02d} [{var_id}] - Video pattern mismatch (expected {expected}, got {video_extracted})")
                    elif not subtitle_match:
                        self.failed_details.append(f"Pattern {pattern_id:02d} [{var_id}] - Subtitle pattern mismatch (expected {expected}, got {subtitle_extracted})")
                elif not video_file:
                    self.failed_details.append(f"Pattern {pattern_id:02d} [{var_id}] - Video file not found")
                elif not subtitle_file:
                    self.failed_details.append(f"Pattern {pattern_id:02d} [{var_id}] - Subtitle file not found")
                
                continue
            
            # Check video extraction
            video_match = entry.extracted_episode == expected
            video_status = "[MATCH]" if video_match else "[MISMATCH]"
            
            # Check subtitle extraction
            subtitle_match = entry.extracted_episode == expected
            subtitle_status = "[MATCH]" if subtitle_match else "[MISMATCH]"
            
            # Check pairing
            paired = bool(entry.original_video and entry.original_subtitle)
            pairing_status = "PAIRED" if paired else "NOT PAIRED"
            
            # Overall status
            overall_pass = video_match and subtitle_match and paired
            overall_status = "PASS" if overall_pass else "FAIL"
            
            # Display results
            video_line = f"  Video:    {entry.original_video:<50} -> Extracted: {entry.extracted_episode:<8} | {video_status}"
            subtitle_line = f"  Subtitle: {entry.original_subtitle:<50} -> Extracted: {entry.extracted_episode:<8} | {subtitle_status}"
            pairing_line = f"  Pairing:  Video <-> Subtitle {pairing_status:<20} | Status: {overall_status}"
            
            print(video_line)
            print(subtitle_line)
            print(pairing_line)
            
            self.report_lines.append(video_line)
            self.report_lines.append(subtitle_line)
            self.report_lines.append(pairing_line)
            
            if not overall_pass:
                # Show error details
                if not video_match or not subtitle_match:
                    error_line = f"  [ERROR] Extraction mismatch! Expected '{expected}', got '{entry.extracted_episode}'"
                    print(error_line)
                    self.report_lines.append(error_line)
                if not paired:
                    error_line = f"  [ERROR] Video and subtitle not paired!"
                    print(error_line)
                    self.report_lines.append(error_line)
                failed += 1
            else:
                passed += 1
            
            separator = "  " + "-" * 94
            print(separator)
            print()
            self.report_lines.append(separator)
            self.report_lines.append("")
        
        # Pattern summary
        pattern_summary = f"Pattern {pattern_id:02d} Summary: {passed}/{passed+failed} PASSED ({passed/(passed+failed)*100:.1f}%)" if (passed+failed) > 0 else f"Pattern {pattern_id:02d} Summary: 0/0"
        print(pattern_summary)
        self.report_lines.append(pattern_summary)
        
        if failed > 0:
            fail_summary = f"                  {failed} FAILED"
            print(fail_summary)
            self.report_lines.append(fail_summary)
        
        print(section_header)
        print()
        self.report_lines.append(section_header)
        self.report_lines.append("")
        
        return (passed, failed)
    
    def run_all_patterns(self, pattern_filter=None, save_report=True):
        """Run tests on all patterns or filtered patterns.
        
        Args:
            pattern_filter: Optional pattern ID to test only one pattern
            save_report: If True, save individual integration report (default: True)
                        Set to False when called from unified test runner
        """
        import time
        start_time = time.time()
        
        # Determine which patterns to test
        if pattern_filter:
            pattern_ids = [pattern_filter] if pattern_filter in self.patterns else []
            if not pattern_ids:
                print(f"[ERROR] Pattern {pattern_filter} not found!")
                return
        else:
            pattern_ids = sorted(self.patterns.keys())
        
        # Print header to console
        print()
        print("=" * 100)
        print("SUBFAST PATTERN INTEGRATION TESTS")
        print("=" * 100)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Test Run: {timestamp}")
        print()
        
        # Run tests
        for pattern_id in pattern_ids:
            passed, failed = self.test_pattern(pattern_id)
            self.passed_variations += passed
            self.failed_variations += failed
            self.total_variations += (passed + failed)
        
        # Final summary
        self.print_final_summary()
        
        # Build report with summary at TOP
        self.build_report(timestamp)
        
        # Save report to file (only if save_report=True)
        if save_report:
            self.save_report()
        
        # Calculate duration
        end_time = time.time()
        self.test_duration = end_time - start_time
        
        # Return exit code (0 = success, 1 = failures)
        return 0 if self.failed_variations == 0 else 1
    
    def print_final_summary(self):
        """Print final test summary to console."""
        print()
        print("=" * 100)
        print("SUMMARY")
        print("=" * 100)
        
        patterns_tested = len([p for p in self.patterns if any(v['var_id'] in str(self.test_results) for v in self.patterns[p]['variations'])])
        
        print(f"Total Patterns Tested:  {patterns_tested}")
        print(f"Total Variations:       {self.total_variations}")
        print(f"Passed:                 {self.passed_variations} ({self.passed_variations/self.total_variations*100:.1f}%)" if self.total_variations > 0 else "Passed: 0")
        print(f"Failed:                 {self.failed_variations} ({self.failed_variations/self.total_variations*100:.1f}%)" if self.total_variations > 0 else "Failed: 0")
        
        if self.failed_variations > 0:
            print()
            print("FAILED VARIATIONS:")
            for detail in self.failed_details:
                print(f"  - {detail}")
        
        print()
        print("=" * 100)
        
        # Return exit code
        return 0 if self.failed_variations == 0 else 1
    
    def build_report(self, timestamp):
        """Build comprehensive report with summary at TOP."""
        report = []
        
        # Header
        report.append("=" * 100)
        report.append("SUBFAST PATTERN INTEGRATION TESTS")
        report.append("=" * 100)
        report.append(f"Test Run: {timestamp}")
        report.append("")
        
        # SUMMARY AT TOP
        report.append("=" * 100)
        report.append("SUMMARY")
        report.append("=" * 100)
        
        patterns_tested = len(set(d.split('[')[0].strip().split()[-1] for d in self.failed_details)) if self.failed_details else len(self.patterns)
        
        report.append(f"Total Patterns Tested:  {patterns_tested}")
        report.append(f"Total Variations:       {self.total_variations}")
        report.append(f"Passed:                 {self.passed_variations} ({self.passed_variations/self.total_variations*100:.1f}%)" if self.total_variations > 0 else "Passed: 0")
        report.append(f"Failed:                 {self.failed_variations} ({self.failed_variations/self.total_variations*100:.1f}%)" if self.total_variations > 0 else "Failed: 0")
        
        if self.failed_variations > 0:
            report.append("")
            report.append("FAILED VARIATIONS:")
            for detail in self.failed_details:
                report.append(f"  - {detail}")
        
        report.append("=" * 100)
        report.append("")
        report.append("")
        
        # DETAILED RESULTS
        report.append("=" * 100)
        report.append("DETAILED TEST RESULTS")
        report.append("=" * 100)
        report.append("")
        
        # Add all test results
        report.extend(self.report_lines)
        
        self.report_lines = report
    
    def save_report(self):
        """Save comprehensive report to tests/reports/."""
        report_content = '\n'.join(self.report_lines)
        
        self.report_file.write_text(report_content, encoding='utf-8')
        
        print()
        print(f"Comprehensive report saved to: {self.report_file}")
        print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Run SubFast pattern integration tests on ACTUAL fixture files',
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
