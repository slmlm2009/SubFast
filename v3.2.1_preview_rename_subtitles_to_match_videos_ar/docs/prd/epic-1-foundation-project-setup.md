# Epic 1: Foundation & Project Setup

**Epic Goal:** Establish the SubFast project structure with proper Windows integration, configuration management, and foundational utilities. This epic delivers a working context menu integration and configuration system that both features will build upon, along with a simple health-check capability to verify the installation.

## Story 1.1: Project Structure and Installation System

**Story:**
As a SubFast user,
I want a clear directory structure and easy installation process,
so that I can quickly set up SubFast on my Windows machine.

**Acceptance Criteria:**

1. Project directory structure created at `C:\subfast\` with `scripts/`, `bin/`, and `resources/` folders
2. Python scripts placed in `scripts/` directory (`subfast_rename.py`, `subfast_embed.py`)
3. `mkvmerge.exe` bundled in `bin/` directory
4. `subfast_logo.ico` placed in `resources/` directory
5. Registry files (`add_subfast_menu.reg`, `remove_subfast_menu.reg`) created at root level
6. Registry files correctly reference `C:\subfast\` installation path
7. README documentation includes step-by-step installation instructions
8. Installation can be verified by checking for SubFast context menu in Windows Explorer

## Story 1.2: Windows Context Menu Integration

**Story:**
As a SubFast user,
I want to access SubFast features via right-click in any folder,
so that I can quickly process subtitles without opening command-line tools.

**Acceptance Criteria:**

1. `add_subfast_menu.reg` registry file creates cascading "SubFast" parent menu
2. Parent menu displays SubFast icon from `resources/subfast_logo.ico`
3. Submenu includes "Rename subtitles" option invoking `scripts/subfast_rename.py`
4. Submenu includes "Embed subtitles" option invoking `scripts/subfast_embed.py`
5. Both menu items pass the current folder path as an argument to respective scripts
6. `remove_subfast_menu.reg` registry file cleanly removes all SubFast menu entries
7. Registry changes take effect after running .reg file (may require Explorer restart)
8. Context menu appears when right-clicking in empty space within any folder

## Story 1.3: Configuration System with Auto-Generation

**Story:**
As a SubFast user and developer,
I want a centralized configuration file with sensible defaults,
so that I can customize behavior without modifying code and the tool works out-of-the-box.

**Acceptance Criteria:**

1. `config.ini` file created at project root with `[General]`, `[Renaming]`, and `[Embedding]` sections
2. If `config.ini` is missing, scripts automatically generate it with default values
3. `[General]` section includes: `detected_video_extensions`, `detected_subtitle_extensions`, `keep_console_open`
4. `[Renaming]` section includes: `renaming_report`, `renaming_language_suffix`
5. `[Embedding]` section includes: `mkvmerge_path`, `embedding_language_code`, `default_flag`, `embedding_report`
6. Default video extensions: `mkv, mp4`
7. Default subtitle extensions: `srt, ass`
8. Configuration validation performed at script startup with clear error messages for invalid values
9. Documentation (`CONFIGURATION_README.md`) explains all configuration options with examples

## Story 1.4: Smart Console Behavior System

**Story:**
As a SubFast user,
I want the console window to automatically close on success but stay open on errors,
so that I don't have to manually close windows but can review error messages when needed.

**Acceptance Criteria:**

1. When operations complete successfully, console window auto-closes after 2 seconds
2. When any error occurs, console window stays open with "Press any key to continue..." prompt
3. Behavior controlled by `keep_console_open` configuration option
4. When `keep_console_open = true`, console always waits for keypress before closing
5. When `keep_console_open = false`, smart behavior applied (auto-close on success)
6. Success message displayed before auto-close (e.g., "Operation completed successfully. Closing in 2 seconds...")
7. Error messages clearly displayed with affected filenames and troubleshooting hints
8. Exit codes properly set: 0 for success, non-zero for errors

## Story 1.5: Common Utilities and File Discovery Module

**Story:**
As a developer,
I want shared utility functions for file discovery and validation,
so that both renaming and embedding scripts use consistent, tested logic.

**Acceptance Criteria:**

1. Common utilities module created for shared functionality between scripts
2. File discovery function scans directory for files matching configured extensions
3. File extension filtering case-insensitive (e.g., `.MKV` and `.mkv` both match)
4. File validation checks for read permissions before processing
5. Path resolution handles relative and absolute paths correctly
6. Utility functions include disk space checking capability
7. File discovery returns sorted lists for consistent processing order
8. Python Launcher validation confirms `py.exe` exists at `C:\Windows\py.exe`
9. Module includes basic health-check function to verify installation components

---
