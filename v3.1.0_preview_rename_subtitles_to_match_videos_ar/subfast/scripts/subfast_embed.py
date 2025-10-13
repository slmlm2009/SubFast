#!/usr/bin/env python3
"""
SubFast - Embedding Module
Version: 3.1.0

Fast subtitle embedding into MKV video files using mkvmerge.
Automatically embeds subtitle files into corresponding MKV video files based on
intelligent pattern matching to find matching pairs.

Features:
- Automatic video-subtitle file matching
- Configurable mkvmerge.exe path
- Backup of original files (.original.mkv suffix)
- Language tag detection from subtitle filenames
- Batch processing of multiple files
"""

import os
import sys
import json
import subprocess
import shutil
import argparse
from pathlib import Path
from datetime import datetime
import time

# Import shared modules
from common import config_loader
from common import pattern_engine
from common import csv_reporter


__version__ = "3.1.0"

# Exit codes
EXIT_SUCCESS = 0
EXIT_FATAL_ERROR = 1
EXIT_PARTIAL_FAILURE = 2
EXIT_COMPLETE_FAILURE = 3


def load_language_codes():
    """Load language codes from JSON file."""
    json_path = Path(__file__).parent.parent / 'resources' / 'data' / 'mkvmerge_language_codes.json'
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[WARNING] Language codes file not found: {json_path}")
        print("[INFO] Language detection will be limited")
        return {'codes': {}, 'common_two_letter_codes': {}}
    except json.JSONDecodeError as e:
        print(f"[WARNING] Failed to parse language codes file: {e}")
        return {'codes': {}, 'common_two_letter_codes': {}}


# Load language codes at module level
LANGUAGE_DATA = load_language_codes()


def is_valid_language_code(lang):
    """Check if language code is valid for mkvmerge."""
    if not lang:
        return False
    code_lower = lang.lower()
    return (code_lower in LANGUAGE_DATA.get('codes', {}) or 
            code_lower in LANGUAGE_DATA.get('common_two_letter_codes', {}))


def normalize_language_code(code):
    """Normalize language code to 3-letter ISO 639-2 format."""
    if not code:
        return None
    code_lower = code.lower()
    
    # Already 3-letter code
    if code_lower in LANGUAGE_DATA.get('codes', {}):
        return code_lower
    
    # Convert 2-letter to 3-letter
    two_letter_map = LANGUAGE_DATA.get('common_two_letter_codes', {})
    if code_lower in two_letter_map:
        return two_letter_map[code_lower]
    
    return None


def detect_language_from_filename(filename):
    """
    Detect language code from subtitle filename.
    
    Looks for patterns like:
    - filename.ar.srt
    - filename.en.forced.srt
    - filename.ara.ass
    """
    name_without_ext = filename.rsplit('.', 1)[0] if '.' in filename else filename
    parts = name_without_ext.split('.')
    
    # Check last few parts for language codes
    for part in reversed(parts[-3:]):
        part_lower = part.lower().strip()
        
        # Skip common non-language parts
        if part_lower in ('forced', 'sdh', 'cc', 'hi'):
            continue
        
        # Try to normalize
        normalized = normalize_language_code(part_lower)
        if normalized:
            return normalized
    
    return None


def detect_language_with_fallback(filename, config_language):
    """
    Detect language with fallback: filename → config → none.
    """
    # Tier 1: Try filename detection
    filename_lang = detect_language_from_filename(filename)
    if filename_lang:
        return filename_lang
    
    # Tier 2: Try config value
    if config_language:
        normalized = normalize_language_code(config_language)
        if normalized:
            return normalized
        else:
            print(f"[WARNING] Invalid language code in config: '{config_language}'")
    
    # Tier 3: No language
    return None


def find_mkvmerge(config_path):
    """
    Find mkvmerge executable.
    
    Search order:
    1. config['mkvmerge_path'] if specified
    2. Script directory
    3. System PATH
    """
    config_mkvmerge = config_path.strip() if config_path else ""
    
    # Check config path first
    if config_mkvmerge and Path(config_mkvmerge).is_file():
        return Path(config_mkvmerge)
    
    # Check script directory
    script_dir = Path(__file__).parent.parent
    local_mkvmerge = script_dir / 'mkvmerge.exe'
    if local_mkvmerge.is_file():
        return local_mkvmerge
    
    # Check system PATH
    if shutil.which('mkvmerge'):
        return Path(shutil.which('mkvmerge'))
    
    return None


