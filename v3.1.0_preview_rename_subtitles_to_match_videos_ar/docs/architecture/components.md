# Components

## 1. Configuration Loader

**Responsibility:** Load, validate, and provide configuration settings with safe defaults

**Key Interfaces:**
```python
def load_config(config_path: Path) -> Configuration:
    """Load config.ini or generate with defaults if missing"""
    
def validate_extensions(extensions: str) -> List[str]:
    """Parse and validate comma-separated extensions"""
    
def validate_boolean(value: str) -> bool:
    """Parse boolean configuration value"""
```

**Dependencies:**
- Python `configparser` module
- File system access for config.ini

**Technology Stack:**
- Python 3.7+ standard library
- INI file format parsing

**Implementation Notes:**
- Creates default config.ini if missing
- Never fails on invalid config (uses defaults with warnings)
- Validates all settings at startup before file processing

---

## 2. File Matcher Engine

**Responsibility:** Scan directories and identify matching video-subtitle pairs using pattern recognition

**Key Interfaces:**
```python
def scan_directory(path: Path, video_exts: List[str], sub_exts: List[str]) -> Tuple[List[VideoFile], List[SubtitleFile]]:
    """Discover all video and subtitle files in directory"""
    
def detect_mode(videos: List[VideoFile], subtitles: List[SubtitleFile]) -> str:
    """Determine if processing mode is 'movie' or 'episode'"""
    
def match_pairs(videos: List[VideoFile], subtitles: List[SubtitleFile]) -> List[MatchedPair]:
    """Match videos to subtitles using episode info or direct pairing"""
```

**Dependencies:**
- Configuration Loader (for extensions)
- Pattern Recognition Engine (for episode detection)
- File system access

**Technology Stack:**
- Python pathlib for file discovery
- Custom matching algorithm with episode number caching

**Implementation Notes:**
- Shared by both rename and embed scripts
- Uses dictionary caching for O(1) episode number lookups (12x performance gain)
- Case-insensitive file extension matching
- Deterministic processing order (sorted by filename)

---

## 3. Pattern Recognition Engine

**Responsibility:** Extract and normalize episode information from filenames using 25+ regex patterns

**Key Interfaces:**
```python
def compile_patterns() -> List[Tuple[str, re.Pattern]]:
    """Compile all regex patterns at script startup"""
    
def extract_episode_info(filename: str) -> Optional[EpisodeInfo]:
    """Try all patterns and return first match, normalized"""
    
def normalize_episode_number(raw: str) -> int:
    """Convert '05', '5', '005' all to integer 5"""
```

**Dependencies:**
- Python `re` module

**Technology Stack:**
- Python regex with compilation optimization
- Ordered pattern matching (most specific first)

**Pattern Categories:**
1. Standard: `S##E##`, `S##Ep##`
2. Alternate: `##x##` with resolution detection
3. Dash: `S## - ##`, `S## - E##`, `S## - EP##`
4. Text: `Season # Episode #`
5. Ordinal: `1st Season`, `2nd Season` + episode
6. Simple: `E##`, `Ep##`, `- ##`

**Implementation Notes:**
- Patterns compiled once at script initialization
- First matching pattern wins (order matters)
- Smart resolution detection prevents `1920x1080` false matches for `##x##`
- All episode numbers normalized to integers for comparison

---

## 4. Renaming Processor

**Responsibility:** Execute the renaming workflow for matched pairs with collision detection

**Key Interfaces:**
```python
def calculate_target_name(video: VideoFile, subtitle: SubtitleFile, language_suffix: str) -> str:
    """Generate target filename: {video_base}.{language_suffix}.{subtitle_ext}"""
    
def check_collision(target_path: Path) -> bool:
    """Return True if target file already exists"""
    
def rename_subtitle(source: Path, target: Path) -> ProcessingResult:
    """Perform atomic rename operation"""
```

**Dependencies:**
- File Matcher Engine
- Configuration Loader
- File system operations

**Technology Stack:**
- Python pathlib for atomic file operations
- Operating system file rename (atomic on NTFS)

**Implementation Notes:**
- No rename performed if collision detected
- Original files never modified on errors
- Real-time console progress reporting
- Maintains original subtitle extension

---

## 5. Embedding Processor

**Responsibility:** Orchestrate mkvmerge subprocess calls for subtitle embedding with backup management

**Key Interfaces:**
```python
def check_disk_space(required_bytes: int, target_drive: Path) -> bool:
    """Verify sufficient disk space before operation"""
    
def detect_language(subtitle: SubtitleFile, config: Configuration) -> Optional[str]:
    """Strategy: filename detection → config fallback → none"""
    
def create_backup_directory(base_path: Path) -> Path:
    """Create backups/ directory on first successful embed"""
    
def embed_subtitle(video: VideoFile, subtitle: SubtitleFile, config: Configuration) -> ProcessingResult:
    """Complete embedding workflow: validate → embed → backup → finalize"""
```

**Dependencies:**
- File Matcher Engine
- Command Builder
- Process Runner
- Configuration Loader

**Technology Stack:**
- Python subprocess with list-based arguments
- Python shutil for file operations
- mkvmerge.exe external dependency

**Workflow:**
1. Check disk space
2. Build mkvmerge command
3. Execute mkvmerge → `video.embedded.mkv`
4. On success: Create/use backups/, move originals, rename embedded
5. On failure: Delete `.embedded.mkv`, keep originals

**Implementation Notes:**
- Temporary `.embedded.mkv` prevents partial success states
- Backups created only after first successful operation
- Original files never deleted (moved to backups)
- Language detection tries filename patterns first

---

## 6. Command Builder

**Responsibility:** Construct safe, Windows-compatible mkvmerge command-line arguments

