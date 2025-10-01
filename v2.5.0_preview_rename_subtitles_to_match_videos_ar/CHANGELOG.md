# Changelog

All notable changes to the subtitle renaming script will be documented in this file.

## [v2.5.0-preview] - 2025-01-10

### Added
- **Full Configuration System** via `config.ini`
  - Configurable language suffix (default: `.ar`)
  - Configurable video file formats (default: `.mkv`, `.mp4`)
  - Configurable subtitle file formats (default: `.srt`, `.ass`)
  - CSV export enable/disable control
  - Automatic config file generation with defaults
  - Validation with fallback to defaults

- **Enhanced CSV Export**
  - Professional summary statistics header
  - Original filename preservation (shows names before renaming)
  - Clear, self-documenting label names
  - Granular reporting (videos vs subtitles separated)
  - Match analysis with both video and subtitle filenames
  - Excel-compatible formatting
  - Execution time tracking in CSV

- **Performance Tracking**
  - Execution time measurement with human-readable formatting
  - Console PERFORMANCE section showing time, files processed, and rename count
  - CSV report includes execution time for benchmarking

- **Improved Console Output**
  - PERFORMANCE summary section
  - Clean "X/Y" format for renamed subtitle count
  - Proper separator placement matching template

### Fixed
- **Hotfix: ##x## Pattern Resolution Conflict**
  - Restricted season matching to 1-2 digits (seasons 1-99 only)
  - Prevents false matches with resolution information (1920x1080, 1280x720, etc.)
  - Maintains backward compatibility for all valid episodes
  - Tested with files containing resolution info in filenames

### Changed
- **CSV Export Improvements**
  - Changed "Unmatched Videos" → "Videos Missing Subtitles"
  - Changed "Unmatched Subtitles" → "Subtitles Missing Videos"
  - Split "Unidentified Files" → "Videos Without Episode Pattern" + "Subtitles Without Episode Pattern"
  - Changed "UNIDENTIFIED FILES:" → "FILES WITHOUT EPISODE PATTERN:"
  - Fixed unmatched subtitles calculation to use arithmetic instead of dictionary lookup
  - Added subtitle filename lookup in MISSING MATCHES section

- **Documentation Updates**
  - Updated GEMINI.md to reflect configurable nature
  - Emphasized that language suffix and formats are no longer hard-coded
  - Added comprehensive CSV export documentation
  - Documented all label improvements and clarifications
  - Added configuration system details

### Technical Improvements
- Implemented rename tracking system to preserve original filenames
- Added comprehensive validation for configuration values
- Created automated config file generation system
- Enhanced error handling and user feedback
- Optimized pattern matching for better performance

## [v2.0.0] - Previous Versions

### Features
- Episode pattern detection (S##E##, ##x##, Season.Episode, etc.)
- Context-aware matching for proper episode identification
- Movie mode for single video + subtitle matching
- Collision handling with unique naming
- Alphabetical prioritization for deterministic behavior
- CSV export functionality (basic)

---

**Note:** This project maintains version history starting from v2.5.0-preview. Earlier versions are documented in commit history.
