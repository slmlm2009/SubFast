#!/usr/bin/env python3
"""
Subtitle Renamer Tool [AR] - CONFIGURABLE VERSION

Automatically renames subtitle files to match corresponding video files based on 
detected episode patterns. Adds customizable language tag before the file extension.

CONFIGURATION:
This version reads settings from config.ini in the script directory.
You can customize:
  - Language suffix (e.g., 'ar', 'en', 'fr', 'es') - default: 'ar'
  - Video file formats (e.g., mkv, mp4, avi, webm) - default: mkv, mp4
  - Subtitle formats (e.g., srt, ass, sub, vtt) - default: srt, ass
  - Enable/disable CSV report generation - default: enabled

If config.ini doesn't exist, it will be created automatically with default values.
Edit config.ini to customize behavior. See inline comments in config.ini for details.

Supports multiple episode naming patterns (S01E01, 2x05, Season.Episode, etc.) and
includes movie matching mode for single video/subtitle pairs.

Optimized version with pre-compiled regex patterns and single-pass file processing
for improved performance on large datasets.

ORIGINAL VERSION: rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking.py
"""

import os
import re
from collections import defaultdict
import configparser
from pathlib import Path
from datetime import datetime
import time


# ============================================================================
# CONFIGURATION SYSTEM
# ============================================================================

# Default configuration values (used if config.ini is missing or invalid)
DEFAULT_CONFIG = {
    'enable_export': False,  # Story 3.1: fallback is false, not true
    'language_suffix': 'ar',
    'video_extensions': ['mkv', 'mp4'],
    'subtitle_extensions': ['srt', 'ass']
}

def get_script_directory():
    """Get the script's directory where config.ini should be located"""
    return Path(__file__).parent

def create_default_config_file(config_path):
    """
    Create config.ini with default values and comprehensive inline documentation.
    
    Args:
        config_path: Path object where config file should be created
    """
    config_content = """# ============================================================================
# Subtitle Renamer Tool - Configuration File
# ============================================================================
# Edit values below to customize behavior.
# Invalid/missing values will use defaults.
# ============================================================================

[General]
# Generate CSV report before renaming (true/false) - default: true

enable_export = true

# Language suffix added before extension (two-character language suffix) - default: ar
# Examples: ar, en, fr, es

language_suffix = ar

[FileFormats]
# Video file extensions to process (comma-separated, no dots) - default: mkv, mp4
# Examples: mkv, mp4, avi, webm

video_extensions = mkv, mp4

# Subtitle file extensions to process (comma-separated, no dots) - default: srt, ass
# Examples: srt, ass, sub, ssa

subtitle_extensions = srt, ass

# ============================================================================
# IMPORTANT: Invalid or missing config values will use ALL default values:
#   - enable_export = false  # Story 3.1: changed from true to false
#   - language_suffix = ar
#   - video_extensions = mkv, mp4
#   - subtitle_extensions = srt, ass
# ============================================================================
"""
    
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f"Created default config.ini at: {config_path}")
    print("Edit this file to customize script behavior.")

def validate_configuration(config_dict):
    """
    Validate and normalize configuration values.
    
    Args:
        config_dict: Dictionary with configuration values
        
    Returns:
        Validated config dictionary, or None if validation fails critically
    """
    validated = {}
    
    # Validate enable_export (Story 3.1: fallback false)
    export_val = str(config_dict.get('enable_export', 'false')).lower()
    validated['enable_export'] = export_val in ('true', 'yes', '1', 'on')
    
    # Validate language_suffix
    suffix = config_dict.get('language_suffix', 'ar').strip()
    # Remove leading dot if present
    if suffix.startswith('.'):
        suffix = suffix[1:]
    
    # Check length and characters
    # Empty string is valid (omits suffix), or 1-10 valid characters
    if len(suffix) == 0:
        # Empty suffix is valid - will omit language tag from renamed files
        validated['language_suffix'] = ''
    elif 1 <= len(suffix) <= 10 and all(c.isalnum() or c in '-_' for c in suffix):
        validated['language_suffix'] = suffix
    else:
        print(f"[WARNING] Invalid language_suffix: '{suffix}' - omitting suffix from filenames")
        print("  Valid: empty string (omit suffix) or 1-10 characters (letters/numbers/hyphens/underscores)")
        validated['language_suffix'] = ''
    
    # Validate video_extensions
    video_exts = config_dict.get('video_extensions', 'mkv,mp4')
    video_list = [ext.strip().lstrip('.').lower() for ext in video_exts.split(',') if ext.strip()]
    if video_list:
        validated['video_extensions'] = video_list
    else:
        print("[WARNING] No valid video extensions - using defaults: mkv, mp4")
        validated['video_extensions'] = ['mkv', 'mp4']
    
    # Validate subtitle_extensions
    sub_exts = config_dict.get('subtitle_extensions', 'srt,ass')
    sub_list = [ext.strip().lstrip('.').lower() for ext in sub_exts.split(',') if ext.strip()]
    if sub_list:
        validated['subtitle_extensions'] = sub_list
    else:
        print("[WARNING] No valid subtitle extensions - using defaults: srt, ass")
        validated['subtitle_extensions'] = ['srt', 'ass']
    
    return validated

