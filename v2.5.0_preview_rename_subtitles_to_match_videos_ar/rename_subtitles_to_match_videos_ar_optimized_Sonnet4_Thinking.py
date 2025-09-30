
import os
import re
from typing import Dict, List, Tuple, Optional, Set
from functools import lru_cache

# Pre-compile all regex patterns for maximum efficiency
class EpisodePatterns:
    """Pre-compiled regex patterns for episode detection"""

    # Season/Episode patterns (ordered by most common first for early exit)
    SE_PATTERNS = [
        re.compile(r'[Ss](\d+)[Ee](\d+)', re.IGNORECASE),  # S01E01
        re.compile(r'(?:^|[._\s-])(\d+)[xX](\d+)(?=[._\s-]|$)', re.IGNORECASE),  # 2x05
        re.compile(r'[Ss]eason\.(\d+)[\s\._-]*[Ee]pisode\.(\d+)', re.IGNORECASE),  # Season.1.Episode.05
        re.compile(r'[Ss](\d+)[\s\._-]*[Ee]p(?:isode)?\.(\d+)', re.IGNORECASE),  # S01.Ep.05
        re.compile(r'[Ss](\d+)[Ee]p(?:isode)?(\d+)', re.IGNORECASE),  # S01Ep05
        re.compile(r'[Ss]eason\s+(\d+)\s+[Ee]pisode\s+(\d+)', re.IGNORECASE),  # Season 1 Episode 05
        re.compile(r'[Ss]eason(\d+)[Ee]pisode(\d+)', re.IGNORECASE),  # Season1Episode05
        re.compile(r'[Ss]eason(\d+)\s+[Ee]pisode(\d+)', re.IGNORECASE),  # Season1 Episode05
        re.compile(r'[Ss]eason(\d+)\s+[Ee]p(?:isode)?(\d+)', re.IGNORECASE),  # Season1 Ep05
        re.compile(r'[Ss]eason(\d+)[Ee]p(?:isode)?(\d+)', re.IGNORECASE),  # Season1Ep05
        re.compile(r'[Ss]eason\s+(\d+)[\s\._-]*[Ee]p(?:isode)?\s*(\d+)', re.IGNORECASE),  # Season 2 Ep15
        re.compile(r'[Ss]eason(\d+)[\s\._-]*[Ee]p(?:isode)?(\d+)', re.IGNORECASE),  # Season2.Ep160
        re.compile(r'[Ss]eason\s+(\d+)\s+[Ee]p(?:isode)?\s*(\d+)', re.IGNORECASE),  # Season 2 Ep 15
    ]

    # Episode-only patterns
    E_PATTERNS = [
        re.compile(r'(?:^|[._\s-])[Ee](\d+)(?=[._\s-]|$)', re.IGNORECASE),  # E01
        re.compile(r'(?:^|[._\s-])[Ee]p(?:isode)?(\d+)(?=[._\s-]|$)', re.IGNORECASE),  # Ep01
    ]

    # Dash pattern
    DASH_PATTERN = re.compile(r'-\s*(\d+)')

    # Common file cleaning patterns
    SEPARATOR_PATTERN = re.compile(r'[._\-]+')
    YEAR_PATTERN = re.compile(r'(?:19|20)\d{2}')
    QUALITY_INDICATORS = frozenset({
        '1080p', '720p', '480p', '2160p', '4k', 'bluray', 'web', 'dvd', 'hd', 'x264', 'x265',
        'h264', 'h265', 'avc', 'hevc', 'aac', 'ac3', 'dts', 'remux', 'proper', 'repack',
        'extended', 'theatrical', 'unrated', 'directors', 'cut', 'multi', 'sub', 'eng', 'en',
        'ara', 'ar', 'eng', 'fre', 'fr', 'ger', 'de', 'ita', 'es', 'spa', 'kor', 'jpn', 'ch',
        'chs', 'cht', 'internal', 'limited', 'unrated', 'xvid', 'divx', 'ntsc', 'pal', 'dc',
        'sync', 'syncopated', 'cc', 'sdh', 'hc', 'proper', 'real', 'final', 'post', 'pre',
        'sync', 'dub', 'dubbed', 'sdh', 'cc'
    })

