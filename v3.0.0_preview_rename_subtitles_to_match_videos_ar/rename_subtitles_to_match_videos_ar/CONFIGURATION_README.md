# Configuration System

### Customization

**Edit `config.ini` to customize behavior:**

```ini
[General]
enable_export = false          # Disable CSV report (14% faster)
language_suffix = en           # Use .en instead of .ar

[FileFormats]
video_extensions = mkv, mp4, avi, webm			# Adding .avi and .webm support in addition to default .mkv, .mp4
subtitle_extensions = srt, ass, ssa, sub	    # Adding .sub and .ssa support in addition to default .srt, .ass
```

**Re-run the script** - it will use your custom settings!

---

## Configuration Options

### Language Suffix
**What it does:** Sets the language tag added before file extension

**Default:** `ar` (Arabic)

**Examples:**
```ini
language_suffix = ar     # Show.S01E05.ar.srt
language_suffix = en     # Show.S01E05.en.srt
language_suffix = es     # Show.S01E05.es.srt
language_suffix =        # Show.S01E05.srt
```

**Constraints:**
- 1-10 characters
- Letters, numbers, hyphens, underscores only
- No dots (use `ar` not `.ar`)

### CSV Export Control
**What it does:** Enables/disables `renaming_report.csv` generation

**Default:** `true` (enabled)

**Values:** `true`, `false`, `yes`, `no`, `1`, `0`, `on`, `off`

**Performance:**
- Enabled: Full analysis report created
- Disabled: 14% faster execution (skips report)

### Video Extensions
**What it does:** Defines which video file types to process

**Default:** `mkv, mp4`

**Common formats:**
```ini
video_extensions = mkv, mp4                      # Default
video_extensions = mkv, mp4, avi, webm           # Add more formats
video_extensions = mkv, mp4, avi, mov, flv, m4v  # Maximum support
```

**Notes:**
- Comma-separated
- Case-insensitive (MKV = mkv)
- Dots optional (.mkv = mkv)

### Subtitle Extensions
**What it does:** Defines which subtitle file types to process

**Default:** `srt, ass`

**Common formats:**
```ini
subtitle_extensions = srt, ass                      # Default
subtitle_extensions = srt, ass, ssa, sub            # Add more formats
subtitle_extensions = srt, ass, ssa, sub, vtt, smi 	# Maximum support
```

---

## Example Use Cases

### Use Case 1: Arabic Subtitles
```ini
[General]
enable_export = true
language_suffix = ar

[FileFormats]
video_extensions = mkv, mp4
subtitle_extensions = srt
```

### Use Case 2: Batch Processing (Speed Priority)
```ini
[General]
enable_export = false          # Skip CSV for speed
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

---

## Error Handling

### Scenario: Missing config.ini
**Behavior:**
```
[INFO] config.ini not found - creating default configuration
Created default config.ini at: /path/to/script/config.ini
Edit this file to customize script behavior.
```
→ Creates default config, continues with defaults

### Scenario: Invalid Language Suffix
**Behavior:**
```
[WARNING] Invalid language_suffix: '???' (invalid characters)
[INFO] Using no suffix: 'none'
Valid characters: letters, numbers, hyphens, underscores only
```
→ Uses 'none', script continues

### Scenario: No Valid Extensions
**Behavior:**
```
[WARNING] No valid video extensions - using defaults: mkv, mp4
```
→ Falls back to defaults, script continues

### Scenario: Corrupted config.ini
**Behavior:**
```
[WARNING] Failed to parse config.ini: [error details]
[INFO] Using default configuration
```
→ Uses defaults, script continues

**All error scenarios allow the script to continue with safe defaults.**

---

## Windows Context Menu Integration

### Quick Access from File Explorer

Both the **renaming script** and **embedding script** can be accessed directly from Windows File Explorer by right-clicking inside any folder.

### Installation

**Prerequisites:**
- Scripts must be installed in: `C:\rename_subtitles_to_match_videos_ar\`
- Python must be installed (provides `py.exe` launcher)
- Administrator privileges required for installation

**Steps to Install:**

1. **Locate the registry files** in `C:\rename_subtitles_to_match_videos_ar\`:
   - `add_subtitle_rename_menu.reg` (for renaming script)
   - `add_embed_subtitle_menu.reg` (for embedding script)

2. **Right-click the registry file** you want to install

3. **Select "Run as administrator"**

4. **Confirm the UAC prompt** when asked to modify the registry

5. **Click "Yes"** when asked if you want to add the information to the registry

**Result:** The context menu option is now installed!

### Using Context Menu Options

**To Rename Subtitles:**
1. Open File Explorer and navigate to a folder containing video and subtitle files
2. **Right-click on empty space** inside the folder (not on a file)
3. Select **"Rename subtitle files"** from the context menu
4. Console window appears showing progress

**To Embed Subtitles:**
1. Open File Explorer and navigate to a folder containing video and subtitle files
2. **Right-click on empty space** inside the folder (not on a file)
3. Select **"Embed subtitles"** from the context menu
4. Console window appears showing progress

**Important:** Right-click on the **empty space inside the folder**, not on the folder itself or on any file.

### Uninstallation

**To Remove Context Menu Options:**

1. **Locate the removal registry files**:
   - `remove_subtitle_rename_menu.reg` (removes renaming option)
   - `remove_embed_subtitle_menu.reg` (removes embedding option)

2. **Right-click the registry file** you want to run

3. **Select "Run as administrator"**

4. **Confirm the UAC prompt** and registry modification

**Result:** The context menu option is removed.

### Troubleshooting

**Problem: Context menu option doesn't appear**
- **Solution:** Verify you ran the `.reg` file as administrator
- **Check:** Look for "Run as administrator" in the right-click menu of the `.reg` file
- **Test:** Try uninstalling and reinstalling the registry entry

**Problem: Script fails to run from context menu**
- **Solution:** Verify Python is installed (check for `C:\Windows\py.exe`)
- **Solution:** Verify scripts are in `C:\rename_subtitles_to_match_videos_ar\`
- **Test:** Run script manually from command line first

**Problem: Wrong folder is processed**
- **Cause:** Right-clicked on folder name instead of inside folder
- **Solution:** Open the folder first, then right-click on empty white space inside it

**Problem: Permission denied errors**
- **Cause:** Running in a protected system directory
- **Solution:** Process files in a user directory (Documents, Desktop, etc.)

### Installation Path Requirement

**Critical:** The registry files assume scripts are installed in:
```
C:\rename_subtitles_to_match_videos_ar\
```

If you install the scripts in a different location, the context menu will not work. You must either:
1. Install scripts to the expected path, OR
2. Edit the `.reg` files manually to update all paths
