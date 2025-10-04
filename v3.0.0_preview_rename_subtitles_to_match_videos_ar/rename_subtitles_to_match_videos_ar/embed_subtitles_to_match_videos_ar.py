#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Subtitle Embedding Tool [AR] - Embed Subtitles into MKV Files

Automatically embeds subtitle files into corresponding MKV video files using mkvmerge.
Leverages intelligent pattern matching from the rename_subtitles_to_match_videos_ar.py
script to find matching pairs of videos and subtitles.

Features:
- Automatic video-subtitle file matching based on episode patterns
- Configurable mkvmerge.exe path
- Backup of original files (.original.mkv suffix)
- Batch processing of multiple files
- Language tag detection from subtitle filenames
- Windows context menu integration

Configuration:
Settings are read from config.ini in the script directory.
Key settings:
  - mkvmerge_path: Path to mkvmerge.exe (optional, defaults to script directory)
  - Default subtitle track properties (language, default flag)

Usage:
    python embed_subtitles_to_match_videos_ar.py [directory]
    python embed_subtitles_to_match_videos_ar.py --test-mkvmerge
    python embed_subtitles_to_match_videos_ar.py --version
"""

import os
import sys
import re
import argparse
import configparser
import subprocess
import shutil
import time
from pathlib import Path

__version__ = "1.0.0"

# Exit codes
EXIT_SUCCESS = 0           # All operations completed successfully
EXIT_FATAL_ERROR = 1       # Fatal error: mkvmerge not found, config invalid, etc.
EXIT_PARTIAL_FAILURE = 2   # Some operations failed, some succeeded
EXIT_COMPLETE_FAILURE = 3  # All operations attempted failed

# Valid ISO-639 language codes (Set 1 and Set 3)
# Loaded from ISO-639_set1_and_set3.txt resource file
VALID_LANGUAGE_CODES = {
    'ab', 'abk', 'aa', 'aar', 'af', 'afr', 'ak', 'aka', 'sq', 'sqi',
    'am', 'amh', 'ar', 'ara', 'an', 'arg', 'hy', 'hye', 'as', 'asm',
    'av', 'ava', 'ae', 'ave', 'ay', 'aym', 'az', 'aze', 'bm', 'bam',
    'ba', 'bak', 'eu', 'eus', 'be', 'bel', 'bn', 'ben', 'bi', 'bis',
    'bs', 'bos', 'br', 'bre', 'bg', 'bul', 'my', 'mya', 'ca', 'cat',
    'km', 'khm', 'ch', 'cha', 'ce', 'che', 'ny', 'nya', 'zh', 'zho',
    'cu', 'chu', 'cv', 'chv', 'kw', 'cor', 'co', 'cos', 'cr', 'cre',
    'hr', 'hrv', 'cs', 'ces', 'da', 'dan', 'dv', 'div', 'nl', 'nld',
    'dz', 'dzo', 'en', 'eng', 'eo', 'epo', 'et', 'est', 'ee', 'ewe',
    'fo', 'fao', 'fj', 'fij', 'fi', 'fin', 'fr', 'fra', 'ff', 'ful',
    'gd', 'gla', 'gl', 'glg', 'lg', 'lug', 'ka', 'kat', 'de', 'deu',
    'el', 'ell', 'gn', 'grn', 'gu', 'guj', 'ht', 'hat', 'ha', 'hau',
    'he', 'heb', 'hz', 'her', 'hi', 'hin', 'ho', 'hmo', 'hu', 'hun',
    'is', 'isl', 'io', 'ido', 'ig', 'ibo', 'id', 'ind', 'ia', 'ina',
    'ie', 'ile', 'iu', 'iku', 'ik', 'ipk', 'ga', 'gle', 'it', 'ita',
    'ja', 'jpn', 'jv', 'jav', 'kl', 'kal', 'kn', 'kan', 'kr', 'kau',
    'ks', 'kas', 'kk', 'kaz', 'ki', 'kik', 'rw', 'kin', 'kv', 'kom',
    'kg', 'kon', 'ko', 'kor', 'kj', 'kua', 'ku', 'kur', 'ky', 'kir',
    'lo', 'lao', 'la', 'lat', 'lv', 'lav', 'li', 'lim', 'ln', 'lin',
    'lt', 'lit', 'lu', 'lub', 'lb', 'ltz', 'mk', 'mkd', 'mg', 'mlg',
    'ms', 'msa', 'ml', 'mal', 'mt', 'mlt', 'gv', 'glv', 'mi', 'mri',
    'mr', 'mar', 'mh', 'mah', 'mn', 'mon', 'na', 'nau', 'nv', 'nav',
    'ng', 'ndo', 'ne', 'nep', 'nd', 'nde', 'se', 'sme', 'no', 'nor',
    'nb', 'nob', 'nn', 'nno', 'oc', 'oci', 'oj', 'oji', 'or', 'ori',
    'om', 'orm', 'os', 'oss', 'pi', 'pli', 'ps', 'pus', 'fa', 'fas',
    'pl', 'pol', 'pt', 'por', 'pa', 'pan', 'qu', 'que', 'ro', 'ron',
    'rm', 'roh', 'rn', 'run', 'ru', 'rus', 'sm', 'smo', 'sg', 'sag',
    'sa', 'san', 'sc', 'srd', 'sr', 'srp', 'sn', 'sna', 'ii', 'iii',
    'sd', 'snd', 'si', 'sin', 'sk', 'slk', 'sl', 'slv', 'so', 'som',
    'nr', 'nbl', 'st', 'sot', 'es', 'spa', 'su', 'sun', 'sw', 'swa',
    'ss', 'ssw', 'sv', 'swe', 'tl', 'tgl', 'ty', 'tah', 'tg', 'tgk',
    'ta', 'tam', 'tt', 'tat', 'te', 'tel', 'th', 'tha', 'bo', 'bod',
    'ti', 'tir', 'to', 'ton', 'ts', 'tso', 'tn', 'tsn', 'tr', 'tur',
    'tk', 'tuk', 'tw', 'twi', 'ug', 'uig', 'uk', 'ukr', 'ur', 'urd',
    'uz', 'uzb', 've', 'ven', 'vi', 'vie', 'vo', 'vol', 'wa', 'wln',
    'cy', 'cym', 'fy', 'fry', 'wo', 'wol', 'xh', 'xho', 'yi', 'yid',
    'yo', 'yor', 'za', 'zha', 'zu', 'zul'
}


def load_config():
    """
    Load configuration from config.ini file.
    
    Reads mkvmerge path and other settings from the [Embedding] section
    of config.ini. If the file doesn't exist or the setting is missing,
    uses sensible defaults.
    
    Returns:
        dict: Configuration dictionary with keys:
            - mkvmerge_path: Path to mkvmerge.exe (or None for default)
            - default_track: Whether subtitle track should be marked as default
            - language: Default language code for subtitle tracks
    """
    script_dir = Path(__file__).parent
    config_path = script_dir / 'config.ini'
    
    # Default configuration (Story 3.1 fallbacks)
    config_dict = {
        'mkvmerge_path': None,
        'default_track': True,
        'language': 'none',    # Story 3.1: fallback is 'none', not 'ar'
        'csv_export': False    # Story 3.1: fallback is false, not true
    }
    
    if not config_path.exists():
        print(f"[INFO] config.ini not found at {config_path}")
        create_default_config(config_path)
        # Continue to load the newly created config
    
    if not config_path.exists():
        # Fallback if creation failed
        print("[INFO] Using default configuration: mkvmerge.exe in script directory")
        return config_dict
    
    try:
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        
        # Read [Embedding] section
        if config.has_section('Embedding'):
            if config.has_option('Embedding', 'mkvmerge_path'):
                path = config.get('Embedding', 'mkvmerge_path').strip()
                if path:
                    config_dict['mkvmerge_path'] = path
            
            if config.has_option('Embedding', 'default_track'):
                try:
                    config_dict['default_track'] = config.getboolean('Embedding', 'default_track')
                except ValueError:
                    config_dict['default_track'] = True  # Fallback to True
                    print("[WARNING] Invalid default_track value, using fallback: true")
            
            if config.has_option('Embedding', 'language'):
                lang = config.get('Embedding', 'language').strip()
                if lang and lang.lower() != 'none':
                    # Validate against ISO-639 codes
                    if lang.lower() in VALID_LANGUAGE_CODES:
                        config_dict['language'] = lang
                    else:
                        print(f"[WARNING] Invalid language code '{lang}' - not a valid ISO-639 code")
                        print(f"[WARNING] Falling back to 'none' (no language tag will be set)")
                        config_dict['language'] = 'none'
                else:
                    config_dict['language'] = 'none'  # Explicit none or empty
        
        # Read [Reporting] section (Story 3.1)
        if config.has_section('Reporting'):
            if config.has_option('Reporting', 'csv_export'):
                try:
                    config_dict['csv_export'] = config.getboolean('Reporting', 'csv_export')
                except ValueError:
                    # Invalid value, use fallback
                    config_dict['csv_export'] = False
                    print("[WARNING] Invalid csv_export value, using fallback: false")
        
        print(f"[INFO] Configuration loaded from: {config_path}")
        if config_dict['mkvmerge_path']:
            print(f"  mkvmerge path: {config_dict['mkvmerge_path']}")
        else:
            print(f"  mkvmerge path: (default - script directory)")
        print(f"  default_track: {'yes' if config_dict['default_track'] else 'no'}")
        print(f"  language: {config_dict['language']}")
        print(f"  csv_export: {'enabled' if config_dict['csv_export'] else 'disabled'}")
        
        return config_dict
        
    except Exception as e:
        print(f"[WARNING] Failed to parse config.ini: {e}")
        print("[INFO] Using default configuration")
        return config_dict


def create_default_config(config_path):
    """
    Create a default config.ini file with example settings.
    
    Story 3.1: Creates config with example values (ar, true) but actual
    fallback defaults are (none, false) when values are missing/invalid.
    
    Args:
        config_path (Path): Path where config.ini should be created
    """
    config = configparser.ConfigParser()
    
    # Add [Embedding] section with example values
    config['Embedding'] = {
        'mkvmerge_path': '',  # Empty = use script directory
        'language': 'ar',     # Example: 'ar', Fallback: 'none'
        'default_track': 'true'
    }
    
    # Add [Reporting] section with example values
    config['Reporting'] = {
        'csv_export': 'true'  # Example: 'true', Fallback: 'false'
    }
    
    # Write config with explanatory comments
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write('# Subtitle Embedding Configuration\n')
        f.write('# Language detection order: Filename suffix → Config value → none (no tag)\n')
        f.write('# CSV export defaults to false if missing/invalid\n\n')
        config.write(f)
    
    print(f"[INFO] Created default config.ini at: {config_path}")
    print("[INFO] Language detection will follow: filename → config → none")


def validate_mkvmerge(mkvmerge_path=None):
    """
    Validate that mkvmerge.exe exists and is executable.
    
    Checks for mkvmerge at the specified path, or in the script directory
    if no path is provided. Runs 'mkvmerge --version' to verify it works.
    
    Args:
        mkvmerge_path: Optional path to mkvmerge.exe. If None, checks script directory.
    
    Returns:
        tuple: (success: bool, resolved_path: str or None, version_info: str or None)
    
    Examples:
        >>> validate_mkvmerge()
        (True, 'C:/path/to/mkvmerge.exe', 'mkvmerge v82.0')
        
        >>> validate_mkvmerge('/invalid/path')
        (False, None, None)
    """
    script_dir = Path(__file__).parent
    
    # Determine path to check
    if mkvmerge_path:
        mkvmerge_exe = Path(mkvmerge_path)
    else:
        mkvmerge_exe = script_dir / 'mkvmerge.exe'
    
    # Check if file exists
    if not mkvmerge_exe.exists():
        return False, None, None
    
    # Check if file is accessible (try to read it)
    if not os.access(mkvmerge_exe, os.R_OK):
        return False, str(mkvmerge_exe), None
    
    # Try to run mkvmerge --version
    try:
        result = subprocess.run(
            [str(mkvmerge_exe), '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            # Parse version from output (first line usually contains version)
            version_info = result.stdout.split('\n')[0] if result.stdout else "mkvmerge (version unknown)"
            return True, str(mkvmerge_exe), version_info
        else:
            return False, str(mkvmerge_exe), None
            
    except subprocess.TimeoutExpired:
        return False, str(mkvmerge_exe), None
    except FileNotFoundError:
        return False, str(mkvmerge_exe), None
    except Exception as e:
        print(f"[WARNING] Error running mkvmerge: {e}")
        return False, str(mkvmerge_exe), None


def detect_subtitle_language(subtitle_filename, config_language):
    """
    Detect subtitle language using 3-tier strategy (Story 3.1).
    
    Tier 1 (Highest Priority): Filename suffix (e.g., movie.ar.srt)
    Tier 2: Config file language value
    Tier 3 (Fallback): 'none' (no language tag)
    
    Args:
        subtitle_filename (str): Name of subtitle file
        config_language (str): Language from config file (or 'none')
    
    Returns:
        str: Detected language code or 'none'
    
    Examples:
        >>> detect_subtitle_language('movie.ar.srt', 'en')
        'ar'  # Filename overrides config
        
        >>> detect_subtitle_language('movie.srt', 'en')
        'en'  # No filename suffix, use config
        
        >>> detect_subtitle_language('movie.srt', 'none')
        'none'  # Both missing, use fallback
    """
    # Tier 1: Check filename for language suffix
    filename_lang = detect_language_from_filename(subtitle_filename)
    if filename_lang:
        return filename_lang
    
    # Tier 2: Use config language if valid (not 'none')
    if config_language and config_language != 'none' and len(config_language) in [2, 3]:
        return config_language
    
    # Tier 3: Default fallback
    return 'none'


def detect_language_from_filename(subtitle_file):
    """
    Detect language code from subtitle filename (Tier 1 helper).
    
    Implements strategy pattern: extract language from filename using common patterns.
    Supports both 2-letter (ISO 639-1) and 3-letter (ISO 639-2) codes.
    
    Args:
        subtitle_file (str or Path): Path to subtitle file
    
    Returns:
        str or None: Language code if detected, None otherwise
    
    Examples:
        >>> detect_language_from_filename('episode.ar.srt')
        'ar'
        
        >>> detect_language_from_filename('movie.eng.srt')
        'eng'
        
        >>> detect_language_from_filename('video.srt')
        None
    """
    filename = Path(subtitle_file).name.lower()
    
    # Common 2-letter ISO 639-1 codes
    two_letter_codes = [
        'ar', 'en', 'fr', 'de', 'es', 'it', 'pt', 'ru', 'ja', 'ko',
        'zh', 'hi', 'tr', 'pl', 'nl', 'sv', 'no', 'da', 'fi', 'cs',
        'el', 'he', 'hu', 'ro', 'sk', 'uk', 'vi', 'th', 'id', 'ms'
    ]
    
    # Common 3-letter ISO 639-2 codes
    three_letter_codes = [
        'ara', 'eng', 'fra', 'deu', 'ger', 'spa', 'ita', 'por', 'rus',
        'jpn', 'kor', 'zho', 'chi', 'hin', 'tur', 'pol', 'nld', 'dut',
        'swe', 'nor', 'dan', 'fin', 'ces', 'cze', 'ell', 'gre', 'heb',
        'hun', 'ron', 'rum', 'slk', 'slo', 'ukr', 'vie', 'tha', 'ind',
        'msa', 'may'
    ]
    
    # Pattern 1: .XX.ext (e.g., episode.ar.srt)
    pattern = r'\.([a-z]{2,3})\.[^.]+$'
    match = re.search(pattern, filename)
    
    if match:
        lang_code = match.group(1)
        if lang_code in two_letter_codes or lang_code in three_letter_codes:
            return lang_code
    
    # Pattern 2: _XX.ext (e.g., episode_ar.srt)
    pattern = r'_([a-z]{2,3})\.[^.]+$'
    match = re.search(pattern, filename)
    
    if match:
        lang_code = match.group(1)
        if lang_code in two_letter_codes or lang_code in three_letter_codes:
            return lang_code
    
    # Pattern 3: [XX] (e.g., episode[ar].srt)
    pattern = r'\[([a-z]{2,3})\]'
    match = re.search(pattern, filename)
    
    if match:
        lang_code = match.group(1)
        if lang_code in two_letter_codes or lang_code in three_letter_codes:
            return lang_code
    
    # No language code detected
    return None


# ============================================================================
# FILE DISCOVERY AND MATCHING (Story 2.1)
# ============================================================================

# Episode pattern detection - reused from rename_subtitles_to_match_videos_ar.py
EPISODE_PATTERNS = [
    (re.compile(r'[Ss](\d+)[Ee](\d+)'), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'(?:^|[._\s-])(\d{1,2})[xX](\d+)(?=[._\s-]|$)'), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss](\d{1,2})\s*-\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss](\d{1,2})\s*-\s*[Ee](\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'[Ss](\d{1,2})\s*-\s*[Ee][Pp](\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s*-\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s+[Ee]pisode\s+(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s+[Ee]\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
    (re.compile(r'(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s+[Ee][Pp]\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2).zfill(2))),
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

# Patterns for movie name matching
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

_episode_cache = {}


def get_episode_number(filename):
    """
    Extract episode information from filename using pattern matching.
    Adapted from rename_subtitles_to_match_videos_ar.py.
    
    Args:
        filename: The filename to parse
        
    Returns:
        Normalized episode string (e.g., 'S01E05') or None if no pattern found
    """
    for pattern, formatter in EPISODE_PATTERNS:
        match = pattern.search(filename)
        if match:
            season, episode = formatter(match)
            return f"S{season}E{episode}"
    return None


def get_episode_number_cached(filename):
    """Cached wrapper for get_episode_number - avoids redundant regex operations"""
    if filename not in _episode_cache:
        _episode_cache[filename] = get_episode_number(filename)
    return _episode_cache[filename]


def extract_base_name(filename):
    """
    Extract and clean base filename for comparison.
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
    Adapted from rename_subtitles_to_match_videos_ar.py.
    
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
    
    video_words = set(video_name.lower().split()) - COMMON_INDICATORS
    subtitle_words = set(subtitle_name.lower().split()) - COMMON_INDICATORS
    
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


