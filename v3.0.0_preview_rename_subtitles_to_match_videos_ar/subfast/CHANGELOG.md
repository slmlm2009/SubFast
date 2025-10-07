# SubFast - Version 3.0.0 Release Notes

**Release Date:** January 2025  
**Major Version Update:** v2.5.0 → v3.0.0

> **📖 Note:** This file is available on the GitHub repository. The downloaded ZIP package contains only essential operational files. For full documentation, visit the GitHub repository.

---

## 🎉 What's New in v3.0.0

SubFast v3.0.0 is a **major release** that brings unified branding, professional project structure, and dual-feature integration in a single context menu.

### **🌟 Major Changes**

#### 1. **Unified "SubFast" Branding**
- **Old:** Separate context menu entries with different names
- **New:** Single branded "SubFast" cascading menu
- Professional icon displays in Windows Explorer
- Consistent branding across all features and documentation

#### 2. **Dual-Feature Context Menu**
- **Old:** Two separate context menu entries:
  - "Rename subtitle files"
  - "Embed subtitles to mkv files"
- **New:** Unified cascading menu:
  - **SubFast** (parent menu with icon)
    - → Rename subtitles
    - → Embed subtitles

**Benefit:** Cleaner right-click menu, better organization

#### 3. **Professional Project Structure**
- **Old:** Flat folder structure
  ```
  rename_subtitles_to_match_videos_ar/
  ├── rename_subtitles_to_match_videos_ar.py
  ├── embed_subtitles_to_match_videos_ar.py
  ├── mkvmerge.exe
  ├── config.ini
  └── registry files...
  ```

- **New:** Organized folder hierarchy
  ```
  subfast/
  ├── scripts/          ← Python scripts
  ├── bin/              ← Binary tools (mkvmerge)
  ├── resources/        ← Logo and documentation
  ├── config.ini        ← Root level for easy access
  └── registry files... ← Root level for easy installation
  ```

**Benefit:** Professional organization, easier maintenance, clearer structure

#### 4. **Simplified Installation**
- **Old:** Required specific path with long folder name
- **New:** Clean installation path: `C:\subfast`
- Registry-based installation (simple double-click)
- Clear, straightforward setup process

#### 5. **Enhanced Documentation**
- Comprehensive documentation on GitHub repository
- CONFIGURATION_README.md included in package for configuration reference
- Detailed CHANGELOG.md and UPGRADE_GUIDE.md on GitHub
- Updated examples and troubleshooting guides

---

## ✨ New Features

### **Smart Console Behavior**
- **Auto-close on success** - No manual window closing needed
- **Stay open on errors** - Review error messages before closing
- Configurable via `keep_console_open` in config.ini

### **Location-Aware Scripts**
- Scripts automatically detect their location
- Config.ini and mkvmerge.exe found via relative paths
- More portable and flexible deployment

### **Updated Configuration System**
- Cleaner config.ini format
- Better organized sections (General, Renaming, Embedding)
- Comprehensive configuration documentation

---

## 🔄 Breaking Changes

### **Folder Name Changed**
- **Old:** `rename_subtitles_to_match_videos_ar`
- **New:** `subfast`

### **Installation Path Changed**
- **Old:** `C:\rename_subtitles_to_match_videos_ar`
- **New:** `C:\subfast`

### **Script Names Changed**
- **Old:** 
  - `rename_subtitles_to_match_videos_ar.py`
  - `embed_subtitles_to_match_videos_ar.py`
- **New:**
  - `scripts/subfast_rename.py`
  - `scripts/subfast_embed.py`

### **Registry Files Changed**
- **Old:** Separate registry files for each feature
  - `add_subtitle_rename_menu.reg`
  - `add_embed_subtitle_menu.reg`
- **New:** Unified registry files
  - `add_subfast_menu.reg` (installs both features)
  - `remove_subfast_menu.reg` (removes both features)

### **Context Menu Structure Changed**
- **Old:** Two separate top-level entries
- **New:** One parent "SubFast" menu with two sub-items

---

## 📦 Migration Guide: Upgrading from v2.x to v3.0.0

**⚠️ IMPORTANT:** v3.0.0 is NOT a drop-in replacement. Follow these steps carefully to upgrade.

### **Step 1: Remove Old Context Menu** (Required)

1. Navigate to your old installation folder:
   ```
   C:\rename_subtitles_to_match_videos_ar\
   ```

2. **If you have v2.5.0 or newer:**
   - Double-click: `remove_subtitle_rename_menu.reg`
   - Click "Yes" to remove
   - Double-click: `remove_embed_subtitle_menu.reg`
   - Click "Yes" to remove