class FileInfo:
    """Optimized file information container"""
    __slots__ = ('name', 'base_name', 'extension', 'episode_string', 'season', 'episode', 'is_video')

    def __init__(self, filename: str, is_video: bool):
        self.name = filename
        self.base_name, self.extension = os.path.splitext(filename)
        self.is_video = is_video
        self.episode_string = self._extract_episode()
        self.season, self.episode = self._extract_numbers() if self.episode_string else ('', '')

    @lru_cache(maxsize=None)
    def _extract_episode(self) -> Optional[str]:
        """Extract episode information from filename with early exit optimization"""
        filename = self.name

        # Try season/episode patterns first (most common)
        for pattern in EpisodePatterns.SE_PATTERNS:
            match = pattern.search(filename)
            if match:
                season = match.group(1).zfill(2)
                episode = match.group(2)
                return f"S{season}E{episode}"

        # Try episode-only patterns
        for pattern in EpisodePatterns.E_PATTERNS:
            match = pattern.search(filename)
            if match:
                episode = match.group(1)
                return f"S01E{episode}"

        # Try dash pattern
        match = EpisodePatterns.DASH_PATTERN.search(filename)
        if match:
            episode_num = match.group(1)
            return f"S01E{episode_num}"

        return None

    def _extract_numbers(self) -> Tuple[str, str]:
        """Extract season and episode numbers from episode string"""
        if not self.episode_string:
            return '', ''

        season_match = re.search(r'S(\d+)', self.episode_string)
        episode_match = re.search(r'E(\d+)', self.episode_string)

        season = season_match.group(1) if season_match else ''
        episode = episode_match.group(1) if episode_match else ''

        return season, episode

    @lru_cache(maxsize=None)
    def get_clean_name(self) -> str:
        """Get cleaned base name for movie matching"""
        clean_name = EpisodePatterns.SEPARATOR_PATTERN.sub(' ', self.base_name)
        return clean_name.strip()