def find_matching_files(directory):
    """
    Find and match MKV video files with corresponding subtitle files.
    
    Implements comprehensive file discovery and matching using patterns from
    rename_subtitles_to_match_videos_ar.py. Supports TV show episodes and movies.
    
    Args:
        directory: Path to directory to scan for files
    
    Returns:
        list: List of tuples (video_file, subtitle_file) as Path objects
    """
    dir_path = Path(directory)
    
    # Scan for video and subtitle files
    video_files = list(dir_path.glob('*.mkv'))
    subtitle_files = list(dir_path.glob('*.srt')) + list(dir_path.glob('*.ass')) + list(dir_path.glob('*.ssa'))
    
    # Filter out hidden files and already-embedded files
    video_files = [v for v in video_files if not v.name.startswith('.')]
    video_files = [v for v in video_files if not v.name.endswith('.embedded.mkv')]
    subtitle_files = [s for s in subtitle_files if not s.name.startswith('.')]
    
    print(f"\n[INFO] Files found: {len(video_files)} videos, {len(subtitle_files)} subtitles")
    
    if not video_files or not subtitle_files:
        print("[INFO] No video-subtitle pairs to match")
        return []
    
    # Build episode context for TV shows
    video_episodes = {}
    video_by_episode = {}
    
    for video in sorted(video_files, key=lambda v: v.name):
        episode_string = get_episode_number_cached(video.name)
        if episode_string:
            match = re.match(r'S(\d+)E(\d+)', episode_string)
            if match:
                season_num = int(match.group(1))
                episode_num = int(match.group(2))
                key = (season_num, episode_num)
                
                if key not in video_episodes:
                    video_episodes[key] = episode_string
                    video_by_episode[episode_string] = video
                elif episode_string not in video_by_episode:
                    video_by_episode[episode_string] = video
    
    # Match subtitles to videos
    matches = []
    matched_videos = set()
    matched_subtitles = set()
    
    # Try episode matching first
    for subtitle in sorted(subtitle_files, key=lambda s: s.name):
        episode_string = get_episode_number_cached(subtitle.name)
        
        if episode_string:
            # Standardize episode format to match video context
            match = re.match(r'S(\d+)E(\d+)', episode_string)
            if match:
                season_num = int(match.group(1))
                episode_num = int(match.group(2))
                key = (season_num, episode_num)
                
                # Use standardized episode string if available
                if key in video_episodes:
                    adjusted_episode = video_episodes[key]
                else:
                    adjusted_episode = episode_string
                
                # Find matching video
                if adjusted_episode in video_by_episode:
                    video = video_by_episode[adjusted_episode]
                    matches.append((video, subtitle))
                    matched_videos.add(video)
                    matched_subtitles.add(subtitle)
    
    # Try movie matching if no episode matches found
    if not matches:
        unmatched_videos = [v for v in video_files if v not in matched_videos]
        unmatched_subtitles = [s for s in subtitle_files if s not in matched_subtitles]
        
        movie_match = match_movie_files(unmatched_videos, unmatched_subtitles)
        if movie_match:
            video, subtitle = movie_match
            matches.append((video, subtitle))
            matched_videos.add(video)
            matched_subtitles.add(subtitle)
            print("[INFO] Movie mode: Matched single video-subtitle pair")
    
    # Report unmatched files
    unmatched_videos = [v for v in video_files if v not in matched_videos]
    unmatched_subtitles = [s for s in subtitle_files if s not in matched_subtitles]
    
    if unmatched_videos:
        print(f"\n[WARNING] {len(unmatched_videos)} video(s) without matching subtitles:")
        for video in unmatched_videos:
            ep = get_episode_number_cached(video.name)
            if ep:
                print(f"  - {video.name} ({ep})")
            else:
                print(f"  - {video.name} (no episode pattern detected)")
    
    if unmatched_subtitles:
        print(f"\n[WARNING] {len(unmatched_subtitles)} subtitle(s) without matching videos:")
        for subtitle in unmatched_subtitles:
            ep = get_episode_number_cached(subtitle.name)
            if ep:
                print(f"  - {subtitle.name} ({ep})")
            else:
                print(f"  - {subtitle.name} (no episode pattern detected)")
    
    # Display matching results
    if matches:
        print(f"\n[INFO] Found {len(matches)} video-subtitle pair(s):")
        for video, subtitle in matches:
            ep = get_episode_number_cached(video.name)
            if ep:
                print(f"  - {video.name} + {subtitle.name} ({ep})")
            else:
                print(f"  - {video.name} + {subtitle.name} (movie)")
        print()
    
    return matches


