# SubFast Project Structure

**Version:** 3.0.0 MVP  
**Last Updated:** 2025-01-05

---

## Overview

SubFast uses a flat project structure for simplicity and ease of deployment. All core files are located in a single directory with a Resources subfolder for assets.

---

## Directory Structure

```
rename_subtitles_to_match_videos_ar/          # Main project folder
│
├── Core Scripts
│   ├── rename_subtitles_to_match_videos_ar.py    # Subtitle renaming script
│   └── embed_subtitles_to_match_videos_ar.py     # Subtitle embedding script
│
├── Dependencies
│   ├── mkvmerge.exe                               # MKVToolNix utility (Windows)
│   └── config.ini                                 # Unified configuration file
│
├── Context Menu Integration
│   ├── add_subfast_menu.reg                       # Install unified context menu
│   └── remove_subfast_menu.reg                    # Remove context menu
│
├── Resources/                                     # Assets folder
│   ├── subfast_logo.ico                          # SubFast icon (user-provided)
│   └── README.txt                                # Icon requirements
│
├── Documentation
│   ├── README.md                                 # Main user documentation
│   └── CONFIGURATION_README.md                   # Configuration guide
│
└── Test Data & Utilities (excluded from distribution)
    ├── tests/                                    # Test files and scripts
    └── __pycache__/                              # Python cache (auto-generated)
```

---

## File Descriptions

### Core Scripts

#### `rename_subtitles_to_match_videos_ar.py`

**Purpose:** Automatically rename subtitle files to match video filenames

**Features:**
- Smart file matching (TV shows and movies)
- Episode number detection (S01E01 pattern)
- Year-based matching for movies
- Language suffix support
- CSV export

**Entry Point:** `if __name__ == "__main__": main()`

**Dependencies:**
- Standard library only (pathlib, re, configparser, csv, etc.)

---

#### `embed_subtitles_to_match_videos_ar.py`

**Purpose:** Embed external subtitle files into MKV video files

**Features:**
- Automatic subtitle embedding using mkvmerge
- Language code detection and configuration
- Default subtitle flag control
- Backup management (optional)
- Batch processing
- CSV export

**Entry Point:** `if __name__ == "__main__": main()`

**Dependencies:**
- Standard library + mkvmerge.exe

---

### Dependencies

#### `mkvmerge.exe`

**Purpose:** MKVToolNix command-line utility for subtitle embedding

**Version:** 88.0 ('All I Know') 64-bit

**Location:**
- Default: Same folder as scripts
- Custom: Specify path in `config.ini` → `mkvmerge_path`

