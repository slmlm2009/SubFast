# Subtitle Renamer Tool [AR]

A powerful Python script that automatically renames subtitle files to match their corresponding video files, with intelligent episode detection and Windows context menu integration.

## Features

### Core Functionality
- **Automatic subtitle renaming** to match video files with `.ar` suffix
- **Multi-format support** for video files (`.mkv`, `.mp4`) and subtitles (`.srt`, `.ass`)
- **Intelligent episode detection** supporting 15+ naming patterns
- **Context-aware matching** handles inconsistent zero-padding between files
- **Movie mode** for single video/subtitle pairs
- **Collision handling** prevents file overwrites with smart naming

### Episode Pattern Recognition
The script recognizes various episode naming conventions:
- `S##E##` (e.g., S01E05, S2E15)
- `##x##` (e.g., 2x05, 1x10)
- `Season # Episode #` (with various separators)
- `S##Ep##` / `SeasonXEpY` formats
- `E##` / `Ep##` patterns (assumes Season 1)
- `- ##` patterns for simple numbering
- And many more variations with flexible spacing and separators

### Windows Integration (v2.0.0+)
- **Right-click context menu** integration
- **Custom icon** for professional appearance
- **One-click execution** from Windows Explorer
- **Registry files** for easy installation/removal

### Advanced Features
- **Detailed reporting** with analysis summaries
- **CSV export** functionality for record keeping
- **Alphabetical prioritization** for consistent behavior
- **Edge case handling** tested across 65+ scenarios

## Installation

### Method 1: Windows Context Menu Integration (Recommended)

1. **Download and Extract**
   ```
   Download the latest release ZIP file
   Extract to C:\rename_subtitles_to_match_videos_ar\
   ```

2. **Install Context Menu**
   ```
   Double-click add_subtitle_rename_menu.reg
   Approve the security warning when prompted
   ```

3. **Verify Installation**
   - Navigate to any folder
   - Right-click in empty space
   - Look for "Rename subtitle files" option

### Method 2: Manual Python Execution

1. **Prerequisites**
   ```bash
   Python 3.x installed
   Download the script file
   ```

2. **Usage**
   ```bash
   cd /path/to/your/video/folder
   python rename_subtitles_to_match_videos_ar_v2.0.0.py
   ```

## Usage

### Windows Context Menu (v2.0.0+)
1. Navigate to folder containing video and subtitle files
2. Right-click in empty folder space
3. Select "Rename subtitle files"
4. Script runs automatically and shows results

### Command Line
1. Open terminal/command prompt
2. Navigate to folder with video and subtitle files
3. Run the Python script
4. Review the detailed output and analysis

## How It Works

### File Processing
1. **Scans directory** for video and subtitle files
2. **Extracts episode information** using pattern matching
3. **Creates mapping** between episodes and video files
4. **Applies context-aware standardization** for consistent matching
5. **Renames subtitles** to match video file names with `.ar` suffix

### Example Transformations
```
Before:
├── Show.Name.S01E05.1080p.mkv
├── Show.Name.S01E06.1080p.mkv
├── subtitle-05.srt
└── subtitle-06.srt

After:
├── Show.Name.S01E05.1080p.mkv
├── Show.Name.S01E05.1080p.ar.srt
├── Show.Name.S01E06.1080p.mkv
└── Show.Name.S01E06.1080p.ar.srt
```

### Smart Matching Examples
The script handles various inconsistencies:
- `S02E015` (video) ↔ `S02E15` (subtitle) → Matched
- `2x05` (video) ↔ `S02E05` (subtitle) → Matched  
- `Season 1 Episode 3` ↔ `S01E03` → Matched

## Supported File Formats

### Video Files
- `.mkv` (Matroska Video)
- `.mp4` (MPEG-4 Video)

### Subtitle Files
- `.srt` (SubRip Text)
- `.ass` (Advanced SubStation Alpha)

## Configuration

The script works out-of-the-box with no configuration required. However, you can modify the source code to:
- Add support for additional file formats
- Customize the subtitle suffix (default: `.ar`)
- Modify episode detection patterns
- Adjust collision handling behavior

## Troubleshooting

### Context Menu Not Appearing
1. Ensure you have administrator privileges
2. Verify the registry file was applied successfully
3. Try logging out and back in to refresh Explorer
4. Check that the script path in the registry matches your installation

### Python Not Found Error
1. Verify Python 3.x is installed
2. Ensure Python Launcher (`py.exe`) is in `C:\Windows\py.exe`
3. Try running from command line first to test Python accessibility

### No Files Renamed
1. Check that video and subtitle files are in the same directory
2. Verify file naming patterns are supported
3. Review the detailed output for pattern detection results
4. Use the CSV export feature to analyze detection results

### Pattern Not Recognized
The script supports many patterns, but if yours isn't recognized:
1. Check the analysis output to see what was detected
2. Consider renaming files to use a supported pattern
3. Modify the `get_episode_number()` function to add custom patterns

## Technical Details

### Requirements
- **Operating System**: Windows (for context menu integration)
- **Python Version**: 3.x
- **Dependencies**: None (uses only standard library)
- **Permissions**: Administrator access for registry modification (one-time)

### File Structure
```
rename_subtitles_to_match_videos_ar/
├── rename_subtitles_to_match_videos_ar_v2.0.0.py
├── add_subtitle_rename_menu.reg
├── remove_subtitle_rename_menu.reg
├── ARAB_STREAMS_LOGO.ico
└── VERSION2__OVERVIEW.md
```

### Performance
- Processes hundreds of files in seconds
- Memory efficient with minimal system impact
- Safe operation with comprehensive error handling

## Contributing

This tool has been extensively tested across 65+ different scenarios. If you encounter issues or have suggestions for additional episode patterns, please:

1. Test the current version thoroughly
2. Provide specific examples of unsupported patterns
3. Include sample file names that demonstrate the issue
4. Consider contributing regex patterns for new formats

## Version History

### v2.0.0 (Current)
- Windows context menu integration
- Enhanced pattern recognition (15+ formats)
- Context-aware episode matching
- Movie mode detection
- Comprehensive collision handling
- Detailed analysis and reporting
- CSV export functionality

### v1.0.0
- Basic episode detection
- Simple S##E## and - ## patterns
- Command-line only operation
- Basic file renaming functionality

## License

This project is released as open source. Feel free to modify and distribute according to your needs.

## Support

For issues, questions, or feature requests, please provide:
- Your operating system and Python version
- Sample file names that demonstrate the issue
- Complete error messages or unexpected behavior
- Steps to reproduce the problem

The script includes detailed logging and analysis output to help diagnose issues quickly.