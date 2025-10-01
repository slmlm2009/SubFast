# Subtitle Renaming Script - Documentation

## Overview
This script automatically renames subtitle files to match their corresponding video files based on episode patterns found in the filenames, then adds a configurable language suffix before the subtitle extension to specify the language in video players.

Originally created for the ARAB STREAM media community with `.ar` as the default language suffix, the script is now **fully configurable** through a `config.ini` file that allows customization of:
- **Language suffix** (default: `.ar` for Arabic)
- **Video file formats** (default: `.mkv`, `.mp4`)
- **Subtitle file formats** (default: `.srt`, `.ass`)
- **CSV export** (default: enabled)

The script handles various naming conventions and provides context-aware matching for proper episode identification.

## Features
- **Fully Configurable**: Customize language suffix, video formats, and subtitle formats via `config.ini`
- **Multi-format Support**: Default support for .srt and .ass subtitle files with .mkv and .mp4 video files (easily expandable)
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
- `##x##` (e.g., 2x05, 12x03) - seasons 1-99 only to avoid resolution conflicts (1920x1080, 1280x720, etc.)
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

The script generates a comprehensive CSV report (`renaming_report.csv`) with professional formatting and detailed statistics:

### Report Structure
1. **Summary Header**
   - Timestamp of execution
   - Working directory path
   - Configuration settings (language suffix, file formats, export status)

2. **Summary Statistics**
   - Total Videos / Total Subtitles
   - Renamed subtitles (X/Y format)
   - Videos Missing Subtitles (videos without matching subtitles)
   - Subtitles Missing Videos (subtitles without matching videos)
   - Videos Without Episode Pattern (unidentified videos)
   - Subtitles Without Episode Pattern (unidentified subtitles)
   - Movie Mode status
   - Execution Time (with human-readable formatting)

3. **File Analysis Table**
   - CSV format showing: Original Filename, Detected Episode, New Name, Action
   - Uses original filenames before any renaming occurred
   - Shows episode pattern detected or (UNIDENTIFIED) for files without patterns

4. **Matched Episodes Section**
   - Lists all successful video-subtitle pairings
   - Shows original subtitle name → renamed subtitle name

5. **Missing Matches Section**
   - Videos that have no matching subtitles (shows video filename)
   - Subtitles that have no matching videos (shows subtitle filename)

6. **Files Without Episode Pattern Section**
   - Lists all files where no episode pattern could be detected
   - Includes both videos and subtitles

### Key Features
- **Original Filenames**: Always shows filenames before renaming for accurate tracking
- **Clear Labels**: Self-documenting statistics that explain what each number represents
- **Granular Reporting**: Separate counts for videos vs subtitles in each category
- **Accurate Calculations**: Proper math for unmatched counts (Total - Renamed - Unidentified)
- **Consistent Formatting**: Headers match summary label terminology
- **Complete Information**: Both video and subtitle filenames shown in MISSING MATCHES section
- **Excel Compatible**: Proper CSV format opens cleanly in spreadsheet applications

### Performance Tracking
The script tracks and displays execution time in both the console output and CSV report:
- Time format adapts to duration: "X.XX seconds", "Xm Y.YYs", or "Xh Ym Zs"
- Console shows PERFORMANCE section with execution time, files processed, and rename statistics
- CSV includes execution time in the summary for benchmarking and performance analysis

## Configuration
- The CSV renaming report export can be controlled via `config.ini`
- Set `enable_export = True` or `False` in the configuration file
- Other configurable options include language suffix, video formats, and subtitle formats
- Configuration file is auto-generated with defaults if not present

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