class OptimizedSubtitleMatcher:
    """Optimized subtitle matching engine"""

    def __init__(self):
        self.directory = os.getcwd()
        self.video_files: Dict[str, FileInfo] = {}
        self.subtitle_files: Dict[str, FileInfo] = {}
        self.video_episodes: Dict[Tuple[int, int], str] = {}
        self.episode_to_video: Dict[str, str] = {}

    def scan_files(self):
        """Single-pass file scanning and categorization"""
        try:
            files = os.listdir(self.directory)
        except OSError as e:
            print(f"Error reading directory: {e}")
            return

        # Single pass through files
        video_exts = {'.mkv', '.mp4'}
        subtitle_exts = {'.srt', '.ass'}

        for filename in files:
            _, ext = os.path.splitext(filename)
            ext_lower = ext.lower()

            if ext_lower in video_exts:
                file_info = FileInfo(filename, True)
                self.video_files[filename] = file_info

                # Build episode reference for context-aware matching
                if file_info.episode_string and file_info.season and file_info.episode:
                    key = (int(file_info.season), int(file_info.episode))
                    if key not in self.video_episodes:  # First occurrence priority
                        self.video_episodes[key] = file_info.episode_string
                        self.episode_to_video[file_info.episode_string] = filename

            elif ext_lower in subtitle_exts:
                file_info = FileInfo(filename, False)
                self.subtitle_files[filename] = file_info

    def find_movie_match(self, video_files: List[str], subtitle_files: List[str]) -> Optional[Tuple[str, str]]:
        """Optimized movie matching logic"""
        if len(video_files) != 1 or len(subtitle_files) != 1:
            return None

        video_file = video_files[0]
        subtitle_file = subtitle_files[0]

        video_info = self.video_files[video_file]
        subtitle_info = self.subtitle_files[subtitle_file]

        # Fast year matching
        video_year_match = EpisodePatterns.YEAR_PATTERN.search(video_file)
        subtitle_year_match = EpisodePatterns.YEAR_PATTERN.search(subtitle_file)

        video_year = video_year_match.group() if video_year_match else None
        subtitle_year = subtitle_year_match.group() if subtitle_year_match else None

        # Years match - high confidence
        if video_year and subtitle_year and video_year == subtitle_year:
            return (video_file, subtitle_file)

        # Fallback to word matching
        video_words = set(video_info.get_clean_name().lower().split())
        subtitle_words = set(subtitle_info.get_clean_name().lower().split())

        # Remove quality indicators
        video_words -= EpisodePatterns.QUALITY_INDICATORS
        subtitle_words -= EpisodePatterns.QUALITY_INDICATORS

        if video_words and subtitle_words:
            common_words = video_words.intersection(subtitle_words)
            match_ratio = len(common_words) / min(len(video_words), len(subtitle_words))

            if match_ratio >= 0.3 or len(common_words) > 0:
                return (video_file, subtitle_file)

        return None

    def generate_unique_name(self, base_name: str, extension: str, original_subtitle: str) -> str:
        """Generate unique filename to avoid conflicts"""
        new_name = f"{base_name}.ar{extension}"
        new_path = os.path.join(self.directory, new_name)

        if not os.path.exists(new_path):
            return new_name

        # Create specific name using original subtitle info
        original_base = os.path.splitext(original_subtitle)[0]
        original_cleaned = re.sub(r'[._\-\s]*[Ss]ub(title)?[._\-\s]*', '', original_base, re.IGNORECASE)

        if not original_cleaned:
            original_cleaned = original_base

        specific_new_name = f"{base_name}.ar_{original_cleaned}{extension}"
        specific_new_name = re.sub(r'[<>:"/\|?*]', '_', specific_new_name)

        new_path = os.path.join(self.directory, specific_new_name)
        counter = 1

        while os.path.exists(new_path):
            name_part, ext_part = os.path.splitext(specific_new_name)
            specific_new_name = f"{name_part}_{counter}{ext_part}"
            new_path = os.path.join(self.directory, specific_new_name)
            counter += 1

        return specific_new_name

    def rename_subtitles(self) -> int:
        """Optimized subtitle renaming with single-pass processing"""
        print(f"\nFILES FOUND: {len(self.video_files)} videos | {len(self.subtitle_files)} subtitles")
        print("="*60)

        if self.video_files:
            video_list = list(self.video_files.keys())
            print(f"Videos: {video_list[:4]}{'...' if len(video_list) > 4 else ''}")

        if self.subtitle_files:
            subtitle_list = list(self.subtitle_files.keys())
            print(f"Subtitles: {subtitle_list[:4]}{'...' if len(subtitle_list) > 4 else ''}")

        print()

        if self.video_episodes:
            print("PROCESSING VIDEOS:")
            print("-" * 40)
            episode_patterns = list(self.video_episodes.values())
            print(f"EPISODE PATTERNS DETECTED: {episode_patterns[:10]}{'...' if len(episode_patterns) > 10 else ''}")
            print()

        renamed_count = 0
        remaining_videos = []
        remaining_subtitles = []

        print("PROCESSING SUBTITLES:")
        print("-" * 40)

        # Process subtitles with optimized matching
        for subtitle_name in sorted(self.subtitle_files.keys()):
            subtitle_info = self.subtitle_files[subtitle_name]

            if not subtitle_info.episode_string:
                remaining_subtitles.append(subtitle_name)
                print(f"NO EPISODE: '{subtitle_name}' -> could not detect episode number")
                continue

            # Context-aware episode matching
            adjusted_episode = self._get_adjusted_episode(subtitle_info)

            if adjusted_episode in self.episode_to_video:
                target_video = self.episode_to_video[adjusted_episode]
                base_name = os.path.splitext(target_video)[0]

                new_name = self.generate_unique_name(base_name, subtitle_info.extension, subtitle_name)

                old_path = os.path.join(self.directory, subtitle_name)
                new_path = os.path.join(self.directory, new_name)

                try:
                    os.rename(old_path, new_path)
                    if "CONFLICT RESOLVED" in new_name or "_" in new_name.split(".ar")[1]:
                        print(f"CONFLICT RESOLVED: Multiple subtitles match '{target_video}' -> renamed '{subtitle_name}' to unique name '{new_name}'")
                    else:
                        print(f"RENAMED: '{subtitle_name}' -> '{new_name}'")
                    renamed_count += 1
                except OSError as e:
                    print(f"ERROR: Could not rename '{subtitle_name}': {e}")
            else:
                print(f"NO MATCH: '{subtitle_name}' -> episode {subtitle_info.episode_string} has no matching video")

        print("-" * 40)
        print()

        # Collect remaining videos (those without matched subtitles)
        for video_name, video_info in self.video_files.items():
            if not video_info.episode_string:
                remaining_videos.append(video_name)

        # Movie matching logic
        if renamed_count == 0 and len(remaining_videos) == 1 and len(remaining_subtitles) == 1:
            movie_match = self.find_movie_match(remaining_videos, remaining_subtitles)

            if movie_match:
                video_file, subtitle_file = movie_match
                base_name = os.path.splitext(video_file)[0]
                subtitle_ext = os.path.splitext(subtitle_file)[1]
                new_name = f"{base_name}.ar{subtitle_ext}"

                old_path = os.path.join(self.directory, subtitle_file)
                new_path = os.path.join(self.directory, new_name)

                try:
                    os.rename(old_path, new_path)
                    print("MOVIE MODE: Found potential movie match!")
                    print(f"RENAMED: '{subtitle_file}' -> '{new_name}'")
                    renamed_count += 1
                except OSError as e:
                    print(f"ERROR: Could not rename '{subtitle_file}': {e}")
            else:
                print("MOVIE MODE: No movie-subtitle match found.")
        elif len(remaining_videos) > 1:
            print(f"MOVIE MODE: {len(remaining_videos)} video files detected -> skipping movie matching logic.")

        return renamed_count

    def _get_adjusted_episode(self, subtitle_info: FileInfo) -> str:
        """Get context-aware adjusted episode string"""
        if not subtitle_info.season or not subtitle_info.episode:
            return subtitle_info.episode_string

        key = (int(subtitle_info.season), int(subtitle_info.episode))

        if key in self.video_episodes:
            adjusted = self.video_episodes[key]
            if adjusted != subtitle_info.episode_string:
                print(f"Context adjustment: {subtitle_info.name} has {subtitle_info.episode_string} but using {adjusted} pattern")
            return adjusted

        return subtitle_info.episode_string

    def print_analysis_summary(self):
        """Print analysis summary with optimized data collection"""
        print("\nANALYSIS SUMMARY:")
        print("="*60)

        # Collect matched and unmatched episodes
        found_matches = set()
        not_found_episodes = set()
        unidentified_files = []

        # Process subtitles to find matches
        for subtitle_name, subtitle_info in self.subtitle_files.items():
            if subtitle_info.episode_string:
                adjusted_episode = self._get_adjusted_episode(subtitle_info)
                if adjusted_episode in self.episode_to_video:
                    found_matches.add(adjusted_episode)
                else:
                    not_found_episodes.add(adjusted_episode)
            else:
                unidentified_files.append(subtitle_name)

        # Add unmatched videos
        for video_name, video_info in self.video_files.items():
            if video_info.episode_string and video_info.episode_string not in found_matches:
                not_found_episodes.add(video_info.episode_string)
            elif not video_info.episode_string:
                unidentified_files.append(video_name)

        # Display results
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

    def export_analysis_to_csv(self):
        """Export analysis with optimized data processing"""
        all_files = list(self.video_files.keys()) + list(self.subtitle_files.keys())

        identified_files = []
        unidentified_files = []

        # Single pass through all files
        for filename in all_files:
            if filename in self.video_files:
                file_info = self.video_files[filename]
            else:
                file_info = self.subtitle_files[filename]

            if file_info.episode_string:
                # Apply context-aware adjustment for subtitles
                if not file_info.is_video:
                    adjusted_episode = self._get_adjusted_episode(file_info)
                    season, episode = self._extract_numbers_from_string(adjusted_episode)
                else:
                    season, episode = file_info.season, file_info.episode

                season_display = season if season else "(None)"
                episode_display = episode if episode else "(None)"
                formatted_output = f"{filename} >> S{season_display}E{episode_display}"

                identified_files.append({
                    'filename': filename,
                    'formatted_output': formatted_output
                })
            else:
                unidentified_files.append(filename)

        # Write to CSV file
        txt_filename = "renaming_report.csv"
        txt_path = os.path.join(self.directory, txt_filename)

        try:
            with open(txt_path, 'w', encoding='utf-8') as txtfile:
                txtfile.write("FILENAME.EXTENSION >> IDENTIFIED SEASON#EPISODE#\n")

                for file_info in sorted(identified_files, key=lambda x: x['filename']):
                    txtfile.write(file_info['formatted_output'] + '\n')

                for filename in sorted(unidentified_files):
                    txtfile.write(f"{filename} >> S(None)E(None)\n")

                if identified_files or unidentified_files:
                    txtfile.write('\n')

                # Add summary sections
                self._write_csv_summary(txtfile)

            print(f"\nExported file renaming records to:")
            print(f"{txt_path}\n")

        except OSError as e:
            print(f"Error writing CSV file: {e}")

    def _extract_numbers_from_string(self, episode_string: str) -> Tuple[str, str]:
        """Extract season/episode numbers from episode string"""
        if not episode_string:
            return '', ''

        season_match = re.search(r'S(\d+)', episode_string)
        episode_match = re.search(r'E(\d+)', episode_string)

        return (season_match.group(1) if season_match else '',
                episode_match.group(1) if episode_match else '')

    def _write_csv_summary(self, txtfile):
        """Write summary sections to CSV file"""
        # Collect matched and unmatched episodes
        found_matches = set()
        not_found_episodes = set()
        unidentified_files = []

        # Process subtitles to find matches
        for subtitle_name, subtitle_info in self.subtitle_files.items():
            if subtitle_info.episode_string:
                adjusted_episode = self._get_adjusted_episode(subtitle_info)
                if adjusted_episode in self.episode_to_video:
                    found_matches.add(adjusted_episode)
                else:
                    not_found_episodes.add(adjusted_episode)
            else:
                unidentified_files.append(subtitle_name)

        # Add unmatched videos
        for video_name, video_info in self.video_files.items():
            if video_info.episode_string:
                # Check if this video episode has a matching subtitle
                has_subtitle_match = False
                if video_info.season and video_info.episode:
                    key = (int(video_info.season), int(video_info.episode))
                    
                    for subtitle_name, subtitle_info in self.subtitle_files.items():
                        if subtitle_info.season and subtitle_info.episode:
                            sub_key = (int(subtitle_info.season), int(subtitle_info.episode))
                            if sub_key == key:
                                has_subtitle_match = True
                                break
                
                if not has_subtitle_match:
                    not_found_episodes.add(video_info.episode_string)
            elif video_info.name not in [sub.name for sub in self.subtitle_files.values()]:
                unidentified_files.append(video_name)

        # Write found matches results
        if found_matches:
            txtfile.write("FOUND AND RENAMED MATCHING SUBTITLE AND VIEDEO FILES FOR THESE EPISODES:\n")
            for episode in sorted(found_matches):
                txtfile.write(f"- {episode}\n")
            txtfile.write('\n')
        
        # Write not found results
        if not_found_episodes:
            txtfile.write("COULDN'T FIND MATCHING SUBTITLE AND VIEDEO FILES FOR THESE EPISODES:\n")
            for episode in sorted(not_found_episodes):
                if episode != "(None)":
                    txtfile.write(f"- {episode}\n")
            txtfile.write('\n')
        
        # Write unidentified files summary
        if unidentified_files:
            txtfile.write("COULDNT IDENTIFY SEASON#EPISODE# FOR THESE FILES:\n")
            for filename in sorted(set(unidentified_files)):
                txtfile.write(f"- {filename}\n")


def rename_subtitles_to_match_videos():
    """Main optimized function"""
    matcher = OptimizedSubtitleMatcher()
    matcher.scan_files()

    renamed_count = matcher.rename_subtitles()

    print("="*60)
    total_subtitles = len(matcher.subtitle_files)

    if renamed_count > 0:
        print(f"COMPLETED TASK: {renamed_count} subtitle file{'s' if renamed_count != 1 else ''} renamed out of {total_subtitles}")
    else:
        print("INFO: No files were renamed.")

    print("="*60)

    matcher.print_analysis_summary()

def export_analysis_to_csv():
    """Optimized CSV export function"""
    matcher = OptimizedSubtitleMatcher()
    matcher.scan_files()
    matcher.export_analysis_to_csv()

if __name__ == "__main__":
    # Export analysis BEFORE renaming
    export_analysis_to_csv()

    # Perform renaming
    rename_subtitles_to_match_videos()
