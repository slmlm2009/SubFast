import os
import re

def get_episode_number(filename):
    # Try to match S##E## pattern (for video files like S01E01)
    match = re.search(r'[Ss](\d+)[Ee](\d+)', filename)
    if match:
        season = match.group(1).zfill(2)  # Ensure 2 digits
        episode = match.group(2).zfill(2)  # Ensure 2 digits
        return f"S{season}E{episode}"
    
    # Try to match - ## pattern (for subtitle files like - 01, - 02)
    match = re.search(r'-\s*(\d+)', filename)
    if match:
        episode_num = match.group(1).zfill(2)  # Ensure 2 digits
        return f"S01E{episode_num}"  # Assume season 1
    
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

    video_dict = {}
    for video in video_files:
        ep = get_episode_number(video)
        if ep:
            video_dict[ep] = video
    
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
            print(f"Could not detect episode number in: {subtitle}")
    
    print(f"\nRenaming complete! {renamed_count} files renamed.")

if __name__ == "__main__":
    rename_subtitles_to_match_videos()
