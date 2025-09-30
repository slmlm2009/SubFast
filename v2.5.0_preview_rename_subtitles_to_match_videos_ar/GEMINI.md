# Subtitle Renaming Script - Documentation

## Overview
This script automatically renames subtitle files (.srt, .ass) to match their corresponding video files (.mkv, .mp4) based on episode patterns found in the filenames then will add .ar before the subtitle extension to specify the language of the subtitle in video players as this script was originally made for ARAB STREAM media community. 
The script handles various naming conventions and provides context-aware matching for proper episode identification.

## Features
- **Multi-format Support**: Handles both .srt and .ass subtitle files with .mkv and .mp4 video files
- **Advanced Pattern Detection**: Recognizes various episode naming patterns including S01E01, 2x05, Season.Episode, etc.
- **Context-Aware Matching**: Correctly matches episodes with different padding (S02E015 vs S02E15)
- **Single-Digit Episode Support**: Detects and handles single-digit episodes (E6, Ep7, etc.)
- **Movie Matching**: Attempts to match subtitles to movies based on filename similarity
- **Year-Based Matching**: Considers year information for better movie matching accuracy
- **Enhanced Terminal Output**: Clear and formatted output with status indicators
- **Analysis Summary**: Shows detailed breakdown of matches, non-matches, and unidentified files
- **Collision Handling**: Prevents file overwrites when multiple subtitles match the same video
- **Alphabetical Prioritization**: Ensures deterministic behavior when multiple files match

## File Selection Prioritization

When multiple files match the same criteria, the script uses **alphabetical order** to ensure deterministic selection:

### Video File Selection
- When multiple video files match the same episode pattern, the alphabetically first video file is selected as the target
- This ensures consistent behavior when multiple videos represent the same episode
- Context-aware matching uses the first video alphabetically as the pattern standard

### Subtitle File Processing
- Subtitle files are processed in alphabetical order to ensure consistent renaming behavior
- When multiple subtitles match the same video, the alphabetically first subtitle gets the standard `.ar` name
- Subsequent matching subtitles receive unique names incorporating their original names

## Handling Edge Cases

The script handles several edge cases with clear messaging:

### Multiple Subtitles for One Video
- When multiple subtitle files match the same video, the alphabetically first subtitle gets the standard `.ar` name
- Subsequent matching subtitles receive unique names incorporating their original names
- A "CONFLICT RESOLVED" message indicates when this handling occurs

### Multiple Subtitles for Multiple Videos  
- When multiple subtitle files match multiple video files that resolve to the same episode pattern, the same unique naming approach is used
- The first video alphabetically establishes the pattern; first subtitle alphabetically gets the standard name, others get unique identifiers

### One Subtitle for Multiple Videos
- When one subtitle matches multiple videos, the alphabetically first matching video is selected
- The subtitle is renamed to match that specific video

## Supported Episode Patterns
- `S##E##` (e.g., S01E01, s02e15)
- `##x##` (e.g., 2x05, 12x03)
- `Season.Episode` (e.g., Season.1.Episode.05, season.2.episode.10)
- `S##.Episode##` (e.g., S01.Episode.05)
- `Season##Ep##` (e.g., Season2Ep15, ShowNameSeason2Episode15)
- `S##Ep##` (e.g., S01Ep05, S2Ep15)
- `Season##.Ep##` (e.g., Yes Season2.Ep160)
- `S##.Ep##` (e.g., Program Season2 Ep15)
- `Season## Episode##` (e.g., Show Name Season 3 Episode 8)
- `Season##Ep##` (e.g., ShowNameSeason2Episode15)
- `E##` patterns (e.g., ShowName E5, ShowName E10)
- `Ep##` patterns (e.g., ShowName Ep8, ShowName Episode12)
- `- ##` patterns (e.g., ShowName - 1, ShowName -10)

## How It Works
1. **Pattern Analysis**: Scans all video files to identify episode patterns
2. **Context Building**: Creates a reference for context-aware matching (alphabetically first video establishes pattern)
3. **Subtitle Processing**: Matches subtitles to videos based on episode numbers
4. **Collision Handling**: Prevents overwrites by creating unique names for conflicting subtitles
5. **Renaming**: Renames subtitles to match the base filename of their corresponding video with `.ar` extension
6. **Movie Mode**: If no episodes match and there's only 1 video and 1 subtitle, attempts movie-style matching

## Output Format
- Renamed subtitles: `{video_base_name}.ar{subtitle_extension}`
- Example: `Show.S01E05.mkv` + `subtitles.srt` → `Show.S01E05.ar.srt`
- For conflicts: `{video_base_name}.ar_{original_sub_name}{subtitle_extension}`
- Example: `Show.S01E05.ar_Subtitle2.srt`

## Terminal Output Features
- Clear section dividers with "=" and "-" lines
- Detailed status for each processing step (CONTEXT ADJUSTMENT, RENAMED, NO MATCH, etc.)
- "CONFLICT RESOLVED" messages for collision handling
- Summary statistics at the end
- Analysis breakdown showing:
  - Episodes with successful matches
  - Episodes without matches
  - Files with no detectable episode information

## CSV Export Function
- Creates a renaming report in template format at the beginning of execution
- Shows file-by-file episode detection
- Categorizes results by match status
- Uses original file names before any renaming
- Filename: `renaming_report.csv`

## Configuration
- The CSV renaming report export can be enabled/disabled by commenting out the export_analysis_to_csv function in the main execution block.

## Key Functions
- `get_episode_number(filename)`: Extracts episode pattern from filename
- `rename_subtitles_to_match_videos()`: Main processing function
- `find_movie_subtitle_match()`: Handles movie-style matching
- `export_analysis_to_csv()`: Generates detailed analysis report

## Error Handling
- Handles cases with no matching files gracefully
- Skips movie matching when multiple video files exist
- Prevents file overwrites with collision handling
- Maintains all original functionality while adding new features