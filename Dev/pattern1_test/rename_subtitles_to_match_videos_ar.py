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
    
    # Try to match E## pattern (for files like Show.Name.E1234)
    # Use word boundary or separators to avoid matching within words like "Title.2023"
    match = re.search(r'(?:^|[._\s-])[Ee](\d{2,})(?=[._\s-]|$)', filename)  
    if match:
        episode = match.group(1)  # Keep original episode digits
        return f"S01E{episode}"  # Assume season 1
    
    # Try to match - ## pattern (for subtitle files like - 01, - 02)
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
        if len(video_words) > 0 and len(subtitle_words) > 0:
            match_ratio = len(common_words) / min(len(video_words), len(subtitle_words))
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

    print(f"Current directory: {directory}")
    print(f"Found {len(video_files)} video files: {video_files[:3]}{'...' if len(video_files) > 3 else ''}")
    print(f"Found {len(subtitle_files)} subtitle files: {subtitle_files[:3]}{'...' if len(subtitle_files) > 3 else ''}")

    # First, try to handle TV episode matching (existing functionality)
    video_dict = {}
    remaining_video_files = []
    remaining_subtitle_files = []

    for video in video_files:
        ep = get_episode_number(video)
        if ep:
            video_dict[ep] = video
        else:
            remaining_video_files.append(video)
    
    print(f"Video episodes detected: {list(video_dict.keys())[:5]}{'...' if len(video_dict) > 5 else ''}")

    renamed_count = 0
    for subtitle in subtitle_files:
        ep = get_episode_number(subtitle)
        print(f"Processing subtitle: {subtitle}, detected episode: {ep}")
        if ep and ep in video_dict:
            base_name = os.path.splitext(video_dict[ep])[0]
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
    
    print(f"\nRenaming complete! {renamed_count} files renamed.")

if __name__ == "__main__":
    rename_subtitles_to_match_videos()
