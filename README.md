# ![logo](https://i.imgur.com/pleZZjw.png)    SubFast

**Fast subtitle renaming and embedding for all languages**

SubFast is a powerful Windows utility for managing subtitles with your video files. It provides two main features accessible through a convenient right-click context menu.


## 🚀 Features

### 1. **Rename Subtitles** 
Automatic renaming of subtitles files to match video files with an added configurable .language_code suffix based on detected matched subtitle/video pairs

![Rename_GIF](https://i.imgur.com/N4eCblh.gif)
- Recognizes wide variety of episode naming patterns
- Context-aware matching handles inconsistent zero-padding between files
- Language suffix support (ar, en, es, etc...)
- Configurable CSV export for reporting the results

### 2. **Embed Subtitles**
Soft-subtitle embedding of external subtitle files directly into detected MKV video files matches for seamless playback.

![Embed_GIF](https://i.imgur.com/lgMeqG3.gif)
- Automatic subtitle/video match identification using same renaming logic (No need for renaming)
- Language code detection and configuration
- Default subtitle flag control
- Backup management
- Batch processing with progress tracking
- Configurable CSV export for reporting the results

---

## 📋 Requirements

- **Windows 10/11**
- **Python 3.7+:** with Python Launcher `py.exe` installed in default location `C:\Windows\py.exe`
- **mkvmerge:** The application is bundled with `mkvmerge.exe` in the `subfast/bin/` directory. If you prefer to use your own system-wide installation, you may delete the bundled executable and specify the absolute path to your `mkvmerge.exe` in the `config.ini` file and handle its update yourself

---

## 🔧 Installation

### Step 1: Extract Files

**IMPORTANT:** Extract SubFast to `C:\subfast` (exact path required for registry files)

```
C:\subfast\
├── scripts/
│   ├── subfast_rename.py
│   └── subfast_embed.py
├── bin/
│   └── mkvmerge.exe
├── resources/
│   ├── subfast_logo.ico
│   └── docs/
│       └── CONFIGURATION_README.md
├── config.ini
├── add_subfast_menu.reg
└── remove_subfast_menu.reg
```

### Step 2: Install Context Menu

1. Double-click: `add_subfast_menu.reg`
2. Click "Yes" when asked to merge registry keys
3. Approve UAC prompt if asked

### Step 3: Verify Installation

- Right-click in any folder
- Look for **SubFast** menu with arrow (►)
- Should show:
  - **Rename subtitles**
  - **Embed subtitles**

---

## 📖 Usage

### Rename Subtitles

1. **Place** video and subtitle files in the same folder
2. **Right-click** in the folder (empty space)
3. **Select:** SubFast → **Rename subtitles**
4. Script runs automatically and rename detected matched subtitle/video pairs

**Example:**
```
Before:
├── ShowName S01E05.1080p.mkv
├── ShowName S01E06.1080p.mkv
├── subtitle-05.srt
└── subtitle-06.srt

After:
├── ShowName S01E05.1080p.mkv
├── ShowName S01E05.1080p.srt  ← Renamed!
├── ShowName S01E06.1080p.mkv
└── ShowName S01E06.1080p.srt  ← Renamed!
```

### Embed Subtitles

1. **Place** MKV videos and subtitle files in the same folder
2. **Right-click** in the folder
3. **Select:** SubFast → **Embed subtitles**
4. Script runs automatically and embeds subtitles into their detected matched MKV video files (Backup of original files will be created automatically under `backup/` folder)

**Result:** Subtitle tracks embedded directly into video files for seamless playback.

---

## ⚙️ Configuration

Edit `config.ini` to customize SubFast behavior:

```ini
[General]
detected_video_extensions = mkv, mp4
detected_subtitle_extensions = srt, ass
keep_console_open = false

[Renaming]
renaming_report = true
renaming_language_suffix = 

[Embedding]
mkvmerge_path = bin\mkvmerge.exe
embedding_language_code = 
default_flag = true
embedding_report = true
```

### Configuration Options Explained:

**[General]**
- `detected_video_extensions` - Video file formats to process (comma-separated)
- `detected_subtitle_extensions` - Subtitle file formats to process (comma-separated)
- `keep_console_open` - Console window behavior:
  - `false` - Auto-close on success, stay open on errors (recommended)
  - `true` - Always wait for keypress before closing

**[Renaming]**
- `renaming_report` - Enable CSV export of renaming operations (`true`/`false`)
- `renaming_language_suffix` - Language tag added to renamed files (e.g., `ar`, `en`, `es`) or empty for none

**[Embedding]**
- `mkvmerge_path` - Path to mkvmerge.exe (relative to config.ini or absolute path)
- `embedding_language_code` - Language code for embedded subtitles or empty to auto-detect
- `default_flag` - Mark embedded subtitle as default track (`true`/`false`)
- `embedding_report` - Enable CSV export of embedding operations (`true`/`false`)

** For detailed configuration documentation, see `CONFIGURATION_README.md` in `\resources\docs\`

---

## 🗑️ Uninstallation

1. Double-click: `remove_subfast_menu.reg`
2. Click "Yes" when asked to remove registry keys
3. Ensure context menu is removed
4. Delete `C:\subfast` folder

---

## 📝 Tecnical Details

### Core Functionality
- **Movie mode** for folders with single video/subtitle pair
- **Multi-format support** for video and subtitle files (fully configurable via config.ini)
- **Intelligent episode detection** supporting *MANY* naming patterns
- **Context-aware matching** handles inconsistent zero-padding between files
- **Collision handling** prevents file overwrites with smart naming and backups
- **Performance oriented** with caching and regex precombilation optimizations
- **Auto-generation** of default config.ini if missing
- **Safe fallbacks** for invalid configurations

### Episode Pattern Recognition
The script recognizes various episode naming conventions:
- `S##E##` (e.g., S01E05, S2E15)
- `##x##` (e.g., 2x05, 1x10) - with smart resolution detection
- `S## - ##` / `S## - E##` / `S## - EP##` formats
- `Season # Episode #` (with various separators)
- `S##Ep##` / `SeasonXEpY` formats
- Ordinal season patterns: `1st Season`, `2nd Season`, etc.
  - With dash: `ShowName 1st Season - 05.mkv`
  - With E: `ShowName 2nd Season E10.srt`
  - With EP: `ShowName 3rd Season EP8.mp4`
- `E##` / `Ep##` patterns (assumes Season 1)
- `- ##` patterns for simple numbering
- And many more variations with flexible spacing and separators

### Smart Matching Examples
The script handles various inconsistencies:
- `S2E8` (video) ↔ `S02E008` (subtitle) → Matched
- `2x05` (video) ↔ `S02E05` (subtitle) → Matched  
- `Season 1 Episode 3` ↔ `S01E03` → Matched

### Supported File Formats

**Default Video Files**
- `.mkv` (Matroska Video)
- `.mp4` (MPEG-4 Video)

**Default Subtitle Files**
- `.srt` (SubRip Text)
- `.ass` (Advanced SubStation Alpha)

**Note #1:** File formats are fully configurable via `config.ini` (v2.5.0+). You can add support for `.avi`, `.webm`, `.mov`, `.sub`, `.ssa`, and more ...

**Note #2:** Subtitle embedding feature will only work with `.mkv` files

### Performance

- Renames 1000+ files in under 1 second
- Performance optimized via episode number caching and regex compiling optimizations
- Disable optional CSV export for additional speed (+14% speed improvement on 1000+ files dataset) 

**Note #3:** Subtitle embedding speed depends heveaily on your disk I/O performance, hence embedding on SSDs will be multiple folds faster than on HDDs

---

## 🛠️ Troubleshooting

### Context Menu Not Appearing
1. Restart explorer.exe process in Task Manager or log out and back in to refresh Explorer
2. Ensure you have administrator privileges and verify the registry file was applied successfully

### Python Not Found Error
1. Verify Python 3.7+ is installed
2. Ensure Python Launcher is at: `C:\Windows\py.exe`
3. Test by opening Command Prompt and typing: `py --version`

### No Files Renamed
1. Check that video and subtitle files are in the same directory
2. Ensure installation path is at `C:\subfast`
3. Verify file naming patterns are supported
5. Use the CSV export feature to analyze detection results

### mkvmerge Not Found

**Solution:**
1. Verify `mkvmerge.exe` exists at: `C:\subfast\bin\mkvmerge.exe`
2. Check `config.ini` has and ensure you have correct path for `mkvmerge_path =`  (empty will default to bin\mkvmerge.exe)

## Contributing

This utility has been extensively tested across multible different scenarios. If you encounter issues or have suggestions for additional episode patterns, please:

1. Test the current version thoroughly
2. Open an issue and provide specific examples
3. Include generated CSV report that along with the issue details
4. Consider contributing regex patterns for new format support

## License

This project is released as open source. Feel free to modify and distribute according to your needs.
