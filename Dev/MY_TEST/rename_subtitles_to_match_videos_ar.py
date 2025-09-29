import os
import re

def get_episode_number(filename):
    # Try to match S##E## pattern (for video files like S01E01)
    match = re.search(r'[Ss](\d+)[Ee](\d+)', filename)
    if match:
        season = match.group(1).zfill(2)  # Ensure 2 digits for season
        episode = match.group(2)  # Keep original episode digits (for 100+ episodes)
        return f"S{season}E{episode}"
    
    # Try to match season.episode pattern (for files like Show.Name.2x05)
    match = re.search(r'(?:^|[._\s-])(\d+)[xX](\d+)(?=[._\s-]|$)', filename)
    if match:
        season = match.group(1).zfill(2)  # Ensure 2 digits for season
        episode = match.group(2)  # Keep original episode digits (for 100+ episodes)
        return f"S{season}E{episode}"
    
    # Try to match Season/Episode words pattern (for files like Show.Name.Season.1.Episode.05)
    match = re.search(r'[Ss]eason\.(\d+)[\s\._-]*[Ee]pisode\.(\d+)', filename, re.IGNORECASE)
    if match:
        season = match.group(1).zfill(2)  # Ensure 2 digits for season
        episode = match.group(2)  # Keep original episode digits (for 100+ episodes)
        return f"S{season}E{episode}"
    
    # Alternative pattern: Show.Name.S01.Ep.05
    match = re.search(r'[Ss](\d+)[\s\._-]*[Ee]p(?:isode)?\.(\d+)', filename, re.IGNORECASE)
    if match:
        season = match.group(1).zfill(2)  # Ensure 2 digits for season
        episode = match.group(2)  # Keep original episode digits (for 100+ episodes)
        return f"S{season}E{episode}"
    
    # NEW PATTERN: Show Name Season X Episode Y (with spaces)
    match = re.search(r'[Ss]eason\s+(\d+)\s+[Ee]pisode\s+(\d+)', filename, re.IGNORECASE)
    if match:
        season = match.group(1).zfill(2)  # Ensure 2 digits for season
        episode = match.group(2)  # Keep original episode digits (for 100+ episodes)
        return f"S{season}E{episode}"
    
    # NEW PATTERN: ShowNameSeasonXEpisodeY (without any spaces)
    match = re.search(r'[Ss]eason(\d+)[Ee]pisode(\d+)', filename, re.IGNORECASE)
    if match:
        season = match.group(1).zfill(2)  # Ensure 2 digits for season
        episode = match.group(2)  # Keep original episode digits (for 100+ episodes)
        return f"S{season}E{episode}"
    
    # NEW PATTERN: ShowNameSeasonX EpisodeY (space only between Season and Episode)
    match = re.search(r'[Ss]eason(\d+)\s+[Ee]pisode(\d+)', filename, re.IGNORECASE)
    if match:
        season = match.group(1).zfill(2)  # Ensure 2 digits for season
        episode = match.group(2)  # Keep original episode digits (for 100+ episodes)
        return f"S{season}E{episode}"
    
    # Try to match E## pattern (for files like Show.Name.E1234)
    # Use word boundary or separators to avoid matching within words like "Title.2023"
    # Changed from \d{2,} to \d+ to allow single digit episodes as well
    match = re.search(r'(?:^|[._\s-])[Ee](\d+)(?=[._\s-]|$)', filename)  
    if match:
        episode = match.group(1)  # Keep original episode digits
        return f"S01E{episode}"  # Assume season 1
    
    # NEW PATTERN: Try to match Ep#### pattern (for files like Show.Name.Ep1234)
    # Use word boundary or separators to avoid matching within other words
    # Changed from \d{2,} to \d+ to allow single digit episodes as well
    match = re.search(r'(?:^|[._\s-])[Ee]p(?:isode)?(\d+)(?=[._\s-]|$)', filename, re.IGNORECASE)  
    if match:
        episode = match.group(1)  # Keep original episode digits
        return f"S01E{episode}"  # Assume season 1
    
    # NEW PATTERN: S##Ep## (without dots) - FIXED ORDER ISSUE
    match = re.search(r'[Ss](\d+)[Ee]p(?:isode)?(\d+)', filename, re.IGNORECASE)
    if match:
        season = match.group(1).zfill(2)  # Ensure 2 digits for season
        episode = match.group(2)  # Keep original episode digits (for 100+ episodes)
        return f"S{season}E{episode}"
    
    # Try to match - ## pattern (for files like - 01, - 02, -1, -123, etc.)
    # This includes -#, -##, -###, -#### with or without spaces
    match = re.search(r'-\s*(\d+)', filename)
    if match:
        episode_num = match.group(1)  # Keep original episode digits (for 100+ episodes)
        return f"S01E{episode_num}"  # Assume season 1
    
    return None