def create_backup(video_path):
    """Create backup of original video file."""
    backup_path = video_path.with_suffix('.original' + video_path.suffix)
    counter = 1
    original_backup = backup_path
    
    while backup_path.exists():
        backup_path = original_backup.with_stem(f"{original_backup.stem}_{counter}")
        counter += 1
    
    shutil.copy2(video_path, backup_path)
    return backup_path


def embed_subtitle(video_path, subtitle_path, mkvmerge_path, language_code, default_flag):
    """
    Embed subtitle into MKV video file using mkvmerge.
    
    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    try:
        # Build mkvmerge command
        output_path = video_path.with_suffix('.temp.mkv')
        
        cmd = [
            str(mkvmerge_path),
            '-o', str(output_path),
            '--no-subtitles',  # Remove existing subtitles
            str(video_path)
        ]
        
        # Add subtitle track
        if language_code:
            cmd.extend(['--language', f'0:{language_code}'])
        
        if default_flag:
            cmd.extend(['--default-track', '0:yes'])
        else:
            cmd.extend(['--default-track', '0:no'])
        
        cmd.append(str(subtitle_path))
        
        # Execute mkvmerge
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        )
        
        if result.returncode == 0:
            # Replace original with new file
            backup_path = create_backup(video_path)
            video_path.unlink()
            output_path.rename(video_path)
            return True, None
        else:
            # Clean up temp file if it exists
            if output_path.exists():
                output_path.unlink()
            return False, result.stderr
            
    except Exception as e:
        return False, str(e)


def build_episode_context(video_files):
    """
    Build reference mappings for episode matching.
    
    Returns:
        Tuple of (video_episodes dict, temp_video_dict)
    """
    video_episodes = {}
    temp_video_dict = {}
    
    for video in sorted(video_files):
        episode_string = pattern_engine.get_episode_number_cached(video)
        if episode_string:
            season, episode = pattern_engine.extract_season_episode_numbers(episode_string)
            if season and episode:
                season_num, episode_num = int(season), int(episode)
                key = (season_num, episode_num)
                
                if key not in video_episodes:
                    video_episodes[key] = episode_string
                    temp_video_dict[episode_string] = video
                elif episode_string not in temp_video_dict:
                    temp_video_dict[episode_string] = video
    
    return video_episodes, temp_video_dict


def process_embedding(folder_path, config, mkvmerge_path):
    """Main embedding logic."""
    # Discover files
    video_exts = tuple(f'.{ext}' for ext in config['video_extensions'])
    subtitle_exts = tuple(f'.{ext}' for ext in config['subtitle_extensions'])
    
    all_video_files = [f for f in folder_path.iterdir() if f.suffix.lower().lstrip('.') in config['video_extensions']]
    all_subtitle_files = [f for f in folder_path.iterdir() if f.suffix.lower().lstrip('.') in config['subtitle_extensions']]
    
    # Filter MKV only
    mkv_videos = [v for v in all_video_files if v.suffix.lower() == '.mkv']
    
    if not mkv_videos:
        print("[INFO] No MKV video files found in directory")
        return []
    
    if not all_subtitle_files:
        print("[INFO] No subtitle files found in directory")
        return []
    
    print(f"\nFILES FOUND: {len(mkv_videos)} MKV videos | {len(all_subtitle_files)} subtitles")
    print("=" * 60 + "\n")
    
    # Build episode mappings
    video_episodes, temp_video_dict = build_episode_context([v.name for v in mkv_videos])
    
    # Process embeddings
    results = []
    embedded_count = 0
    failed_count = 0
    
    print("PROCESSING EMBEDDINGS:")
    print("-" * 40)
    
    for subtitle_file in sorted(all_subtitle_files):
        ep = pattern_engine.get_episode_number_cached(subtitle_file.name)
        
        # Standardize episode format
        adjusted_episode_string = ep
        if ep:
            season, episode = pattern_engine.extract_season_episode_numbers(ep)
            if season and episode:
                key = (int(season), int(episode))
                if key in video_episodes:
                    adjusted_episode_string = video_episodes[key]
        
        # Find matching video
        target_video_name = None
        if adjusted_episode_string and adjusted_episode_string in temp_video_dict:
            target_video_name = temp_video_dict[adjusted_episode_string]
        elif ep and ep in temp_video_dict:
            target_video_name = temp_video_dict[ep]
        
        if target_video_name:
            target_video_path = folder_path / target_video_name
            
            # Detect language
            language_code = detect_language_with_fallback(
                subtitle_file.name,
                config.get('embedding_language_code')
            )
            
            print(f"\nEMBEDDING: '{subtitle_file.name}' into '{target_video_name}'")
            if language_code:
                lang_name = LANGUAGE_DATA.get('codes', {}).get(language_code, {}).get('name', language_code)
                print(f"  Language: {lang_name} ({language_code})")
            else:
                print(f"  Language: (none detected)")
            
            # Embed subtitle
            success, error = embed_subtitle(
                target_video_path,
                subtitle_file,
                mkvmerge_path,
                language_code,
                config.get('default_flag', True)
            )
            
            if success:
                print(f"  ✓ SUCCESS")
                embedded_count += 1
                results.append({
                    'subtitle': subtitle_file.name,
                    'video': target_video_name,
                    'episode': adjusted_episode_string,
                    'language': language_code or 'N/A',
                    'status': 'success'
                })
            else:
                print(f"  ✗ FAILED: {error}")
                failed_count += 1
                results.append({
                    'subtitle': subtitle_file.name,
                    'video': target_video_name,
                    'episode': adjusted_episode_string,
                    'language': language_code or 'N/A',
                    'status': 'failed',
                    'error': error
                })
        else:
            print(f"\nNO MATCH: '{subtitle_file.name}' -> episode {ep or '(undetected)'}")
            results.append({
                'subtitle': subtitle_file.name,
                'video': None,
                'episode': ep or 'N/A',
                'language': 'N/A',
                'status': 'no_match'
            })
    
    print("\n" + "=" * 60)
    print(f"COMPLETED: {embedded_count} embedded | {failed_count} failed | {len(all_subtitle_files) - embedded_count - failed_count} unmatched")
    print("=" * 60)
    
    return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='SubFast Subtitle Embedding v3.1.0')
    parser.add_argument('directory', nargs='?', default='.', help='Target directory (default: current)')
    parser.add_argument('--test-mkvmerge', action='store_true', help='Test mkvmerge availability')
    parser.add_argument('--version', action='store_true', help='Show version')
    args = parser.parse_args()
    
    if args.version:
        print(f"SubFast Embedding Module v{__version__}")
        return 0
    
    print("\n" + "=" * 60)
    print("SubFast v3.1.0 - Subtitle Embedding")
    print("=" * 60 + "\n")
    
    # Load configuration
    config = config_loader.load_config()
    
    # Find mkvmerge
    mkvmerge_path = find_mkvmerge(config.get('mkvmerge_path', ''))
    
    if args.test_mkvmerge:
        if mkvmerge_path:
            print(f"✓ mkvmerge found: {mkvmerge_path}")
            return EXIT_SUCCESS
        else:
            print("✗ mkvmerge not found")
            print("  Install mkvmerge or specify path in config.ini")
            return EXIT_FATAL_ERROR
    
    if not mkvmerge_path:
        print("[ERROR] mkvmerge.exe not found!")
        print("  Please install MKVToolNix or specify mkvmerge_path in config.ini")
        return EXIT_FATAL_ERROR
    
    print(f"[INFO] Using mkvmerge: {mkvmerge_path}")
    
    # Get target directory
    folder_path = Path(args.directory).resolve()
    if not folder_path.is_dir():
        print(f"[ERROR] Directory not found: {folder_path}")
        return EXIT_FATAL_ERROR
    
    print(f"[INFO] Processing directory: {folder_path}\n")
    
    # Track execution time
    start_time = time.time()
    
    # Process embeddings
    results = process_embedding(folder_path, config, mkvmerge_path)
    
    # Calculate execution time
    elapsed_time = time.time() - start_time
    time_str = csv_reporter.format_execution_time(elapsed_time)
    
    # Display performance
    print("\nPERFORMANCE:")
    print("=" * 60)
    print(f"Total Execution Time: {time_str}")
    print(f"Operations: {len(results)} total")
    print("=" * 60)
    
    # Export CSV if enabled
    if config.get('embedding_report', False):
        csv_path = folder_path / 'embedding_report.csv'
        csv_reporter.generate_csv_report(results, csv_path, 'embedding')
        csv_reporter.print_summary(results, 'Embedding')
    
    # Determine exit code
    successful = sum(1 for r in results if r.get('status') == 'success')
    failed = sum(1 for r in results if r.get('status') == 'failed')
    
    if failed == 0:
        exit_code = EXIT_SUCCESS
    elif successful > 0:
        exit_code = EXIT_PARTIAL_FAILURE
    else:
        exit_code = EXIT_COMPLETE_FAILURE
    
    # Smart console behavior
    keep_console_open = config.get('keep_console_open', False)
    if keep_console_open or exit_code != EXIT_SUCCESS:
        input("\nPress Enter to close this window...")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