3. **If you have v2.0.0 - v2.4.x:**
   - Locate your old removal registry files
   - Run them to clean up old context menu entries

4. **Verify removal:**
   - Right-click in any folder
   - Old context menu entries should be gone

### **Step 2: Backup Your Configuration** (Optional but Recommended)

If you customized your `config.ini` file:

1. Open: `C:\rename_subtitles_to_match_videos_ar\config.ini`
2. Copy your custom settings (language suffix, file extensions, etc.)
3. Save for later reference

### **Step 3: Delete Old Installation** (Safe to Remove)

1. Close any open Explorer windows in the old folder
2. Delete the entire folder:
   ```
   C:\rename_subtitles_to_match_videos_ar\
   ```

**What you're removing:**
- ✅ Old Python scripts (renamed in v3.0.0)
- ✅ Old registry files (replaced in v3.0.0)
- ✅ Old folder structure (reorganized in v3.0.0)

**Note:** Your video/subtitle files are NOT affected. This only removes the SubFast tool itself.

### **Step 4: Install SubFast v3.0.0**

1. **Download** SubFast v3.0.0 ZIP file

2. **Extract** to the new location:
   ```
   C:\subfast\
   ```
   
   **IMPORTANT:** The exact path must be `C:\subfast`

3. **Verify** the folder structure:
   ```
   C:\subfast\
   ├── scripts/
   ├── bin/
   ├── resources/
   ├── config.ini
   ├── add_subfast_menu.reg
   └── remove_subfast_menu.reg
   ```

### **Step 5: Configure SubFast** (Restore Your Settings)

1. Open: `C:\subfast\config.ini`

2. **Apply your old settings** (if you backed them up):
   ```ini
   [Renaming]
   renaming_language_suffix = ar    ← Your language
   
   [Embedding]
   embedding_language_code = ara    ← Your language code
   ```

3. Save the file

### **Step 6: Install New Context Menu**

1. Navigate to: `C:\subfast\`

2. **Double-click:** `add_subfast_menu.reg`

3. **Click "Yes"** when prompted to merge registry keys

4. **Approve UAC** if prompted

5. **Verify installation:**
   - Right-click in any folder
   - Look for **SubFast** menu with icon
   - Expand it to see:
     - Rename subtitles
     - Embed subtitles

### **Step 7: Test the Installation**

1. **Create a test folder** with:
   - 1 video file (e.g., `Test S01E01.mkv`)
   - 1 subtitle file (e.g., `subtitle-01.srt`)

2. **Test Rename:**
   - Right-click in the test folder
   - Select: SubFast → **Rename subtitles**
   - Verify subtitle renamed to match video

3. **Test Embed:**
   - Right-click in the test folder
   - Select: SubFast → **Embed subtitles**
   - Verify subtitle embedded into MKV

**✅ If both tests pass, migration is complete!**

---

## 🔧 Configuration Changes

### **Config.ini Format Updated**

**v2.5.0 format:**
```ini
[General]
enable_export = true
language_suffix = ar

[FileFormats]
video_extensions = mkv, mp4
subtitle_extensions = srt, ass
```

**v3.0.0 format:**
```ini
[General]
detected_video_extensions = mkv, mp4
detected_subtitle_extensions = srt, ass
keep_console_open = false

[Renaming]
renaming_report = true
renaming_language_suffix = ar

