"""
CSV Reporter Module

Handles CSV export functionality for renaming and embedding operations.
Provides consistent reporting format across both modules with enhanced text table output.

Version: 3.1.0
"""

import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional


def generate_csv_report(
    results: List[Dict[str, Any]],
    output_path: Path,
    operation_type: str = 'renaming',
    # Enhanced parameters for rich reporting
    original_videos: Optional[List[str]] = None,
    video_episodes: Optional[Dict] = None,
    temp_video_dict: Optional[Dict] = None,
    config: Optional[Dict] = None,
    execution_time_str: Optional[str] = None,
    renamed_count: Optional[int] = None,
    movie_mode: bool = False,
    # Embedding-specific parameters
    all_videos: Optional[List[str]] = None,
    all_subtitles: Optional[List[str]] = None,
    elapsed_seconds: Optional[float] = None
) -> None:
    """
    Generate comprehensive report for SubFast operations.
    
    Args:
        results: List of operation result dictionaries
        output_path: Path where CSV file should be written
        operation_type: Either 'renaming' or 'embedding'
        original_videos: List of original video filenames (for enhanced reports)
        video_episodes: Episode mapping dictionary (for matched episodes section)
        temp_video_dict: Video lookup dictionary (for matched episodes section)
        config: Configuration dictionary (for header details)
        execution_time_str: Formatted execution time string
        renamed_count: Number of files renamed/embedded
        movie_mode: Whether movie mode was activated
    """
    if not results:
        print("[INFO] No results to export")
        return
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            if operation_type == 'renaming':
                _write_renaming_report(
                    f, results, output_path,
                    original_videos, video_episodes, temp_video_dict,
                    config, execution_time_str, renamed_count, movie_mode
                )
            elif operation_type == 'embedding':
                _write_embedding_report(
                    f, results, output_path, config,
                    execution_time_str, elapsed_seconds,
                    all_videos, all_subtitles
                )
            else:
                raise ValueError(f"Unknown operation type: {operation_type}")
        
        print(f"\n[INFO] CSV report exported: {output_path}")
    
    except Exception as e:
        print(f"[WARNING] Failed to generate CSV report: {e}")


def format_text_table(file_rows: List[Dict[str, str]]) -> str:
    """
    Format file data as bordered text table.
    
    Args:
        file_rows: List of dicts with keys: filename, detected_episode, action, new_name
        
    Returns:
        Formatted text table string with borders
    """
    if not file_rows:
        return ""
    
    # Calculate column widths
    col1_width = max(len(row['filename']) for row in file_rows)
    col1_width = max(col1_width, len('Original Filename'))
    col1_width = min(col1_width + 2, 82)  # Cap at 82 for padding
    
    col2_width = max(18, len('Detected Episode') + 2)
    col3_width = max(10, len('Action') + 2)
    
    col4_width = max(len(row['new_name']) for row in file_rows)
    col4_width = max(col4_width, len('New Name'))
    col4_width = min(col4_width + 2, 82)  # Cap at 82 for padding
    
    # Create border line
    border = f"+{'-' * col1_width}+{'-' * col2_width}+{'-' * col3_width}+{'-' * col4_width}+"
    
    # Build table
    lines = []
    lines.append(border)
    
    # Header row
    header = (
        f"| {'Original Filename'.ljust(col1_width - 2)} "
        f"| {'Detected Episode'.ljust(col2_width - 2)} "
        f"| {'Action'.ljust(col3_width - 2)} "
        f"| {'New Name'.ljust(col4_width - 2)} |"
    )
    lines.append(header)
    lines.append(border)
    
    # Data rows
    for row in file_rows:
        filename = row['filename'][:col1_width - 2].ljust(col1_width - 2)
        episode = row['detected_episode'].ljust(col2_width - 2)
        action = row['action'].ljust(col3_width - 2)
        new_name = row['new_name'][:col4_width - 2].ljust(col4_width - 2)
        
        lines.append(f"| {filename} | {episode} | {action} | {new_name} |")
    
    lines.append(border)
    
    return '\n'.join(lines)


