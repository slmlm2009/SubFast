# SubFast

**Fast subtitle renaming and embedding for all languages**

SubFast is a powerful Windows utility for managing subtitles with your video files. It provides two main features accessible through a convenient right-click context menu.

---

## 🚀 Features

### 1. **Rename Subtitles** 
Automatic renaming of subtitles files to match video files with an added configurable .language_code suffix based on detected matched subtitle/video pairs

- Works with TV shows/Anime and Movies
- Recognizes 25+ episode naming patterns
- Context-aware matching handles inconsistent formatting and and padding
- Language suffix support (ar, en, es, etc...)
- Configurable CSV export for reporting the results

**Supported Episode Patterns (+25):**
- `S##E##` (e.g., S01E05, S2E15)
- `##x##` (e.g., 2x05, 1x10)
- `S## - ##` / `S## - E##` / `S## - EP##`
- `Season # Episode #`
- Ordinal seasons: `1st Season - 05`, `2nd Season E10`
- `E##` / `Ep##` patterns
- And many more variations

### 2. **Embed Subtitles**
Soft-subtitle embedding of external subtitle files directly into detected MKV video files matches for seamless playback.

- Automatic subtitle/video match identification using same renaming logic (No need for renaming)
- Language code detection and configuration
- Default subtitle flag control
- Backup management
- Batch processing with progress tracking
- Configurable CSV export for reporting the results

---

## 📋 Requirements

- **Windows 10/11**
- **Python 3.7+** (with Python Launcher `py.exe` installed in default location `C:\Windows\py.exe`)
- **mkvmerge** (bundled in package under bin/ directory, or you can edit config.ini to provide absolute path to mkvmerge.exe if already installed on system)

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

## 🛠️ Troubleshooting

### Context Menu Not Appearing

**Solution:**
1. Restart Windows Explorer (Task Manager → Explorer.exe → Restart)

### Python Not Found Error

**Solution:**
1. Verify Python 3.7+ is installed
2. Ensure Python Launcher is at: `C:\Windows\py.exe`
3. Test by opening Command Prompt and typing: `py --version`

### No Files Renamed

**Possible Causes:**
1. Installation path is not `C:\subfast`
2. File naming patterns not recognized
3. Check the CSV export report for details

### mkvmerge Not Found

**Solution:**
1. Verify `mkvmerge.exe` exists at: `C:\subfast\bin\mkvmerge.exe`
2. Check `config.ini` has and ensure you have correct path for `mkvmerge_path =`  (empty will default to bin\mkvmerge.exe)

---

## 📊 Supported File Formats (Default Config)

### Video Files (Default)
- `.mkv` (Matroska Video)
- `.mp4` (MPEG-4 Video)

### Subtitle Files (Default)
- `.srt` (SubRip Text)
- `.ass` (Advanced SubStation Alpha)

**Note:** File formats are fully configurable via `config.ini`. You can add support for `.avi`, `.webm`, `.sub`, `.ssa`, and more.

---

## ⚡ Performance

- Renames 1000+ files in under 1 second
- Performance optimized via episode number caching and regex compiling optimizations
- Disable optional CSV export for additional speed (+ 14% on 1000+ files dataset) 

---

## 🎯 Version History

### v3.0.0 (Current - January 2025)
**Major Changes:**
- **Added new MKV soft-sub subtitle embedding feature** through mkvmerge (credits to MKVToolNix devs)
- **Dual-feature context menu** (Rename + Embed in one menu under SubFast parent menu)
- **Smart console behavior** (auto-close on success, stay open on errors)

**Technical Improvements:**
- Unified configuration system to handle config of both features in one config.ini file
- New Folder structure (scripts/, bin/, resources/)
- Enhanced error messages


### v2.5.0 (October 2024)
- Configuration system via config.ini
- 9 new episode patterns (25+ total)
- 12x performance improvement
- Enhanced CSV export
- Configurable language suffix

### v2.0.0
- Windows context menu integration
- Custom icon support
- 15+ episode patterns
- Movie mode detection

### v1.0.0
- Initial release
- Basic S##E##pattern support
- Command-line operation

---

## 📝 License

This project is released as open source. Feel free to modify and distribute according to your needs.

---

## 💬 Support

For issues or suggestions:
1. Check the troubleshooting section above
2. Examine the CSV export reports for detailed analysis
3. Open an issue with specific example and generated CSV report

---

**SubFast - Fast subtitle renaming and embedding for all languages** 🚀