def load_configuration():
    """
    Load configuration from config.ini file.
    
    Returns:
        Dictionary with validated configuration values
        
    Behavior:
        - If config.ini exists: Load and validate settings
        - If config.ini missing: Create with defaults and return defaults
        - If parsing fails: Print warning and return defaults
    """
    script_dir = get_script_directory()
    config_path = script_dir / 'config.ini'
    
    # If config file doesn't exist, create it with defaults
    if not config_path.exists():
        print(f"[INFO] config.ini not found - creating default configuration")
        create_default_config_file(config_path)
        return DEFAULT_CONFIG.copy()
    
    # Try to parse config file
    config = configparser.ConfigParser()
    try:
        config.read(config_path, encoding='utf-8')
        
        # Extract values
        config_dict = {
            'enable_export': config.get('General', 'enable_export', fallback='false'),  # Story 3.1
            'language_suffix': config.get('General', 'language_suffix', fallback='ar'),
            'video_extensions': config.get('FileFormats', 'video_extensions', fallback='mkv, mp4'),
            'subtitle_extensions': config.get('FileFormats', 'subtitle_extensions', fallback='srt, ass')
        }
        
        # Validate and return
        validated = validate_configuration(config_dict)
        
        print(f"[INFO] Configuration loaded from: {config_path}")
        # Display language suffix (or "none" if empty)
        if validated['language_suffix']:
            print(f"  Language suffix: .{validated['language_suffix']}")
        else:
            print(f"  Language suffix: (none - omitted from filenames)")
        print(f"  Video formats: {', '.join(validated['video_extensions'])}")
        print(f"  Subtitle formats: {', '.join(validated['subtitle_extensions'])}")
        print(f"  CSV export: {'enabled' if validated['enable_export'] else 'disabled'}")
        
        return validated
        
    except Exception as e:
        print(f"[WARNING] Failed to parse config.ini: {e}")
        print("[INFO] Using default configuration")
        return DEFAULT_CONFIG.copy()

# Load configuration at module level
CONFIG = load_configuration()

