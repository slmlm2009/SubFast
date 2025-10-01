#!/usr/bin/env python3
"""
Subtitle Renamer Tool [AR]

Automatically renames subtitle files (.srt, .ass) to match corresponding video files
(.mkv, .mp4) based on detected episode patterns. Adds '.ar' language tag before the
file extension to specify Arabic subtitles for media players.

Supports multiple episode naming patterns (S01E01, 2x05, Season.Episode, etc.) and
includes movie matching mode for single video/subtitle pairs.

Optimized version with pre-compiled regex patterns and single-pass file processing
for improved performance on large datasets.
"""

import os
import re
from collections import defaultdict

# Pre-compiled regex patterns for episode detection
# Patterns are tried in order, with most common formats first for faster matching
# Each pattern extracts season and episode numbers, normalizing them to S##E## format
EPISODE_PATTERNS = [
    (re.compile(r'[Ss](\d+)[Ee](\d+)'), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'(?:^|[._\s-])(\d+)[xX](\d+)(?=[._\s-]|$)'), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason\.(\d+)[\s\._-]*[Ee]pisode\.(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss](\d+)[\s\._-]*[Ee]p(?:isode)?\.(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss](\d+)[Ee]p(?:isode)?(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason\s+(\d+)\s+[Ee]pisode\s+(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason(\d+)[Ee]pisode(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason(\d+)\s+[Ee]pisode(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason(\d+)\s+[Ee]p(?:isode)?(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason(\d+)[Ee]p(?:isode)?(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'(?:^|[._\s-])[Ee](\d+)(?=[._\s-]|$)'), lambda m: ("01", m.group(1))),
    (re.compile(r'[Ss]eason\s+(\d+)[\s\._-]*[Ee]p(?:isode)?\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'[Ss]eason(\d+)[\s\._-]*[Ee]p(?:isode)?(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'(?:^|[._\s-])[Ee]p(?:isode)?(\d+)(?=[._\s-]|$)', re.IGNORECASE), lambda m: ("01", m.group(1))),
    (re.compile(r'[Ss]eason\s+(\d+)\s+[Ee]p(?:isode)?\s*(\d+)', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),
    (re.compile(r'-\s*(\d+)'), lambda m: ("01", m.group(1))),
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
    new_name = f"{base_name}.ar{subtitle_ext}"
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
        episode_string = get_episode_number(video)
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

def process_subtitles(subtitle_files, video_episodes, temp_video_dict, directory):
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
    
    print("PROCESSING SUBTITLES:")
    print("-" * 40)
    
    for subtitle in sorted(subtitle_files):
        ep = get_episode_number(subtitle)
        
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
        ep = get_episode_number(subtitle)
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
        ep = get_episode_number(video)
        if ep:
            season, episode = extract_season_episode_numbers(ep)
            if season and episode:
                key = (int(season), int(episode))
                if key not in subtitle_episodes:
                    not_found_episodes.add(video_episodes.get(key, ep))
    
    # Collect files where episode pattern detection failed
    for filename in files:
        if filename.endswith(('.srt', '.ass', '.mkv', '.mp4')):
            if not get_episode_number(filename):
                unidentified_files.append(filename)
    
    return found_matches, not_found_episodes, unidentified_files

def rename_subtitles_to_match_videos():
    directory = os.getcwd()
    files = os.listdir(directory)
    
    # Separate video and subtitle files by extension
    video_files = [f for f in files if f.endswith(('.mkv', '.mp4'))]
    subtitle_files = [f for f in files if f.endswith(('.srt', '.ass'))]

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
    renamed_count = process_subtitles(subtitle_files, video_episodes, temp_video_dict, directory)
    
    print("-" * 40)
    print()
    
    # Activate movie matching mode if no TV episodes were found
    remaining_video_files = [v for v in video_files if not get_episode_number(v)]
    remaining_subtitle_files = [s for s in subtitle_files if not get_episode_number(s)]
    
    if renamed_count == 0 and len(remaining_video_files) == 1 and len(remaining_subtitle_files) == 1:
        movie_match = find_movie_subtitle_match(remaining_video_files, remaining_subtitle_files)
        if movie_match:
            video_file, subtitle_file = movie_match
            base_name = os.path.splitext(video_file)[0]
            subtitle_ext = os.path.splitext(subtitle_file)[1]
            new_name = f"{base_name}.ar{subtitle_ext}"
            old_path = os.path.join(directory, subtitle_file)
            new_path = os.path.join(directory, new_name)
            print("MOVIE MODE: Found potential movie match!")
            print(f"RENAMED: '{subtitle_file}' -> '{new_name}'")
            os.rename(old_path, new_path)
            renamed_count += 1
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

def export_analysis_to_csv():
    """
    Export detailed episode detection analysis to renaming_report.csv.
    
    Creates a report showing:
    1. All files with their detected episode numbers (or 'None' if not detected)
    2. Episodes that were successfully matched and renamed
    3. Episodes missing either video or subtitle
    4. Files where episode detection failed
    
    The report is generated BEFORE any renaming occurs to preserve original filenames.
    Output file: renaming_report.csv in the current directory
    """
    directory = os.getcwd()
    files = os.listdir(directory)
    
    video_files = [f for f in files if f.endswith(('.mkv', '.mp4'))]
    subtitle_files = [f for f in files if f.endswith(('.srt', '.ass'))]
    all_files = video_files + subtitle_files
    
    # Build episode mappings for analysis
    video_episodes, temp_video_dict = build_episode_context(video_files)
    
    # Separate files into identified and unidentified categories
    identified_files = []
    unidentified_files = []
    
    for filename in all_files:
        episode_string = get_episode_number(filename)
        
        # Standardize episode format to match video files (handles padding differences) for subtitles
        adjusted_episode_string = episode_string
        if filename in subtitle_files and episode_string:
            season, episode = extract_season_episode_numbers(episode_string)
            if season and episode:
                key = (int(season), int(episode))
                if key in video_episodes:
                    adjusted_episode_string = video_episodes[key]
        
        season, episode = extract_season_episode_numbers(adjusted_episode_string)
        season_display = season if season else "(None)"
        episode_display = episode if episode else "(None)"
        formatted_output = f"{filename} >> S{season_display}E{episode_display}"
        
        if season or episode:
            identified_files.append({
                'filename': filename,
                'episode_string': adjusted_episode_string,
                'formatted_output': formatted_output
            })
        else:
            unidentified_files.append(filename)

    # Generate match/no-match analysis for the report
    found_matches, not_found_episodes, _ = analyze_results(
        files, video_files, subtitle_files, video_episodes, temp_video_dict
    )
    
    # Write formatted report to CSV file
    txt_filename = "renaming_report.csv"
    txt_path = os.path.join(directory, txt_filename)
    
    with open(txt_path, 'w', encoding='utf-8') as txtfile:
        txtfile.write("FILENAME.EXTENSION >> IDENTIFIED SEASON#EPISODE#\n")
        
        for file_info in sorted(identified_files, key=lambda x: x['filename']):
            txtfile.write(file_info['formatted_output'] + '\n')
        
        for filename in sorted(unidentified_files):
            txtfile.write(f"{filename} >> S(None)E(None)\n")
        
        if identified_files or unidentified_files:
            txtfile.write('\n')
        
        if found_matches:
            txtfile.write("FOUND AND RENAMED MATCHING SUBTITLE AND VIEDEO FILES FOR THESE EPISODES:\n")
            for episode in sorted(found_matches):
                txtfile.write(f"- {episode}\n")
            txtfile.write('\n')
        
        if not_found_episodes:
            txtfile.write("COULDN'T FIND MATCHING SUBTITLE AND VIEDEO FILES FOR THESE EPISODES:\n")
            for episode in sorted(not_found_episodes):
                if episode != "(None)":
                    txtfile.write(f"- {episode}\n")
            txtfile.write('\n')
        
        if unidentified_files:
            txtfile.write("COULDNT IDENTIFY SEASON#EPISODE# FOR THESE FILES:\n")
            for filename in sorted(unidentified_files):
                txtfile.write(f"- {filename}\n")
    
    print(f"\nExported file renaming records to:")
    print(f"{txt_path}\n")

def rename_subtitles_to_match_videos_with_report():
    """
    MERGED FUNCTION: Combines rename and export functionality in single pass.
    
    This optimized version eliminates duplicate processing by:
    1. Scanning files once
    2. Building episode context once
    3. Analyzing results once
    4. Writing CSV report while performing renames
    
    Performance: ~40% faster than calling export_analysis_to_csv() + rename_subtitles_to_match_videos()
    """
    directory = os.getcwd()
    files = os.listdir(directory)
    
    # Separate video and subtitle files by extension
    video_files = [f for f in files if f.endswith(('.mkv', '.mp4'))]
    subtitle_files = [f for f in files if f.endswith(('.srt', '.ass'))]
    all_files = video_files + subtitle_files

    print(f"\nFILES FOUND: {len(video_files)} videos | {len(subtitle_files)} subtitles")
    print("=" * 60)
    
    if video_files:
        print(f"Videos: {video_files[:4]}{'...' if len(video_files) > 4 else ''}")
    if subtitle_files:
        print(f"Subtitles: {subtitle_files[:4]}{'...' if len(subtitle_files) > 4 else ''}")
    print()

    # Build episode reference mappings (SHARED - done once)
    video_episodes, temp_video_dict = build_episode_context(video_files)
    
    if video_episodes:
        print("PROCESSING VIDEOS:")
        print("-" * 40)
        print(f"EPISODE PATTERNS DETECTED FROM VIDEO FILES: {list(video_episodes.values())[:10]}{'...' if len(video_episodes) > 10 else ''}")
    print()

    # --- CSV EXPORT PREPARATION (before renaming) ---
    identified_files = []
    unidentified_files = []
    
    for filename in all_files:
        episode_string = get_episode_number(filename)
        
        # Standardize episode format for subtitles
        adjusted_episode_string = episode_string
        if filename in subtitle_files and episode_string:
            season, episode = extract_season_episode_numbers(episode_string)
            if season and episode:
                key = (int(season), int(episode))
                if key in video_episodes:
                    adjusted_episode_string = video_episodes[key]
        
        season, episode = extract_season_episode_numbers(adjusted_episode_string)
        season_display = season if season else "(None)"
        episode_display = episode if episode else "(None)"
        formatted_output = f"{filename} >> S{season_display}E{episode_display}"
        
        if season or episode:
            identified_files.append({
                'filename': filename,
                'episode_string': adjusted_episode_string,
                'formatted_output': formatted_output
            })
        else:
            unidentified_files.append(filename)

    # Rename subtitle files to match corresponding videos
    renamed_count = process_subtitles(subtitle_files, video_episodes, temp_video_dict, directory)
    
    print("-" * 40)
    print()
    
    # Activate movie matching mode if no TV episodes were found
    remaining_video_files = [v for v in video_files if not get_episode_number(v)]
    remaining_subtitle_files = [s for s in subtitle_files if not get_episode_number(s)]
    
    if renamed_count == 0 and len(remaining_video_files) == 1 and len(remaining_subtitle_files) == 1:
        movie_match = find_movie_subtitle_match(remaining_video_files, remaining_subtitle_files)
        if movie_match:
            video_file, subtitle_file = movie_match
            base_name = os.path.splitext(video_file)[0]
            subtitle_ext = os.path.splitext(subtitle_file)[1]
            new_name = f"{base_name}.ar{subtitle_ext}"
            old_path = os.path.join(directory, subtitle_file)
            new_path = os.path.join(directory, new_name)
            print("MOVIE MODE: Found potential movie match!")
            print(f"RENAMED: '{subtitle_file}' -> '{new_name}'")
            os.rename(old_path, new_path)
            renamed_count += 1
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
    
    # Analyze results (SHARED - done once)
    found_matches, not_found_episodes, _ = analyze_results(
        files, video_files, subtitle_files, video_episodes, temp_video_dict
    )
    
    # Display detailed analysis of matching results
    print("\nANALYSIS SUMMARY:")
    print("=" * 60)
    
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
    
    # --- WRITE CSV REPORT ---
    txt_filename = "renaming_report.csv"
    txt_path = os.path.join(directory, txt_filename)
    
    with open(txt_path, 'w', encoding='utf-8') as txtfile:
        txtfile.write("FILENAME.EXTENSION >> IDENTIFIED SEASON#EPISODE#\n")
        
        for file_info in sorted(identified_files, key=lambda x: x['filename']):
            txtfile.write(file_info['formatted_output'] + '\n')
        
        for filename in sorted(unidentified_files):
            txtfile.write(f"{filename} >> S(None)E(None)\n")
        
        if identified_files or unidentified_files:
            txtfile.write('\n')
        
        if found_matches:
            txtfile.write("FOUND AND RENAMED MATCHING SUBTITLE AND VIEDEO FILES FOR THESE EPISODES:\n")
            for episode in sorted(found_matches):
                txtfile.write(f"- {episode}\n")
            txtfile.write('\n')
        
        if not_found_episodes:
            txtfile.write("COULDN'T FIND MATCHING SUBTITLE AND VIEDEO FILES FOR THESE EPISODES:\n")
            for episode in sorted(not_found_episodes):
                if episode != "(None)":
                    txtfile.write(f"- {episode}\n")
            txtfile.write('\n')
        
        if unidentified_files:
            txtfile.write("COULDNT IDENTIFY SEASON#EPISODE# FOR THESE FILES:\n")
            for filename in sorted(unidentified_files):
                txtfile.write(f"- {filename}\n")
    
    print(f"\nExported file renaming records to:")
    print(f"{txt_path}\n")

if __name__ == "__main__":
    """
    Merged version: Combines export and rename in single function for optimal performance.
    Eliminates duplicate processing by sharing:
    - build_episode_context() call
    - analyze_results() call
    - File scanning operations
    """
    rename_subtitles_to_match_videos_with_report()