def build_mkvmerge_command(video_file, subtitle_file, output_file, config):
    """
    Build mkvmerge command line for embedding subtitle into video.
    
    Generates Windows-compatible subprocess command as list of arguments.
    Implements language detection strategy and configurable default track flag.
    
    Args:
        video_file (str or Path): Path to source MKV video file
        subtitle_file (str or Path): Path to subtitle file to embed
        output_file (str or Path): Path for output merged file
        config (dict): Configuration dictionary from load_config()
    
    Returns:
        list: Command line arguments for subprocess.run()
    
    Example:
        >>> config = {'mkvmerge_path': None, 'default_track': True, 'language': 'ar'}
        >>> cmd = build_mkvmerge_command('video.mkv', 'sub.srt', 'out.mkv', config)
        >>> cmd[0]  # mkvmerge path
        >>> cmd[1:3]  # ['-o', 'out.mkv']
    """
    # Get validated mkvmerge path
    success, mkvmerge_path, _ = validate_mkvmerge(config.get('mkvmerge_path'))
    
    if not success:
        raise FileNotFoundError("mkvmerge.exe not found or not executable")
    
    # Build command as list (Windows subprocess pattern)
    command = [
        str(mkvmerge_path),
        '-o', str(output_file),
        str(video_file)
    ]
    
    # Story 3.1: 3-tier language detection (filename → config → none)
    config_language = config.get('language', 'none')
    detected_language = detect_subtitle_language(Path(subtitle_file).name, config_language)
    
    # Only add language option if not 'none'
    if detected_language and detected_language != 'none':
        command.extend(['--language', f'0:{detected_language}'])
    
    # Add default track flag (explicit yes or no)
    if config.get('default_track', True):
        command.extend(['--default-track', '0:yes'])
    else:
        command.extend(['--default-track', '0:no'])
    
    # Add subtitle file
    command.append(str(subtitle_file))
    
    return command