[Embedding]
mkvmerge_path = bin\mkvmerge.exe
embedding_language_code = ara
default_flag = true
embedding_report = true
```

**Changes:**
- ✅ Split into separate `[Renaming]` and `[Embedding]` sections
- ✅ Renamed `enable_export` → `renaming_report` / `embedding_report`
- ✅ Renamed `language_suffix` → `renaming_language_suffix`
- ✅ Added `embedding_language_code` for embed feature
- ✅ Added `keep_console_open` for console behavior
- ✅ Moved to root level (easier access)

---

## 🛠️ Technical Improvements

### **Path Resolution**
- Scripts auto-detect installation location
- Config.ini found via relative path from script location
- mkvmerge.exe found via configurable relative path

### **Error Handling**
- Improved error messages with specific file paths
- Better validation of required files
- Clear troubleshooting guidance

### **Performance**
- No performance changes (maintains v2.5.0 optimizations)
- 12x episode caching still active
- Regex pre-compilation preserved

---

## 📊 Compatibility

### **Windows Compatibility**
- ✅ Windows 10 (all versions)
- ✅ Windows 11 (all versions)
- ✅ Requires Python 3.7+ (same as v2.5.0)

### **Config.ini Compatibility**
- ⚠️ **NOT directly compatible** with v2.5.0 format
- Manual migration required (see Configuration Changes above)
- Default config.ini provided with sensible defaults

### **Script Functionality**
- ✅ All v2.5.0 features preserved
- ✅ Same episode pattern recognition (25+ patterns)
- ✅ Same matching algorithms
- ✅ Same CSV export functionality

---

## ❓ Frequently Asked Questions

### **Can I keep both v2.x and v3.0.0 installed?**
**No.** The context menu entries will conflict. You must remove v2.x before installing v3.0.0.

### **Will my old config.ini work with v3.0.0?**
**No.** The config format changed. You'll need to manually transfer your settings to the new format (see Configuration Changes).

### **What happens to my videos and subtitles?**
**Nothing.** SubFast only affects its own program files. Your media files remain untouched during the upgrade.

### **Do I need to reinstall Python?**
**No.** If Python 3.7+ is already installed and working with v2.x, it will continue to work with v3.0.0.

### **Can I go back to v2.x after upgrading?**
**Yes.** Keep a backup of your v2.x folder before deleting. To downgrade:
1. Remove v3.0.0 context menu
2. Delete `C:\subfast\`
3. Restore v2.x folder
4. Reinstall v2.x context menu

### **Where is the documentation now?**
**On GitHub Repository:**
- `README.md` - Main documentation and installation guide
- `CHANGELOG.md` - Release notes and upgrade information (this file)
- `UPGRADE_GUIDE.md` - Quick migration guide from v2.x

**In Your Installation (resources\doc\):**
- `CONFIGURATION_README.md` - Configuration reference guide

---

## 🐛 Known Issues

### **Windows Explorer Refresh**
- **Issue:** Context menu may not update immediately after installation
- **Solution:** Restart Windows Explorer or log out/in

### **UAC Prompts**
- **Issue:** Registry modification requires Administrator approval
- **Solution:** Click "Yes" on UAC prompt. This is normal and expected.

### **Path Hardcoded to C:\subfast**
- **Issue:** Registry files only work if installed at `C:\subfast`
- **Solution:** Extract to exactly `C:\subfast` (not D:\, Desktop, etc.)

---

## 📝 Full Changelog

### **Added**
- ✅ Unified "SubFast" cascading context menu
- ✅ SubFast logo integration in context menu
- ✅ Professional folder structure (scripts/, bin/, resources/)
- ✅ Smart console behavior (auto-close on success)
- ✅ Location-aware path resolution
- ✅ Comprehensive documentation on GitHub repository
- ✅ Enhanced configuration guide (CONFIGURATION_README.md)
- ✅ `keep_console_open` configuration option
- ✅ Separate `[Renaming]` and `[Embedding]` config sections

### **Changed**
- 🔄 Folder name: `rename_subtitles_to_match_videos_ar` → `subfast`
- 🔄 Installation path: `C:\rename_subtitles_to_match_videos_ar` → `C:\subfast`
- 🔄 Script names: Added `subfast_` prefix, moved to `scripts/` folder
- 🔄 Context menu: Separate entries → Unified cascading menu
- 🔄 Registry files: Unified into `add_subfast_menu.reg` and `remove_subfast_menu.reg`
- 🔄 Config.ini: Reorganized into clearer sections
- 🔄 Documentation: Consolidated and moved to `resources/doc/`

### **Removed**
- ❌ Old separate context menu entries
- ❌ Flat folder structure
- ❌ Old registry file format
- ❌ Long folder/script names

### **Deprecated**
- ⚠️ v2.x config.ini format (manual migration required)
- ⚠️ Old installation paths
- ⚠️ Old registry files

---

## 🙏 Acknowledgments

Thank you to all SubFast users for your feedback and support. Version 3.0.0 represents a major milestone in making SubFast more professional, easier to use, and better organized.

---

## 📞 Support

For issues with the v3.0.0 update:
1. Review the README.md on GitHub (complete installation guide)
2. Check this CHANGELOG.md on GitHub (full release notes and migration guide)
3. See UPGRADE_GUIDE.md on GitHub for quick migration steps
4. Consult `C:\subfast\resources\doc\CONFIGURATION_README.md` for configuration help
5. Report issues on GitHub with detailed steps to reproduce

---

**SubFast v3.0.0 - Fast subtitle renaming and embedding for all languages** 🚀
