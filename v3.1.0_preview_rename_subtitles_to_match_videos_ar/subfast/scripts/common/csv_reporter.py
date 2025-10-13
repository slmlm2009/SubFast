"""
CSV Reporter Module

Handles CSV export functionality for renaming and embedding operations.
Provides consistent reporting format across both modules.

Version: 3.1.0
"""

import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any


def generate_csv_report(
    results: List[Dict[str, Any]],
    output_path: Path,
    operation_type: str = 'renaming'
) -> None:
    """
    Generate CSV report for SubFast operations.
    
    Args:
        results: List of operation result dictionaries
        output_path: Path where CSV file should be written
        operation_type: Either 'renaming' or 'embedding'
    """
    if not results:
        print("[INFO] No results to export")
        return
    
    try:
        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            if operation_type == 'renaming':
                _write_renaming_report(f, results)
            elif operation_type == 'embedding':
                _write_embedding_report(f, results)
            else:
                raise ValueError(f"Unknown operation type: {operation_type}")
        
        print(f"\n[INFO] CSV report exported: {output_path}")
    
    except Exception as e:
        print(f"[WARNING] Failed to generate CSV report: {e}")


def _write_renaming_report(file_handle, results: List[Dict[str, Any]]) -> None:
    """Write renaming-specific CSV report."""
    writer = csv.writer(file_handle)
    
    # Header
    writer.writerow([
        'Original Filename',
        'New Filename',
        'Status',
        'Episode',
        'Timestamp'
    ])
    
    # Data rows
    for result in results:
        writer.writerow([
            result.get('original_name', result.get('original', '')),
            result.get('new_name', ''),
            result.get('status', 'Unknown'),
            result.get('episode', 'N/A'),
            datetime.now().isoformat()
        ])


def _write_embedding_report(file_handle, results: List[Dict[str, Any]]) -> None:
    """Write embedding-specific CSV report."""
    writer = csv.writer(file_handle)
    
    # Header
    writer.writerow([
        'Original Video',
        'Original Subtitle',
        'Language Code',
        'Status',
        'Error Message',
        'Timestamp',
        'Execution Time (s)'
    ])
    
    # Data rows
    for result in results:
        writer.writerow([
            result.get('video', ''),
            result.get('subtitle', ''),
            result.get('language', 'None'),
            result.get('status', 'Unknown'),
            result.get('error', ''),
            result.get('timestamp', datetime.now().isoformat()),
            f"{result.get('execution_time', 0):.3f}"
        ])


def format_execution_time(seconds: float) -> str:
    """
    Format execution time in human-readable format.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted string (e.g., "2.5s" or "1m 30s")
    """
    if seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"


def calculate_statistics(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate summary statistics from results.
    
    Args:
        results: List of operation results
        
    Returns:
        Dictionary with statistics (total, success, failed, etc.)
    """
    total = len(results)
    # Accept multiple success statuses: 'renamed', 'success', 'Success', 'embedded'
    success_statuses = {'renamed', 'success', 'Success', 'embedded'}
    success = sum(1 for r in results if r.get('status') in success_statuses)
    failed = total - success
    
    total_time = sum(r.get('execution_time', 0) for r in results)
    avg_time = total_time / total if total > 0 else 0
    
    return {
        'total': total,
        'success': success,
        'failed': failed,
        'success_rate': (success / total * 100) if total > 0 else 0,
        'total_time': total_time,
        'average_time': avg_time
    }


def print_summary(
    results: List[Dict[str, Any]], 
    operation_name: str = 'Operation',
    execution_time: str = None,
    renamed_count: int = None,
    total_subtitles: int = None,
    total_files: int = None
) -> None:
    """
    Print formatted summary of operations.
    
    Args:
        results: List of operation results
        operation_name: Name of the operation for display
        execution_time: Formatted execution time string
        renamed_count: Number of successfully renamed files
        total_subtitles: Total number of subtitle files
        total_files: Total number of files processed (videos + subtitles)
    """
    stats = calculate_statistics(results)
    
    print("\n" + "=" * 60)
    print(f"{operation_name} Summary")
    print("=" * 60)
    
    # Use provided values if available, otherwise calculate from results
    if total_files is not None:
        print(f"Files Processed: {total_files}")
    else:
        print(f"Total files processed: {stats['total']}")
    
    if renamed_count is not None and total_subtitles is not None:
        print(f"Subtitles Renamed: {renamed_count}/{total_subtitles}")
        success_rate = (renamed_count / total_subtitles * 100) if total_subtitles > 0 else 0
        print(f"Success rate: {success_rate:.1f}%")
    else:
        print(f"Successful: {stats['success']}")
        print(f"Failed: {stats['failed']}")
        print(f"Success rate: {stats['success_rate']:.1f}%")
    
    if execution_time:
        print(f"Total Execution Time: {execution_time}")
    else:
        print(f"Total time: {format_execution_time(stats['total_time'])}")
    
    print("=" * 60)