# ============================================================================
# Story 2.2: Backup and Output File Management Functions
# ============================================================================

def has_sufficient_space(video_file, subtitle_file):
    """
    Check if there is sufficient disk space for the embedding operation.
    
    Required space = video file size + subtitle file size + 10% overhead
    
    Args:
        video_file (Path): Path to video file
        subtitle_file (Path): Path to subtitle file
    
    Returns:
        bool: True if sufficient space available, False otherwise
    """
    video_size = video_file.stat().st_size
    subtitle_size = subtitle_file.stat().st_size
    required_space = video_size + subtitle_size + int((video_size + subtitle_size) * 0.10)
    
    # Check available space on the drive containing the video file
    disk_usage = shutil.disk_usage(video_file.parent)
    available_space = disk_usage.free
    
    return available_space > required_space


def ensure_backups_directory(working_dir):
    """
    Create backups/ directory if it doesn't exist.
    
    Args:
        working_dir (Path): Working directory where backups/ should be created
    
    Returns:
        Path: Path to the backups directory
    """
    backups_dir = working_dir / 'backups'
    if not backups_dir.exists():
        backups_dir.mkdir(exist_ok=True)
        print("[BACKUP] Creating backups/ directory...")
    return backups_dir


def backup_originals(video_file, subtitle_file, backups_dir):
    """
    Intelligently backup original files to backups directory.
    
    Checks each file independently - only moves files that don't already
    exist in the backups directory.
    
    Args:
        video_file (Path): Path to original video file
        subtitle_file (Path): Path to original subtitle file
        backups_dir (Path): Path to backups directory
    
    Returns:
        tuple[bool, bool]: (video_backed_up, subtitle_backed_up)
            - True if file was backed up in this operation
            - False if file already exists in backups (skipped)
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
    Delete subtitle from working directory ONLY if it exists in backups.
    
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
    Rename .embedded.mkv to final .mkv filename (overwrites if exists).
    
    Args:
        embedded_file (Path): Path to temporary .embedded.mkv file
        final_name (Path): Path to final .mkv filename
    """
    embedded_file.replace(final_name)