def extract_base_name(filename):
    """Extract the base name without extension and common separators"""
    # Remove extension
    base_name = os.path.splitext(filename)[0]
    # Remove common separators and clean up
    base_name = re.sub(r'[._\-]+', ' ', base_name)
    return base_name.strip()

def extract_season_episode_numbers(episode_string):
    """Extract season and episode numbers from episode string like S01E05"""
    if episode_string:
        season_match = re.search(r'S(\d+)', episode_string)
        episode_match = re.search(r'E(\d+)', episode_string)
        
        season = season_match.group(1) if season_match else ""
        episode = episode_match.group(1) if episode_match else ""
        
        return season, episode
    return "", ""

def find_movie_subtitle_match(video_files, subtitle_files):
    \"\"\"Find a potential movie-subtitle match based on filename similarity\"\"\"
    if len(video_files) != 1 or len(subtitle_files) != 1:
        # Only proceed if there's exactly one video and one subtitle
        return None
    
    video_name = extract_base_name(video_files[0])
    subtitle_name = extract_base_name(subtitle_files[0])
    
    # Extract years from filenames
    video_year_match = re.search(r'(?:19|20)\d{2}', video_files[0])
    subtitle_year_match = re.search(r'(?:19|20)\d{2}', subtitle_files[0])
    
    video_year = video_year_match.group() if video_year_match else None
    subtitle_year = subtitle_year_match.group() if subtitle_year_match else None
    
    # Split both names into words (remove common file parts like 1080p, 720p, etc.)
    video_words = set(re.split(r'\s+', video_name.lower()))
    subtitle_words = set(re.split(r'\s+', subtitle_name.lower()))
    
    # Remove common video quality/resolution indicators
    common_indicators = {'1080p', '720p', '480p', '2160p', '4k', 'bluray', 'web', 'dvd', 'hd', 'x264', 'x265', 
                         'h264', 'h265', 'avc', 'hevc', 'aac', 'ac3', 'dts', 'remux', 'proper', 'repack', 
                         'extended', 'theatrical', 'unrated', 'directors', 'cut', 'multi', 'sub', 'eng', 'en', 
                         'ara', 'ar', 'eng', 'fre', 'fr', 'ger', 'de', 'ita', 'es', 'spa', 'kor', 'jpn', 'ch',
                         'chs', 'cht', 'internal', 'limited', 'unrated', 'xvid', 'divx', 'ntsc', 'pal', 'dc',
                         'sync', 'syncopated', 'cc', 'sdh', 'hc', 'proper', 'real', 'final', 'post', 'pre', 
                         'sync', 'dub', 'dubbed', 'sdh', 'cc'}
    
    video_words = video_words - common_indicators
    subtitle_words = subtitle_words - common_indicators
    
    # Check if there's a significant overlap between the words
    common_words = video_words.intersection(subtitle_words)
    
    # Check if years match (higher priority match)
    years_match = (video_year and subtitle_year and video_year == subtitle_year)
    
    # If years match, be more lenient with word matching
    if years_match:
        # If years match, require only that there's some basic similarity or both contain the year
        if len(common_words) > 0 or ('19' in str(video_year) or '20' in str(video_year)):
            return (video_files[0], subtitle_files[0])
    else:
        # Otherwise, use the original matching logic
        if len(video_words) > 0 and len(subtitle_words) > 0:
            match_ratio = len(common_words) / min(len(video_words), len(subtitle_words))
            if match_ratio >= 0.3 or len(common_words) > 0:  # At least one common word or 30% match
                return (video_files[0], subtitle_files[0])
    
    return None

