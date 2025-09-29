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
    
    # NEW PATTERN: Show.Name.S01Ep05 or Show.Name.S1Ep15 (without dots)
    match = re.search(r'[Ss](\d+)[Ee]p(?:isode)?(\d+)', filename, re.IGNORECASE)
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
    
    # NEW PATTERN: ShowNameSeasonX EpY format (space only between Season and Ep)
    match = re.search(r'[Ss]eason(\d+)\s+[Ee]p(?:isode)?(\d+)', filename, re.IGNORECASE)
    if match:
        season = match.group(1).zfill(2)  # Ensure 2 digits for season
        episode = match.group(2)  # Keep original episode digits (for 100+ episodes)
        return f"S{season}E{episode}"
    
    # NEW PATTERN: SeasonXEpY format (with no space between Season and number, and Ep)
    match = re.search(r'[Ss]eason(\d+)[Ee]p(?:isode)?(\d+)', filename, re.IGNORECASE)
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
    
    # NEW PATTERN: Show Name Season X EpY format (like "Program Season2 Ep15")
    match = re.search(r'[Ss]eason\s+(\d+)[\s\._-]*[Ee]p(?:isode)?\s*(\d+)', filename, re.IGNORECASE)
    if match:
        season = match.group(1).zfill(2)  # Ensure 2 digits for season
        episode = match.group(2)  # Keep original episode digits (for 100+ episodes)
        return f"S{season}E{episode}"
    
    # NEW PATTERN: Show Name SeasonX.EpY format (like "Yes Season2.Ep160")
    match = re.search(r'[Ss]eason(\d+)[\s\._-]*[Ee]p(?:isode)?(\d+)', filename, re.IGNORECASE)
    if match:
        season = match.group(1).zfill(2)  # Ensure 2 digits for season
        episode = match.group(2)  # Keep original episode digits (for 100+ episodes)
        return f"S{season}E{episode}"
    
    # NEW PATTERN: Try to match Ep#### pattern (for files like Show.Name.Ep1234)
    # Use word boundary or separators to avoid matching within other words
    # Changed from \d{2,} to \d+ to allow single digit episodes as well
    match = re.search(r'(?:^|[._\s-])[Ee]p(?:isode)?(\d+)(?=[._\s-]|$)', filename, re.IGNORECASE)  
    if match:
        episode = match.group(1)  # Keep original episode digits
        return f"S01E{episode}"  # Assume season 1
    
    # NEW PATTERN: Show Name with Season X Ep Y format (like "Program Season2 Ep15")
    match = re.search(r'[Ss]eason\s+(\d+)\s+[Ee]p(?:isode)?\s*(\d+)', filename, re.IGNORECASE)
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
    """Find a potential movie-subtitle match based on filename similarity"""
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
        if len(video_words) > 0 and len(subtitle_files) > 0:
            match_ratio = len(common_words) / min(len(video_words), len(subtitle_files))
            if match_ratio >= 0.3 or len(common_words) > 0:  # At least one common word or 30% match
                return (video_files[0], subtitle_files[0])
    
    return None