# Pre-compiled regex patterns for episode detection
# Patterns are tried in order, with most common formats first for faster matching
# Each pattern extracts season and episode numbers, normalizing them to S##E## format
EPISODE_PATTERNS = [
    (re.compile(r'[Ss](\d+)[Ee](\d+)'), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'(?:^|[._\s-])(\d{1,2})[xX](\d+)(?=[._\s-]|$)'), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    # NEW: S## - ## format (e.g., S01 - 05, S2 - 10)
    (re.compile(r'[Ss](\d{1,2})\s*-\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    # NEW: S## - E## format (e.g., S01 - E05, S2 - E10)
    (re.compile(r'[Ss](\d{1,2})\s*-\s*[Ee](\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    # NEW: S## - EP## format (e.g., S01 - EP05, S2 - EP10)
    (re.compile(r'[Ss](\d{1,2})\s*-\s*[Ee][Pp](\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    # NEW: Ordinal Season patterns (placed HERE to match before generic patterns)
    # Pattern: 1st Season - 05 → S01E05
    (re.compile(r'(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s*-\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    # Pattern: 3rd Season Episode 8 → S03E08 (FIXES THE BUG!)
    (re.compile(r'(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s+[Ee]pisode\s+(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    # Pattern: 2nd Season E10 → S02E10
    (re.compile(r'(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s+[Ee]\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    # Pattern: 2nd Season EP10 → S02E10
    (re.compile(r'(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s+[Ee][Pp]\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    # NEW: Season ## - ## format (e.g., Season 2 - 23, Season 12 - 103)
    (re.compile(r'[Ss]eason\s+(\d{1,2})\s*-\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss]eason(\d{1,2})\s*-\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss]eason\.(\d+)[\s\._-]*[Ee]pisode\.(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss](\d+)[\s\._-]*[Ee]p(?:isode)?\.(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss](\d+)[Ee]p(?:isode)?(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss]eason\s+(\d+)\s+[Ee]pisode\s+(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss]eason(\d+)[Ee]pisode(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss]eason(\d+)\s+[Ee]pisode(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss]eason(\d+)\s+[Ee]p(?:isode)?(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss]eason(\d+)[Ee]p(?:isode)?(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'(?:^|[._\s-])[Ee](\d+)(?=[._\s-]|$)'), lambda m: ("01", m.group(1).zfill(2))),
    (re.compile(r'[Ss]eason\s+(\d+)[\s\._-]*[Ee]p(?:isode)?\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss]eason(\d+)[\s\._-]*[Ee]p(?:isode)?(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'(?:^|[._\s-])[Ee]p(?:isode)?\s*(\d+)(?=[._\s-]|$)', re.IGNORECASE), lambda m: ("01", m.group(1).zfill(2))),
    (re.compile(r'[Ss]eason\s+(\d+)\s+[Ee]p(?:isode)?\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'-\s*(\d+)'), lambda m: ("01", m.group(1).zfill(2))),
]

# Pre-compiled utility regex patterns for filename processing
PROBLEMATIC_CHARS = re.compile(r'[<>:"/\|?*]')  # Invalid characters for filenames
SUBTITLE_SUFFIX_PATTERN = re.compile(r'[._\-\s]*[Ss]ub(title)?[._\-\s]*', re.IGNORECASE)  # Remove "sub" markers
YEAR_PATTERN = re.compile(r'(?:19|20)\d{2}')  # Match 4-digit years (1900-2099)
BASE_NAME_CLEANUP = re.compile(r'[._\-]+')  # Replace separators with spaces

# Common video quality and format indicators to exclude when matching movie titles
# These words are filtered out to improve title similarity matching between video and subtitle files
COMMON_INDICATORS = {
    '1080p', '720p', '480p', '2160p', '4k', 'bluray', 'web', 'dvd', 'hd', 'x264', 'x265', 
    'h264', 'h265', 'avc', 'hevc', 'aac', 'ac3', 'dts', 'remux', 'proper', 'repack', 
    'extended', 'theatrical', 'unrated', 'directors', 'cut', 'multi', 'sub', 'eng', 'en', 
    'ara', 'ar', 'eng', 'fre', 'fr', 'ger', 'de', 'ita', 'es', 'spa', 'kor', 'jpn', 'ch',
    'chs', 'cht', 'internal', 'limited', 'unrated', 'xvid', 'divx', 'ntsc', 'pal', 'dc',
    'sync', 'syncopated', 'cc', 'sdh', 'hc', 'proper', 'real', 'final', 'post', 'pre', 
    'sync', 'dub', 'dubbed', 'sdh', 'cc'
}

# Performance optimization: Episode number cache
_episode_cache = {}

def get_episode_number(filename):
    """
    Extract episode information from filename and normalize to S##E## format.
    
    Args:
        filename: The filename to parse
        
    Returns:
        Normalized episode string (e.g., 'S01E05') or None if no pattern found
        
    Examples:
        'Show.S01E05.mkv' -> 'S01E05'
        'Show.2x10.mkv' -> 'S02E10'
        'Show - 15.mkv' -> 'S01E15' (assumes Season 1)
    """
    for pattern, formatter in EPISODE_PATTERNS:
        match = pattern.search(filename)
        if match:
            season, episode = formatter(match)
            return f"S{season}E{episode}"
    return None

def get_episode_number_cached(filename):
    """Cached wrapper - extracts episode once per filename."""
    if filename not in _episode_cache:
        _episode_cache[filename] = get_episode_number(filename)
    return _episode_cache[filename]

def extract_season_episode_numbers(episode_string):
    """
    Parse normalized episode string to extract season and episode numbers.
    
    Args:
        episode_string: Episode string in S##E## format (e.g., 'S01E05')
        
    Returns:
        Tuple of (season_number, episode_number) as strings, or ("", "") if invalid
    """
    if not episode_string:
        return "", ""
    
    match = re.match(r'S(\d+)E(\d+)', episode_string)
    if match:
        return match.group(1), match.group(2)
    return "", ""

def extract_base_name(filename):
    """
    Extract and clean the base filename for comparison.
    
    Removes file extension and converts separators (., _, -) to spaces for
    better word-based matching in movie mode.
    
    Args:
        filename: The filename to process
        
    Returns:
        Cleaned base name with spaces instead of separators
    """
    base_name = os.path.splitext(filename)[0]
    base_name = BASE_NAME_CLEANUP.sub(' ', base_name)
    return base_name.strip()

def find_movie_subtitle_match(video_files, subtitle_files):
    """
    Match a single movie file with a single subtitle file based on title similarity.
    
    Uses two matching strategies:
    1. Year matching: If both files contain the same 4-digit year, they're considered a match
    2. Word overlap: Compares common words after removing quality indicators (720p, x264, etc.)
    
    Args:
        video_files: List of video filenames (must contain exactly 1 file)
        subtitle_files: List of subtitle filenames (must contain exactly 1 file)
        
    Returns:
        Tuple of (video_file, subtitle_file) if match found, None otherwise
    """
    if len(video_files) != 1 or len(subtitle_files) != 1:
        return None
    
    video_name = extract_base_name(video_files[0])
    subtitle_name = extract_base_name(subtitle_files[0])
    
    # Extract release years if present in filenames
    video_year_match = YEAR_PATTERN.search(video_files[0])
    subtitle_year_match = YEAR_PATTERN.search(subtitle_files[0])
    
    video_year = video_year_match.group() if video_year_match else None
    subtitle_year = subtitle_year_match.group() if subtitle_year_match else None
    
    # Split into words and filter out quality/format indicators for cleaner comparison
    video_words = set(video_name.lower().split()) - COMMON_INDICATORS
    subtitle_words = set(subtitle_name.lower().split()) - COMMON_INDICATORS
    
    common_words = video_words.intersection(subtitle_words)
    years_match = (video_year and subtitle_year and video_year == subtitle_year)
    
    if years_match:
        if len(common_words) > 0 or (video_year and ('19' in video_year or '20' in video_year)):
            return (video_files[0], subtitle_files[0])
    else:
        if len(video_words) > 0 and len(subtitle_words) > 0:
            match_ratio = len(common_words) / min(len(video_words), len(subtitle_words))
            if match_ratio >= 0.3 or len(common_words) > 0:
                return (video_files[0], subtitle_files[0])
    
    return None

def generate_unique_name(base_name, subtitle_ext, subtitle, directory):
    """
    Generate a unique filename when multiple subtitles match the same video.
    
    First attempts the standard format: {video_base}.ar{ext}
    If that exists, creates a unique variant: {video_base}.ar_{original_sub_name}{ext}
    If that also exists, adds a numeric counter.
    
    Args:
        base_name: Base name of the video file (without extension)
        subtitle_ext: Extension of the subtitle file (e.g., '.srt')
        subtitle: Original subtitle filename
        directory: Target directory path
        
    Returns:
        Tuple of (new_filename, full_path)
    """
    # Build filename with optional language suffix
    if CONFIG['language_suffix']:
        # Build filename with optional language suffix
        if CONFIG['language_suffix']:
            new_name = f"{base_name}.{CONFIG['language_suffix']}{subtitle_ext}"
        else:
            new_name = f"{base_name}{subtitle_ext}"
    else:
        new_name = f"{base_name}{subtitle_ext}"
    new_path = os.path.join(directory, new_name)
    
    if not os.path.exists(new_path):
        return new_name, new_path
    
    # File already exists - create unique name incorporating original subtitle name
    original_base = os.path.splitext(subtitle)[0]
    original_cleaned = SUBTITLE_SUFFIX_PATTERN.sub('', original_base)
    if not original_cleaned:
        original_cleaned = original_base
    
    specific_new_name = f"{base_name}.ar_{original_cleaned}{subtitle_ext}"
    specific_new_name = PROBLEMATIC_CHARS.sub('_', specific_new_name)
    
    new_path = os.path.join(directory, specific_new_name)
    counter = 1
    original_specific_name = specific_new_name
    
    while os.path.exists(new_path):
        name_part, ext_part = os.path.splitext(original_specific_name)
        specific_new_name = f"{name_part}_{counter}{ext_part}"
        new_path = os.path.join(directory, specific_new_name)
        counter += 1
    
    return specific_new_name, new_path

def build_episode_context(video_files):
    """
    Build reference mappings for context-aware episode matching.
    
    Creates mappings to handle cases where the same episode uses different
    numbering formats (e.g., S02E015 vs S02E15). The first video file found
    (alphabetically) establishes the canonical pattern for that episode.
    
    Args:
        video_files: List of video filenames
        
    Returns:
        Tuple of (video_episodes dict, temp_video_dict)
        - video_episodes: Maps (season, episode) tuples to canonical episode strings
        - temp_video_dict: Maps episode strings to video filenames
    """
    video_episodes = {}
    temp_video_dict = {}
    
    # Process alphabetically to ensure deterministic pattern selection when multiple
    # videos have the same episode number with different formatting
    for video in sorted(video_files):
        episode_string = get_episode_number_cached(video)
        if episode_string:
            season, episode = extract_season_episode_numbers(episode_string)
            if season and episode:
                season_num, episode_num = int(season), int(episode)
                key = (season_num, episode_num)
                
                if key not in video_episodes:
                    video_episodes[key] = episode_string
                    temp_video_dict[episode_string] = video
                elif episode_string not in temp_video_dict:
                    temp_video_dict[episode_string] = video
    
    return video_episodes, temp_video_dict

def process_subtitles(subtitle_files, video_episodes, temp_video_dict, directory, rename_mapping=None):
    """
    Process and rename subtitle files to match their corresponding videos.
    
    For each subtitle:
    1. Detect episode pattern
    2. Apply context-aware standardization (adjust S02E015 to S02E15 if needed)
    3. Find matching video file
    4. Rename to {video_base}.ar{subtitle_ext}
    5. Handle collisions by creating unique names
    
    Args:
        subtitle_files: List of subtitle filenames to process
        video_episodes: Episode standardization map from build_episode_context()
        temp_video_dict: Video filename lookup map from build_episode_context()
        directory: Working directory path
        
    Returns:
        Number of successfully renamed files
    """
    renamed_count = 0
    if rename_mapping is None:
        rename_mapping = {}
    
    print("PROCESSING SUBTITLES:")
    print("-" * 40)
    
    for subtitle in sorted(subtitle_files):
        ep = get_episode_number_cached(subtitle)
        
        # Standardize episode format to match video files (handles padding differences)
        adjusted_episode_string = ep
        if ep:
            season, episode = extract_season_episode_numbers(ep)
            if season and episode:
                key = (int(season), int(episode))
                if key in video_episodes:
                    video_pattern = video_episodes[key]
                    if video_pattern != ep:
                        print(f"'{subtitle}' -> {ep} adjusted to {video_pattern} (context-aware)")
                    adjusted_episode_string = video_pattern

        # Find corresponding video file and perform rename
        target_video = None
        if adjusted_episode_string and adjusted_episode_string in temp_video_dict:
            target_video = temp_video_dict[adjusted_episode_string]
        elif ep and ep in temp_video_dict:
            target_video = temp_video_dict[ep]
            adjusted_episode_string = ep

        if target_video:
            base_name = os.path.splitext(target_video)[0]
            subtitle_ext = os.path.splitext(subtitle)[1]
            
            new_name, new_path = generate_unique_name(base_name, subtitle_ext, subtitle, directory)
            
            if "ar_" in new_name or "_" in os.path.basename(new_path):
                print(f"CONFLICT RESOLVED: Multiple subtitles match '{target_video}' -> renamed '{subtitle}' to unique name '{new_name}'")
            else:
                print(f"RENAMED: '{subtitle}' -> '{new_name}'")
            
            old_path = os.path.join(directory, subtitle)
            os.rename(old_path, new_path)
            renamed_count += 1
        elif ep:
            print(f"NO MATCH: '{subtitle}' -> episode {ep} has no matching video")
        else:
            print(f"NO EPISODE: '{subtitle}' -> could not detect episode number")
    
    return renamed_count

def analyze_results(files, video_files, subtitle_files, video_episodes, temp_video_dict):
    """
    Analyze matching results and categorize files for summary report.
    
    Categorizes files into:
    - found_matches: Episodes where both video and subtitle were successfully matched
    - not_found_episodes: Episodes with only video OR only subtitle
    - unidentified_files: Files where no episode pattern could be detected
    
    Args:
        files: All files in directory
        video_files: List of video filenames
        subtitle_files: List of subtitle filenames
        video_episodes: Episode standardization map
        temp_video_dict: Video filename lookup map
        
    Returns:
        Tuple of (found_matches set, not_found_episodes set, unidentified_files list)
    """
    found_matches = set()
    not_found_episodes = set()
    unidentified_files = []
    
    # Build map of which episodes have matching subtitles
    subtitle_episodes = {}
    for subtitle in subtitle_files:
        ep = get_episode_number_cached(subtitle)
        if ep:
            season, episode = extract_season_episode_numbers(ep)
            if season and episode:
                key = (int(season), int(episode))
                adjusted_ep = video_episodes.get(key, ep)
                if adjusted_ep in temp_video_dict or ep in temp_video_dict:
                    found_matches.add(adjusted_ep if adjusted_ep in temp_video_dict else ep)
                else:
                    not_found_episodes.add(adjusted_ep)
                subtitle_episodes[key] = True
        else:
            not_found_episodes.add("(None)")
    
    # Identify videos that don't have corresponding subtitle files
    for video in video_files:
        ep = get_episode_number_cached(video)
        if ep:
            season, episode = extract_season_episode_numbers(ep)
            if season and episode:
                key = (int(season), int(episode))
                if key not in subtitle_episodes:
                    not_found_episodes.add(video_episodes.get(key, ep))
    
    # Collect files where episode pattern detection failed
    for filename in files:
        # Check if file is a video or subtitle based on CONFIG
        video_exts = tuple(f'.{ext}' for ext in CONFIG['video_extensions'])
        subtitle_exts = tuple(f'.{ext}' for ext in CONFIG['subtitle_extensions'])
        if filename.lower().endswith(video_exts + subtitle_exts):
            if not get_episode_number_cached(filename):
                unidentified_files.append(filename)
    
    return found_matches, not_found_episodes, unidentified_files

def rename_subtitles_to_match_videos():
    directory = os.getcwd()
    files = os.listdir(directory)
    
    # Separate video and subtitle files by extension (from CONFIG)
    video_exts = tuple(f'.{ext}' for ext in CONFIG['video_extensions'])
    subtitle_exts = tuple(f'.{ext}' for ext in CONFIG['subtitle_extensions'])
    video_files = [f for f in files if f.lower().endswith(video_exts)]
    subtitle_files = [f for f in files if f.lower().endswith(subtitle_exts)]
    
    # Store original file lists for CSV export (before any renaming)
    original_video_files = video_files.copy()
    original_subtitle_files = subtitle_files.copy()
    rename_mapping = {}  # Maps original_name -> new_name (or None if not renamed)

    print(f"\nFILES FOUND: {len(video_files)} videos | {len(subtitle_files)} subtitles")
    print("=" * 60)
    
    if video_files:
        print(f"Videos: {video_files[:4]}{'...' if len(video_files) > 4 else ''}")
    if subtitle_files:
        print(f"Subtitles: {subtitle_files[:4]}{'...' if len(subtitle_files) > 4 else ''}")
    print()

    # Build episode reference mappings for context-aware matching
    video_episodes, temp_video_dict = build_episode_context(video_files)
    
    if video_episodes:
        print("PROCESSING VIDEOS:")
        print("-" * 40)
        print(f"EPISODE PATTERNS DETECTED FROM VIDEO FILES: {list(video_episodes.values())[:10]}{'...' if len(video_episodes) > 10 else ''}")
    print()

    # Rename subtitle files to match corresponding videos
    renamed_count = process_subtitles(subtitle_files, video_episodes, temp_video_dict, directory, rename_mapping)
    
    print("-" * 40)
    print()
    
    # Activate movie matching mode if no TV episodes were found
    remaining_video_files = [v for v in video_files if not get_episode_number_cached(v)]
    remaining_subtitle_files = [s for s in subtitle_files if not get_episode_number_cached(s)]
    movie_mode_detected = False
    
    if renamed_count == 0 and len(remaining_video_files) == 1 and len(remaining_subtitle_files) == 1:
        movie_match = find_movie_subtitle_match(remaining_video_files, remaining_subtitle_files)
        if movie_match:
            video_file, subtitle_file = movie_match
            base_name = os.path.splitext(video_file)[0]
            subtitle_ext = os.path.splitext(subtitle_file)[1]
            # Build filename with optional language suffix
            if CONFIG['language_suffix']:
                # Build filename with optional language suffix
                if CONFIG['language_suffix']:
                    new_name = f"{base_name}.{CONFIG['language_suffix']}{subtitle_ext}"
                else:
                    new_name = f"{base_name}{subtitle_ext}"
            else:
                new_name = f"{base_name}{subtitle_ext}"
            old_path = os.path.join(directory, subtitle_file)
            new_path = os.path.join(directory, new_name)
            print("MOVIE MODE: Found potential movie match!")
            print(f"RENAMED: '{subtitle_file}' -> '{new_name}'")
            os.rename(old_path, new_path)
            rename_mapping[subtitle_file] = new_name
            renamed_count += 1
            movie_mode_detected = True
        else:
            print("MOVIE MODE: No movie-subtitle match found.")
    elif len(remaining_video_files) > 1:
        print(f"MOVIE MODE: {len(remaining_video_files)} video files detected -> skipping movie matching logic.")
    
    print("=" * 60)
    total_candidate_files = len(subtitle_files)
    if renamed_count > 0:
        print(f"COMPLETED TASK: {renamed_count} subtitle file{'s' if renamed_count != 1 else ''} renamed out of {total_candidate_files}")
    else:
        print("INFO: No files were renamed.")
    print("=" * 60)
    
    # Display detailed analysis of matching results
    print("\nANALYSIS SUMMARY:")
    print("=" * 60)
    
    found_matches, not_found_episodes, unidentified_files = analyze_results(
        files, video_files, subtitle_files, video_episodes, temp_video_dict
    )
    
    if found_matches:
        print("FOUND AND RENAMED MATCHING SUBTITLE AND VIDEO FILES FOR THESE EPISODES:")
        for episode in sorted(found_matches):
            print(f"- {episode}")
        print()

    if not_found_episodes:
        print("COULDN'T FIND MATCHING SUBTITLE AND VIDEO FILES FOR THESE EPISODES:")
        for episode in sorted(not_found_episodes):
            if episode != "(None)":
                print(f"- {episode}")
        print()

    if unidentified_files:
        print("COULDN'T IDENTIFY SEASON#EPISODE# FOR THESE FILES:")
        for filename in sorted(unidentified_files):
            print(f"- {filename}")
        print()
    
    return renamed_count, movie_mode_detected, original_video_files, original_subtitle_files, rename_mapping

def export_analysis_to_csv(renamed_count=0, movie_mode=False, original_videos=None, original_subtitles=None, rename_map=None, execution_time=None):
    """
    Export detailed analysis to renaming_report.csv in improved format.
    
    Creates a comprehensive report with:
    - Summary header with timestamp, config, and statistics
    - Proper CSV table showing ORIGINAL filenames with detected episodes and actions
    - Match summary showing successful pairings
    - Missing matches and unidentified files
    
    Args:
        renamed_count: Number of subtitles successfully renamed
        movie_mode: Whether movie matching mode was activated
        original_videos: List of original video filenames (before renaming)
        original_subtitles: List of original subtitle filenames (before renaming)
        rename_map: Dictionary mapping original names to new names
    
    Output file: renaming_report.csv in the current directory
    """
    directory = os.getcwd()
    
    # Use provided original file lists, or fall back to current directory
    if original_videos is None or original_subtitles is None:
        files = os.listdir(directory)
        video_exts = tuple(f'.{ext}' for ext in CONFIG['video_extensions'])
        subtitle_exts = tuple(f'.{ext}' for ext in CONFIG['subtitle_extensions'])
        video_files = [f for f in files if f.lower().endswith(video_exts)]
        subtitle_files = [f for f in files if f.lower().endswith(subtitle_exts)]
    else:
        video_files = original_videos
        subtitle_files = original_subtitles
        # Build files list from original videos and subtitles
        files = original_videos + original_subtitles
    
    if rename_map is None:
        rename_map = {}
    
    # Build episode mappings for analysis
    video_episodes, temp_video_dict = build_episode_context(video_files)
    
    # Generate match/no-match analysis
    found_matches, not_found_episodes, unidentified_files = analyze_results(
        files, video_files, subtitle_files, video_episodes, temp_video_dict
    )
    
    # Build file data rows for the table
    file_rows = []
    
    # Process video files first
    for video in sorted(video_files):
        episode_string = get_episode_number_cached(video)
        if episode_string:
            # Standardize episode format
            season, episode = extract_season_episode_numbers(episode_string)
            if season and episode:
                key = (int(season), int(episode))
                if key in video_episodes:
                    episode_string = video_episodes[key]
            detected_episode = episode_string
        elif movie_mode:
            detected_episode = "Movie"
        else:
            detected_episode = "(UNIDENTIFIED)"
        
        file_rows.append({
            'filename': video,
            'detected_episode': detected_episode,
            'new_name': "No Change",
            'action': "--"
        })
    
    # Process subtitle files
    for subtitle in sorted(subtitle_files):
        episode_string = get_episode_number_cached(subtitle)
        
        # Standardize episode format to match video files
        if episode_string:
            season, episode = extract_season_episode_numbers(episode_string)
            if season and episode:
                key = (int(season), int(episode))
                if key in video_episodes:
                    episode_string = video_episodes[key]
            detected_episode = episode_string
            
            # Determine new name based on matching or rename_map
            if subtitle in rename_map and rename_map[subtitle]:
                new_name = rename_map[subtitle]
                action = "RENAMED"
            elif episode_string in temp_video_dict:
                video_file = temp_video_dict[episode_string]
                base_name = os.path.splitext(video_file)[0]
                subtitle_ext = os.path.splitext(subtitle)[1]
                # Build filename with optional language suffix
                if CONFIG['language_suffix']:
                    new_name = f"{base_name}.{CONFIG['language_suffix']}{subtitle_ext}"
                else:
                    new_name = f"{base_name}{subtitle_ext}"
                action = "RENAMED"
            else:
                new_name = "No Change"
                action = "NO MATCH"
        elif movie_mode:
            detected_episode = "Movie"
            # Check rename_map first, then calculate
            if subtitle in rename_map and rename_map[subtitle]:
                new_name = rename_map[subtitle]
                action = "RENAMED"
            elif len(video_files) == 1:
                video_file = video_files[0]
                base_name = os.path.splitext(video_file)[0]
                subtitle_ext = os.path.splitext(subtitle)[1]
                # Build filename with optional language suffix
                if CONFIG['language_suffix']:
                    new_name = f"{base_name}.{CONFIG['language_suffix']}{subtitle_ext}"
                else:
                    new_name = f"{base_name}{subtitle_ext}"
                action = "RENAMED"
            else:
                new_name = "No Change"
                action = "NO MATCH"
        else:
            detected_episode = "(UNIDENTIFIED)"
            new_name = "No Change"
            action = "--"
        
        file_rows.append({
            'filename': subtitle,
            'detected_episode': detected_episode,
            'new_name': new_name,
            'action': action
        })
    
    # Calculate statistics
    total_videos = len(video_files)
    total_subtitles = len(subtitle_files)
    unmatched_videos = len([ep for ep in not_found_episodes if ep in [video_episodes.get((int(s), int(e))) for s, e in [extract_season_episode_numbers(ep)] if s and e]])
    # Calculate unmatched subtitles properly:
    # Unmatched = subtitles with episodes that weren't renamed (excluding unidentified)
    unidentified_subtitle_count = len([s for s in subtitle_files if not get_episode_number_cached(s)])
    unmatched_subtitles = max(0, total_subtitles - renamed_count - unidentified_subtitle_count)
    
    # Calculate unidentified videos separately
    unidentified_video_count = len([v for v in video_files if not get_episode_number_cached(v)])
    
    # For movie mode, don't count files in unidentified if they were handled
    unidentified_count = len(unidentified_files)
    if movie_mode and unidentified_count > 0:
        # Remove movie files from unidentified count
        unidentified_count = len([f for f in unidentified_files if f not in video_files and f not in subtitle_files])
    
    # Write the CSV report
    csv_filename = "renaming_report.csv"
    csv_path = os.path.join(directory, csv_filename)
    
    # Get configuration display string
    lang_str = CONFIG['language_suffix'] if CONFIG['language_suffix'] else '(none)'
    config_str = f"language={lang_str}, videos={'|'.join(CONFIG['video_extensions'])}, subtitles={'|'.join(CONFIG['subtitle_extensions'])}, export={CONFIG['enable_export']}"
    
    with open(csv_path, 'w', encoding='utf-8', newline='') as csvfile:
        # SECTION 1: Summary Header
        csvfile.write("# Subtitle Renaming Report\n")
        csvfile.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        csvfile.write(f"# Directory: {directory}\n")
        csvfile.write(f"# Configuration: {config_str}\n")
        csvfile.write("#\n")
        csvfile.write("# SUMMARY:\n")
        csvfile.write(f"# Total Videos: {total_videos}\n")
        csvfile.write(f"# Total Subtitles: {total_subtitles}\n")
        csvfile.write(f"# Renamed: {renamed_count}/{total_subtitles} subtitles\n")
        csvfile.write(f"# Videos Missing Subtitles: {unmatched_videos}\n")
        csvfile.write(f"# Subtitles Missing Videos: {unmatched_subtitles}\n")
        csvfile.write(f"# Videos Without Episode Pattern: {unidentified_video_count}\n")
        csvfile.write(f"# Subtitles Without Episode Pattern: {unidentified_subtitle_count}\n")
        csvfile.write(f"# Movie Mode: {'Yes' if movie_mode else 'No'}\n")
        csvfile.write(f"# Execution Time: {execution_time if execution_time else 'N/A'}\n")
        csvfile.write("#\n")
        
        # SECTION 2: File Analysis Table
        csvfile.write("Original Filename,Detected Episode,New Name,Action\n")
        for row in file_rows:
            csvfile.write(f"{row['filename']},{row['detected_episode']},{row['new_name']},{row['action']}\n")
        
        csvfile.write("#\n")
        
        # SECTION 3: Match Summary
        if movie_mode:
            csvfile.write("# MOVIE MODE DETECTED:\n")
            if len(video_files) == 1 and len(subtitle_files) == 1:
                video_file = video_files[0]
                subtitle_file = subtitle_files[0]
                base_name = os.path.splitext(video_file)[0]
                subtitle_ext = os.path.splitext(subtitle_file)[1]
                # Build filename with optional language suffix
                if CONFIG['language_suffix']:
                    new_name = f"{base_name}.{CONFIG['language_suffix']}{subtitle_ext}"
                else:
                    new_name = f"{base_name}{subtitle_ext}"
                csvfile.write("# Successfully matched single video + subtitle pair\n")
                csvfile.write(f"# Video: {video_file}\n")
                csvfile.write(f"# Subtitle: {subtitle_file} -> {new_name}\n")
            csvfile.write("#\n")
        
        if found_matches:
            csvfile.write("# MATCHED EPISODES:\n")
            for episode in sorted(found_matches):
                if episode in temp_video_dict:
                    video_file = temp_video_dict[episode]
                    # Find the subtitle that was matched
                    base_name = os.path.splitext(video_file)[0]
                    # Look for renamed subtitle
                    matched_subtitle = None
                    for sub in subtitle_files:
                        sub_ep = get_episode_number_cached(sub)
                        if sub_ep:
                            season, ep = extract_season_episode_numbers(sub_ep)
                            if season and ep:
                                key = (int(season), int(ep))
                                if key in video_episodes and video_episodes[key] == episode:
                                    matched_subtitle = sub
                                    break
                    
                    if matched_subtitle:
                        subtitle_ext = os.path.splitext(matched_subtitle)[1]
                        # Build filename with optional language suffix
                        if CONFIG['language_suffix']:
                            new_name = f"{base_name}.{CONFIG['language_suffix']}{subtitle_ext}"
                        else:
                            new_name = f"{base_name}{subtitle_ext}"
                        csvfile.write(f"# {episode} -> Video: {video_file} | Subtitle: {matched_subtitle} -> {new_name}\n")
            csvfile.write("#\n")
        
        if not_found_episodes:
            # Build subtitle lookup dict for missing matches section
            temp_subtitle_dict = {}
            for subtitle in subtitle_files:
                ep = get_episode_number_cached(subtitle)
                if ep:
                    season, episode = extract_season_episode_numbers(ep)
                    if season and episode:
                        key = (int(season), int(episode))
                        adjusted_ep = video_episodes.get(key, ep)
                        if adjusted_ep not in temp_subtitle_dict:
                            temp_subtitle_dict[adjusted_ep] = subtitle
                        if ep not in temp_subtitle_dict:
                            temp_subtitle_dict[ep] = subtitle
            
            csvfile.write("# MISSING MATCHES:\n")
            for episode in sorted(not_found_episodes):
                if episode != "(None)":
                    # Determine what's missing
                    if episode in temp_video_dict:
                        csvfile.write(f"# {episode} -> Has Video: {temp_video_dict[episode]} | Missing: Subtitle\n")
                    else:
                        csvfile.write(f"# {episode} -> Has Subtitle: {temp_subtitle_dict.get(episode, '(unknown)')} | Missing: Video\n")
            csvfile.write("#\n")
        
        if unidentified_files:
            csvfile.write("# FILES WITHOUT EPISODE PATTERN:\n")
            if movie_mode:
                csvfile.write("# (none - movie mode handled files)\n")
            else:
                for filename in sorted(unidentified_files):
                    csvfile.write(f"# {filename} (no episode pattern detected)\n")
            csvfile.write("#\n")
    
    print(f"\nExported file renaming records to:")
    print(f"{csv_path}\n")

if __name__ == "__main__":
    """
    Main execution block.
    CSV export is now performed AFTER renaming to accurately report results.
    Export is controlled by config.ini (enable_export setting).
    """
    # Track execution time
    start_time = time.time()
    
    renamed_count, movie_mode_detected, original_videos, original_subtitles, rename_map = rename_subtitles_to_match_videos()
    
    # Calculate execution time
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Format time (human-readable)
    if elapsed_time < 60:
        time_str = f"{elapsed_time:.2f} seconds"
    elif elapsed_time < 3600:
        minutes = int(elapsed_time // 60)
        seconds = elapsed_time % 60
        time_str = f"{minutes}m {seconds:.2f}s"
    else:
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = elapsed_time % 60
        time_str = f"{hours}h {minutes}m {seconds:.0f}s"
    
    # Display performance summary
    print("PERFORMANCE:")
    print("=" * 60)
    print(f"Total Execution Time: {time_str}")
    print(f"Files Processed: {len(original_videos) + len(original_subtitles)}")
    print(f"Subtitles Renamed: {renamed_count}/{len(original_subtitles)}")
    print("=" * 60)
    
    if CONFIG['enable_export']:
        export_analysis_to_csv(renamed_count, movie_mode_detected, original_videos, original_subtitles, rename_map, time_str)