def _write_renaming_report(
    file_handle,
    results: List[Dict[str, Any]],
    output_path: Path,
    original_videos: Optional[List[str]] = None,
    video_episodes: Optional[Dict] = None,
    temp_video_dict: Optional[Dict] = None,
    config: Optional[Dict] = None,
    execution_time_str: Optional[str] = None,
    renamed_count: Optional[int] = None,
    movie_mode: bool = False
) -> None:
    """Write comprehensive renaming report with text table format."""
    
    # SubFast ASCII Banner
    banner = r"""# ==========================================
#    ____        _     _____          _   
#   / ___| _   _| |__ |  ___|_ _  ___| |_ 
#   \___ \| | | | '_ \| |_ / _` |/ __| __|
#    ___) | |_| | |_) |  _| (_| |\__ \ |_ 
#   |____/ \__,_|_.__/|_|  \__,_||___/\__|
#                                         
#    Fast subtitle renaming and embedding
# 
# ==========================================
#
"""
    file_handle.write(banner)
    
    # Report header
    file_handle.write("# Subtitle Renaming Report\n")
    file_handle.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    file_handle.write(f"# Directory: {output_path.parent}\n")
    
    # Configuration summary
    if config:
        lang_suffix = config.get('language_suffix', 'ar') if config.get('language_suffix') else '(none)'
        video_exts = '|'.join(config.get('video_extensions', ['mkv', 'mp4']))
        subtitle_exts = '|'.join(config.get('subtitle_extensions', ['srt', 'ass']))
        file_handle.write(f"# Configuration: language={lang_suffix}, videos={video_exts}, subtitles={subtitle_exts}\n")
    
    file_handle.write("#\n")
    
    # Import pattern_engine for accurate calculations
    from . import pattern_engine
    
    # Calculate accurate statistics
    file_handle.write("# SUMMARY:\n")
    total_videos = len(original_videos) if original_videos else 0
    total_subtitles = len(results)
    renamed = renamed_count if renamed_count is not None else sum(1 for r in results if r.get('status') == 'renamed')
    
    # Videos Missing Subtitles - ACCURATE
    # = Videos with identifiable episode BUT no matching renamed subtitle
    videos_with_episodes = {}  # episode -> video_filename
    for video in original_videos or []:
        episode = pattern_engine.get_episode_number_cached(video)
        if episode:  # Has identifiable episode
            videos_with_episodes[episode] = video
    
    renamed_episodes = set()  # Episodes that have renamed subtitles
    for result in results:
        if result.get('status') == 'renamed':
            episode = result.get('episode')
            if episode and episode != 'N/A':
                renamed_episodes.add(episode)
    
    videos_missing_subtitles = len(set(videos_with_episodes.keys()) - renamed_episodes)
    
    # Subtitles Missing Videos - ACCURATE
    # = Subtitles with identifiable episode BUT no matching video
    subtitles_with_episodes = {}  # episode -> subtitle_filename
    for result in results:
        episode = result.get('episode')
        if episode and episode != 'N/A':
            subtitles_with_episodes[episode] = result.get('original_name')
    
    video_episodes_set = set(videos_with_episodes.keys())
    subtitle_episodes_set = set(subtitles_with_episodes.keys())
    
    subs_without_videos = len(subtitle_episodes_set - video_episodes_set)
    
    # Videos Without Episode Pattern - ACCURATE
    videos_without_pattern = 0
    for video in original_videos or []:
        if not pattern_engine.get_episode_number_cached(video):
            videos_without_pattern += 1
    
    # Subtitles Without Episode Pattern - ACCURATE
    subs_without_pattern = sum(1 for r in results if r.get('episode') == 'N/A')
    
    file_handle.write(f"# Total Videos: {total_videos}\n")
    file_handle.write(f"# Total Subtitles: {total_subtitles}\n")
    file_handle.write(f"# Renamed: {renamed}/{total_subtitles} subtitles\n")
    file_handle.write(f"# Videos Missing Subtitles: {videos_missing_subtitles}\n")
    file_handle.write(f"# Subtitles Missing Videos: {subs_without_videos}\n")
    file_handle.write(f"# Videos Without Episode Pattern: {videos_without_pattern}\n")
    file_handle.write(f"# Subtitles Without Episode Pattern: {subs_without_pattern}\n")
    file_handle.write(f"# Movie Mode: {'Yes' if movie_mode else 'No'}\n")
    file_handle.write(f"# Execution Time: {execution_time_str or 'N/A'}\n")
    file_handle.write("#\n")
    
    # Build file rows for text table
    file_rows = []
    
    # Add video files first with enhanced Action logic
    if original_videos:
        for video in sorted(original_videos):
            episode = pattern_engine.get_episode_number_cached(video) or 'N/A'
            display_episode = episode if episode != 'N/A' else '(UNIDENTIFIED)'
            
            # Determine action for video
            if movie_mode and episode == 'N/A':
                # Movie mode handling
                action = 'MATCHED' if renamed > 0 else 'NO MATCH'
                display_episode = 'Movie'
            elif episode == 'N/A':
                # Unidentified episode - can't match
                action = '--'
            elif episode in renamed_episodes:
                # Has matching renamed subtitle
                action = 'MATCHED'
            else:
                # Has episode but no matching subtitle
                action = 'NO MATCH'
            
            file_rows.append({
                'filename': video,
                'detected_episode': display_episode,
                'action': action,
                'new_name': 'No Change'
            })
    
    # Add subtitle files with enhanced Action logic
    for result in sorted(results, key=lambda x: x.get('original_name', '')):
        original = result.get('original_name', '')
        new_name = result.get('new_name', '')
        status = result.get('status', 'no_match')
        episode = result.get('episode', 'N/A')
        
        # Determine action for subtitle
        if status == 'renamed' and new_name:
            action = 'RENAMED'
        elif episode == 'N/A':
            # Unidentified - can't match
            action = '--'
        else:
            # Has episode but no video match
            action = 'NO MATCH'
        
        display_new_name = new_name if new_name else 'No Change'
        display_episode = episode if episode != 'N/A' else '(UNIDENTIFIED)'
        
        if movie_mode and new_name:
            display_episode = 'Movie'
        
        file_rows.append({
            'filename': original,
            'detected_episode': display_episode,
            'action': action,
            'new_name': display_new_name
        })
    
    # Write text table
    table = format_text_table(file_rows)
    file_handle.write(table + '\n')
    file_handle.write("#\n")
    
    # Matched episodes section
    if temp_video_dict and video_episodes:
        file_handle.write("# MATCHED EPISODES:\n")
        
        # Build list of matched episodes
        matched_episodes = []
        for result in results:
            if result.get('status') == 'renamed' and result.get('new_name'):
                episode = result.get('episode', '')
                if episode and episode != 'N/A' and episode in temp_video_dict:
                    video_file = temp_video_dict[episode]
                    subtitle_file = result.get('original_name', '')
                    new_name = result.get('new_name', '')
                    matched_episodes.append((episode, video_file, subtitle_file, new_name))
        
        # Write matched episodes
        for episode, video, subtitle, new_name in sorted(matched_episodes):
            file_handle.write(f"# {episode} -> Video: {video} | Subtitle: {subtitle} -> {new_name}\n")
        
        file_handle.write("#\n")
    
    # Missing matches section
    if temp_video_dict or video_episodes:
        # Episodes with videos but no subtitles
        videos_without_subs_list = sorted(video_episodes_set - subtitle_episodes_set)
        # Episodes with subtitles but no videos
        subs_without_videos_list = sorted(subtitle_episodes_set - video_episodes_set)
        
        if videos_without_subs_list or subs_without_videos_list:
            file_handle.write("# MISSING MATCHES:\n")
            
            # Videos without subtitles
            for episode in videos_without_subs_list:
                video_file = videos_with_episodes.get(episode, 'Unknown')
                file_handle.write(f"# {episode} -> Has Video: {video_file} | Missing: Subtitle\n")
            
            # Subtitles without videos
            for episode in subs_without_videos_list:
                subtitle_file = subtitles_with_episodes.get(episode, 'Unknown')
                file_handle.write(f"# {episode} -> Has Subtitle: {subtitle_file} | Missing: Video\n")
            
            file_handle.write("#\n")
    
    # Files without episode pattern section
    unidentified_files = [
        row['filename'] 
        for row in file_rows 
        if row['detected_episode'] == '(UNIDENTIFIED)'
    ]
    
    if unidentified_files:
        file_handle.write("# FILES WITHOUT EPISODE PATTERN:\n")
        for filename in sorted(unidentified_files):
            file_handle.write(f"# {filename} (no episode pattern detected)\n")
        file_handle.write("#\n")


