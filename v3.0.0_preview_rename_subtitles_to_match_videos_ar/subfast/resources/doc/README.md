# SubFast

**Fast subtitle renaming and embedding for all languages**

SubFast is a powerful Windows utility for managing subtitles with your video files. It provides two main features accessible through a convenient right-click context menu.

---

## 🚀 Features

### 1. **Rename Subtitles** 
Automatically rename subtitle files to match your video filenames, making organization effortless.

- Supports TV shows (S01E01 pattern) and movies
- Recognizes 25+ episode naming patterns
- Context-aware matching handles inconsistent formatting
- Language suffix support (ar, en, es, etc.)
- CSV export for tracking operations

**Supported Episode Patterns:**
- `S##E##` (e.g., S01E05, S2E15)
- `##x##` (e.g., 2x05, 1x10)
- `S## - ##` / `S## - E##` / `S## - EP##`
- `Season # Episode #`
- Ordinal seasons: `1st Season - 05`, `2nd Season E10`
- `E##` / `Ep##` patterns
- And many more variations

### 2. **Embed Subtitles**
Embed external subtitle files directly into MKV video files for seamless playback.

- Automatic subtitle integration using mkvmerge
- Language code detection and configuration
- Default subtitle flag control
- Backup management (optional)
- Batch processing with progress tracking
- CSV export for operation logs

---

## 📋 Requirements

- **Windows 10/11**
- **Python 3.7+** (with Python Launcher `py.exe`)
- **mkvmerge** (included in package)

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
│   └── doc/
│       ├── README.md                    ← This file
│       └── CONFIGURATION_README.md
├── config.ini
├── add_subfast_menu.reg
└── remove_subfast_menu.reg
```

### Step 2: Add Logo

Your logo file (`subfast_logo.ico`) should already be in:
```
C:\subfast\resources\subfast_logo.ico
```

### Step 3: Install Context Menu

1. Double-click: `add_subfast_menu.reg`
2. Click "Yes" when asked to merge registry keys
3. Approve UAC prompt if asked

### Step 4: Verify Installation

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
4. Script runs automatically and shows results

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
4. Script embeds subtitles into MKV files

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

### Common Configuration Examples:

**Arabic Subtitles with Reports:**
```ini
[Renaming]
renaming_report = true
renaming_language_suffix = ar

[Embedding]
embedding_language_code = ara
embedding_report = true
```

**English Subtitles:**
```ini
[Renaming]
renaming_language_suffix = en

[Embedding]
embedding_language_code = eng
```

**No Language Suffix (Clean Names):**
```ini
[Renaming]
renaming_language_suffix = 

[Embedding]
embedding_language_code = 
```

**Speed Priority (Disable Reports):**
```ini
[Renaming]
renaming_report = false

[Embedding]
embedding_report = false
```

For detailed configuration documentation, see `CONFIGURATION_README.md` in this folder

---

## 🗑️ Uninstallation

1. Double-click: `remove_subfast_menu.reg`
2. Click "Yes" when asked to remove registry keys
3. Context menu removed!

---

## 🛠️ Troubleshooting

### Context Menu Not Appearing

**Solution:**
1. Restart Windows Explorer (Task Manager → Explorer.exe → Restart)
2. Or log out and back in to refresh

### Python Not Found Error

**Solution:**
1. Verify Python 3.7+ is installed
2. Ensure Python Launcher is at: `C:\Windows\py.exe`
3. Test by opening Command Prompt and typing: `py --version`

### No Files Renamed

**Possible Causes:**
1. Video and subtitle files not in same folder
2. Installation path is not `C:\subfast`
3. File naming patterns not recognized
4. Check the CSV export report for details

### mkvmerge Not Found

**Solution:**
1. Verify `mkvmerge.exe` exists at: `C:\subfast\bin\mkvmerge.exe`
2. Check `config.ini` has correct path: `mkvmerge_path = bin\mkvmerge.exe`

---

## 📊 Supported File Formats

### Video Files (Default)
- `.mkv` (Matroska Video)
- `.mp4` (MPEG-4 Video)

### Subtitle Files (Default)
- `.srt` (SubRip Text)
- `.ass` (Advanced SubStation Alpha)

**Note:** File formats are fully configurable via `config.ini`. You can add support for `.avi`, `.webm`, `.sub`, `.vtt`, and more.

---

## ⚡ Performance

- Processes 1000+ files in under 1 second
- 12x performance improvement via episode number caching
- Smart pattern matching with regex optimization
- Optional CSV export disable for additional speed

---

## 🎯 Version History

### v3.0.0 (Current - January 2025)
**Major Changes:**
- **Unified SubFast branding** throughout
- **Dual-feature context menu** (Rename + Embed in one menu)
- **Professional folder structure** (scripts/, bin/, resources/)
- **Registry-based installation** (simple and robust)
- **Location detection** for config and mkvmerge
- **Comprehensive documentation** with installation guide

**New Features:**
- Cascading context menu with SubFast icon
- Both features accessible from single menu
- Smart console behavior (auto-close on success, stay open on errors)

**Technical Improvements:**
- Organized project structure
- Path auto-detection for portability
- Enhanced error messages
- Updated configuration system

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
2. Review `CONFIGURATION_README.md` in this folder
3. Examine the CSV export reports for detailed analysis
4. Open an issue with specific examples and CSV data

---

**SubFast - Fast subtitle renaming and embedding for all languages** 🚀