# CSV Export Functionality - Can be commented out if not needed
def export_analysis_to_csv():
    \"\"\"Export episode analysis results to a CSV file\"\"\"
    import csv
    
    directory = os.getcwd()
    files = os.listdir(directory)
    
    # Support both .mkv and .mp4 video files and .srt and .ass subtitle files
    video_files = [f for f in files if f.endswith(('.mkv', '.mp4'))]
    subtitle_files = [f for f in files if f.endswith(('.srt', '.ass'))]
    
    all_files = video_files + subtitle_files
    
    # First pass: Get all episode patterns for video files to create a reference
    video_episodes = {}
    episode_to_pattern = {}  # Maps (season_num, episode_num) to the pattern used
    for filename in video_files:
        episode_string = get_episode_number(filename)
        if episode_string:
            season, episode = extract_season_episode_numbers(episode_string)
            if season and episode:
                season_num = int(season)
                episode_num = int(episode)  # Convert to int to remove leading zeros
                key = (season_num, episode_num)
                video_episodes[key] = episode_string
                if key not in episode_to_pattern:
                    episode_to_pattern[key] = episode_string

    # Prepare results for CSV
    results = []
    
    for filename in all_files:
        # Get episode number using the same logic as the original script
        episode_string = get_episode_number(filename)
        
        # Apply context-aware standardization for subtitles too
        adjusted_episode_string = episode_string
        if filename in subtitle_files and episode_string:
            season, episode = extract_season_episode_numbers(episode_string)
            if season and episode:
                season_num = int(season)
                episode_num = int(episode)  # Convert to int to remove leading zeros
                key = (season_num, episode_num)
                
                # Check if this episode exists in video files (regardless of padding)
                if key in video_episodes:
                    # This subtitle has the same season/episode as a video file, just with different padding
                    video_pattern = video_episodes[key]
                    adjusted_episode_string = video_pattern  # Use the same pattern as the video
        
        # Extract season and episode numbers from adjusted string
        season, episode = extract_season_episode_numbers(adjusted_episode_string)
        
        # Classify file type
        file_type = \"Video\" if filename in video_files else \"Subtitle\"
        
        # Format the episode identification string as requested
        season_display = season if season else \"(None)\"
        episode_display = episode if episode else \"(None)\"
        formatted_output = filename + \" >> S\" + season_display + \"E\" + episode_display
        
        results.append({
            'filename': filename,
            'file_type': file_type,
            'episode_pattern': adjusted_episode_string or 'None',
            'formatted_output': formatted_output
        })
    
    # Write results to CSV with the requested format
    csv_filename = \"episode_analysis.csv\"
    csv_path = os.path.join(directory, csv_filename)
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['filename', 'file_type', 'episode_pattern', 'formatted_output']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    print(f\"\\nCSV analysis exported to: {csv_path}\")
    print(f\"Exported {len(results)} file records to CSV.\")

def rename_subtitles_to_match_videos():
    directory = os.getcwd()
    files = os.listdir(directory)
    
    # Support both .mkv and .mp4 video files
    video_files = [f for f in files if f.endswith(('.mkv', '.mp4'))]
    
    # Support both .srt and .ass subtitle files
    subtitle_files = [f for f in files if f.endswith(('.srt', '.ass'))]

    print(f"Current directory: {directory}")
    print(f"Found {len(video_files)} video files: {video_files[:3]}{'...' if len(video_files) > 3 else ''}")
    print(f"Found {len(subtitle_files)} subtitle files: {subtitle_files[:3]}{'...' if len(subtitle_files) > 3 else ''}")

    # First, build a reference of all video episodes for context-aware matching
    # This helps handle cases like S02E015 vs S02E15 that represent the same episode
    video_episodes = {}
    episode_to_pattern = {}  # Maps (season_num, episode_num) to the pattern used
    temp_video_dict = {}  # Store the original episode patterns
    
    for video in video_files:
        episode_string = get_episode_number(video)
        if episode_string:
            season, episode = extract_season_episode_numbers(episode_string)
            if season and episode:
                season_num = int(season)
                episode_num = int(episode)  # Convert to int to remove leading zeros
                key = (season_num, episode_num)
                video_episodes[key] = episode_string
                temp_video_dict[episode_string] = video
                if key not in episode_to_pattern:
                    episode_to_pattern[key] = episode_string
        else:
            # Add videos without episodes to remaining list for movie matching
            pass  # We'll add them later after processing episodes

    print(f"Video episode patterns: {video_episodes}")

    # Separate videos with and without episode numbers
    video_dict = {}
    remaining_video_files = []
    
    for video in video_files:
        ep = get_episode_number(video)
        if ep:
            # Apply context-aware episode standardization for consistency
            season, episode = extract_season_episode_numbers(ep)
            if season and episode:
                season_num = int(season)
                episode_num = int(episode)
                key = (season_num, episode_num)
                
                # Use the pattern found in other video files if available (context-aware)
                if key in video_episodes and video_episodes[key] != ep:
                    print(f"Context adjustment: {video} has {ep} but using {video_episodes[key]} pattern")
                    video_dict[video_episodes[key]] = video
                else:
                    video_dict[ep] = video
            else:
                video_dict[ep] = video
        else:
            remaining_video_files.append(video)

    # For subtitle matching, apply the same context-aware logic
    remaining_subtitle_files = []
    renamed_count = 0

    for subtitle in subtitle_files:
        ep = get_episode_number(subtitle)
        print(f"Processing subtitle: {subtitle}, detected episode: {ep}")
        
        # Apply context-aware standardization for subtitles too
        adjusted_episode_string = ep
        if ep:
            season, episode = extract_season_episode_numbers(ep)
            if season and episode:
                season_num = int(season)
                episode_num = int(episode)
                key = (season_num, episode_num)
                
                # Check if this episode exists in video files (regardless of padding)
                if key in video_episodes:
                    # This subtitle has the same season/episode as a video file, just with different padding
                    video_pattern = video_episodes[key]
                    print(f"Context adjustment: {subtitle} has {ep} but video has {video_pattern}")
                    adjusted_episode_string = video_pattern  # Use the same pattern as the video

        # Now match using the potentially adjusted episode string
        if adjusted_episode_string and adjusted_episode_string in temp_video_dict:
            base_name = os.path.splitext(temp_video_dict[adjusted_episode_string])[0]
            subtitle_ext = os.path.splitext(subtitle)[1]  # Get original subtitle extension
            new_name = f"{base_name}.ar{subtitle_ext}"
            old_path = os.path.join(directory, subtitle)
            new_path = os.path.join(directory, new_name)
            print(f"Renaming: {subtitle} -> {new_name}")
            os.rename(old_path, new_path)
            renamed_count += 1
        elif ep and ep in temp_video_dict:  # Also check original pattern
            base_name = os.path.splitext(temp_video_dict[ep])[0]
            subtitle_ext = os.path.splitext(subtitle)[1]  # Get original subtitle extension
            new_name = f"{base_name}.ar{subtitle_ext}"
            old_path = os.path.join(directory, subtitle)
            new_path = os.path.join(directory, new_name)
            print(f"Renaming: {subtitle} -> {new_name}")
            os.rename(old_path, new_path)
            renamed_count += 1
        elif ep:
            print(f"No matching video found for episode {ep}")
        else:
            # This subtitle doesn't have episode info, keep it for potential movie matching
            remaining_subtitle_files.append(subtitle)
            print(f"Could not detect episode number in: {subtitle}")
    
    # After handling TV episodes, check for movie-subtitle match if no episodes were processed
    if renamed_count == 0 and len(remaining_video_files) == 1 and len(remaining_subtitle_files) == 1:
        movie_match = find_movie_subtitle_match(remaining_video_files, remaining_subtitle_files)
        if movie_match:
            video_file, subtitle_file = movie_match
            base_name = os.path.splitext(video_file)[0]
            subtitle_ext = os.path.splitext(subtitle_file)[1]
            new_name = f"{base_name}.ar{subtitle_ext}"
            old_path = os.path.join(directory, subtitle_file)
            new_path = os.path.join(directory, new_name)
            print(f"Movie mode: Found potential match - renaming subtitle to match movie")
            print(f"Renaming: {subtitle_file} -> {new_name}")
            os.rename(old_path, new_path)
            renamed_count += 1
        else:
            print("No movie-subtitle match found in potential movie files.")
    elif len(remaining_video_files) > 1:
        print(f"Multiple video files detected, skipping movie matching logic completely.")
    
    print(f\"\\nRenaming complete! {renamed_count} files renamed.\")\n    \n    # Optional: Export analysis to CSV - comment out the next line if not needed\n    export_analysis_to_csv()\n\nif __name__ == \"__main__\":\n    rename_subtitles_to_match_videos()