def cleanup_failed_merge(embedded_file):
    """
    Delete temporary .embedded.mkv file after merge failure.
    Original files remain untouched.
    
    Args:
        embedded_file (Path): Path to temporary .embedded.mkv file
    """
    if embedded_file.exists():
        embedded_file.unlink()
        print(f"[CLEANUP] Removed temporary file: {embedded_file.name}")


# ============================================================================
# End of Story 2.2 Functions
# ============================================================================


def validate_file_pair(video_file, subtitle_file):
    """
    Validate that video and subtitle files are suitable for embedding.
    
    Checks file existence, extensions, and permissions.
    
    Args:
        video_file (str or Path): Path to video file
        subtitle_file (str or Path): Path to subtitle file
    
    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    video_path = Path(video_file)
    subtitle_path = Path(subtitle_file)
    
    # Check video file exists
    if not video_path.exists():
        return False, f"Video file not found: {video_path}"
    
    # Check video extension
    if video_path.suffix.lower() != '.mkv':
        return False, f"Video file must be .mkv format: {video_path}"
    
    # Check video read permission
    if not os.access(video_path, os.R_OK):
        return False, f"Cannot read video file (permission denied): {video_path}"
    
    # Check subtitle file exists
    if not subtitle_path.exists():
        return False, f"Subtitle file not found: {subtitle_path}"
    
    # Check subtitle extension
    valid_subtitle_exts = ['.srt', '.ass', '.ssa']
    if subtitle_path.suffix.lower() not in valid_subtitle_exts:
        return False, f"Subtitle file must be .srt, .ass, or .ssa format: {subtitle_path}"
    
    # Check subtitle read permission
    if not os.access(subtitle_path, os.R_OK):
        return False, f"Cannot read subtitle file (permission denied): {subtitle_path}"
    
    # Check output directory is writable
    output_dir = video_path.parent
    if not os.access(output_dir, os.W_OK):
        return False, f"Cannot write to output directory (permission denied): {output_dir}"
    
    return True, None


def embed_subtitle_pair(video_path, subtitle_path, config, backups_dir=None):
    """
    Embed a single subtitle file into a video file with intelligent backup management.
    
    Story 2.2: Implements the complete workflow:
    1. Check disk space
    2. Create temporary .embedded.mkv file
    3. On success: backup originals to backups/, rename embedded to final
    4. On failure: cleanup temp file, originals untouched
    
    Args:
        video_path (str or Path): Path to source MKV video file
        subtitle_path (str or Path): Path to subtitle file to embed
        config (dict): Configuration dictionary from load_config()
        backups_dir (Path, optional): Path to backups directory (created if None)
    
    Returns:
        tuple: (success: bool, output_file: Path or None, error_message: str or None, backups_dir: Path or None)
            - backups_dir is returned so batch processing can reuse it
    
    Example:
        >>> config = load_config()
        >>> success, output, error, backups = embed_subtitle_pair('video.mkv', 'sub.ar.srt', config)
        >>> if success:
        ...     print(f"Created: {output}")
    """
    video_path = Path(video_path)
    subtitle_path = Path(subtitle_path)
    
    # Validate file pair
    valid, error_msg = validate_file_pair(video_path, subtitle_path)
    if not valid:
        return False, None, error_msg, backups_dir
    
    # Story 2.2: Check disk space before operations
    if not has_sufficient_space(video_path, subtitle_path):
        error_msg = f"Insufficient disk space for {video_path.name}"
        print(f"[ERROR] {error_msg}")
        return False, None, error_msg, backups_dir
    
    # Generate temporary embedded filename
    embedded_file = video_path.parent / f"{video_path.stem}.embedded.mkv"
    final_file = video_path  # Final name is the original video name
    
    # Detect language for logging
    language = detect_language_from_filename(subtitle_path)
    if language:
        print(f"[INFO] Detected language: {language}")
    else:
        fallback_lang = config.get('language')
        if fallback_lang:
            print(f"[INFO] No language in filename, using config default: {fallback_lang}")
        else:
            print(f"[INFO] No language detected or configured")
    
    # Build mkvmerge command
    try:
        command = build_mkvmerge_command(video_path, subtitle_path, embedded_file, config)
    except FileNotFoundError as e:
        return False, None, str(e), backups_dir
    
    print(f"[INFO] Executing mkvmerge...")
    print(f"  Video: {video_path.name}")
    print(f"  Subtitle: {subtitle_path.name}")
    print(f"  Temporary output: {embedded_file.name}")
    
    # Execute mkvmerge command
    success, stdout, stderr = run_command(command)
    
    if not success:
        # Merge failed - cleanup temp file
        cleanup_failed_merge(embedded_file)
        error_msg = f"mkvmerge failed: {stderr if stderr else 'Unknown error'}"
        print(f"[ERROR] {error_msg}")
        return False, None, error_msg, backups_dir
    
    # Merge succeeded - Story 2.2: Backup workflow
    try:
        # Create backups directory on first success
        if backups_dir is None:
            backups_dir = ensure_backups_directory(video_path.parent)
        
        # Intelligently backup originals (checks each file independently)
        video_backed_up, subtitle_backed_up = backup_originals(video_path, subtitle_path, backups_dir)
        
        # Only delete subtitle if it's safely in backups/
        safe_delete_subtitle(subtitle_path, backups_dir)
        
        # Rename embedded file to original name (overwrites original video)
        rename_embedded_to_final(embedded_file, final_file)
        
        print(f"[SUCCESS] Created: {final_file.name}")
        return True, final_file, None, backups_dir
        
    except Exception as e:
        # Ensure temp file cleanup on any error
        cleanup_failed_merge(embedded_file)
        error_msg = f"Backup workflow failed: {str(e)}"
        print(f"[ERROR] {error_msg}")
        return False, None, error_msg, backups_dir


def run_command(command):
    """
    Execute a command using subprocess and return the result.
    
    Args:
        command: List of command arguments to execute
    
    Returns:
        tuple: (success: bool, stdout: str, stderr: str)
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout for mkvmerge operations
        )
        
        success = (result.returncode == 0)
        return success, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out after 5 minutes"
    except Exception as e:
        return False, "", str(e)


