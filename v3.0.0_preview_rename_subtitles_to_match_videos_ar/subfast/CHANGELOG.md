# SubFast - Version 3.0.0 Release Notes

**Release Date:** 09-OCT-2025  
**Major Version Update:** v2.5.0 → v3.0.0

---

## 🎉 What's New in v3.0.0

SubFast v3.0.0 is a **major release** that brings a new **SubFast** branding and a second brand new major feature which is automatic soft-subtitle embedding into detected MKV videos matches (Automatic implementation of mkvmerge of the MKVToolNix suite)

### **🌟 Major Changes**

### 1. **Embed Subtitles Feature**
Soft-subtitle embedding of external subtitle files directly into detected MKV video files matches for seamless playback.
- Automatic subtitle/video match identification using same renaming logic (No need for renaming)
- Language code detection and configuration
- Default subtitle flag control
- Backup management
- Batch processing with progress tracking
- Configurable CSV export for reporting the results

#### 2. **Dual-Feature Windows Context Menu**
- **New:** Unified "SubFast" cascading menu when right click:
  - **SubFast** (parent menu with icon)
    - → Rename subtitles
    - → Embed subtitles
	
### 3. **Smart Console Behavior**
- **Auto-close on success** - No manual window closing needed
- **Stay open on errors** - Review error messages before closing
- Configurable via `keep_console_open` in config.ini


## 📦 Migration Guide: Upgrading from v2.x to v3.0.0

**⚠️ IMPORTANT:** v3.0.0 is NOT a drop-in replacement. Follow these steps to upgrade.

### **Step 1: Remove Old Context Menu** (Required)

1. Navigate to your old installation folder:
   ```
   C:\rename_subtitles_to_match_videos_ar\
   ```

2. **If you have v2.0.0 or newer:**
   - Double-click: `remove_subtitle_rename_menu.reg`
   - Click "Yes" to remove

3. **Verify removal:**
   - Right-click in any folder
   - Old context menu entries should be gone

4. **Delete the entire folder** `C:\rename_subtitles_to_match_videos_ar\` 

### **Step 2: Delete Old Installation** (Safe to Remove)

1. Close any open Explorer windows in the old folder
2. Delete the entire folder:
   ```
   C:\rename_subtitles_to_match_videos_ar\
   ```

### **Step 3: Install SubFast v3.0.0**

1. **Download** SubFast v3.0.0 ZIP file (two bundles with one of them pre-configured for Arabic locals)

2. **Extract** to the new location:
   ```
   C:\subfast\
   ```
   
   **IMPORTANT:** The exact path must be `C:\subfast`

### **Step 4: Install New Context Menu**

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
	 
---

## 🔧 Configuration Changes

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
- ✅ Added `keep_console_open` for console behavior

---

## 🛠️ Technical Improvements


### **Error Handling**
- Improved error messages with specific file paths
- Better validation of required files
- Clear troubleshooting guidance

#### **Project Directory Structure**
- **Old:**
  ```
  rename_subtitles_to_match_videos_ar/
  ├── rename_subtitles_to_match_videos_ar.py
  ├── config.ini
  ├── ARAB_STREAMS_LOGO.ico
  ├── CONFIGURATION_README.md
  ├── ARAB_STREAMS_LOGO.ico
  ├── add_subtitle_rename_menu.reg
  └── remove_subtitle_rename_menu.reg
  ```

- **New:** Organized folder hierarchy
  ```
  subfast/
  ├── scripts/          ← Python scripts
  ├── bin/              ← Binary tools (mkvmerge)
  ├── resources/        ← Logo and documentation
  ├── config.ini        ← Root level for easy access
  └── registry files... ← Root level for easy installation