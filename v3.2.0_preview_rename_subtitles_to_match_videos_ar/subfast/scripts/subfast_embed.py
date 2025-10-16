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

# Timeout constants for mkvmerge operations
TIMEOUT_BASE = 300  # 5 minutes minimum
TIMEOUT_PER_GB = 120  # 2 minutes per GB
TIMEOUT_MAX = 1800  # 30 minutes maximum cap

# Movie mode matching patterns and helpers
import re
YEAR_PATTERN = re.compile(r'(?:19|20)\d{2}')
BASE_NAME_CLEANUP = re.compile(r'[._\-]+')

COMMON_INDICATORS = {
    '1080p', '720p', '480p', '2160p', '4k', 'bluray', 'web', 'dvd', 'hd', 'x264', 'x265',
    'h264', 'h265', 'avc', 'hevc', 'aac', 'ac3', 'dts', 'remux', 'proper', 'repack',
    'extended', 'theatrical', 'unrated', 'directors', 'cut', 'multi', 'sub', 'eng', 'en',
    'ara', 'ar', 'eng', 'fre', 'fr', 'ger', 'de', 'ita', 'es', 'spa', 'kor', 'jpn', 'ch',
    'chs', 'cht', 'internal', 'limited', 'xvid', 'divx', 'ntsc', 'pal', 'dc',
    'sync', 'syncopated', 'cc', 'sdh', 'hc', 'final', 'post', 'pre',
    'dub', 'dubbed'
}

