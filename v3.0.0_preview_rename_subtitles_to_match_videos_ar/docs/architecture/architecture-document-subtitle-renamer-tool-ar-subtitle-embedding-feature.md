# Architecture Document: Subtitle Renamer Tool [AR] - Subtitle Embedding Feature

* **Project Name**: Subtitle Renamer Tool [AR]
* **Feature**: Subtitle Embedding via `mkvmerge`


## 1. High-Level Architecture

### 1.1. Technical Summary

The architecture for the subtitle embedding feature is designed as a standalone Python script, `embed_subtitles_to_match_videos_ar.py`. This script will function as a command-line tool that orchestrates file system operations and calls to the external `mkvmerge.exe` utility. It is designed to be modular, reusing the proven file matching logic from the existing `rename_subtitles_to_match_videos_ar.py` script to ensure consistency and reliability. The architecture emphasizes clear separation of concerns: configuration, file processing, `mkvmerge` command generation, and reporting.

### 1.2. High-Level Overview \& Project Diagram

The system operates in a simple, linear flow initiated by the user via a Windows context menu command.

1. **User Action**: The user right-clicks a folder and selects "Embed subtitles".
2. **Script Execution**: Windows executes `embed_subtitles_to_match_videos_ar.py`, passing the folder path as an argument.
3. **Core Logic**: The script scans the folder, matches `.mkv` files with subtitle files, renames the original videos for backup, and then invokes `mkvmerge.exe` for each pair to create the new, merged video.
4. **Output**: A new `.mkv` file with the original name is created, and an optional CSV report is generated.
```mermaid
graph TD
    A[User Right-Clicks Folder] --> B{Windows Shell};
    B -- Executes --> C[embed_subtitles_to_match_videos_ar.py];
    C -- Reads --> D[config.ini];
    C -- Finds & Matches --> E{Video & Subtitle Files};
    C -- Invokes --> F[mkvmerge.exe];
    F -- Creates --> G[New Merged '.mkv' File];
    C -- Generates --> H[embedding_report.csv];
```


### 1.3. Architectural and Design Patterns

* **Modular Design**: The script will be organized into distinct functions, each with a single responsibility (e.g., `load_config`, `find_matching_files`, `build_mkvmerge_command`, `run_command`, `generate_report`).
* **Facade Pattern**: The main script will act as a facade, providing a simple interface to the more complex underlying logic of file matching and command execution.
* **Strategy Pattern**: The language detection logic (`FR4`) will implement a strategy pattern: first, it will try to extract the language from the filename; if that fails, it will fall back to the strategy of using the language from the config file.


## 2. Tech Stack

| Category | Technology | Version/Path | Purpose \& Rationale |
| :-- | :-- | :-- | :-- |
| **Language** | Python | 3.8+ | Primary development language. Chosen for its strong file system libraries, ease of scripting, and cross-platform nature. |
| **External Tool** | MKVToolNix | Latest | The suite that provides `mkvmerge.exe`. Required for the core functionality of muxing Matroska files. |
| **Configuration** | INI File | `config.ini` | A single, unified file for both scripts, using sections to separate settings. This provides a simple, centralized, and human-readable format for all user configuration. |
| **OS Integration** | Windows Registry | `.reg` file | To provide the required "Embed subtitles" context menu option in Windows File Explorer. |

### 2.1. Windows Subprocess Execution Guidelines

**Target Operating System:** Windows is the primary deployment platform for this tool.

**Subprocess Best Practices for Windows:**

The script executes external commands (primarily `mkvmerge.exe`) using Python's `subprocess` module. To ensure reliable operation on Windows systems regardless of shell configuration:

1. **Always Use List-Based Arguments**
   - Pass commands as a `list` of strings, not a single concatenated string
   - This avoids shell parsing issues and ensures proper argument quoting
   - Python handles proper escaping automatically

2. **Avoid `shell=True`**
   - Do NOT use `shell=True` unless shell-specific features are required
   - List-based arguments work directly without shell involvement
   - This prevents issues with non-standard COMSPEC environment variables

3. **Use `pathlib.Path` for All File Paths**
   - Convert Path objects to strings explicitly with `str()`
   - Works correctly with Windows path separators (backslashes)
   - Handles spaces and special characters automatically

