## Product Requirements Document: Subtitle Renamer Tool [AR] - Subtitle Embedding Feature

* **Project Name**: Subtitle Renamer Tool [AR]
* **Feature**: Subtitle Embedding via `mkvmerge`


### 1. Introduction \& Background

The "Subtitle Renamer Tool [AR]" is an existing, functional Python script that automates the process of renaming subtitle files to match their corresponding video files. It leverages intelligent pattern matching for episodes and movies and provides a seamless workflow through Windows context menu integration.

This document outlines the requirements for a major new feature: **the ability to embed subtitles directly into `.mkv` video files.** This new functionality will exist as a separate but complementary script, `embed_subtitles_to_match_videos_ar.py`, leveraging the power of the `mkvmerge` command-line tool.

### 2. Problem Statement

Users who have organized their subtitle files with the existing renamer tool still face the manual, time-consuming task of embedding those subtitles into their video files. This often involves opening a GUI application and processing files one by one. This manual process is inefficient, especially for users with large media libraries, and creates a disconnected experience between renaming and finalizing the media files.

The new feature will solve this by **automating the subtitle embedding process** for `.mkv` files in a single, batch operation, callable directly from the Windows context menu.
### 3. Goals \& Objectives

* **Automate Subtitle Embedding**: Create a script that automatically finds matching pairs of `.mkv` videos and subtitles and merges them.
* **Seamless User Experience**: Integrate the script into the Windows right-click context menu, providing a "one-click" solution for embedding subtitles within a folder.
* **Leverage Existing Logic**: Utilize the robust file and episode matching logic from the original `rename_subtitles_to_match_videos_ar.py` script to ensure consistency and accuracy.
* **Ensure No Data Loss**: The process will be non-destructive by creating backups of original files before generating new, merged video files.


### 4. Target Audience

The target users are existing and new users of the "Subtitle Renamer Tool [AR]" who manage local libraries of `.mkv` media files and want a permanent, all-in-one solution for their videos and subtitles.

### 5. Functional Requirements

| ID | Requirement | Description |
| :-- | :-- | :-- |
| **FR1** | **New Script** | A new Python script named `embed_subtitles_to_match_videos_ar.py` will be created to house the embedding functionality. |
| **FR2** | **File Discovery \& Matching** | The script must scan the directory it's run from to identify all `.mkv` files and all subtitle files (e.g., `.srt`, `.ass`). It will then match video files to their corresponding subtitle files using the same episode/movie detection logic as the original renaming script. |
| **FR3** | **`mkvmerge` CLI Integration** | The script will execute command-line operations using `mkvmerge.exe` to perform the merge. The path to `mkvmerge.exe` will be configurable. However, if not configured, it will assume `mkvmerge.exe` is in the same directory as `embed_subtitles_to_match_videos_ar.py`. |
| **FR4** | **Embedding Logic** | For each matched pair, the script will generate and run a `mkvmerge` command. The command will mux (merge) the original video stream, all its original audio/subtitle tracks, and the new external subtitle file into a new output file. The muxed subtitle track will be tagged as "default" unless configured otherwise in the config file. **Additionally, the subtitle track language tag will be inferred from the subtitle filename (e.g., .{ar, en, fr} in the filename). If not found, it will fall back to the language configured in the config file (defaulting to none).** |
| **FR5** | **Output File Management** | The script will rename the original video files to `[Original_Filename].original.mkv` first. Then, to ensure no overwrites, it will generate new muxed video files with the original file names `[Original_Filename].mkv`. |
| **FR6** | **Batch Processing** | The script must be able to process all matched video-subtitle pairs within a folder in a single execution. |
| **FR7** | **Windows Context Menu** | A new registry file (`add_embed_subtitle_menu.reg`) will be created. When run, it will add an "Embed subtitles" command to the folder context menu in Windows File Explorer, which executes the `embed_subtitles_to_match_videos_ar.py` script and assumes both it and `mkvmerge.exe` reside in `C:\rename_subtitles_to_match_videos_ar\`. |
| **FR8** | **Configuration** | The script will use a `config.ini` file, similar to the existing tool. This file will allow users to configure: the path to `mkvmerge.exe`, the output filename pattern, and default subtitle track properties (e.g., language, `default track` flag). |
| **FR9** | **User Feedback and Reporting** | The script will provide clear, real-time feedback to the console, indicating which files are processed, the status of the merge operation (success/failure), and the final output filename. It will also support exporting an `embedding_report.csv`, building on the `export_analysis_to_csv` function from the renaming script. CSV export will be configurable (enable/disable) via the config file. |

### 6. Non-Functional Requirements

| ID | Requirement | Description |
| :-- | :-- | :-- |
| **NFR1** | **Dependency** | The feature requires `mkvmerge.exe` (part of the MKVToolNix suite) to be present on the user's system. The path to the executable must be correctly configured. |
| **NFR2** | **Platform** | The core script should be written in Python 3 for cross-platform compatibility. However, the context menu integration (`.reg` file) is specific to the Windows operating system. |
| **NFR3** | **Performance** | The script should handle directories with a large number of files efficiently, processing them in a reasonable amount of time. |
| **NFR4** | **Error Handling** | The script must gracefully handle errors, such as `mkvmerge.exe` not being found, permissions issues, or a failed merge operation, and report these errors to the user. |

### 7. Out of Scope

* Embedding subtitles into video formats other than `.mkv`.
* Providing a graphical user interface (GUI).
* Transcoding or re-compressing video or audio streams. The script will only perform stream copying (muxing).
* Removing or modifying existing tracks within the original `.mkv` file.
