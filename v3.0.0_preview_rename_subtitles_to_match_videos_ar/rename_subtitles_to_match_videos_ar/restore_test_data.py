#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Restore Test Data - Reset Test Files Before New Test Run

This script restores original test files from backups/ folders back to their
parent directories, preparing for a fresh test run.

WORKFLOW:
1. Run integration test → creates embedded files, moves originals to backups/
2. Manually verify results (check embedded videos work)
3. Run this script → restores originals from backups/ for next test
4. Run integration test again → fresh test with original files

Usage:
    python restore_test_data.py
    
Or from tests:
    from restore_test_data import restore_test_data
    restore_test_data()
"""

import sys
from pathlib import Path
import shutil


def restore_test_data(base_dir=None):
    """
    Restore original test files from backups/ folders.
    
    This function:
    1. Finds all backups/ directories in test folders
    2. Moves original files back to parent directory
    3. Removes embedded files (ones without matching backups)
    4. Removes empty backups/ directories
    
    Args:
        base_dir: Base directory containing test folders (default: ../tests)
        
    Returns:
        tuple: (total_restored, directories_processed)
    """
    if base_dir is None:
        # Default to tests/ directory relative to this script
        script_dir = Path(__file__).parent
        base_dir = script_dir.parent / 'tests'
    else:
        base_dir = Path(base_dir)
    
    if not base_dir.exists():
        print(f"[ERROR] Test directory not found: {base_dir}")
        return 0, 0
    
    print("="*80)
    print("RESTORING TEST DATA FROM BACKUPS")
    print("="*80)
    print(f"Base directory: {base_dir}\n")
    
    total_restored = 0
    directories_processed = 0
    
    # Find all backups/ directories recursively
    backup_dirs = list(base_dir.rglob('backups'))
    
    if not backup_dirs:
        print("[INFO] No backups/ directories found - test data already in original state")
        return 0, 0
    
    for backup_dir in backup_dirs:
        if not backup_dir.is_dir():
            continue
            
        parent_dir = backup_dir.parent
        print(f"\n[RESTORE] Processing: {parent_dir.relative_to(base_dir)}/")
        print(f"          Backup folder: {backup_dir.relative_to(base_dir)}/")
        
        # Get list of files in backup
        backup_files = list(backup_dir.glob('*'))
        
        if not backup_files:
            print(f"  [INFO] Backup folder is empty, removing it")
            backup_dir.rmdir()
            continue
        
        files_restored = 0
        
        # Restore each file from backup
        for backup_file in backup_files:
            if not backup_file.is_file():
                continue
                
            dest_file = parent_dir / backup_file.name
            
            # If embedded version exists in parent, remove it first
            if dest_file.exists():
                print(f"  [DELETE] Removing embedded version: {dest_file.name}")
                dest_file.unlink()
            
            # Move original from backup back to parent
            print(f"  [RESTORE] {backup_file.name}")
            shutil.move(str(backup_file), str(dest_file))
            files_restored += 1
            total_restored += 1
        
        # Remove empty backups directory
        try:
            backup_dir.rmdir()
            print(f"  [CLEANUP] Removed empty backups/ folder")
        except OSError:
            print(f"  [WARNING] Could not remove backups/ folder (not empty)")
        
        directories_processed += 1
        print(f"  [SUMMARY] Restored {files_restored} file(s)")
    
    print("\n" + "="*80)
    print("RESTORATION COMPLETE")
    print("="*80)
    print(f"Total files restored: {total_restored}")
    print(f"Directories processed: {directories_processed}")
    print("\nTest data is ready for a fresh test run!")
    print("="*80)
    
    return total_restored, directories_processed


def main():
    """Command-line interface for restore script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Restore test data from backups before new test run',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python restore_test_data.py
  python restore_test_data.py --test-dir ../tests
  
Workflow:
  1. Run integration test
  2. Manually verify embedded videos work
  3. Run this script to restore originals
  4. Run integration test again for fresh test
        """
    )
    
    parser.add_argument(
        '--test-dir',
        type=str,
        help='Path to tests directory (default: ../tests relative to script)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be restored without actually doing it'
    )
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("[DRY RUN MODE - No files will be modified]\n")
        # TODO: Implement dry-run logic
        print("[INFO] Dry-run mode not yet implemented")
        return 1
    
    try:
        restored, processed = restore_test_data(args.test_dir)
        
        if restored == 0:
            print("\n[INFO] No files needed restoration")
            return 0
        
        return 0
        
    except Exception as e:
        print(f"\n[ERROR] Restoration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
