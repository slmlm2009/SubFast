
# Project Overview

This project is a Python script that renames subtitle files (e.g., `.srt`, `.ass`) to match the corresponding video files (e.g., `.mkv`, `.mp4`) in the same directory. It is designed to be run from the Windows Explorer context menu. The script intelligently extracts season and episode numbers from filenames to ensure correct matching.

## Key Files

*   `rename_subtitles_to_match_videos_ar.py`: The core Python script that contains the logic for renaming files.
*   `add_subtitle_rename_menu.reg`: A Windows registry file that adds a "Rename subtitle files" option to the folder context menu. This makes it easy to run the script without opening a command prompt.
*   `remove_subtitle_rename_menu.reg`: A Windows registry file to remove the context menu item.
*   `ARAB_STREAMS_LOGO.ico`: An icon file used for the context menu item.

## Dependencies

*   **Python 3:** The script is written in Python 3 and requires it to be installed.
*   **Python Launcher:** The script relies on the Python Launcher (`py.exe`) being installed and located at `C:\Windows\py.exe`. This is the default location for the launcher on Windows.
*   **File Location:** For the context menu integration to work correctly, the project folder must be placed in the C: root directory with the exact name `rename_subtitles_to_match_videos_ar`. The Python script and icon file names must also remain unchanged.

## How to Use

1.  **Installation:**
    *   Place the `rename_subtitles_to_match_videos_ar` folder in your `C:\` root directory.
    *   Double-click `add_subtitle_rename_menu.reg` to add the context menu item. You may need to approve a security warning.

2.  **Running the script:**
    *   Navigate to a folder containing video and subtitle files.
    *   Right-click anywhere in the folder background.
    *   Select "Rename subtitle files" from the context menu.
    *   The script will automatically rename the subtitle files to match the video files.

## Development Conventions

*   The script is written in Python and uses the `os` and `re` standard libraries.
*   The script is designed to be run on Windows, as it uses Windows registry files for context menu integration.
*   The script assumes that both video and subtitle files are in the same directory.
*   The script can handle `S##E##` and `- ##` patterns for episode number extraction.
*   The script adds an `.ar` suffix to the renamed subtitle files.