def rename_subtitles_to_match_videos():
    directory = os.getcwd()
    files = os.listdir(directory)
    
    # Support both .mkv and .mp4 video files
    video_files = [f for f in files if f.endswith(('.mkv', '.mp4'))]
    
    # Support both .srt and .ass subtitle files
    subtitle_files = [f for f in files if f.endswith(('.srt', '.ass'))]

    #print("="*60)
    #print(f"DIRECTORY: {directory}")
    print(f"\nFILES FOUND: {len(video_files)} videos | {len(subtitle_files)} subtitles")
    print("="*60)
    
    if video_files:
        print(f"Videos: {video_files[:4]}{'...' if len(video_files) > 4 else ''}")
    if subtitle_files:
        print(f"Subtitles: {subtitle_files[:4]}{'...' if len(subtitle_files) > 4 else ''}")
    print()

    # First, build a reference of all video episodes for context-aware matching
    # This helps handle cases like S02E015 vs S02E15 that represent the same episode
    video_episodes = {}
    episode_to_pattern = {}  # Maps (season_num, episode_num) to the pattern used
    temp_video_dict = {}  # Store the original episode patterns
    
    # Sort video files alphabetically for consistent behavior when multiple videos match
    sorted_video_files_for_context = sorted(video_files)
    for video in sorted_video_files_for_context:
        episode_string = get_episode_number(video)
        if episode_string:
            season, episode = extract_season_episode_numbers(episode_string)
            if season and episode:
                season_num = int(season)
                episode_num = int(episode)  # Convert to int to remove leading zeros
                key = (season_num, episode_num)
                video_episodes[key] = episode_string
                # Only store the first video for each episode pattern to ensure deterministic behavior
                if episode_string not in temp_video_dict:
                    temp_video_dict[episode_string] = video
                if key not in episode_to_pattern:
                    episode_to_pattern[key] = episode_string
        else:
            # Add videos without episodes to remaining list for movie matching
            pass  # We'll add them later after processing episodes

    if video_episodes:
        print(f"PROCESSING VIDEOS:")
        print("-" * 40)
        print(f"EPISODE PATTERNS DETECTED FROM VIDEO FILES: {list(video_episodes.values())[:10]}{'...' if len(video_episodes) > 10 else ''}")
    print()

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
                    print(f"CONTEXT ADJUSTMENT: '{video}' has {ep} -> using {video_episodes[key]} pattern")
                    video_dict[video_episodes[key]] = video
                else:
                    video_dict[ep] = video
            else:
                video_dict[ep] = video
        else:
            remaining_video_files.append(video)

    # For subtitle matching, apply the same context-aware logic
    # Sort subtitle files alphabetically for consistent processing order
    sorted_subtitle_files = sorted(subtitle_files)
    remaining_subtitle_files = []
    renamed_count = 0

    print("PROCESSING SUBTITLES:")
    print("-" * 40)
    
    for subtitle in sorted_subtitle_files:
        ep = get_episode_number(subtitle)
        
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
                    print(f"'{subtitle}' -> {ep} adjusted to {video_pattern} (context-aware)")
                    adjusted_episode_string = video_pattern  # Use the same pattern as the video

        # Now match using the potentially adjusted episode string
        if adjusted_episode_string and adjusted_episode_string in temp_video_dict:
            base_name = os.path.splitext(temp_video_dict[adjusted_episode_string])[0]
            subtitle_ext = os.path.splitext(subtitle)[1]  # Get original subtitle extension
            new_name = f"{base_name}.ar{subtitle_ext}"
            
            # Check if target file already exists (collision handling)
            new_path = os.path.join(directory, new_name)
            if os.path.exists(new_path):
                # Handle the case where multiple subtitles target the same video file
                # Create a more specific name using information from the original subtitle file
                original_base = os.path.splitext(subtitle)[0]
                # Remove common suffixes and clean up the name
                original_cleaned = re.sub(r'[._\-\s]*[Ss]ub(title)?[._\-\s]*', '', original_base, flags=re.IGNORECASE)
                if original_cleaned == "":  # If the cleaned name is empty, use the original name
                    original_cleaned = original_base
                
                # Create a new name that includes the original subtitle identifier
                specific_new_name = f"{base_name}.ar_{original_cleaned}{subtitle_ext}"
                
                # Clean up any problematic characters in the specific part
                specific_new_name = re.sub(r'[<>:"/\|?*]', '_', specific_new_name)
                
                new_path = os.path.join(directory, specific_new_name)
                counter = 1
                original_specific_name = specific_new_name
                # If that specific name also exists, add a counter
                while os.path.exists(new_path):
                    name_part, ext_part = os.path.splitext(original_specific_name)
                    new_name = f"{name_part}_{counter}{ext_part}"
                    new_path = os.path.join(directory, new_name)
                    counter += 1
                
                new_name = os.path.basename(new_path)
                print(f"CONFLICT RESOLVED: Multiple subtitles match '{temp_video_dict[adjusted_episode_string]}' -> renamed '{subtitle}' to unique name '{new_name}'")
            else:
                print(f"RENAMED: '{subtitle}' -> '{new_name}'")
                
            old_path = os.path.join(directory, subtitle)
            os.rename(old_path, new_path)
            renamed_count += 1
        elif ep and ep in temp_video_dict:  # Also check original pattern
            base_name = os.path.splitext(temp_video_dict[ep])[0]
            subtitle_ext = os.path.splitext(subtitle)[1]  # Get original subtitle extension
            new_name = f"{base_name}.ar{subtitle_ext}"
            
            # Check if target file already exists (collision handling)
            new_path = os.path.join(directory, new_name)
            if os.path.exists(new_path):
                # Handle the case where multiple subtitles target the same video file
                # Create a more specific name using information from the original subtitle file
                original_base = os.path.splitext(subtitle)[0]
                # Remove common suffixes and clean up the name
                original_cleaned = re.sub(r'[._\-\s]*[Ss]ub(title)?[._\-\s]*', '', original_base, flags=re.IGNORECASE)
                if original_cleaned == "":  # If the cleaned name is empty, use the original name
                    original_cleaned = original_base
                
                # Create a new name that includes the original subtitle identifier
                specific_new_name = f"{base_name}.ar_{original_cleaned}{subtitle_ext}"
                
                # Clean up any problematic characters in the specific part
                specific_new_name = re.sub(r'[<>:"/\|?*]', '_', specific_new_name)
                
                new_path = os.path.join(directory, specific_new_name)
                counter = 1
                original_specific_name = specific_new_name
                # If that specific name also exists, add a counter
                while os.path.exists(new_path):
                    name_part, ext_part = os.path.splitext(original_specific_name)
                    new_name = f"{name_part}_{counter}{ext_part}"
                    new_path = os.path.join(directory, new_name)
                    counter += 1
                
                new_name = os.path.basename(new_path)
                print(f"CONFLICT RESOLVED: Multiple subtitles match '{temp_video_dict[ep]}' -> renamed '{subtitle}' to unique name '{new_name}'")
            else:
                print(f"RENAMED: '{subtitle}' -> '{new_name}'")
                
            old_path = os.path.join(directory, subtitle)
            os.rename(old_path, new_path)
            renamed_count += 1
        elif ep:
            print(f"NO MATCH: '{subtitle}' -> episode {ep} has no matching video")
        else:
            # This subtitle doesn't have episode info, keep it for potential movie matching
            remaining_subtitle_files.append(subtitle)
            print(f"NO EPISODE: '{subtitle}' -> could not detect episode number")
    
    print("-" * 40)
    print()
    
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
            print(f"MOVIE MODE: Found potential movie match!")
            print(f"RENAMED: '{subtitle_file}' -> '{new_name}'")
            os.rename(old_path, new_path)
            renamed_count += 1
        else:
            print("MOVIE MODE: No movie-subtitle match found.")
    elif len(remaining_video_files) > 1:
        print(f"MOVIE MODE: {len(remaining_video_files)} video files detected -> skipping movie matching logic.")
    
    print("="*60)
    total_candidate_files = len([f for f in files if f.endswith(('.srt', '.ass'))])
    if renamed_count > 0:
        print(f"COMPLETED TASK: {renamed_count} subtitle file{'s' if renamed_count != 1 else ''} renamed out of {total_candidate_files}")
    else:
        print("INFO: No files were renamed.")
    print("="*60)
    
    # Now add analysis summary using the same logic as export_analysis_to_csv function
    print("\nANALYSIS SUMMARY:")
    print("="*60)
    
    # Determine which episodes had matches by checking the actual renaming that would happen
    found_matches = set()
    not_found_episodes = set()
    
    # Identify episodes that would be matched by the main function
    temp_video_dict_analysis = {}
    for video in video_files:
        episode_string = get_episode_number(video)
        if episode_string:
            temp_video_dict_analysis[episode_string] = video
    
    # Process subtitles to see which ones would match
    for subtitle in subtitle_files:
        ep = get_episode_number(subtitle)
        if ep:
            season, episode = extract_season_episode_numbers(ep)
            if season and episode:
                season_num = int(season)
                episode_num = int(episode)
                key = (season_num, episode_num)
                
                # Apply context-aware standardization for subtitles too
                adjusted_episode_string = ep
                if key in video_episodes:
                    video_pattern = video_episodes[key]
                    adjusted_episode_string = video_pattern  # Use the same pattern as the video

                # Now match using the potentially adjusted episode string
                if adjusted_episode_string and adjusted_episode_string in temp_video_dict_analysis:
                    found_matches.add(adjusted_episode_string)
                elif ep and ep in temp_video_dict_analysis:  # Also check original pattern
                    found_matches.add(ep)
                else:
                    not_found_episodes.add(adjusted_episode_string or ep)
        else:
            # This subtitle doesn't have episode info
            not_found_episodes.add("(None)")
    
    # Also add episodes from videos that don't have matching subtitles
    for video in video_files:
        ep = get_episode_number(video)
        if ep:
            season, episode = extract_season_episode_numbers(ep)
            if season and episode:
                season_num = int(season)
                episode_num = int(episode)
                key = (season_num, episode_num)
                
                # Check if this video episode has a matching subtitle
                has_subtitle_match = False
                for subtitle in subtitle_files:
                    sub_ep = get_episode_number(subtitle)
                    if sub_ep:
                        sub_season, sub_episode = extract_season_episode_numbers(sub_ep)
                        if sub_season and sub_episode:
                            sub_season_num = int(sub_season)
                            sub_episode_num = int(sub_episode)
                            if sub_season_num == season_num and sub_episode_num == episode_num:
                                has_subtitle_match = True
                                break
                
                if not has_subtitle_match:
                    # This video episode doesn't have a matching subtitle
                    if key in video_episodes:
                        not_found_episodes.add(video_episodes[key])
                    else:
                        not_found_episodes.add(ep)

    # Identify files that couldn't have episode numbers detected
    unidentified_files = []
    for filename in files:
        if filename.endswith(('.srt', '.ass', '.mkv', '.mp4')):
            ep = get_episode_number(filename)
            if not ep:
                unidentified_files.append(filename)

    # Display the summary
    if found_matches:
        print("FOUND AND RENAMED MATCHING SUBTITLE AND VIDEO FILES FOR THESE EPISODES:")
        for episode in sorted(found_matches):
            print(f"- {episode}")
        print()

    if not_found_episodes:
        print("COULDN'T FIND MATCHING SUBTITLE AND VIDEO FILES FOR THESE EPISODES:")
        for episode in sorted(not_found_episodes):
            if episode != "(None)":  # Don't list "(None)" in this section
                print(f"- {episode}")
        print()

    if unidentified_files:
        print("COULDN'T IDENTIFY SEASON#EPISODE# FOR THESE FILES:")
        for filename in sorted(unidentified_files):
            print(f"- {filename}")
        print()