def generate_report(processed_files, output_path, config):
    """
    Generate CSV report of embedding operations (Story 3.3).
    
    Story 3.1: Checks config['csv_export'] flag (fallback: false).
    Only generates report if csv_export is True.
    
    Args:
        processed_files: List of processed file information
        output_path: Path where CSV report should be saved
        config: Configuration dictionary with csv_export flag
    """
    # Story 3.1: Check csv_export flag
    csv_export = config.get('csv_export', False)
    if not csv_export:
        return  # Skip CSV generation
    
    # TODO: Implement CSV generation in Story 3.3
    print("[INFO] CSV export enabled but not yet implemented (Story 3.3)")
    pass


def print_operation_summary(results):
    """
    Display a formatted summary of embedding operations.
    
    Shows success/failure counts and details of any failures.
    
    Args:
        results (list): List of result dictionaries with keys:
            - video: Path to video file
            - subtitle: Path to subtitle file
            - success: bool indicating success
            - output: Path to output file (if successful)
            - error: Error message (if failed)
    """
    print()
    print("=" * 80)
    print("OPERATION SUMMARY")
    print("=" * 80)
    
    total = len(results)
    successful = sum(1 for r in results if r['success'])
    failed = total - successful
    
    print(f"Total Processed: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    
    if failed > 0:
        print()
        print("FAILURES:")
        failure_num = 1
        for result in results:
            if not result['success']:
                print(f"  [{failure_num}] {result['video'].name} + {result['subtitle'].name}")
                print(f"      Error: {result['error']}")
                print()
                failure_num += 1
    
    print("=" * 80)


def determine_exit_code(results, mkvmerge_valid=True):
    """
    Determine appropriate exit code based on operation results.
    
    Args:
        results (list): List of result dictionaries
        mkvmerge_valid (bool): Whether mkvmerge was found and validated
    
    Returns:
        int: Exit code (EXIT_SUCCESS, EXIT_FATAL_ERROR, EXIT_PARTIAL_FAILURE, EXIT_COMPLETE_FAILURE)
    """
    if not mkvmerge_valid:
        return EXIT_FATAL_ERROR
    
    if not results:
        # No files to process is not an error
        return EXIT_SUCCESS
    
    failed_count = sum(1 for r in results if not r['success'])
    total_count = len(results)
    
    if failed_count == 0:
        return EXIT_SUCCESS
    elif failed_count == total_count:
        return EXIT_COMPLETE_FAILURE
    else:
        return EXIT_PARTIAL_FAILURE


def display_batch_progress(current: int, total: int, filename: str) -> None:
    """
    Display progress for current file in batch processing.
    
    Args:
        current: Current file number (1-indexed)
        total: Total number of files to process
        filename: Name of the file being processed
    """
    percentage = int((current / total) * 100)
    print(f"\n[{current}/{total}] ({percentage}%) Processing: {filename}...")
    print("-" * 60)


def format_duration(seconds: float) -> str:
    """
    Convert seconds to human-readable duration format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string (e.g., "2m 35s", "1h 15m 30s")
    """
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes}m {remaining_seconds}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        remaining_seconds = int(seconds % 60)
        return f"{hours}h {minutes}m {remaining_seconds}s"


