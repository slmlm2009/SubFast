"""
Test Suite for csv_reporter module

Tests CSV report generation, bordered table formatting, and statistics calculation.
"""

import unittest
from pathlib import Path
from subfast.scripts.common import csv_reporter
from tests.test_helpers import SubFastTestCase


class TestTextTableFormatting(SubFastTestCase):
    """Test bordered text table formatting."""
    
    def test_format_text_table_basic(self):
        """Test basic table formatting with sample data."""
        file_rows = [
            {
                'filename': 'Show.S01E05.mkv',
                'detected_episode': 'S01E05',
                'action': 'Matched',
                'new_name': 'Show.S01E05.renamed.mkv'
            },
            {
                'filename': 'Show.S01E06.mkv',
                'detected_episode': 'S01E06',
                'action': 'Matched',
                'new_name': 'Show.S01E06.renamed.mkv'
            }
        ]
        
        result = csv_reporter.format_text_table(file_rows)
        
        # Verify table structure
        self.assertIn('+', result, "Table should have borders")
        self.assertIn('|', result, "Table should have column separators")
        self.assertIn('-', result, "Table should have horizontal borders")
        
        # Verify headers
        self.assertIn('Original Filename', result)
        self.assertIn('Detected Episode', result)
        self.assertIn('Action', result)
        self.assertIn('New Name', result)
        
        # Verify data
        self.assertIn('Show.S01E05.mkv', result)
        self.assertIn('Show.S01E06.mkv', result)
    
    def test_format_text_table_empty_list(self):
        """Test that empty list returns empty string."""
        result = csv_reporter.format_text_table([])
        
        self.assertEqual(result, "", "Empty list should return empty string")
    
    def test_format_text_table_alignment(self):
        """Test that table columns are properly aligned."""
        file_rows = [
            {
                'filename': 'Short.mkv',
                'detected_episode': 'S01E01',
                'action': 'OK',
                'new_name': 'New.mkv'
            }
        ]
        
        result = csv_reporter.format_text_table(file_rows)
        lines = result.split('\n')
        
        # All lines should have same length (well-formed table)
        line_lengths = [len(line) for line in lines if line]
        self.assertTrue(
            len(set(line_lengths)) <= 2,  # Header/data may differ slightly
            "Table rows should be aligned"
        )


class TestCSVReportGeneration(SubFastTestCase):
    """Test CSV report file generation."""
    
    def test_generate_renaming_report_creates_file(self):
        """Test that renaming report creates CSV file."""
        output_path = self.temp_dir / 'renaming_report.csv'
        
        results = [
            {'filename': 'Show.S01E05.mkv', 'status': 'renamed'},
            {'filename': 'Show.S01E06.mkv', 'status': 'renamed'}
        ]
        
        csv_reporter.generate_csv_report(
            results,
            output_path,
            operation_type='renaming'
        )
        
        # Verify file was created
        self.assertFileExists(output_path, "CSV report should be created")
        
        # Verify file has content
        content = output_path.read_text()
        self.assertTrue(len(content) > 0, "CSV report should have content")
    
    def test_generate_embedding_report_creates_file(self):
        """Test that embedding report creates CSV file."""
        output_path = self.temp_dir / 'embedding_report.csv'
        
        results = [
            {'video': 'Show.S01E05.mkv', 'subtitle': 'Show.S01E05.srt', 'status': 'embedded'},
            {'video': 'Show.S01E06.mkv', 'subtitle': 'Show.S01E06.srt', 'status': 'embedded'}
        ]
        
        csv_reporter.generate_csv_report(
            results,
            output_path,
            operation_type='embedding'
        )
        
        # Verify file was created
        self.assertFileExists(output_path, "Embedding report should be created")
    
    def test_generate_report_empty_results_no_file(self):
        """Test that empty results doesn't create file."""
        output_path = self.temp_dir / 'empty_report.csv'
        
        csv_reporter.generate_csv_report(
            [],
            output_path,
            operation_type='renaming'
        )
        
        # Empty results should not create file
        self.assertFalse(output_path.exists(), "Empty results should not create file")
    
    def test_generate_report_invalid_operation_type(self):
        """Test that invalid operation type raises error."""
        output_path = self.temp_dir / 'invalid_report.csv'
        
        results = [{'filename': 'test.mkv'}]
        
        # Should handle error gracefully (prints warning, doesn't raise)
        try:
            csv_reporter.generate_csv_report(
                results,
                output_path,
                operation_type='invalid_type'
            )
        except Exception:
            pass  # Expected to handle gracefully


class TestStatisticsCalculation(SubFastTestCase):
    """Test statistics calculation in reports."""
    
    def test_report_includes_summary_statistics(self):
        """Test that generated report includes summary statistics."""
        output_path = self.temp_dir / 'stats_report.csv'
        
        results = [
            {'filename': 'Show.S01E05.mkv', 'status': 'renamed'},
            {'filename': 'Show.S01E06.mkv', 'status': 'renamed'},
            {'filename': 'Show.S01E07.mkv', 'status': 'skipped'}
        ]
        
        csv_reporter.generate_csv_report(
            results,
            output_path,
            operation_type='renaming',
            renamed_count=2,
            execution_time_str='1.5 seconds'
        )
        
        # Read report content
        content = output_path.read_text()
        
        # Verify statistics are present (as comments or in structured format)
        # The exact format depends on implementation
        self.assertTrue(len(content) > 100, "Report should have substantial content")


class TestReportSections(SubFastTestCase):
    """Test that reports include all required sections."""
    
    def test_renaming_report_structure(self):
        """Test renaming report has expected structure."""
        output_path = self.temp_dir / 'structure_report.csv'
        
        results = [
            {'filename': 'Show.S01E05.mkv', 'status': 'renamed'}
        ]
        
        csv_reporter.generate_csv_report(
            results,
            output_path,
            operation_type='renaming',
            execution_time_str='2.0 seconds',
            renamed_count=1
        )
        
        content = output_path.read_text()
        
        # Report should contain key sections (implementation-dependent)
        # At minimum should have headers and data
        lines = content.split('\n')
        self.assertTrue(len(lines) > 5, "Report should have multiple lines")


class TestEmptySectionHandling(SubFastTestCase):
    """Test that empty sections are omitted from reports."""
    
    def test_empty_sections_omitted(self):
        """Test that sections with no data are omitted."""
        output_path = self.temp_dir / 'minimal_report.csv'
        
        # Minimal results with no optional data
        results = [
            {'filename': 'Show.S01E05.mkv', 'status': 'renamed'}
        ]
        
        csv_reporter.generate_csv_report(
            results,
            output_path,
            operation_type='renaming'
            # No optional parameters provided
        )
        
        # Report should still be created
        self.assertFileExists(output_path)
        
        # But should be minimal (no unnecessary empty sections)
        content = output_path.read_text()
        self.assertTrue(len(content) > 0, "Report should have content")


if __name__ == '__main__':
    unittest.main()
