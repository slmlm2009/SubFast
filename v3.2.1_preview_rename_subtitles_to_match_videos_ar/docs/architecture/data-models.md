# Data Models

SubFast operates on file system objects without persistent data storage. The conceptual data models represent runtime structures used during processing.

## VideoFile

**Purpose:** Represents a video file discovered in the processing directory

**Attributes:**
- `path`: Path - Absolute path to video file
- `filename`: str - Base filename without extension
- `extension`: str - File extension (e.g., '.mkv', '.mp4')
- `episode_info`: Optional[EpisodeInfo] - Extracted episode information if detected
- `matched_subtitle`: Optional[SubtitleFile] - Associated subtitle file if match found

**Relationships:**
- One-to-zero-or-one with SubtitleFile (matched pair)

## SubtitleFile

**Purpose:** Represents a subtitle file discovered in the processing directory

**Attributes:**
- `path`: Path - Absolute path to subtitle file
- `filename`: str - Base filename without extension
- `extension`: str - File extension (e.g., '.srt', '.ass')
- `episode_info`: Optional[EpisodeInfo] - Extracted episode information if detected
- `detected_language`: Optional[str] - Language code extracted from filename
- `matched_video`: Optional[VideoFile] - Associated video file if match found

**Relationships:**
- One-to-zero-or-one with VideoFile (matched pair)

## EpisodeInfo

**Purpose:** Normalized episode identification extracted from filenames

**Attributes:**
- `season_number`: int - Normalized season number
- `episode_number`: int - Normalized episode number
- `pattern_matched`: str - Name of regex pattern that matched
- `raw_match`: str - Original matched string before normalization

**Example:**
```python
# "Show.S02E008.mkv" → EpisodeInfo(season=2, episode=8, pattern='S##E##', raw='S02E008')
# "Show.2x5.mkv" → EpisodeInfo(season=2, episode=5, pattern='##x##', raw='2x5')
```

## MatchedPair

**Purpose:** Validated video-subtitle pair ready for processing

**Attributes:**
- `video`: VideoFile
- `subtitle`: SubtitleFile
- `confidence`: str - Match confidence ('high' for episode match, 'movie' for single-pair)
- `target_name`: str - Calculated target filename for subtitle

**Operations:**
- Validates no filename collision before renaming
- Constructs complete target path with optional language suffix

## ProcessingResult

**Purpose:** Result of a single file operation (rename or embed)

**Attributes:**
- `source_video`: str - Original video filename
- `source_subtitle`: str - Original subtitle filename  
- `operation`: str - Operation type ('rename' or 'embed')
- `status`: str - Result status ('success', 'failed', 'skipped')
- `error_message`: Optional[str] - Error details if failed
- `execution_time`: float - Time taken in seconds

**Usage:**
- Collected for batch summary reporting
- Exported to CSV when reporting enabled

## Configuration

**Purpose:** Loaded and validated user configuration

**Attributes:**

**[General]**
- `detected_video_extensions`: List[str] - Video formats to process
- `detected_subtitle_extensions`: List[str] - Subtitle formats to process
- `keep_console_open`: bool - Console window behavior

**[Renaming]**
- `renaming_report`: bool - Enable CSV export for renaming
- `renaming_language_suffix`: str - Language suffix to append

**[Embedding]**
- `mkvmerge_path`: str - Path to mkvmerge.exe (resolved to absolute)
- `embedding_language_code`: str - Default language code for embedding
- `default_flag`: bool - Mark embedded subtitle as default track
- `embedding_report`: bool - Enable CSV export for embedding

**Validation:**
- Auto-generates missing config.ini with defaults
- Provides safe defaults for all invalid values
- Logs warnings for invalid settings

---
