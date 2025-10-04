# Subtitle Renamer Tool [AR]

A powerful Python script that automatically renames subtitle files to match their corresponding video files, with intelligent episode detection, full configuration support, and Windows context menu integration.

## Features

### Core Functionality
- **Automatic subtitle renaming** to match video files with configurable language suffix
- **Multi-format support** for video and subtitle files (fully configurable)
- **Intelligent episode detection** supporting *MANY* naming patterns
- **Context-aware matching** handles inconsistent zero-padding between files
- **Movie mode** for single video/subtitle pairs
- **Collision handling** prevents file overwrites with smart naming
- **Configuration system** via `config.ini` for customization
- **Performance oriented** with caching and regex precombilation optimizations achivieng multible folds speed improvements on large datasets compared to basic python scripting

### Episode Pattern Recognition
The script recognizes various episode naming conventions:
- `S##E##` (e.g., S01E05, S2E15)
- `##x##` (e.g., 2x05, 1x10) - with smart resolution detection
- `S## - ##` / `S## - E##` / `S## - EP##` formats
- `Season # Episode #` (with various separators)
- `S##Ep##` / `SeasonXEpY` formats
- Ordinal season patterns: `1st Season`, `2nd Season`, etc.
  - With dash: `ShowName 1st Season - 05.mkv`
  - With E: `ShowName 2nd Season E10.srt`
  - With EP: `ShowName 3rd Season EP8.mp4`
- `E##` / `Ep##` patterns (assumes Season 1)
- `- ##` patterns for simple numbering
- And many more variations with flexible spacing and separators