# CSV Export Functionality - Can be commented out if not needed
def export_analysis_to_csv():
    """Export episode analysis results to a text file in TEMPLATE format"""
    
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

    # Categorize files based on detection results
    identified_files = []
    unidentified_files = []
    
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
        
        # Format the episode identification string as requested in template
        season_display = season if season else "(None)"
        episode_display = episode if episode else "(None)"
        formatted_output = filename + " >> S" + season_display + "E" + episode_display
        
        if season or episode:
            identified_files.append({
                'filename': filename,
                'episode_string': adjusted_episode_string,
                'formatted_output': formatted_output
            })
        else:
            unidentified_files.append(filename)

    # Determine which episodes had matches by checking the actual renaming that would happen
    # This requires simulating the matching process from rename_subtitles_to_match_videos
    found_matches = set()
    not_found_episodes = set()
    
    # Identify episodes that would be matched by the main function
    # Sort the video files alphabetically for consistent selection when multiple videos match
    sorted_video_files = sorted(video_files)
    temp_video_dict = {}
    for video in sorted_video_files:
        episode_string = get_episode_number(video)
        if episode_string:
            # Only store the first occurrence to ensure deterministic behavior
            if episode_string not in temp_video_dict:
                temp_video_dict[episode_string] = video
    
    # Process subtitles to see which ones would match
    for subtitle in subtitle_files:
        ep = get_episode_number(subtitle)
        if ep:
            season, episode = extract_season_episode_numbers(ep)
            if season and episode:
                season_num = int(season)
                episode_num = int(episode)
                key = (season_num, episode_num)
                
                # Apply context-aware standardization for subtitles too
                adjusted_episode_string = ep
                if key in video_episodes:
                    video_pattern = video_episodes[key]
                    adjusted_episode_string = video_pattern  # Use the same pattern as the video

                # Now match using the potentially adjusted episode string
                if adjusted_episode_string and adjusted_episode_string in temp_video_dict:
                    found_matches.add(adjusted_episode_string)
                elif ep and ep in temp_video_dict:  # Also check original pattern
                    found_matches.add(ep)
                else:
                    not_found_episodes.add(adjusted_episode_string or ep)
        else:
            # This subtitle doesn't have episode info
            not_found_episodes.add("(None)")
    
    # Also add episodes from videos that don't have matching subtitles
    for video in video_files:
        ep = get_episode_number(video)
        if ep:
            season, episode = extract_season_episode_numbers(ep)
            if season and episode:
                season_num = int(season)
                episode_num = int(episode)
                key = (season_num, episode_num)
                
                # Check if this video episode has a matching subtitle
                has_subtitle_match = False
                for subtitle in subtitle_files:
                    sub_ep = get_episode_number(subtitle)
                    if sub_ep:
                        sub_season, sub_episode = extract_season_episode_numbers(sub_ep)
                        if sub_season and sub_episode:
                            sub_season_num = int(sub_season)
                            sub_episode_num = int(sub_episode)
                            if sub_season_num == season_num and sub_episode_num == episode_num:
                                has_subtitle_match = True
                                break
                
                if not has_subtitle_match:
                    # This video episode doesn't have a matching subtitle
                    if key in video_episodes:
                        not_found_episodes.add(video_episodes[key])
                    else:
                        not_found_episodes.add(ep)

    # Write results to text file in the template format
    txt_filename = "renaming_report.csv"  # Changed from episode_analysis.csv to renaming_report.csv
    txt_path = os.path.join(directory, txt_filename)
    
    with open(txt_path, 'w', encoding='utf-8') as txtfile:
        # Write header row as per template
        txtfile.write("FILENAME.EXTENSION >> IDENTIFIED SEASON#EPISODE#\n")
        
        # Write all identified files in the template format
        for file_info in sorted(identified_files, key=lambda x: x['filename']):
            txtfile.write(file_info['formatted_output'] + '\n')
        
        # Write all unidentified files in the template format
        for filename in sorted(unidentified_files):
            season_display = "(None)"
            episode_display = "(None)"
            formatted_output = filename + " >> S" + season_display + "E" + episode_display
            txtfile.write(formatted_output + '\n')
        
        # Add blank line before categorized results
        if identified_files or unidentified_files:
            txtfile.write('\n')
        
        # Write found matches results
        if found_matches:
            txtfile.write("FOUND AND RENAMED MATCHING SUBTITLE AND VIEDEO FILES FOR THESE EPISODES:\n")
            for episode in sorted(found_matches):
                txtfile.write("- " + episode + "\n")
            txtfile.write('\n')
        
        # Write not found results
        if not_found_episodes:
            txtfile.write("COULDN'T FIND MATCHING SUBTITLE AND VIEDEO FILES FOR THESE EPISODES:\n")
            for episode in sorted(not_found_episodes):
                if episode != "(None)":  # Don't list "(None)" in this section
                    txtfile.write("- " + episode + "\n")
            txtfile.write('\n')
        
        # Write unidentified files summary
        if unidentified_files:
            txtfile.write("COULDNT IDENTIFY SEASON#EPISODE# FOR THESE FILES:\n")
            for filename in sorted(unidentified_files):
                txtfile.write("- " + filename + "\n")
    
    print(f"\nExported file renaming records to:")
    print(f"{txt_path}\n")

if __name__ == "__main__":
    # Export analysis BEFORE any renaming occurs to capture original state
    export_analysis_to_csv()
    # Then perform the renaming
    rename_subtitles_to_match_videos()
