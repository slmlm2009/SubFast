import os
import re
import csv

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
    match = re.search(r'(?:^|[._\s-])[Ee](\d{2,})(?=[._\s-]|$)', filename)  
    if match:
        episode = match.group(1)  # Keep original episode digits
        return f"S01E{episode}"  # Assume season 1
    
    # NEW PATTERN: Try to match Ep#### pattern (for files like Show.Name.Ep1234)
    # Use word boundary or separators to avoid matching within other words
    match = re.search(r'(?:^|[._\s-])[Ee]p(?:isode)?(\d{2,})(?=[._\s-]|$)', filename, re.IGNORECASE)  
    if match:
        episode = match.group(1)  # Keep original episode digits
        return f"S01E{episode}"  # Assume season 1
    
    # Try to match - ## pattern (for subtitle files like - 01, - 02)
    match = re.search(r'-\s*(\d+)', filename)
    if match:
        episode_num = match.group(1)  # Keep original episode digits (for 100+ episodes)
        return f"S01E{episode_num}"  # Assume season 1
    
    return None

def extract_season_episode_numbers(episode_string):
    """Extract season and episode numbers from episode string like S01E05"""
    if episode_string:
        season_match = re.search(r'S(\d+)', episode_string)
        episode_match = re.search(r'E(\d+)', episode_string)
        
        season = season_match.group(1) if season_match else ""
        episode = episode_match.group(1) if episode_match else ""
        
        return season, episode
    return "", ""

def analyze_files():
    directory = os.getcwd()
    files = os.listdir(directory)
    
    # Support both .mkv and .mp4 video files and .srt and .ass subtitle files
    video_files = [f for f in files if f.endswith(('.mkv', '.mp4'))]
    subtitle_files = [f for f in files if f.endswith(('.srt', '.ass'))]
    
    all_files = video_files + subtitle_files
    
    print(f"Current directory: {directory}")
    print(f"Found {len(video_files)} video files and {len(subtitle_files)} subtitle files")
    
    # Prepare results for CSV
    results = []
    
    for filename in all_files:
        # Get episode number using the same logic as the original script
        episode_string = get_episode_number(filename)
        
        # Extract season and episode numbers
        season, episode = extract_season_episode_numbers(episode_string)
        
        # Classify file type
        file_type = "Video" if filename in video_files else "Subtitle"
        
        results.append({
            'filename': filename,
            'type': file_type,
            'episode_string': episode_string or "None",
            'season': season,
            'episode': episode
        })
        
        print(f"File: {filename} | Type: {file_type} | Episode String: {episode_string or 'None'} | Season: {season or 'N/A'} | Episode: {episode or 'N/A'}")
    
    # Write results to CSV
    csv_filename = \"episode_analysis.csv\"
    csv_path = os.path.join(directory, csv_filename)
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['filename', 'type', 'episode_string', 'season', 'episode']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    # Print the results in the requested format
    print(f\"\\nAnalysis complete! Results saved to {csv_filename}\")
    print(\"Printed results:\")
    for result in results:
        filename = result['filename']
        season = result['season'] if result['season'] else 'UNK'
        episode = result['episode'] if result['episode'] else 'UNK'
        episode_string = result['episode_string']
        
        if episode_string and episode_string != \"None\":
            print(f\"{filename} >> S{season}E{episode}\")
        else:
            print(f\"{filename} >> S{season}E{episode}\")
    
    print(f\"\\nProcessed {len(results)} files total.\")

if __name__ == "__main__":
    analyze_files()