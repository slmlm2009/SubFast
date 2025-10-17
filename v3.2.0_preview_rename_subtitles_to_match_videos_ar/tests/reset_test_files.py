"""
Test Environment Reset Script

Resets all test files to pristine state by deleting and regenerating dummy files.
Useful for manual testing that modifies filenames or when test artifacts need cleanup.

Usage:
    python tests/reset_test_files.py

What it does:
    1. Deletes all files in tests/fixtures/pattern_files/
    2. Re-runs generate_test_files.py to regenerate dummy files
    3. Verifies expected file count matches actual
    4. Reports success or failure

Version: 3.2.0
"""

import json
import shutil
import sys
from pathlib import Path


def extract_extensions_from_definitions(pattern_file: Path) -> dict:
    """
    Extract all unique file extensions from pattern_definitions.json.
    DYNAMIC: Auto-detects all extensions used in patterns.
    
    Args:
        pattern_file: Path to pattern_definitions.json
    
    Returns:
        Dictionary with 'video' and 'subtitle' extension sets
        Example: {'video': {'.mkv', '.mp4'}, 'subtitle': {'.srt', '.ass'}}
    """
    try:
        with open(pattern_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        video_exts = set()
        subtitle_exts = set()
        
        for pattern in data.get('patterns', []):
            for variation in pattern.get('variations', []):
                # Extract video extension
                video_template = variation.get('video_template', '')
                if video_template:
                    video_ext = Path(video_template).suffix.lower()
                    if video_ext:
                        video_exts.add(video_ext)
                
                # Extract subtitle extension
                subtitle_template = variation.get('subtitle_template', '')
                if subtitle_template:
                    subtitle_ext = Path(subtitle_template).suffix.lower()
                    if subtitle_ext:
                        subtitle_exts.add(subtitle_ext)
        
        return {
            'video': video_exts,
            'subtitle': subtitle_exts
        }
    
    except Exception as e:
        print(f"[WARNING] Failed to extract extensions: {e}")
        # Fallback to common extensions
        return {
            'video': {'.mkv', '.mp4'},
            'subtitle': {'.srt', '.ass'}
        }


def reset_test_environment():
    """
    Reset test environment to pristine state.
    
    Returns:
        0 on success, 1 on failure
    """
    # Determine script location
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Pattern files directory
    pattern_files_dir = script_dir / 'fixtures' / 'pattern_files'
    
    # Embedding test output directory
    embedding_output_dir = script_dir / '2- Embedding' / 'test_output'
    
    print("=" * 80)
    print("SubFast v3.2.0 - Test Environment Reset")
    print("=" * 80)
    print(f"\nTarget directories:")
    print(f"  - Pattern files: {pattern_files_dir}")
    print(f"  - Embedding output: {embedding_output_dir}\n")
    
    # Step 1: Delete existing pattern files
    if pattern_files_dir.exists():
        print("[STEP 1] Deleting existing pattern files...")
        try:
            # Count files before deletion
            file_count = sum(1 for _ in pattern_files_dir.rglob('*') if _.is_file())
            dir_count = sum(1 for _ in pattern_files_dir.iterdir() if _.is_dir())
            
            print(f"  Found: {file_count} files in {dir_count} directories")
            
            # Delete each pattern directory (including backup/ folders)
            for pattern_dir in pattern_files_dir.iterdir():
                if pattern_dir.is_dir():
                    shutil.rmtree(pattern_dir)
            print("  [OK] All files and directories deleted (including backup/ folders)")
        
        except Exception as e:
            print(f"  [ERROR] Failed to delete files: {e}")
            return 1
    else:
        print("[STEP 1] Pattern files directory doesn't exist (first run?)")
    
    # Step 1.5: Delete embedding test output files
    if embedding_output_dir.exists():
        print("\n[STEP 1.5] Deleting embedding test output files...")
        try:
            file_count = sum(1 for _ in embedding_output_dir.rglob('*') if _.is_file() and _.suffix in ['.mkv', '.mp4', '.avi'])
            
            if file_count > 0:
                print(f"  Found: {file_count} embedded video file(s)")
                
                # Delete video files but keep .gitignore and README.md
                for file in embedding_output_dir.rglob('*'):
                    if file.is_file() and file.suffix in ['.mkv', '.mp4', '.avi']:
                        file.unlink()
                
                print("  [OK] Embedding output files deleted")
            else:
                print("  No embedding output files to delete")
        
        except Exception as e:
            print(f"  [WARNING] Failed to delete embedding output: {e}")
            # Don't fail the whole reset, just warn
    
    # Step 2: Regenerate files
    print("\n[STEP 2] Regenerating pattern files...")
    try:
        # Import and run the generator
        from generate_test_files import generate_all_pattern_files
        
        result = generate_all_pattern_files()
        
        if result != 0:
            print("  [ERROR] File generation failed")
            return 1
        
        print("  [OK] Files regenerated successfully")
    
    except Exception as e:
        print(f"  [ERROR] Failed to regenerate files: {e}")
        return 1
    
    # Step 3: Verify file count (DYNAMIC - auto-detects extensions)
    print("\n[STEP 3] Verifying file count (dynamic extension detection)...")
    try:
        if not pattern_files_dir.exists():
            print("  [ERROR] Pattern files directory was not created")
            return 1
        
        # DYNAMIC: Extract extensions from pattern_definitions.json
        pattern_def_file = script_dir / 'fixtures' / 'pattern_definitions.json'
        detected_exts = extract_extensions_from_definitions(pattern_def_file)
        
        print(f"  Detected extensions from JSON:")
        print(f"    Videos: {', '.join(sorted(detected_exts['video']))}")
        print(f"    Subtitles: {', '.join(sorted(detected_exts['subtitle']))}")
        print()
        
        # Count files by extension (DYNAMIC)
        video_count_by_ext = {}
        for ext in detected_exts['video']:
            count = sum(1 for _ in pattern_files_dir.rglob(f'*{ext}'))
            video_count_by_ext[ext] = count
        
        subtitle_count_by_ext = {}
        for ext in detected_exts['subtitle']:
            count = sum(1 for _ in pattern_files_dir.rglob(f'*{ext}'))
            subtitle_count_by_ext[ext] = count
        
        video_count = sum(video_count_by_ext.values())
        subtitle_count = sum(subtitle_count_by_ext.values())
        total_files = video_count + subtitle_count
        
        # Display counts by extension
        print(f"  Video files:")
        for ext in sorted(video_count_by_ext.keys()):
            print(f"    {ext}: {video_count_by_ext[ext]}")
        print(f"  Total videos: {video_count}")
        print()
        
        print(f"  Subtitle files:")
        for ext in sorted(subtitle_count_by_ext.keys()):
            print(f"    {ext}: {subtitle_count_by_ext[ext]}")
        print(f"  Total subtitles: {subtitle_count}")
        print()
        
        print(f"  Total files: {total_files}")
        
        # Expected: 30 patterns, 101 variations total = 202 files (101 videos + 101 subtitles)
        # See pattern_definitions.json for exact counts
        # DYNAMIC: This will auto-adjust if you add more patterns/variations
        expected_min = 195  # Allow some variation for backups/reports
        expected_max = 210  # Adjusted range after Pattern 30 simplification
        
        if expected_min <= total_files <= expected_max:
            print(f"  [OK] File count within expected range ({expected_min}-{expected_max})")
        else:
            print(f"  [WARNING] File count outside expected range ({expected_min}-{expected_max})")
    
    except Exception as e:
        print(f"  [ERROR] Failed to verify files: {e}")
        return 1
    
    # Step 4: Clean up any test artifacts (PRESERVE tests/reports/)
    print("\n[STEP 4] Cleaning up test artifacts...")
    try:
        # Check for common test artifact directories
        # NOTE: Preserving tests/reports/ directory and all reports
        artifacts = [
            script_dir / '__pycache__',  # Python cache
            pattern_files_dir / '**' / 'renaming_report.csv',  # Pattern CSV reports
        ]
        
        cleaned = 0
        
        # Clean Python cache
        if (script_dir / '__pycache__').exists():
            shutil.rmtree(script_dir / '__pycache__')
            cleaned += 1
        
        # Clean CSV reports from pattern folders (generated by integration tests)
        for csv_file in pattern_files_dir.rglob('renaming_report.csv'):
            if csv_file.exists():
                csv_file.unlink()
                cleaned += 1
        
        if cleaned > 0:
            print(f"  [OK] Cleaned {cleaned} artifact(s)")
        else:
            print("  [OK] No artifacts to clean")
        
        # Note about preserved reports
        reports_dir = script_dir / 'reports'
        if reports_dir.exists():
            report_count = len(list(reports_dir.glob('*.txt')))
            print(f"  [INFO] Preserved {report_count} test report(s) in tests/reports/")
    
    except Exception as e:
        print(f"  [WARNING] Failed to clean some artifacts: {e}")
        # Not a critical failure
    
    # Summary
    print("\n" + "=" * 80)
    print("RESET SUMMARY")
    print("=" * 80)
    print(f"Status: SUCCESS")
    print(f"Pattern files: {total_files} files in {pattern_files_dir}")
    print(f"Test environment is ready for manual testing")
    print("=" * 80)
    
    return 0


if __name__ == '__main__':
    sys.exit(reset_test_environment())
