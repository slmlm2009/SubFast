"""
Pattern Matching Integration Tests

These tests validate the ENTIRE workflow:
1. Run subfast_rename.py on dummy files
2. Parse generated CSV reports
3. Verify extracted episodes match expected results
4. Verify video/subtitle pairing works correctly

This is TRUE integration testing - testing what users actually experience.
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
import unittest
from typing import Dict, List

from tests.csv_report_parser import CSVReportParser, extract_var_tag


class PatternIntegrationTest(unittest.TestCase):
    """Base class for pattern integration tests."""
    
    @classmethod
    def setUpClass(cls):
        """Load pattern definitions once for all tests."""
        pattern_file = Path(__file__).parent / 'fixtures' / 'pattern_definitions.json'
        with open(pattern_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        cls.patterns = {p['id']: p for p in data['patterns']}
        cls.fixtures_dir = Path(__file__).parent / 'fixtures' / 'pattern_files'
    
    def run_rename_on_pattern(self, pattern_id: int) -> Path:
        """
        Run REAL subfast_rename.py on a pattern directory.
        
        Args:
            pattern_id: Pattern ID to test
        
        Returns:
            Path to generated renaming_report.csv
        """
        pattern = self.patterns[pattern_id]
        pattern_name_clean = pattern['name'].replace('##', '').replace('#', '').replace(' ', '_').strip('_')
        pattern_dir = self.fixtures_dir / f"pattern_{pattern_id:02d}_{pattern_name_clean}"
        
        # Create temporary directory for testing
        temp_dir = Path(tempfile.mkdtemp(prefix=f"subfast_test_pattern_{pattern_id:02d}_"))
        
        # Copy files to temp directory
        temp_pattern_dir = temp_dir / pattern_dir.name
        shutil.copytree(pattern_dir, temp_pattern_dir)
        
        # Use REAL script and config
        rename_script = project_root / 'subfast' / 'scripts' / 'subfast_rename.py'
        real_config = project_root / 'subfast' / 'config.ini'
        
        # Copy real config to temp directory so script can find it
        temp_config = temp_pattern_dir / 'config.ini'
        shutil.copy(real_config, temp_config)
        
        try:
            # Run script in the pattern directory (script expects to run in target directory)
            result = subprocess.run(
                [sys.executable, str(rename_script)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(temp_pattern_dir)  # Run IN the directory with files
            )
            
            # Find generated CSV report (should be in same directory)
            csv_report = temp_pattern_dir / 'renaming_report.csv'
            
            if not csv_report.exists():
                self.fail(
                    f"CSV report not generated!\n"
                    f"Script: {rename_script}\n"
                    f"Working Directory: {temp_pattern_dir}\n"
                    f"Config: {temp_config}\n"
                    f"Exit Code: {result.returncode}\n"
                    f"STDOUT:\n{result.stdout}\n"
                    f"STDERR:\n{result.stderr}"
                )
            
            return csv_report
            
        except subprocess.TimeoutExpired:
            self.fail(f"Renaming script timed out for pattern {pattern_id}")
        except Exception as e:
            self.fail(f"Failed to run renaming script: {e}")
    
    def verify_pattern(self, pattern_id: int):
        """
        Verify a pattern by running integration test.
        
        Args:
            pattern_id: Pattern ID to verify
        """
        pattern = self.patterns[pattern_id]
        variations = pattern['variations']
        
        # Run renaming script
        csv_path = self.run_rename_on_pattern(pattern_id)
        
        # Parse CSV report
        parser = CSVReportParser(csv_path)
        
        # Verify each variation
        for variation in variations:
            var_id = variation['var_id']
            expected = variation['expected']
            
            with self.subTest(pattern=pattern_id, var_id=var_id):
                # Find entry in CSV report
                entry = parser.find_by_var_tag(var_id)
                
                self.assertIsNotNone(
                    entry,
                    f"Pattern {pattern_id} [{var_id}]: No entry found in CSV report!"
                )
                
                # Verify extracted episode matches expected
                self.assertEqual(
                    entry.extracted_episode,
                    expected,
                    f"Pattern {pattern_id} [{var_id}]: "
                    f"Expected '{expected}', extracted '{entry.extracted_episode}'\n"
                    f"Video: {entry.original_video}\n"
                    f"Subtitle: {entry.original_subtitle}"
                )
                
                # Verify pairing (both video and subtitle should be present)
                self.assertTrue(
                    entry.original_video and entry.original_subtitle,
                    f"Pattern {pattern_id} [{var_id}]: "
                    f"Video and subtitle not paired!\n"
                    f"Video: {entry.original_video or 'MISSING'}\n"
                    f"Subtitle: {entry.original_subtitle or 'MISSING'}"
                )


# Generate test class for each pattern
def create_pattern_test_class(pattern_id: int, pattern_name: str):
    """Dynamically create a test class for a pattern."""
    
    class_name = f"TestPattern{pattern_id:02d}_{pattern_name.replace(' ', '').replace('#', '').replace('.', '_')}"
    
    def test_pattern(self):
        """Test this pattern."""
        self.verify_pattern(pattern_id)
    
    # Create class dynamically
    test_class = type(
        class_name,
        (PatternIntegrationTest,),
        {
            'test_pattern': test_pattern,
            '__doc__': f'Integration tests for Pattern {pattern_id}: {pattern_name}'
        }
    )
    
    return test_class


# Load patterns and generate test classes
pattern_file = Path(__file__).parent / 'fixtures' / 'pattern_definitions.json'
with open(pattern_file, 'r', encoding='utf-8') as f:
    pattern_data = json.load(f)

# Create test class for each pattern
for pattern in pattern_data['patterns']:
    pattern_id = pattern['id']
    pattern_name = pattern['name']
    test_class = create_pattern_test_class(pattern_id, pattern_name)
    globals()[test_class.__name__] = test_class


if __name__ == '__main__':
    unittest.main(verbosity=2)