4. **Store Resolved Executable Paths**
   - Validate and resolve the full path to `mkvmerge.exe` during initialization
   - Use the resolved path for all subsequent subprocess calls
   - Avoids PATH lookup overhead and ensures consistency

**Correct Windows Subprocess Pattern:**

```python
# CORRECT - Windows-compatible approach
import subprocess
from pathlib import Path

mkvmerge_path = Path("C:/path/to/mkvmerge.exe")
output_file = Path("output.mkv")
video_file = Path("video.mkv")
subtitle_file = Path("subtitle.srt")

result = subprocess.run(
    [
        str(mkvmerge_path),
        '-o', str(output_file),
        str(video_file),
        '--language', '0:ar',
        '--default-track', '0:yes',
        str(subtitle_file)
    ],
    capture_output=True,
    text=True,
    timeout=300
)
```

**Incorrect Patterns to Avoid:**

```python
# INCORRECT - Shell string (bash-style, may fail on Windows)
subprocess.run('mkvmerge -o output.mkv video.mkv subtitle.srt', shell=True)

# INCORRECT - String concatenation (fragile with spaces/special chars)
cmd = f'{mkvmerge_path} -o {output_file} {video_file} {subtitle_file}'
subprocess.run(cmd, shell=True)
```

**Rationale:** List-based subprocess calls work consistently on Windows CMD regardless of the COMSPEC environment variable, handle path quoting automatically, and eliminate shell injection risks.

## 3. Component Breakdown

* **`main`**: The entry point of the script. Parses command-line arguments, orchestrates calls to other components, and handles top-level error trapping.
* **`config_loader`**: Responsible for reading and validating settings from the single, unified `config.ini`. It will parse settings from specific sections (`[General]`, `[FileFormats]`, `[Embedding]`) and provide default values if the file or a setting is missing.
* **`file_matcher`**: Reused/adapted from `rename_subtitles_to_match_videos_ar.py`. It contains the logic to scan a directory and accurately match video and subtitle files.
* **`command_builder`**: Constructs the precise `mkvmerge` command-line string for each matched pair.
* **`process_runner`**: Executes the generated `mkvmerge` command using Python's `subprocess` module.
* **`file_manager`**: Handles the file system operations as defined in the PRD (renaming the original video file).
* **`report_generator`**: Implements the logic for writing the `embedding_report.csv` file if enabled.


## 4. Core Workflow (Sequence Diagram)

```mermaid
sequenceDiagram
    participant User
    participant WindowsExplorer
    participant EmbedScript as embed_subtitles_to_match_videos_ar.py
    participant MKVMerge as mkvmerge.exe

    User->>WindowsExplorer: Right-click folder, select "Embed subtitles"
    WindowsExplorer->>EmbedScript: Execute with folder path
    EmbedScript->>EmbedScript: load_configuration()
    EmbedScript->>EmbedScript: find_and_match_files()
    loop For each matched pair
        EmbedScript->>EmbedScript: rename_original_video()
        EmbedScript->>EmbedScript: build_mkvmerge_command()
        EmbedScript->>MKVMerge: Execute command
        MKVMerge-->>EmbedScript: Return exit code
        EmbedScript->>EmbedScript: Log success/failure
    end
    EmbedScript->>EmbedScript: generate_csv_report()
```


## 5. Source Tree

The corrected project directory will be as follows :[^1]

```
C:/rename_subtitles_to_match_videos_ar/
├── embed_subtitles_to_match_videos_ar.py
├── add_embed_subtitle_menu.reg
├── remove_embed_subtitle_menu.reg
├── mkvmerge.exe
├── rename_subtitles_to_match_videos_ar.py
├── config.ini
├── add_subtitle_rename_menu.reg
├── remove_subtitle_rename_menu.reg
├── ARAB_STREAMS_LOGO.ico
└── CONFIGURATION_README.md
```


## 6. Infrastructure and Deployment

* **Infrastructure**: The tool runs locally on a user's Windows machine.
* **Deployment**: The user must place the project folder at `C:\rename_subtitles_to_match_videos_ar\`, run the `.reg` file to install the context menu, and ensure `mkvmerge.exe` is either in the folder or its path is set in `config.ini`.