def display_batch_summary(total: int, successful: int, failed: int, duration: float) -> None:
    """
    Display comprehensive summary after batch processing.
    
    Args:
        total: Total number of pairs found
        successful: Number of successful operations
        failed: Number of failed operations
        duration: Total processing time in seconds
    """
    success_rate = (successful / total * 100) if total > 0 else 0
    formatted_time = format_duration(duration)
    
    print("\n" + "=" * 40)
    print("=== BATCH PROCESSING COMPLETE ===")
    print("=" * 40)
    print(f"Total pairs found: {total}")
    print(f"Successfully processed: {successful}")
    print(f"Failed operations: {failed}")
    print(f"Success rate: {success_rate:.1f}%")
    print(f"Total time: {formatted_time}")
    print("=" * 40)


def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Embed subtitle files into MKV video files using mkvmerge',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    Process files in current directory
  %(prog)s /path/to/videos    Process files in specified directory
  %(prog)s --test-mkvmerge    Test mkvmerge connectivity
  %(prog)s --version          Show script version
        """
    )
    
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory containing video and subtitle files (default: current directory)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    parser.add_argument(
        '--test-mkvmerge',
        action='store_true',
        help='Test mkvmerge connectivity and exit'
    )
    
    return parser.parse_args()


def main():
    """
    Main entry point for the subtitle embedding script.
    
    Workflow:
    1. Parse command-line arguments
    2. Load configuration
    3. Validate mkvmerge (fail fast if not found)
    4. Find matching files (if not in test mode)
    5. Process each file pair with resilient batch processing
    6. Display operation summary
    7. Return appropriate exit code
    
    Returns:
        int: Exit code
            0 (EXIT_SUCCESS): All operations succeeded
            1 (EXIT_FATAL_ERROR): mkvmerge not found or fatal error
            2 (EXIT_PARTIAL_FAILURE): Some operations failed, some succeeded
            3 (EXIT_COMPLETE_FAILURE): All operations failed
    """
    print("=" * 60)
    print("Subtitle Embedding Tool [AR]")
    print(f"Version {__version__}")
    print("=" * 60)
    print()
    
    # Parse arguments
    args = parse_arguments()
    
    # Load configuration
    config = load_config()
    print()
    
    # Validate mkvmerge (EARLY VALIDATION - fail fast)
    print("Validating mkvmerge...")
    success, mkvmerge_path, version_info = validate_mkvmerge(config['mkvmerge_path'])
    
    if not success:
        print("[ERROR] mkvmerge.exe not found or not executable")
        if mkvmerge_path:
            print(f"  Checked path: {mkvmerge_path}")
        else:
            script_dir = Path(__file__).parent
            print(f"  Checked path: {script_dir / 'mkvmerge.exe'}")
        print("\nPlease ensure:")
        print("  1. MKVToolNix is installed")
        print("  2. mkvmerge.exe is in the script directory, OR")
        print("  3. mkvmerge_path is correctly set in config.ini [Embedding] section")
        return EXIT_FATAL_ERROR
    
    print(f"[OK] {version_info}")
    print(f"  Path: {mkvmerge_path}")
    print()
    
    # If test mode, exit here
    if args.test_mkvmerge:
        print("[SUCCESS] mkvmerge connectivity test passed")
        return EXIT_SUCCESS
    
    # Validate target directory
    target_dir = Path(args.directory).resolve()
    if not target_dir.exists():
        print(f"[ERROR] Directory does not exist: {target_dir}")
        return EXIT_FATAL_ERROR
    
    if not target_dir.is_dir():
        print(f"[ERROR] Path is not a directory: {target_dir}")
        return EXIT_FATAL_ERROR
    
    print(f"Target directory: {target_dir}")
    print()
    
    # Find matching video-subtitle pairs
    print("Searching for matching video and subtitle files...")
    file_pairs = find_matching_files(target_dir)
    
    if not file_pairs:
        print("[INFO] No matching video-subtitle pairs found")
        return EXIT_SUCCESS
    
    print(f"[INFO] Found {len(file_pairs)} video-subtitle pair(s)")
    print()
    
    # Initialize tracking (Story 2.3)
    total_pairs = len(file_pairs)
    successful_count = 0
    failed_count = 0
    start_time = time.time()
    
    # Process each file pair with resilient batch processing (Story 2.2 + 2.3)
    results = []
    backups_dir = None  # Lazy creation on first successful merge
    
    for idx, (video_file, subtitle_file) in enumerate(file_pairs, 1):
        # Display progress (Story 2.3)
        display_batch_progress(idx, total_pairs, video_file.name)
        print(f"           Subtitle: {subtitle_file.name}")
        
        # Process the pair with error recovery (Story 2.2 + 2.3)
        try:
            success, output_file, error_message, backups_dir = embed_subtitle_pair(
                video_file, subtitle_file, config, backups_dir
            )
            
            # Track result
            results.append({
                'video': video_file,
                'subtitle': subtitle_file,
                'success': success,
                'output': output_file,
                'error': error_message
            })
            
            # Display result and update counters (Story 2.3)
            if success:
                successful_count += 1
                print(f"[SUCCESS] Completed: {video_file.name}")
            else:
                failed_count += 1
                print(f"[ERROR] Failed: {error_message}")
        except Exception as e:
            # Graceful error recovery (Story 2.3)
            failed_count += 1
            error_msg = str(e)
            print(f"[ERROR] Failed to process pair: {video_file.name} + {subtitle_file.name}")
            print(f"Error details: {error_msg}")
            
            # Track failed result
            results.append({
                'video': video_file,
                'subtitle': subtitle_file,
                'success': False,
                'output': None,
                'error': error_msg
            })
            # Continue to next pair - don't stop batch processing
        
        print()
    
    # Calculate total duration (Story 2.3)
    total_duration = time.time() - start_time
    
    # Display comprehensive batch summary (Story 2.3)
    display_batch_summary(total_pairs, successful_count, failed_count, total_duration)
    
    # Story 2.2: Final tip about backups
    if backups_dir and backups_dir.exists():
        print()
        print("Tip: Verify merged files before manually deleting backups/ directory")
        print(f"     Backups location: {backups_dir}")
    
    # Return appropriate exit code
    return determine_exit_code(results)


if __name__ == "__main__":
    sys.exit(main())