### Windows Right-Click Context Menu Integration (v2.0.0+)
![Demo_GIF](https://i.imgur.com/7y839Yy.gif)
- **Right-click context menu** integration
- **Custom icon** for professional appearance
- **One-click execution** from Windows Explorer
- **Registry files** for easy installation/removal

### Configuration System (v2.5.0+)
- **config.ini support** for customization
- **Configurable language suffix** (ar, en, fr, es, etc.)
- **Configurable file formats** for videos and subtitles
- **CSV export control** (enable/disable)
- **Auto-generation** of default config on first run
- **Safe fallbacks** for invalid configurations

### Advanced Features
- **Renaming Report CSV export** with execution time tracking and detailed statistics
- **Edge case handling** tested across 65+ scenarios
- **Episode number caching** for 12x faster performance on large datasets

## Installation and Usage ##
*Step-by-step video walkthrough for v2.0.0 (Arabic):*  
*https://www.youtube.com/watch?v=et1uv5DbEmA&t=12s*


### Method 1: Windows Context Menu Integration (Recommended)

1. **Prerequisites**
   ```
   Python 3.x installed and added to PATH
   Python Launcher (`py.exe`) is in `C:\Windows\py.exe`
   ```
2. **Download and Extract**
   ```
   Download the latest release ZIP file
   Extract "rename_subtitles_to_match_videos_ar" folder to C:\
   Ensure script path is `C:\rename_subtitles_to_match_videos_ar\rename_subtitles_to_match_videos_ar.py` 
   ```

3. **Install Context Menu**
   ```
   Double-click add_subtitle_rename_menu.reg inside "rename_subtitles_to_match_videos_ar" folder
   Approve the security warning when prompted
   ```

4. **Verify Installation**
   - Navigate to any folder
   - Right-click in empty space
   - Look for "Rename subtitle files" option

5. **Usage**
   ```
   Navigate to folder containing video and subtitle files
   Right-click in empty folder space
   Select "Rename subtitle files"
   Script runs automatically and shows results
   ```

### Method 2: Manual Python Execution through Python Launcher

1. **Prerequisites**
   ```
   Python 3.x installed and added to PATH
   Python Launcher (`py.exe`) is in `C:\Windows\py.exe`
   ```

2. **Usage**
   ```
   copy "rename_subtitles_to_match_videos_ar.py" to \path\to\your\media\folder
   double click "rename_subtitles_to_match_videos_ar.py" and open with Python Launcher
   ```

### Method 3: Manual Python Execution through Command Line

1. **Prerequisites**
   ```
   Python 3.x installed and added to PATH
   Download the script file
   ```

2. **Usage**
   ```
   copy "rename_subtitles_to_match_videos_ar.py" to \path\to\your\media\folder
   cd \path\to\your\media\folder
   python .\rename_subtitles_to_match_videos_ar.py
   ```

## Configuration (v2.5.0+)

The script supports full customization via `config.ini` file placed in the same directory as the script.

### Auto-Configuration
On first run, the script automatically creates a `config.ini` file with default settings:
- Language suffix: `.ar`
- Video formats: `.mkv`, `.mp4`
- Subtitle formats: `.srt`, `.ass`
- CSV export: enabled

### Customization Options

**Edit `config.ini` to customize:**

```ini
[General]
enable_export = true          # Enable/disable CSV report generation
language_suffix = ar          # Language tag (ar, en, fr, es, etc. or keep empty if none required) 

[FileFormats]
video_extensions = mkv, mp4, avi, webm
subtitle_extensions = srt, ass, sub, vtt
```

### Example Use Cases

### Use Case 1: Regular use with Arabic Language Suffix [default]
```ini
[General]
enable_export = true
language_suffix = es

[FileFormats]
video_extensions = mkv, mp4
subtitle_extensions = srt
```

### Use Case 2: Batch Processing (Speed Priority)
```ini
[General]
enable_export = false          # Skip CSV for speed (14% improvement)
language_suffix = ar
video_extensions = mkv, mp4
subtitle_extensions = srt, ass
```

### Use Case 3: Maximum Format Support
```ini
[General]
enable_export = true
language_suffix = ar
video_extensions = mkv, mp4, avi, webm, mov, flv, m4v
subtitle_extensions = srt, ass, sub, vtt, ssa, smi
```

For detailed configuration documentation, see `CONFIGURATION_README.md` in the release package.

## How It Works

### File Processing
1. **Scans directory** for video and subtitle files
2. **Extracts episode information** using pattern matching
3. **Creates mapping** between episodes and video files
4. **Applies context-aware standardization** for consistent matching
5. **Renames subtitles** to match video file names with the configured language suffix

### Example Transformations
```
Before:
├── ShowName S01E05.1080p.mkv
├── ShowName S01E06.1080p.mkv
├── subtitle-05.srt
└── subtitle-06.srt

After:
├── ShowName S01E05.1080p.mkv
├── ShowName S01E05.1080p.ar.srt
├── ShowName S01E06.1080p.mkv
└── ShowName S01E06.1080p.ar.srt
```

### Smart Matching Examples
The script handles various inconsistencies:
- `S2E8` (video) ↔ `S02E008` (subtitle) → Matched
- `2x05` (video) ↔ `S02E05` (subtitle) → Matched  
- `Season 1 Episode 3` ↔ `S01E03` → Matched

## Supported File Formats

### Default Video Files
- `.mkv` (Matroska Video)
- `.mp4` (MPEG-4 Video)

### Default Subtitle Files
- `.srt` (SubRip Text)
- `.ass` (Advanced SubStation Alpha)

**Note:** File formats are fully configurable via `config.ini` (v2.5.0+). You can add support for `.avi`, `.webm`, `.mov`, `.flv`, `.sub`, `.vtt`, `.ssa`, `.smi`, and more.

## Advanced Customization

The script works out-of-the-box with no configuration required except of changing the language suffix if not Arabic user. For most users, the `config.ini` file (v2.5.0+) provides all necessary customization options. However, advanced users can modify the source code to:
- Add custom episode detection patterns
- Adjust collision handling behavior
- Modify matching algorithms
- Add new features or integrations

## Troubleshooting

### Context Menu Not Appearing
1. Restart explorer.exe process in Task Manager or log out and back in to refresh Explorer
2. Ensure you have administrator privileges and verify the registry file was applied successfully

### Python Not Found Error
1. Verify Python 3.x is installed
2. Ensure Python Launcher (`py.exe`) is in `C:\Windows\py.exe`
3. Try running from command line first to test Python accessibility

### No Files Renamed
1. Check that video and subtitle files are in the same directory
2. In case using the right-click context menue integration, ensure that the script path is `C:\rename_subtitles_to_match_videos_ar\rename_subtitles_to_match_videos_ar.py`
3. Verify file naming patterns are supported
5. Use the CSV export feature to analyze detection results

## Technical Details

### Requirements
- **Operating System**: Windows
- **Dependencies**:
1. Python 3.x installed and added to PATH
2. Python Launcher (`py.exe`) is in `C:\Windows\py.exe`
- **Permissions**: Administrator access for registry modification (one-time)

### File Structure
```
rename_subtitles_to_match_videos_ar/
├── rename_subtitles_to_match_videos_ar.py
├── config.ini
├── add_subtitle_rename_menu.reg
├── remove_subtitle_rename_menu.reg
├── ARAB_STREAMS_LOGO.icon
└── CONFIGURATION_README.md
```

### Performance
- Processes 1000+ files in under 1 second (optimized via episode number caching)
- Safe operation with comprehensive error handling
- Execution time tracking with human-readable formatting
- Optional CSV export disable for 14% additional speed boost

## Contributing

This tool has been extensively tested across 65+ different scenarios. If you encounter issues or have suggestions for additional episode patterns, please:

1. Test the current version thoroughly
2. Open an issue and provide specific examples of unsupported patterns
3. Include naming_report.csv that demonstrates the issue
4. Consider contributing regex patterns for new formats

## Version History

### v2.5.0 (Current - October 2025)
- **Configuration system** via config.ini
- **9 new episode patterns** (25+ total patterns)
  - `S## - ##` / `S## - E##` / `S## - EP##` formats
  - Ordinal season patterns (1st/2nd/3rd Season)
- **12x performance improvement** via episode number caching
- **Enhanced CSV export** with original filename tracking and execution time
- **Configurable language suffix** and file formats
- **Smart resolution detection** (fixes ##x## pattern conflicts)
- **Performance tracking** with detailed metrics
- Bug fixes for negative count display and pattern conflicts
- Memory usage optimization (42% reduction)

### v2.0.0
- Windows context menu integration
- Enhanced pattern recognition (15+ formats)
- Context-aware episode matching
- Movie mode detection
- Comprehensive collision handling
- Detailed analysis and reporting
- Basic CSV export functionality

### v1.0.0
- Basic episode detection
- Simple S##E## and - ## patterns
- Command-line only operation
- Basic file renaming functionality

## License

This project is released as open source. Feel free to modify and distribute according to your needs.

## Support and Contributing
- Test the latest version thoroughly
- Open an issue and provide specific examples of unsupported patterns or unintended behaviour
- Include naming_report.csv that demonstrates the issue
- Consider contributing regex patterns for new formats