**Key Interfaces:**
```python
def build_mkvmerge_command(
    mkvmerge_path: Path,
    video: Path,
    subtitle: Path,
    output: Path,
    language: Optional[str],
    default_flag: bool
) -> List[str]:
    """Build list-based subprocess arguments for mkvmerge"""
```

**Dependencies:**
- Configuration Loader (for mkvmerge path)

**Technology Stack:**
- Python list construction for subprocess
- Explicit string conversion of Path objects

**Command Structure:**
```python
[
    str(mkvmerge_path),
    '-o', str(output_path),        # Output file
    str(video_path),                # Input video with all tracks
    '--language', f'0:{lang_code}', # Language tag if detected
    '--default-track', f'0:{yes|no}', # Default flag from config
    str(subtitle_path)              # Subtitle file to embed
]
```

**Critical Implementation Rule:**
```python
# CORRECT - Windows compatible
subprocess.run([str(mkvmerge), '-o', str(output), ...], ...)

# INCORRECT - May fail on non-standard COMSPEC
subprocess.run(f'{mkvmerge} -o {output} ...', shell=True)
```

**Rationale:**
- List-based arguments avoid shell parsing issues
- Works consistently regardless of Windows shell configuration
- Automatic proper quoting of paths with spaces
- No shell injection vulnerabilities

---

## 7. Process Runner

**Responsibility:** Execute mkvmerge subprocess with timeout, error capture, and exit code handling

**Key Interfaces:**
```python
def run_mkvmerge(command: List[str], timeout: int = 300) -> Tuple[int, str, str]:
    """Execute mkvmerge and return (exit_code, stdout, stderr)"""
    
def validate_output_file(output: Path, min_size: int) -> bool:
    """Verify mkvmerge created valid output file"""
```

**Dependencies:**
- Command Builder

**Technology Stack:**
- Python subprocess.run with capture
- Timeout enforcement (5 minutes default)

**Implementation Notes:**
- Captures stdout/stderr for error diagnosis
- Enforces timeout to prevent hanging
- Validates output file existence and size
- Returns structured results for error handling

---

## 8. CSV Reporter

**Responsibility:** Generate optional CSV reports of processing results for auditing

**Key Interfaces:**
```python
def export_renaming_report(results: List[ProcessingResult], output_path: Path):
    """Generate renaming_report.csv in processed directory"""
    
def export_embedding_report(results: List[ProcessingResult], output_path: Path):
    """Generate embedding_report.csv in processed directory"""
```

**Dependencies:**
- Configuration Loader (for report enable flags)

**Technology Stack:**
- Python csv module
- UTF-8 with BOM encoding for Excel compatibility

**CSV Formats:**

**Renaming Report:**
```csv
Original Filename,New Filename,Status,Timestamp,Execution Time
subtitle-05.srt,Show.S01E05.ar.srt,Success,2025-01-12T10:30:00,0.002
```

**Embedding Report:**
```csv
Original Video,Original Subtitle,Language Code,Status,Timestamp,Execution Time
video.mkv,subtitle.srt,ara,Success,2025-01-12T10:35:00,45.231
```

**Implementation Notes:**
- CSV generation optional (configurable)
- Overwrites previous report in same directory
- UTF-8 BOM for Excel auto-detection
- Timestamps in ISO 8601 format
- Execution time in seconds with millisecond precision

---

## 9. Error Handler

**Responsibility:** Centralized error handling, logging, and user-friendly error messages

**Key Interfaces:**
```python
def handle_config_error(error: Exception) -> Configuration:
    """Log warning and return default configuration"""
    
def handle_file_operation_error(operation: str, file_path: Path, error: Exception) -> ProcessingResult:
    """Log error and return failed result with message"""
    
def handle_mkvmerge_error(video: Path, exit_code: int, stderr: str) -> ProcessingResult:
    """Parse mkvmerge error and create user-friendly message"""
```

**Dependencies:**
- None (standalone utility module)

**Technology Stack:**
- Python exception handling
- Console output formatting

**Error Categories:**
1. **Configuration Errors:** Invalid config values (non-fatal, use defaults)
2. **File System Errors:** Permissions, disk space, missing files
3. **mkvmerge Errors:** Tool not found, execution failures, invalid files
4. **Pattern Matching Errors:** Unrecognized filename patterns (non-fatal)

**User Message Format:**
```
ERROR: [Category] - [Specific Issue]
File: [affected_filename]
Reason: [detailed_explanation]
Action: [suggested_fix]
```

**Example:**
```
ERROR: Disk Space - Insufficient space for embedding
File: LargeMovie.mkv
Reason: Required 5.2GB, available 2.1GB
Action: Free up disk space or process file on different drive
```

---

## 10. Smart Console Manager

**Responsibility:** Control console window behavior based on operation success/failure

**Key Interfaces:**
```python
def should_auto_close(config: Configuration, has_errors: bool) -> bool:
    """Determine if console should auto-close"""
    
def display_summary(results: List[ProcessingResult]):
    """Show batch processing summary before close"""
    
def wait_for_user_exit():
    """Display 'Press any key to continue...' and wait"""
```

**Dependencies:**
- Configuration Loader

**Technology Stack:**
- Python `input()` for keypress wait
- Python `time.sleep()` for auto-close delay

**Behavior Logic:**
```python
if config.keep_console_open:
    wait_for_user_exit()
elif has_errors:
    wait_for_user_exit()  # Keep open to review errors
else:
    display_summary()
    print("Operation completed successfully. Closing in 2 seconds...")
    time.sleep(2)
    # Auto-close
```

**Implementation Notes:**
- Errors always keep console open
- Success shows 2-second countdown before close
- Config override forces manual close
- Summary always displayed before any close

---