def calculate_embedding_statistics(
    results: List[Dict[str, Any]],
    all_videos: List[str],
    all_subtitles: List[str]
) -> Dict[str, Any]:
    """
    Calculate comprehensive embedding statistics.
    
    Args:
        results: List of embedding results
        all_videos: List of all video filenames found
        all_subtitles: List of all subtitle filenames found
        
    Returns:
        Dictionary with statistics
    """
    total_videos = len(all_videos)
    total_subtitles = len(all_subtitles)
    
    # Pairs matched = results with a video (success or failed)
    pairs_matched = sum(1 for r in results if r.get('video') and r.get('status') in ('success', 'failed'))
    
    successfully_embedded = sum(1 for r in results if r.get('status') == 'success')
    failed = sum(1 for r in results if r.get('status') == 'failed')
    
    # Videos without subtitles = videos not in successful/failed results
    matched_videos = {r.get('video') for r in results if r.get('video') and r.get('status') in ('success', 'failed')}
    videos_without_subtitles = total_videos - len(matched_videos)
    
    # Subtitles without videos = results with status 'no_match'
    subtitles_without_videos = sum(1 for r in results if r.get('status') == 'no_match')
    
    # Success rate based on pairs matched
    success_rate = (successfully_embedded / pairs_matched * 100) if pairs_matched > 0 else 0
    
    return {
        'total_videos': total_videos,
        'total_subtitles': total_subtitles,
        'pairs_matched': pairs_matched,
        'successfully_embedded': successfully_embedded,
        'failed': failed,
        'videos_without_subtitles': videos_without_subtitles,
        'subtitles_without_videos': subtitles_without_videos,
        'success_rate': success_rate
    }


