#!/usr/bin/env python3
"""
SubFast - Renaming Module
Version: 3.1.0

Fast subtitle renaming for all languages.
Automatically renames subtitle files to match corresponding video files based on 
detected episode patterns. Adds customizable language tag before the file extension.

Supports multiple episode naming patterns (S01E01, 2x05, Season.Episode, etc.) and
includes movie matching mode for single video/subtitle pairs.
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime
import time

# Import shared modules
from common import config_loader
from common import pattern_engine
from common import csv_reporter


# Utility regex patterns for filename processing
PROBLEMATIC_CHARS = re.compile(r'[<>:"/\|?*]')
SUBTITLE_SUFFIX_PATTERN = re.compile(r'[._\-\s]*[Ss]ub(title)?[._\-\s]*', re.IGNORECASE)
YEAR_PATTERN = re.compile(r'(?:19|20)\d{2}')
BASE_NAME_CLEANUP = re.compile(r'[._\-]+')

# Common quality/format indicators to exclude when matching movie titles
COMMON_INDICATORS = {
    '1080p', '720p', '480p', '2160p', '4k', 'bluray', 'web', 'dvd', 'hd', 'x264', 'x265', 
    'h264', 'h265', 'avc', 'hevc', 'aac', 'ac3', 'dts', 'remux', 'proper', 'repack', 
    'extended', 'theatrical', 'unrated', 'directors', 'cut', 'multi', 'sub', 'eng', 'en', 
    'ara', 'ar', 'eng', 'fre', 'fr', 'ger', 'de', 'ita', 'es', 'spa', 'kor', 'jpn', 'ch',
    'chs', 'cht', 'internal', 'limited', 'unrated', 'xvid', 'divx', 'ntsc', 'pal', 'dc',
    'sync', 'syncopated', 'cc', 'sdh', 'hc', 'proper', 'real', 'final', 'post', 'pre', 
    'sync', 'dub', 'dubbed', 'sdh', 'cc'
}


def extract_base_name(filename):
    """Extract and clean base filename for comparison."""
    base_name = os.path.splitext(filename)[0]
    base_name = BASE_NAME_CLEANUP.sub(' ', base_name)
    return base_name.strip()


def find_movie_subtitle_match(video_files, subtitle_files):
    """
    Match single movie file with single subtitle based on title similarity.
    
    Uses two strategies:
    1. Year matching: If both contain same 4-digit year
    2. Word overlap: Compares common words after removing quality indicators
    
    Returns:
        Tuple of (video_file, subtitle_file) if match found, None otherwise
    """
    if len(video_files) != 1 or len(subtitle_files) != 1:
        return None
    
    video_name = extract_base_name(video_files[0])
    subtitle_name = extract_base_name(subtitle_files[0])
    
    # Extract release years if present
    video_year_match = YEAR_PATTERN.search(video_files[0])
    subtitle_year_match = YEAR_PATTERN.search(subtitle_files[0])
    
    video_year = video_year_match.group() if video_year_match else None
    subtitle_year = subtitle_year_match.group() if subtitle_year_match else None
    
    # Split into words and filter out quality indicators
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


def build_subtitle_filename(base_name, subtitle_ext, language_suffix):
    """Generate subtitle filename with optional language suffix."""
    if language_suffix:
        return f"{base_name}.{language_suffix}{subtitle_ext}"
    else:
        return f"{base_name}{subtitle_ext}"


def generate_unique_name(base_name, subtitle_ext, subtitle, directory, language_suffix):
    """
    Generate unique filename when multiple subtitles match same video.
    
    First attempts standard format: {video_base}.ar{ext}
    If exists, creates unique variant with original subtitle name.
    """
    new_name = build_subtitle_filename(base_name, subtitle_ext, language_suffix)
    new_path = os.path.join(directory, new_name)
    
    if not os.path.exists(new_path):
        return new_name, new_path
    
    # File exists - create unique name with original subtitle name
    original_base = os.path.splitext(subtitle)[0]
    original_cleaned = SUBTITLE_SUFFIX_PATTERN.sub('', original_base)
    if not original_cleaned:
        original_cleaned = original_base
    
    suffix_part = f"{language_suffix}_" if language_suffix else ""
    specific_new_name = f"{base_name}.{suffix_part}{original_cleaned}{subtitle_ext}"
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
    
    Returns:
        Tuple of (video_episodes dict, temp_video_dict)
        - video_episodes: Maps (season, episode) tuples to canonical episode strings
        - temp_video_dict: Maps episode strings to video filenames
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


def process_subtitles(subtitle_files, video_episodes, temp_video_dict, directory, config, rename_mapping):
    """
    Process and rename subtitle files to match their corresponding videos.
    
    Returns:
        Number of successfully renamed files
    """
    renamed_count = 0
    language_suffix = config.get('language_suffix', '')
    
    print("PROCESSING SUBTITLES:")
    print("-" * 40)
    
    for subtitle in sorted(subtitle_files):
        ep = pattern_engine.get_episode_number_cached(subtitle)
        
        # Standardize episode format to match video files
        adjusted_episode_string = ep
        if ep:
            season, episode = pattern_engine.extract_season_episode_numbers(ep)
            if season and episode:
                key = (int(season), int(episode))
                if key in video_episodes:
                    video_pattern = video_episodes[key]
                    if video_pattern != ep:
                        print(f"'{subtitle}' -> {ep} adjusted to {video_pattern} (context-aware)")
                    adjusted_episode_string = video_pattern

        # Find corresponding video and rename
        target_video = None
        if adjusted_episode_string and adjusted_episode_string in temp_video_dict:
            target_video = temp_video_dict[adjusted_episode_string]
        elif ep and ep in temp_video_dict:
            target_video = temp_video_dict[ep]
            adjusted_episode_string = ep

        if target_video:
            base_name = os.path.splitext(target_video)[0]
            subtitle_ext = os.path.splitext(subtitle)[1]
            
            new_name, new_path = generate_unique_name(base_name, subtitle_ext, subtitle, directory, language_suffix)
            
            if "_" in new_name and language_suffix in new_name:
                print(f"CONFLICT RESOLVED: Multiple subtitles match '{target_video}' -> renamed '{subtitle}' to unique name '{new_name}'")
            else:
                print(f"RENAMED: '{subtitle}' -> '{new_name}'")
            
            old_path = os.path.join(directory, subtitle)
            os.rename(old_path, new_path)
            rename_mapping[subtitle] = new_name
            renamed_count += 1
        elif ep:
            print(f"NO MATCH: '{subtitle}' -> episode {ep} has no matching video")
            rename_mapping[subtitle] = None
        else:
            print(f"NO EPISODE: '{subtitle}' -> could not detect episode number")
            rename_mapping[subtitle] = None
    
    return renamed_count


def analyze_results(files, video_files, subtitle_files, video_episodes, temp_video_dict):
    """
    Analyze matching results and categorize files for summary report.
    
    Returns:
        Tuple of (found_matches set, not_found_episodes set, unidentified_files list)
    """
    found_matches = set()
    not_found_episodes = set()
    unidentified_files = []
    
    # Build map of which episodes have matching subtitles
    subtitle_episodes = {}
    for subtitle in subtitle_files:
        ep = pattern_engine.get_episode_number_cached(subtitle)
        if ep:
            season, episode = pattern_engine.extract_season_episode_numbers(ep)
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
    
    # Identify videos without corresponding subtitles
    for video in video_files:
        ep = pattern_engine.get_episode_number_cached(video)
        if ep:
            season, episode = pattern_engine.extract_season_episode_numbers(ep)
            if season and episode:
                key = (int(season), int(episode))
                if key not in subtitle_episodes:
                    not_found_episodes.add(video_episodes.get(key, ep))
    
    # Collect files where episode pattern detection failed
    video_exts = tuple(f'.{ext}' for ext in CONFIG['video_extensions'])
    subtitle_exts = tuple(f'.{ext}' for ext in CONFIG['subtitle_extensions'])
    for filename in files:
        if filename.lower().endswith(video_exts + subtitle_exts):
            if not pattern_engine.get_episode_number_cached(filename):
                unidentified_files.append(filename)
    
    return found_matches, not_found_episodes, unidentified_files


def rename_subtitles_to_match_videos(config):
    """Main renaming logic."""
    directory = os.getcwd()
    files = os.listdir(directory)
    
    # Separate video and subtitle files by extension
    video_exts = tuple(f'.{ext}' for ext in config['video_extensions'])
    subtitle_exts = tuple(f'.{ext}' for ext in config['subtitle_extensions'])
    video_files = [f for f in files if f.lower().endswith(video_exts)]
    subtitle_files = [f for f in files if f.lower().endswith(subtitle_exts)]
    
    # Store original lists for reporting
    original_video_files = video_files.copy()
    original_subtitle_files = subtitle_files.copy()
    rename_mapping = {}

    print(f"\nFILES FOUND: {len(video_files)} videos | {len(subtitle_files)} subtitles")
    print("=" * 60)
    
    if video_files:
        print(f"Videos: {video_files[:4]}{'...' if len(video_files) > 4 else ''}")
    if subtitle_files:
        print(f"Subtitles: {subtitle_files[:4]}{'...' if len(subtitle_files) > 4 else ''}")
    print()

    # Build episode reference mappings
    video_episodes, temp_video_dict = build_episode_context(video_files)
    
    if video_episodes:
        print("PROCESSING VIDEOS:")
        print("-" * 40)
        print(f"EPISODE PATTERNS DETECTED: {list(video_episodes.values())[:10]}{'...' if len(video_episodes) > 10 else ''}")
    print()

    # Rename subtitle files to match videos
    renamed_count = process_subtitles(subtitle_files, video_episodes, temp_video_dict, directory, config, rename_mapping)
    
    print("-" * 40)
    print()
    
    # Try movie matching mode if no episodes found
    remaining_video_files = [v for v in video_files if not pattern_engine.get_episode_number_cached(v)]
    remaining_subtitle_files = [s for s in subtitle_files if not pattern_engine.get_episode_number_cached(s)]
    movie_mode_detected = False
    
    if renamed_count == 0 and len(remaining_video_files) == 1 and len(remaining_subtitle_files) == 1:
        movie_match = find_movie_subtitle_match(remaining_video_files, remaining_subtitle_files)
        if movie_match:
            video_file, subtitle_file = movie_match
            base_name = os.path.splitext(video_file)[0]
            subtitle_ext = os.path.splitext(subtitle_file)[1]
            new_name = build_subtitle_filename(base_name, subtitle_ext, config.get('language_suffix'))
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
    
    # Display detailed analysis
    print("\nANALYSIS SUMMARY:")
    print("=" * 60)
    
    found_matches, not_found_episodes, unidentified_files = analyze_results(
        files, video_files, subtitle_files, video_episodes, temp_video_dict
    )
    
    if found_matches:
        print("FOUND AND RENAMED MATCHING FILES FOR THESE EPISODES:")
        for episode in sorted(found_matches):
            print(f"- {episode}")
        print()

    if not_found_episodes:
        print("COULDN'T FIND MATCHING FILES FOR THESE EPISODES:")
        for episode in sorted(not_found_episodes):
            if episode != "(None)":
                print(f"- {episode}")
        print()

    if unidentified_files:
        print("COULDN'T IDENTIFY EPISODE PATTERN FOR THESE FILES:")
        for filename in sorted(unidentified_files):
            print(f"- {filename}")
        print()
    
    return renamed_count, movie_mode_detected, original_video_files, original_subtitle_files, rename_mapping


def main():
    """Main entry point."""
    print("\n" + "=" * 60)
    print("SubFast v3.1.0 - Subtitle Renaming")
    print("=" * 60 + "\n")
    
    # Load configuration
    config = config_loader.load_config()
    global CONFIG
    CONFIG = config
    
    # Track execution time
    start_time = time.time()
    
    # Execute renaming
    renamed_count, movie_mode, original_videos, original_subtitles, rename_map = rename_subtitles_to_match_videos(config)
    
    # Calculate execution time
    elapsed_time = time.time() - start_time
    time_str = csv_reporter.format_execution_time(elapsed_time)
    
    # Prepare results for CSV export and summary
    results = []
    for subtitle in original_subtitles:
        result = {
            'original_name': subtitle,
            'new_name': rename_map.get(subtitle),
            'status': 'renamed' if rename_map.get(subtitle) else 'no_match',
            'episode': pattern_engine.get_episode_number_cached(subtitle) or 'N/A'
        }
        results.append(result)
    
    # Display summary
    total_files = len(original_videos) + len(original_subtitles)
    csv_reporter.print_summary(results, 'Renaming', time_str, renamed_count, len(original_subtitles), total_files)
    
    # Export CSV report if enabled
    if config.get('renaming_report', False):
        csv_path = Path.cwd() / 'renaming_report.csv'
        csv_reporter.generate_csv_report(results, csv_path, 'renaming')
    
    # Smart console behavior
    keep_console_open = config.get('keep_console_open', False)
    if keep_console_open:
        input("\nPress Enter to close this window...")
    
    sys.exit(0)


if __name__ == "__main__":
    main()