# Linguistic filler words (stop words) to exclude from movie title matching
# These words appear frequently in titles but have little semantic value for distinguishing movies
# Filtering these prevents false matches like "Movie of Year" matching "Subtitle of 2025"
# Similar to COMMON_INDICATORS which filters technical terms, this filters linguistic noise
FILLER_WORDS = {
    # Articles
    'a', 'an', 'the',
    # Prepositions
    'of', 'in', 'on', 'at', 'to', 'for', 'with', 'from', 'by',
    'about', 'as', 'into', 'through', 'during', 'before', 'after',
    'above', 'below', 'between', 'among', 'under', 'over',
    # Conjunctions
    'and', 'or', 'but', 'nor', 'yet', 'so',
    # Common pronouns
    'it', 'its', 'this', 'that', 'these', 'those',
    # Common verbs
    'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did',
    # Other common words
    'not', 'all', 'no', 'some', 'more', 'most', 'very',
    'can', 'will', 'just', 'should', 'than', 'also', 'only',
    # Numbers as words
    'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'
}


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
    2. Script directory bin/ subdirectory
    3. System PATH
    """
    config_mkvmerge = config_path.strip() if config_path else ""
    
    # Check config path first
    if config_mkvmerge and Path(config_mkvmerge).is_file():
        return Path(config_mkvmerge)
    
    # Check bin/ subdirectory (v3.0.0 compatible location)
    script_dir = Path(__file__).parent.parent
    local_mkvmerge = script_dir / 'bin' / 'mkvmerge.exe'
    if local_mkvmerge.is_file():
        return local_mkvmerge
    
    # Check system PATH
    if shutil.which('mkvmerge'):
        return Path(shutil.which('mkvmerge'))
    
    return None


def ensure_backups_directory(working_dir):
    """
    Create backups/ directory if it doesn't exist (v3.0.0 workflow).
    
    Args:
        working_dir (Path): Working directory where backups/ should be created
    
    Returns:
        Path: Path to the backups directory
    """
    backups_dir = working_dir / 'backups'
    if not backups_dir.exists():
        backups_dir.mkdir(exist_ok=True)
        print("[INFO] Creating backups/ directory...")
    return backups_dir


def backup_originals(video_file, subtitle_file, backups_dir):
    """
    Intelligently backup original files to backups directory (v3.0.0 workflow).
    
    Checks each file independently - only moves files that don't already
    exist in the backups directory.
    
    Args:
        video_file (Path): Path to original video file
        subtitle_file (Path): Path to original subtitle file
        backups_dir (Path): Path to backups directory
    
    Returns:
        tuple[bool, bool]: (video_backed_up, subtitle_backed_up)
    """
    video_backup = backups_dir / video_file.name
    subtitle_backup = backups_dir / subtitle_file.name
    
    video_backed_up = False
    subtitle_backed_up = False
    
    # Check and backup video if needed
    if video_backup.exists():
        print(f"[INFO] Video backup already exists: {video_file.name}")
    else:
        shutil.move(str(video_file), str(video_backup))
        video_backed_up = True
        print(f"[BACKUP] Moved {video_file.name} -> backups/")
    
    # Check and backup subtitle if needed
    if subtitle_backup.exists():
        print(f"[INFO] Subtitle backup already exists: {subtitle_file.name}")
    else:
        shutil.move(str(subtitle_file), str(subtitle_backup))
        subtitle_backed_up = True
        print(f"[BACKUP] Moved {subtitle_file.name} -> backups/")
    
    return video_backed_up, subtitle_backed_up


def safe_delete_subtitle(subtitle_file, backups_dir):
    """
    Delete subtitle from working directory ONLY if it exists in backups (v3.0.0 workflow).
    
    Safety check prevents data loss if backup failed silently.
    
    Args:
        subtitle_file (Path): Path to subtitle file in working directory
        backups_dir (Path): Path to backups directory
    """
    subtitle_backup = backups_dir / subtitle_file.name
    
    if subtitle_backup.exists() and subtitle_file.exists():
        subtitle_file.unlink()
        print(f"[CLEANUP] Removed subtitle from working dir: {subtitle_file.name}")
    elif not subtitle_backup.exists():
        print(f"[WARNING] Subtitle not in backups/ - keeping in working dir: {subtitle_file.name}")


def rename_embedded_to_final(embedded_file, final_name):
    """
    Rename .embedded.mkv to final .mkv filename (v3.0.0 workflow).
    
    Args:
        embedded_file (Path): Path to temporary .embedded.mkv file
        final_name (Path): Path to final .mkv filename
    """
    embedded_file.replace(final_name)


def cleanup_failed_merge(embedded_file):
    """
    Delete temporary .embedded.mkv file after merge failure (v3.0.0 workflow).
    Original files remain untouched.
    
    Args:
        embedded_file (Path): Path to temporary .embedded.mkv file
    """
    if embedded_file.exists():
        embedded_file.unlink()
        print(f"[CLEANUP] Removed temporary file: {embedded_file.name}")


def embed_subtitle(video_path, subtitle_path, mkvmerge_path, language_code, default_flag, backups_dir=None, config=None):
    """
    Embed subtitle into MKV video file using v3.0.0 workflow.
    
    Workflow:
    1. Create temporary .embedded.mkv file
    2. On success: 
       - Create backups/ directory if needed
       - Move original video + subtitle to backups/
       - Rename .embedded.mkv to original video name
    3. On failure: cleanup temp file, originals untouched
    
    Dynamic Timeout:
    - Base: 300s (5 minutes)
    - Scales: +120s per GB of combined file size
    - Maximum: 1800s (30 minutes)
    
    Args:
        video_path: Path to video file
        subtitle_path: Path to subtitle file
        mkvmerge_path: Path to mkvmerge executable
        language_code: Language code for subtitle
        default_flag: Whether to set as default track
        backups_dir: Optional existing backups directory (created if None)
        config: Configuration dictionary (unused, kept for compatibility)
    
    Returns:
        tuple: (success: bool, error_message: str or None, backups_dir: Path or None)
    """
    try:
        # Generate temporary embedded filename (v3.0.0 pattern)
        embedded_file = video_path.parent / f"{video_path.stem}.embedded.mkv"
        final_file = video_path  # Final name is the original video name
        
        # Build mkvmerge command
        cmd = [
            str(mkvmerge_path),
            '-o', str(embedded_file),
            str(video_path)
        ]
        
        # Add subtitle track with language if specified
        if language_code:
            cmd.extend(['--language', f'0:{language_code}'])
        
        if default_flag:
            cmd.extend(['--default-track', '0:yes'])
        else:
            cmd.extend(['--default-track', '0:no'])
        
        cmd.append(str(subtitle_path))
        
        # Calculate dynamic timeout (v3.0.0 system)
        try:
            total_bytes = video_path.stat().st_size + subtitle_path.stat().st_size
        except Exception:
            total_bytes = 0
        
        # Dynamic timeout: base 300s + 120s per GB, capped at 1800s (30 min)
        gb = total_bytes / (1024 ** 3)
        dyn_timeout = TIMEOUT_BASE + int(max(0, gb) * TIMEOUT_PER_GB)
        timeout_seconds = max(TIMEOUT_BASE, min(TIMEOUT_MAX, dyn_timeout))
        
        # Execute mkvmerge with dynamic timeout
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
            timeout=timeout_seconds
        )
        
        if result.returncode == 0:
            # Merge succeeded - v3.0.0 backup workflow
            try:
                # Create backups directory on first success
                if backups_dir is None:
                    backups_dir = ensure_backups_directory(video_path.parent)
                
                # Intelligently backup originals (checks each file independently)
                video_backed_up, subtitle_backed_up = backup_originals(video_path, subtitle_path, backups_dir)
                
                # Only delete subtitle if it's safely in backups/
                safe_delete_subtitle(subtitle_path, backups_dir)
                
                # Rename embedded file to original name
                rename_embedded_to_final(embedded_file, final_file)
                
                print(f"[SUCCESS] Created: {final_file.name}")
                return True, None, backups_dir
                
            except Exception as e:
                # Ensure temp file cleanup on any error
                cleanup_failed_merge(embedded_file)
                error_msg = f"Backup workflow failed: {str(e)}"
                print(f"[ERROR] {error_msg}")
                return False, error_msg, backups_dir
        else:
            # Merge failed - cleanup temp file
            cleanup_failed_merge(embedded_file)
            error_msg = result.stderr if result.stderr else 'Unknown mkvmerge error'
            return False, error_msg, backups_dir
            
    except subprocess.TimeoutExpired:
        if 'embedded_file' in locals():
            cleanup_failed_merge(Path(locals()['embedded_file']))
        return False, "mkvmerge timeout (file too large or system too slow)", backups_dir
    except Exception as e:
        if 'embedded_file' in locals():
            cleanup_failed_merge(Path(locals()['embedded_file']))
        return False, str(e), backups_dir


def extract_base_name(filename):
    """
    Extract and clean base filename for movie comparison.
    Converts separators (., _, -) to spaces.
    
    Args:
        filename: The filename to process
        
    Returns:
        Cleaned base name with spaces
    """
    base_name = Path(filename).stem
    base_name = BASE_NAME_CLEANUP.sub(' ', base_name)
    return base_name.strip()


def match_movie_files(video_files, subtitle_files):
    """
    Match single movie file with single subtitle file based on title similarity.
    
    Uses two matching strategies:
    1. Year matching: If both files contain the same 4-digit year
    2. Word overlap: Compares common words after removing quality indicators
    
    Args:
        video_files: List of video Path objects
        subtitle_files: List of subtitle Path objects
        
    Returns:
        Tuple of (video_file, subtitle_file) if match found, None otherwise
    """
    if len(video_files) != 1 or len(subtitle_files) != 1:
        return None
    
    video_name = extract_base_name(video_files[0].name)
    subtitle_name = extract_base_name(subtitle_files[0].name)
    
    video_year_match = YEAR_PATTERN.search(video_files[0].name)
    subtitle_year_match = YEAR_PATTERN.search(subtitle_files[0].name)
    
    video_year = video_year_match.group() if video_year_match else None
    subtitle_year = subtitle_year_match.group() if subtitle_year_match else None
    
    # Filter out both technical indicators AND linguistic filler words
    video_words = set(video_name.lower().split()) - COMMON_INDICATORS - FILLER_WORDS
    subtitle_words = set(subtitle_name.lower().split()) - COMMON_INDICATORS - FILLER_WORDS
    
    common_words = video_words.intersection(subtitle_words)
    years_match = (video_year and subtitle_year and video_year == subtitle_year)
    
    if years_match:
        if len(common_words) > 0:
            return (video_files[0], subtitle_files[0])
    else:
        if len(video_words) > 0 and len(subtitle_words) > 0:
            match_ratio = len(common_words) / min(len(video_words), len(subtitle_words))
            if match_ratio >= 0.3 or len(common_words) > 0:
                return (video_files[0], subtitle_files[0])
    
    return None


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
    
    # Process embeddings with v3.0.0 workflow
    results = []
    embedded_count = 0
    failed_count = 0
    backups_dir = None  # Track backups directory across iterations
    
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
            
            # Embed subtitle with v3.0.0 workflow (tracks backups_dir + dynamic timeout)
            success, error, backups_dir = embed_subtitle(
                target_video_path,
                subtitle_file,
                mkvmerge_path,
                language_code,
                config.get('default_flag', True),
                backups_dir,  # Pass existing backups_dir
                config  # Pass config for dynamic timeout calculation
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
    
    # Movie mode fallback - try if no embeddings succeeded
    if embedded_count == 0 and len(mkv_videos) == 1 and len(all_subtitle_files) == 1:
        print("\n" + "=" * 60)
        print("MOVIE MODE: Attempting title-based matching...")
        print("=" * 60)
        
        movie_match = match_movie_files(mkv_videos, all_subtitle_files)
        
        if movie_match:
            video_file, subtitle_file = movie_match
            
            print(f"\n[MOVIE MODE] Matched: '{video_file.name}' + '{subtitle_file.name}'")
            
            # Detect language
            language_code = detect_language_with_fallback(
                subtitle_file.name,
                config.get('embedding_language_code')
            )
            
            print(f"\nEMBEDDING: '{subtitle_file.name}' into '{video_file.name}'")
            if language_code:
                lang_name = LANGUAGE_DATA.get('codes', {}).get(language_code, {}).get('name', language_code)
                print(f"  Language: {lang_name} ({language_code})")
            else:
                print(f"  Language: (none detected)")
            
            # Embed subtitle
            success, error, backups_dir = embed_subtitle(
                video_file,
                subtitle_file,
                mkvmerge_path,
                language_code,
                config.get('default_flag', True),
                backups_dir,
                config
            )
            
            if success:
                print(f"  ✓ SUCCESS")
                embedded_count += 1
                
                # Update results - replace the 'no_match' entry with success
                results = [r for r in results if r.get('subtitle') != subtitle_file.name]
                results.append({
                    'subtitle': subtitle_file.name,
                    'video': video_file.name,
                    'episode': 'Movie',
                    'language': language_code or 'N/A',
                    'status': 'success'
                })
            else:
                print(f"  ✗ FAILED: {error}")
                failed_count += 1
                
                # Update results - replace the 'no_match' entry with failed
                results = [r for r in results if r.get('subtitle') != subtitle_file.name]
                results.append({
                    'subtitle': subtitle_file.name,
                    'video': video_file.name,
                    'episode': 'Movie',
                    'language': language_code or 'N/A',
                    'status': 'failed',
                    'error': error
                })
        else:
            print("\n[MOVIE MODE] No match found - files are too dissimilar")
    
    print("\n" + "=" * 60)
    print(f"COMPLETED: {embedded_count} embedded | {failed_count} failed | {len(all_subtitle_files) - embedded_count - failed_count} unmatched")
    print("=" * 60)
    
    # Return results plus additional context for comprehensive reporting
    return {
        'results': results,
        'all_videos': [v.name for v in mkv_videos],
        'all_subtitles': [s.name for s in all_subtitle_files]
    }


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
            print(f"[OK] mkvmerge found: {mkvmerge_path}")
            exit_code = EXIT_SUCCESS
        else:
            print("[ERROR] mkvmerge not found")
            print("  Install mkvmerge or specify path in config.ini")
            exit_code = EXIT_FATAL_ERROR
        
        # Console handling for test mode
        keep_console_open = config.get('keep_console_open', False)
        if keep_console_open or exit_code != EXIT_SUCCESS:
            input("\nPress Enter to close this window...")
        return exit_code
    
    if not mkvmerge_path:
        script_dir = Path(__file__).parent.parent
        print("[ERROR] mkvmerge.exe not found!")
        print(f"  Checked: {script_dir / 'bin' / 'mkvmerge.exe'}")
        print("  Checked: System PATH")
        print("\nPlease ensure:")
        print("  1. MKVToolNix is installed, OR")
        print("  2. Place mkvmerge.exe in bin/ directory, OR")
        print("  3. Set mkvmerge_path in config.ini [Embedding] section")
        
        # Console handling - ALWAYS execute
        keep_console_open = config.get('keep_console_open', False)
        if keep_console_open or True:  # Always stay open on fatal errors
            input("\nPress Enter to close this window...")
        return EXIT_FATAL_ERROR
    
    print(f"[INFO] Using mkvmerge: {mkvmerge_path}")
    
    # Get target directory
    folder_path = Path(args.directory).resolve()
    if not folder_path.is_dir():
        print(f"[ERROR] Directory not found: {folder_path}")
        
        # Console handling - ALWAYS execute
        keep_console_open = config.get('keep_console_open', False)
        if keep_console_open or True:  # Always stay open on fatal errors
            input("\nPress Enter to close this window...")
        return EXIT_FATAL_ERROR
    
    print(f"[INFO] Processing directory: {folder_path}\n")
    
    # Track execution time
    start_time = time.time()
    
    # Process embeddings
    process_data = process_embedding(folder_path, config, mkvmerge_path)
    results = process_data['results']
    all_videos = process_data['all_videos']
    all_subtitles = process_data['all_subtitles']
    
    # Calculate execution time
    elapsed_time = time.time() - start_time
    time_str = csv_reporter.format_execution_time(elapsed_time)
    
    # Export CSV if enabled
    if config.get('embedding_report', False):
        csv_path = folder_path / 'embedding_report.csv'
        csv_reporter.generate_csv_report(
            results=results,
            output_path=csv_path,
            operation_type='embedding',
            config=config,
            execution_time_str=time_str,
            all_videos=all_videos,
            all_subtitles=all_subtitles,
            elapsed_seconds=elapsed_time
        )
    
    # Always display summary with accurate timing
    csv_reporter.print_summary(
        results, 
        'Embedding',
        execution_time=time_str,
        total_files=len(results),
        elapsed_seconds=elapsed_time
    )
    
    # Determine exit code
    successful = sum(1 for r in results if r.get('status') == 'success')
    failed = sum(1 for r in results if r.get('status') == 'failed')
    
    if failed == 0:
        exit_code = EXIT_SUCCESS
    elif successful > 0:
        exit_code = EXIT_PARTIAL_FAILURE
    else:
        exit_code = EXIT_COMPLETE_FAILURE
    
    # v3.0.0: Final tip about backups
    backups_dir = folder_path / 'backups'
    if successful > 0 and backups_dir.exists():
        print()
        print("Tip: Verify merged files before manually deleting backups directory")
        print(f"     Backups location: {backups_dir}")
    
    # Smart console behavior
    keep_console_open = config.get('keep_console_open', False)
    if keep_console_open or exit_code != EXIT_SUCCESS:
        input("\nPress Enter to close this window...")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