def format_embedding_text_table(
    results: List[Dict[str, Any]],
    all_videos: List[str],
    all_subtitles: List[str]
) -> str:
    """
    Format embedding results as bordered text table.
    
    Args:
        results: List of embedding results
        all_videos: List of all video filenames
        all_subtitles: List of all subtitle filenames
        
    Returns:
        Formatted text table string with borders
    """
    # Build comprehensive row list
    table_rows = []
    
    # Import pattern_engine for episode detection
    from . import pattern_engine
    
    # Track which videos have been matched
    matched_videos = {r.get('video') for r in results if r.get('video') and r.get('status') in ('success', 'failed')}
    
    # Add matched pairs (success and failed)
    for result in results:
        if result.get('status') in ('success', 'failed'):
            video = result.get('video', 'Unknown')
            subtitle = result.get('subtitle', 'Unknown')
            episode = result.get('episode', 'N/A')
            language = result.get('language', 'none')
            status = 'EMBEDDED' if result.get('status') == 'success' else 'FAILED'
            
            table_rows.append({
                'video': video,
                'subtitle': subtitle,
                'episode': episode,
                'language': language,
                'status': status,
                'sort_key': (video, subtitle)
            })
    
    # Add unmatched videos (videos without subtitles)
    unmatched_videos = [v for v in all_videos if v not in matched_videos]
    for video in unmatched_videos:
        episode = pattern_engine.get_episode_number_cached(video) or 'N/A'
        table_rows.append({
            'video': video,
            'subtitle': '(no match)',
            'episode': episode,
            'language': '--',
            'status': 'NO SUBTITLE',
            'sort_key': (video, '')
        })
    
    # Add unmatched subtitles (subtitles without videos)
    for result in results:
        if result.get('status') == 'no_match':
            subtitle = result.get('subtitle', 'Unknown')
            episode = result.get('episode', 'N/A')
            table_rows.append({
                'video': '(no match)',
                'subtitle': subtitle,
                'episode': episode,
                'language': '--',
                'status': 'NO VIDEO',
                'sort_key': ('', subtitle)
            })
    
    if not table_rows:
        return "(No files to display)"
    
    # Sort rows
    table_rows.sort(key=lambda r: r['sort_key'])
    
    # Calculate column widths
    col1_width = max(len(row['video']) for row in table_rows)
    col1_width = max(col1_width, len('Video File'))
    col1_width = min(col1_width + 2, 82)
    
    col2_width = max(len(row['subtitle']) for row in table_rows)
    col2_width = max(col2_width, len('Subtitle File'))
    col2_width = min(col2_width + 2, 82)
    
    col3_width = max(len(row['episode']) for row in table_rows)
    col3_width = max(col3_width, len('Episode'))
    col3_width = max(col3_width + 2, 10)
    
    col4_width = max(len(row['language']) for row in table_rows)
    col4_width = max(col4_width, len('Language'))
    col4_width = max(col4_width + 2, 10)
    
    col5_width = max(len(row['status']) for row in table_rows)
    col5_width = max(col5_width, len('Status'))
    col5_width = max(col5_width + 2, 12)
    
    # Create border line
    border = f"+{'-' * col1_width}+{'-' * col2_width}+{'-' * col3_width}+{'-' * col4_width}+{'-' * col5_width}+"
    
    # Build table
    lines = []
    lines.append(border)
    
    # Header row
    header = (
        f"| {'Video File'.ljust(col1_width - 2)} "
        f"| {'Subtitle File'.ljust(col2_width - 2)} "
        f"| {'Episode'.ljust(col3_width - 2)} "
        f"| {'Language'.ljust(col4_width - 2)} "
        f"| {'Status'.ljust(col5_width - 2)} |"
    )
    lines.append(header)
    lines.append(border)
    
    # Data rows
    for row in table_rows:
        video = row['video'][:col1_width - 2].ljust(col1_width - 2)
        subtitle = row['subtitle'][:col2_width - 2].ljust(col2_width - 2)
        episode = row['episode'].ljust(col3_width - 2)
        language = row['language'].ljust(col4_width - 2)
        status = row['status'].ljust(col5_width - 2)
        
        lines.append(f"| {video} | {subtitle} | {episode} | {language} | {status} |")
    
    lines.append(border)
    
    return '\n'.join(lines)


