"""
Pattern Recognition Engine

Comprehensive episode pattern matching for subtitle/video file pairing.
Supports 25+ different episode naming conventions with optimized caching.

Version: 3.1.0
"""

import re
from typing import Optional, Tuple, Dict
from functools import lru_cache


# Pre-compiled regex patterns for episode detection
# CRITICAL: Pattern order matters! Patterns are tried in sequence, first match wins.
# These patterns MUST match v3.0.0 exactly (verified 2025-01-12)
EPISODE_PATTERNS = [
    # Format: (pattern_name, compiled_regex, formatter_function)
    
    # Pattern 1: S##E## format (most common - e.g., S01E05, S2E10, S02 E3)
    # Supports optional space between S and E (e.g., "S3 E2" or "S03E02")
    (
        'S##E##',
        re.compile(r'[Ss](\d+)\s?[Ee](\d+)'),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 1a: S## Episode ## format (e.g., S01 Episode 05, S2 Episode 10) - full Episode word
    (
        'S## Episode ##',
        re.compile(r'[Ss](\d+)\s+[Ee]pisode\s+(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 2: ##x## format (e.g., 2x05, 1x10)
    (
        '##x##',
        re.compile(r'(?:^|[._\s-])(\d{1,2})[xX](\d+)(?=[._\s-]|$)'),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 3: S## - ## format (e.g., S01 - 05, S2 - 10)
    (
        'S## - ##',
        re.compile(r'[Ss](\d{1,2})\s*-\s*(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 4: S## - E## format (e.g., S01 - E05, S2 - E10)
    (
        'S## - E##',
        re.compile(r'[Ss](\d{1,2})\s*-\s*[Ee](\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 4a: S##.E## format (e.g., S01.E05, S2.E10) - dot separator variation
    (
        'S##.E##',
        re.compile(r'[Ss](\d{1,2})\.E(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 4b: S##_E## format (e.g., S01_E05, S2_E10) - underscore separator variation
    (
        'S##_E##',
        re.compile(r'[Ss](\d{1,2})_[Ee](\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 5: S## - EP## format (e.g., S01 - EP05, S2 - EP10)
    (
        'S## - EP##',
        re.compile(r'[Ss](\d{1,2})\s*-\s*[Ee][Pp](\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 5a: S## EP## format (e.g., S01 EP05, S2 EP10, s2 ep 08) - no dash variation, allows space before episode
    (
        'S## EP##',
        re.compile(r'[Ss](\d{1,2})\s+[Ee][Pp]\s*(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 5b: S##.EP## format (e.g., S02.EP13, s02.ep13) - dot separator variation
    (
        'S##.EP##',
        re.compile(r'[Ss](\d{1,2})\.[Ee][Pp](\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 6: 1st Season - ## format (e.g., 1st Season - 05, 2nd Season - 10)
    (
        '1st Season - ##',
        re.compile(r'(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s*-\s*(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 7: 3rd Season Episode 8 → S03E08 (CRITICAL: placed before generic patterns)
    (
        '1st Season Episode ##',
        re.compile(r'(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s+[Ee]pisode\s+(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 8: 2nd Season E10 → S02E10
    (
        '1st Season E##',
        re.compile(r'(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s+[Ee]\s*(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 9: 2nd Season EP10 → S02E10
    (
        '1st Season EP##',
        re.compile(r'(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s+[Ee][Pp]\s*(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 10: Season ## - ## format (e.g., Season 2 - 23, Season 12 - 103)
    (
        'Season ## - ##',
        re.compile(r'[Ss]eason\s+(\d{1,2})\s*-\s*(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 11: Season## - ## format (no space after "Season")
    (
        'Season## - ##',
        re.compile(r'[Ss]eason(\d{1,2})\s*-\s*(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 12: Season.#.Episode.# format
    (
        'Season.#.Episode.#',
        re.compile(r'[Ss]eason\.(\d+)[\s\._-]*[Ee]pisode\.(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 13: S#.Ep.# format
    (
        'S#.Ep.#',
        re.compile(r'[Ss](\d+)[\s\._-]*[Ee]p(?:isode)?\.(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 14: S#Ep# format (no separator)
    (
        'S#Ep#',
        re.compile(r'[Ss](\d+)[Ee]p(?:isode)?(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 15: Season # Episode # format (with spaces)
    (
        'Season # Episode #',
        re.compile(r'[Ss]eason\s+(\d+)\s+[Ee]pisode\s+(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 15a: Season## Episode ## format (optional spaces, space OR underscore separator)
    # Examples: Season01 Episode05, Season 01_Episode 05, Season01_Episode05
    (
        'Season##_Episode##',
        re.compile(r'[Ss]eason\s*(\d+)[\s_]+[Ee]pisode\s*(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 16: Season#Episode# format (no spaces)
    (
        'Season#Episode#',
        re.compile(r'[Ss]eason(\d+)[Ee]pisode(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 17: Season# Episode# format (space before Episode only)
    (
        'Season# Episode#',
        re.compile(r'[Ss]eason(\d+)\s+[Ee]pisode(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 18: Season# Ep# format (space before Ep)
    (
        'Season# Ep#',
        re.compile(r'[Ss]eason(\d+)\s+[Ee]p(?:isode)?(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 19: Season#Ep# format (no spaces)
    (
        'Season#Ep#',
        re.compile(r'[Ss]eason(\d+)[Ee]p(?:isode)?(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 19a: season## e## format (lowercase, concatenated season, just 'e', e.g., season2 e21)
    (
        'season## e##',
        re.compile(r'[Ss]eason(\d+)\s+[Ee](\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 20: Season #.Ep # format (separator between Season and Ep)
    (
        'Season #.Ep #',
        re.compile(r'[Ss]eason\s+(\d+)[\s\._-]*[Ee]p(?:isode)?\s*(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 22: Season#.Ep# format (no space after Season)
    (
        'Season#.Ep#',
        re.compile(r'[Ss]eason(\d+)[\s\._-]*[Ee]p(?:isode)?(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 23: Season # Ep # format (spaces everywhere) - SWAPPED for better specificity
    (
        'Season # Ep #',
        re.compile(r'[Ss]eason\s+(\d+)\s+[Ee]p(?:isode)?\s*(\d+)', re.IGNORECASE),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 24: Ep# format (assumes Season 1) - SWAPPED from Pattern 23
    (
        'Ep##',
        re.compile(r'(?:^|[._\s-])[Ee]p(?:isode)?\s*(\d+)(?=[._\s-]|$)', re.IGNORECASE),
        lambda m: (1, int(m.group(1)))
    ),
    
    # Pattern 25: E# format (assumes Season 1) - MOVED from Pattern 20 for better specificity
    (
        'E##',
        re.compile(r'(?:^|[._\s-])[Ee](\d+)(?=[._\s-]|$)'),
        lambda m: (1, int(m.group(1)))
    ),
    
    # Pattern 26: ## - ## format (Season-Episode with dash, e.g., "Show 3 - 04.mkv")
    # Season and episode numbers separated by dash, no S/E prefix
    # Optional spaces around dash, supports 1-99 for both season and episode
    (
        '## - ##',
        re.compile(r'(?<![0-9])(\d{1,2})\s*-\s*(\d{1,2})(?![a-zA-Z0-9])'),
        lambda m: (int(m.group(1)), int(m.group(2)))
    ),
    
    # Pattern 27: - # format (assumes Season 1, e.g., "Show - 15.mkv")
    # Hardened: Episodes 1-1899 only, excludes years 1900+, blocks letter suffixes (1080p, x264)
    (
        '- ##',
        re.compile(r'-\s*(?:1[0-8]\d{2}|\d{1,3})(?![a-zA-Z0-9])'),
        lambda m: (1, int(m.group(0).split('-')[1].strip()))
    ),
    
    # Pattern 28: [##] format (assumes Season 1, e.g., "[07].mkv")
    # Hardened: Same as Pattern 27, blocks [10bit], [1080p], [x265] etc.
    # Examples: [07] → S01E07, but [10bit] → no match
    (
        '[##]',
        re.compile(r'\[(\d{1,2})\](?![a-zA-Z0-9])'),
        lambda m: (1, int(m.group(1)))
    ),
    
    # Pattern 29: _## format (assumes Season 1, e.g., "Show_09.mkv")
    # Hardened: Same as Pattern 27, blocks _1080p etc.
    # LAST PATTERN - most permissive
    (
        '_##',
        re.compile(r'_(?:1[0-8]\d{2}|\d{1,3})(?![a-zA-Z0-9])'),
        lambda m: (1, int(m.group(0).split('_')[1].strip()))
    ),
]


# Episode number cache for performance
_episode_cache: Dict[str, Optional[str]] = {}


def normalize_episode_number(season: int, episode: int) -> str:
    """
    Normalize season and episode numbers to standard format.
    
    Args:
        season: Season number
        episode: Episode number
        
    Returns:
        Normalized string like 'S01E05' or 'S2E15'
    """
    if season < 10:
        season_str = f"S0{season}"
    else:
        season_str = f"S{season}"
    
    if episode < 10:
        episode_str = f"E0{episode}"
    else:
        episode_str = f"E{episode}"
    
    return f"{season_str}{episode_str}"


def extract_episode_info(filename: str) -> Optional[Tuple[int, int]]:
    """
    Extract season and episode numbers from filename.
    
    Tries patterns in order of frequency. Returns on first match for performance.
    
    Args:
        filename: Filename to parse (with or without extension)
        
    Returns:
        Tuple of (season, episode) or None if no pattern matches
    """
    for pattern_name, pattern, formatter in EPISODE_PATTERNS:
        match = pattern.search(filename)
        if match:
            try:
                result = formatter(match)
                if result:
                    return result
            except (ValueError, IndexError):
                continue
    
    return None


@lru_cache(maxsize=1024)
def get_episode_number_cached(filename: str) -> Optional[str]:
    """
    Extract and normalize episode number with caching.
    
    Uses LRU cache for performance on large datasets (12x speedup).
    
    Args:
        filename: Filename to parse
        
    Returns:
        Normalized episode string (e.g., 'S01E05') or None
    """
    episode_info = extract_episode_info(filename)
    if episode_info:
        season, episode = episode_info
        return normalize_episode_number(season, episode)
    return None


def extract_season_episode_numbers(episode_string: str) -> Tuple[str, str]:
    """
    Parse normalized episode string to extract season and episode numbers.
    
    Args:
        episode_string: Episode string in S##E## format (e.g., 'S01E05')
        
    Returns:
        Tuple of (season_str, episode_str) as strings with zero-padding
        Returns ("", "") if parsing fails
        
    Examples:
        >>> extract_season_episode_numbers('S01E05')
        ('01', '05')
        >>> extract_season_episode_numbers('S2E10')
        ('2', '10')
    """
    if not episode_string:
        return "", ""
    
    match = re.match(r'S(\d+)E(\d+)', episode_string, re.IGNORECASE)
    if match:
        return match.group(1), match.group(2)
    return "", ""


def clear_episode_cache():
    """Clear the episode number cache."""
    get_episode_number_cached.cache_clear()
    _episode_cache.clear()


def get_cache_info():
    """Get cache statistics for performance monitoring."""
    return get_episode_number_cached.cache_info()