**Source:** [MKVToolNix](https://mkvtoolnix.download/)

---

#### `config.ini`

**Purpose:** Unified configuration file for both scripts

**Auto-Creation:** Generated on first script run if missing

**Sections:**
- `[General]` - File extensions, console behavior
- `[Renaming]` - Language suffix, CSV export
- `[Embedding]` - mkvmerge path, language code, flags

**Location:** Must be in same folder as scripts

---

### Context Menu Integration

#### `add_subfast_menu.reg`

**Purpose:** Install SubFast cascading context menu in Windows Explorer

**Structure:**
```
SubFast (parent menu)
  ├── Rename Subtitles (calls renaming script)
  └── Embed Subtitles (calls embedding script)
```

**Requirements:**
- Administrator privileges
- Python in system PATH
- Logo file in Resources/ folder

**Registry Path:** `HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast`

---

#### `remove_subfast_menu.reg`

**Purpose:** Clean removal of SubFast context menu

**Action:** Deletes entire SubFast registry key and all children

**Requirements:** Administrator privileges

---

### Resources Folder

#### `subfast_logo.ico`

**Purpose:** Icon displayed in Windows context menu

**Format:** Windows Icon (.ico)

**Recommended Sizes:**
- 16x16 (small)
- 32x32 (medium)
- 48x48 (large)
- 256x256 (extra large)

**Placement:** User must place logo after extraction

---

#### `README.txt`

**Purpose:** Instructions for icon placement

**Content:** Icon format requirements and usage information

---

### Documentation

#### `README.md`

**Purpose:** Main user-facing documentation

**Content:**
- Feature overview
- Installation instructions
- Usage examples
- Configuration quick-start
- Troubleshooting

**Audience:** End users

---

#### `CONFIGURATION_README.md`

**Purpose:** Detailed configuration guide

**Content:**
- All config.ini settings explained
- Examples for common scenarios
- Context menu structure documentation

**Audience:** Power users, administrators

---

## Design Decisions

### Why Flat Structure?

**Advantages:**
1. **Simple Deployment** - Single folder to extract
2. **Easy Context Menu Integration** - `%~dp0` resolves to script directory
3. **Clear File Organization** - All core files immediately visible
4. **Minimal Complexity** - No nested paths to manage

**Trade-offs:**
- Less scalable for very large projects
- Resources folder is the only subdirectory

---

### Why Resources Subfolder?

**Reasons:**
1. **Asset Organization** - Separates binary assets from code
2. **Future Extensibility** - Easy to add more resources (icons, images, etc.)
3. **Clean Root** - Keeps main folder uncluttered

**Alternative Considered:**
- Root-level icon placement
- **Rejected:** Less organized, harder to manage multiple assets

---

### Why Unified Registry File?

**Previous Approach:**
- Separate .reg files for each feature
- Result: Two context menu entries

**Current Approach:**
- Single cascading menu with parent/child structure
- Result: One branded entry point with submenu

**Benefits:**
1. **User Experience** - Cleaner context menu
2. **Branding** - Single "SubFast" identity
3. **Maintainability** - One registry structure to manage
4. **Extensibility** - Easy to add more features as children

---

## Context Menu Implementation

### Windows Registry Structure

```
HKEY_CLASSES_ROOT\
  Directory\
    Background\
      shell\
        SubFast\                        # Parent menu
          "MUIVerb" = "SubFast"
          "SubCommands" = ""
          "Icon" = "[path to logo]"
          shell\
            Rename\                     # Child 1
              "MUIVerb" = "Rename Subtitles"
              "Position" = "Top"
              command\
                @ = "python.exe [path to script]"
            Embed\                      # Child 2
              "MUIVerb" = "Embed Subtitles"
              command\
                @ = "python.exe [path to script]"
```

### Key Concepts

- **`SubCommands=""`** → Enables cascading menu
- **`Position="Top"`** → Forces item to top of submenu
- **`%~dp0`** → Dynamic path to .reg file's directory
- **`%V`** → Passes target directory to script

---

## Distribution Package

### What to Include

✅ **Must Include:**
- Both Python scripts
- mkvmerge.exe
- Registry files (add/remove)
- Documentation (README.md, CONFIGURATION_README.md)
- Resources folder with README.txt

✅ **Optional:**
- Sample config.ini (or auto-generate on first run)
- Resources/subfast_logo.ico (or user provides)

❌ **Exclude:**
- `__pycache__/`
- `.pyc` files
- Test data
- Development tools
- Git files

---

## Future Scalability

If the project grows beyond flat structure:

### Option B: Organized Structure

```
subfast/
├── scripts/
│   ├── rename_subtitles_to_match_videos_ar.py
│   └── embed_subtitles_to_match_videos_ar.py
├── bin/
│   └── mkvmerge.exe
├── resources/
│   └── subfast_logo.ico
├── docs/
│   ├── README.md
│   └── CONFIGURATION_README.md
├── config.ini
└── [registry files]
```

**Migration Path:**
1. Update registry files with new paths
2. Update documentation
3. Provide migration script or instructions

---

## Version History

**v3.0.0 (MVP - Current)**
- Flat structure with Resources subfolder
- Unified context menu
- Complete documentation
- Both renaming and embedding features

**Future Considerations:**
- Installer package
- Windows Store distribution
- Auto-update mechanism

---

**Structure optimized for MVP deployment and user experience** 🏗️