def _write_embedding_report(
    file_handle,
    results: List[Dict[str, Any]],
    output_path: Path,
    config: Optional[Dict] = None,
    execution_time_str: Optional[str] = None,
    elapsed_seconds: Optional[float] = None,
    all_videos: Optional[List[str]] = None,
    all_subtitles: Optional[List[str]] = None
) -> None:
    """Write comprehensive embedding report with text table format."""
    
    # SubFast ASCII Banner
    banner = r"""# ==========================================
#    ____        _     _____          _   
#   / ___| _   _| |__ |  ___|_ _  ___| |_ 
#   \___ \| | | | '_ \| |_ / _` |/ __| __|
#    ___) | |_| | |_) |  _| (_| |\__ \ |_ 
#   |____/ \__,_|_.__/|_|  \__,_||___/\__|
#                                         
#    Fast subtitle renaming and embedding
# 
# ==========================================
#
"""
    file_handle.write(banner)
    
    # Report header
    file_handle.write("# SubFast Embedding Report\n")
    file_handle.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    file_handle.write(f"# Directory: {output_path.parent}\n")
    file_handle.write("#\n")
    
    # Configuration summary
    if config:
        mkvmerge_path = config.get('mkvmerge_path', '')
        if not mkvmerge_path:
            mkvmerge_display = 'default - bin/mkvmerge.exe'
        else:
            mkvmerge_display = mkvmerge_path
        
        lang_code = config.get('embedding_language_code', 'none')
        if not lang_code:
            lang_code = 'none'
        
        default_flag = 'yes' if config.get('default_flag', True) else 'no'
        
        file_handle.write("# CONFIGURATION:\n")
        file_handle.write(f"# mkvmerge path: {mkvmerge_display}\n")
        file_handle.write(f"# Language code: {lang_code}\n")
        file_handle.write(f"# Default flag: {default_flag}\n")
        file_handle.write(f"# Embedding report: enabled\n")
        file_handle.write("#\n")
    
    # Calculate statistics
    stats = calculate_embedding_statistics(results, all_videos or [], all_subtitles or [])
    
    # Statistics summary
    file_handle.write("# STATISTICS:\n")
    file_handle.write(f"# Total Videos: {stats['total_videos']}\n")
    file_handle.write(f"# Total Subtitles: {stats['total_subtitles']}\n")
    file_handle.write(f"# Pairs Matched: {stats['pairs_matched']}\n")
    file_handle.write(f"# Successfully Embedded: {stats['successfully_embedded']}\n")
    file_handle.write(f"# Failed: {stats['failed']}\n")
    file_handle.write(f"# Videos Without Subtitles: {stats['videos_without_subtitles']}\n")
    file_handle.write(f"# Subtitles Without Videos: {stats['subtitles_without_videos']}\n")
    file_handle.write(f"# Success Rate: {stats['success_rate']:.1f}%\n")
    
    if execution_time_str:
        file_handle.write(f"# Total Execution Time: {execution_time_str}\n")
        if elapsed_seconds and stats['pairs_matched'] > 0:
            avg_per_file = elapsed_seconds / stats['pairs_matched']
            avg_str = format_execution_time(avg_per_file)
            file_handle.write(f"# Average Time Per File: {avg_str}\n")
    
    file_handle.write("#\n")
    
    # Generate text table
    table = format_embedding_text_table(results, all_videos or [], all_subtitles or [])
    file_handle.write(table + '\n')
    file_handle.write("#\n")
    
    # Successfully embedded pairs section
    successful_pairs = [r for r in results if r.get('status') == 'success']
    file_handle.write("# SUCCESSFULLY EMBEDDED PAIRS:\n")
    if successful_pairs:
        for result in sorted(successful_pairs, key=lambda r: r.get('episode', 'ZZZ')):
            episode = result.get('episode', 'N/A')
            video = result.get('video', 'Unknown')
            subtitle = result.get('subtitle', 'Unknown')
            language = result.get('language', 'none')
            file_handle.write(f"# {episode} -> Video: {video} | Subtitle: {subtitle} | Language: {language}\n")
        file_handle.write(f"# ({len(successful_pairs)} total)\n")
    else:
        file_handle.write("# (None)\n")
    file_handle.write("#\n")
    
    # Failed operations section - only show if there are failures
    failed_ops = [r for r in results if r.get('status') == 'failed']
    if failed_ops:
        file_handle.write("# FAILED OPERATIONS:\n")
        for result in sorted(failed_ops, key=lambda r: r.get('episode', 'ZZZ')):
            episode = result.get('episode', 'N/A')
            video = result.get('video', 'Unknown')
            subtitle = result.get('subtitle', 'Unknown')
            error = result.get('error', 'Unknown error')
            file_handle.write(f"# {episode} -> Video: {video} | Subtitle: {subtitle}\n")
            file_handle.write(f"#   Error: {error}\n")
        file_handle.write(f"# ({len(failed_ops)} total)\n")
        file_handle.write("#\n")
    
    # Unmatched videos section - only show if there are unmatched videos
    if all_videos:
        matched_videos = {r.get('video') for r in results if r.get('video') and r.get('status') in ('success', 'failed')}
        unmatched_videos = [v for v in all_videos if v not in matched_videos]
        
        if unmatched_videos:
            file_handle.write("# VIDEOS WITHOUT MATCHING SUBTITLES:\n")
            # Import pattern_engine to get episode numbers
            from . import pattern_engine
            for video in sorted(unmatched_videos):
                episode = pattern_engine.get_episode_number_cached(video) or 'N/A'
                file_handle.write(f"# {episode} -> {video}\n")
            file_handle.write(f"# ({len(unmatched_videos)} total)\n")
            file_handle.write("#\n")
    
    # Unmatched subtitles section - only show if there are unmatched subtitles
    unmatched_subs = [r for r in results if r.get('status') == 'no_match']
    if unmatched_subs:
        file_handle.write("# SUBTITLES WITHOUT MATCHING VIDEOS:\n")
        for result in sorted(unmatched_subs, key=lambda r: r.get('episode', 'ZZZ')):
            episode = result.get('episode', 'N/A')
            subtitle = result.get('subtitle', 'Unknown')
            file_handle.write(f"# {episode} -> {subtitle}\n")
        file_handle.write(f"# ({len(unmatched_subs)} total)\n")
        file_handle.write("#\n")


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
    total_files: int = None,
    elapsed_seconds: float = None
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
        elapsed_seconds: Raw elapsed time in seconds (for average calculation)
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
        # Add average time per file if we have the data
        if elapsed_seconds and stats['total'] > 0:
            avg_per_file = elapsed_seconds / stats['total']
            avg_str = format_execution_time(avg_per_file)
            print(f"Average time per file: {avg_str}")
    else:
        print(f"Total time: {format_execution_time(stats['total_time'])}")
    
    print("=" * 60)
