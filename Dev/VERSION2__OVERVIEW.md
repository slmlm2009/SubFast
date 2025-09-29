
# Version V2.0.0 Overview

- This version comes with major updates including support for many additional patterns recognition (e.g. 
- Now the script it is designed to be run directly from the Windows Explorer Right-Click context menu.
- Regoures bug fixes and edge case handeling scenarios with leading to massive core logic improvements (tested for more than 65 scenarios!).

## Files inside The Zipped Folder

*   `rename_subtitles_to_match_videos_ar.py`: The core Python script that contains the logic for renaming files.
*   `add_subtitle_rename_menu.reg`: A Windows registry file that adds a "Rename subtitle files" option to the folder context menu. This makes it easy to run the script without opening a command prompt.
*   `remove_subtitle_rename_menu.reg`: A Windows registry file to remove the context menu item.
*   `ARAB_STREAMS_LOGO.ico`: An icon file used for the context menu item.

## How to Use

1.  **Installation:**
    *   Place the `rename_subtitles_to_match_videos_ar` folder in your `C:\` root directory.
    *   Double-click `add_subtitle_rename_menu.reg` to add the context menu item. You may need to approve a security warning.

2.  **Running the script:**
    *   Navigate to a folder containing video and subtitle files.
    *   Right-click anywhere in the folder background.
    *   Select "Rename subtitle files" from the context menu.
    *   The script will automatically rename the subtitle files to match the video files.

## Dependencies

*   **Python 3:** The script is written in Python 3 and requires it to be installed.
*   **Python Launcher:** The script relies on the Python Launcher (`py.exe`) being installed and located at `C:\Windows\py.exe`. This is the default location for the launcher on Windows.
*   **File Location:** For the context menu integration to work correctly, the project folder must be placed in the C: root directory with the exact name `rename_subtitles_to_match_videos_ar`. The Python script and icon file names must also remain unchanged.