# Epic 3: User Experience & Configuration

**Epic Goal:** Provide seamless Windows integration and user feedback

**Epic Description:**
This epic focuses on delivering an excellent user experience through flexible configuration, Windows context menu integration, and comprehensive reporting. It ensures users can easily customize the tool's behavior, invoke it with a single right-click, and receive detailed feedback about operations.

**Functional Requirements Covered:** FR7, FR8, FR9

**Non-Functional Requirements Covered:** NFR2 (platform compatibility)

---

## Story 3.1: Implement Configuration File Handling

**Story:**
As a user, I want to configure the script's behavior through a configuration file, so that I can customize it to my preferences without modifying code.

**Acceptance Criteria:**
1. The script reads configuration from a `config.ini` file in the same directory
2. Configuration includes: path to `mkvmerge.exe`
3. Configuration includes: default subtitle track properties (language, default track flag)
4. Configuration includes: CSV export enable/disable flag
5. If `config.ini` doesn't exist, the script creates one with default values
6. Invalid configuration values are detected and reported with clear error messages
7. Configuration values are validated on startup before processing begins

---

## Story 3.2: Add Windows Context Menu Integration

**Story:**
As a Windows user, I want to embed subtitles by right-clicking a folder, so that I can quickly process files without opening a terminal.

**Acceptance Criteria:**
1. A registry file `add_embed_subtitle_menu.reg` is created
2. Running the registry file adds "Embed subtitles" to the folder context menu
3. The context menu entry executes `embed_subtitles_to_match_videos_ar.py` with the folder path
4. The script and `mkvmerge.exe` are assumed to be in `C:\rename_subtitles_to_match_videos_ar\`
5. A console window appears during processing to show progress
6. A companion registry file `remove_embed_subtitle_menu.reg` is created for uninstallation
7. The registry integration works on Windows 10 and Windows 11

---

## Story 3.3: Implement User Feedback and CSV Reporting

**Story:**
As a user, I want to receive clear feedback during processing and optionally export a detailed report, so that I can track what was done and troubleshoot any issues.

**Acceptance Criteria:**
1. Real-time console output shows which file is currently being processed
2. Success/failure status is displayed for each operation
3. The final output filename is displayed after each successful merge
4. A CSV report (`embedding_report.csv`) can be exported with processing details
5. Implement smart console behavior for both codes. (if code executed without major exit code, console window will automatically close, if not, it will be active and waiting for a key input to be closed.
7. Having a configurable option to have the console window remains open at completion until a key is pressed - this is shared for both scripts (disabled by default, will not affect smart console behavior).
5. The CSV includes: original filename, subtitle filename, output filename, status, timestamp
6. CSV export is configurable via the `config.ini` file (enabled for example default, disabled in case of fall-off)
7. The CSV uses the same structure as the renaming script's `export_analysis_to_csv` function
8. Error details are included in the CSV for failed operations
9. The CSV is saved in the same directory as the processed files
10. A summary is displayed at the top showing total files, successes, failures, and processing time
