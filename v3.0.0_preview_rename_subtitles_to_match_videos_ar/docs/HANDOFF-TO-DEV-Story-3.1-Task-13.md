# Developer Handoff: Story 3.1 Task 13 - Unified Configuration

**Date:** 2025-01-12  
**From:** Bob (Scrum Master)  
**To:** James (Developer)  
**Story:** 3.1 - Configuration File Handling  
**Task:** Task 13 - Unify Configuration Structure for Both Scripts

---

## 🎯 Mission

Implement unified `config.ini` structure that works for BOTH renaming and embedding scripts, with:
- ✅ Clearer key naming (detected_*, renaming_*, embedding_ prefixes)
- ✅ Empty language values by default
- ✅ Backward compatibility with auto-migration
- ✅ Graceful handling of missing sections
- ✅ Corrupted config auto-repair

---

## 📋 Story Status

**Updated:** Story 3.1 reopened and enhanced  
**Status:** In Progress (was: DONE)  
**File:** `docs/stories/3.1.configuration-file-handling.md`  
**New Task:** Task 13 added with comprehensive subtasks  
**New ACs:** 12-19 added

---

## 🔑 Key Name Changes Reference

### Shared Settings (→ [General])
- `video_extensions` → `detected_video_extensions`
- `subtitle_extensions` → `detected_subtitle_extensions`

### Renaming Script (→ [Renaming])
- `enable_export` → `renaming_report`
- `language_suffix` → `renaming_language_suffix` (EMPTY by default)

### Embedding Script (→ [Embedding])
- `language` → `embedding_language_code` (EMPTY by default)
- `csv_export` → `embedding_report`
- `default_track` → `default_flag`

### Section Changes
- `[FileFormats]` → Merged into `[General]`
- `[Reporting]` → Merged into `[Embedding]` as `embedding_report`

---

## 📐 New Unified Structure

```ini
# ============================================================================
# Unified Configuration - Subtitle Tools [AR]
# ============================================================================
# Shared by both renaming and embedding scripts
# Language values empty by default (populated for language-specific distributions)
# ============================================================================

[General]
# Video file extensions to detect (comma-separated, no dots)
detected_video_extensions = mkv, mp4

# Subtitle file extensions to detect (comma-separated, no dots)
detected_subtitle_extensions = srt, ass

[Renaming]
# Generate CSV report before renaming (true/false)
renaming_report = false

# Language suffix added to renamed files (leave empty for no suffix)
# Examples: ar, en, fr, es, ja
renaming_language_suffix = 

[Embedding]
# Path to mkvmerge.exe (leave empty to use script directory)
mkvmerge_path = 

# Language code for embedded subtitle track (leave empty for no language tag)
# Must be valid ISO 639-2 code (2-3 letters)
embedding_language_code = 

# Set embedded subtitle as default track (yes/no)
default_flag = yes

# Generate CSV report after embedding (true/false)
embedding_report = false
```

---

## ✅ What's Required

### 1. Migration Functions (Both Scripts)
Implement in both `rename_subtitles_to_match_videos_ar.py` and `embed_subtitles_to_match_videos_ar.py`:

**`migrate_old_config(config, config_path) -> bool`**
- Detect old key names
- Migrate to new key names
- Handle section renames
- Save config
- Return True if migrated

**`ensure_section_exists(config, section, defaults, config_path) -> bool`**
- Add missing sections
- Add missing keys
- Save config
- Return True if modified

**Corrupted Config Handling:**
- Try-except on `config.read()`
- Catch `MissingSectionHeaderError` and `ParsingError`
- Backup to timestamped file
- Recreate fresh config

### 2. Update Both Scripts

**rename_subtitles_to_match_videos_ar.py:**
- Update `load_configuration()` - read from new sections/keys
- Update `create_default_config_file()` - generate unified structure
- Replace ALL code references to old key names
- Add migration/section handling

**embed_subtitles_to_match_videos_ar.py:**
- Update `load_config()` - read from new sections/keys
- Update `create_default_config()` - generate unified structure
- Replace ALL code references to old key names
- Add migration/section handling
- Add reading of `detected_video_extensions` and `detected_subtitle_extensions` from `[General]`

### 3. Update Documentation

**CONFIGURATION_README.md:**
- Replace all old key names with new throughout
- Document unified structure
- Document migration behavior
- Note empty language defaults

### 4. Comprehensive Testing

Test EVERY scenario in Task 13:
- Fresh install (empty languages)
- Old renaming config migration
- Old embedding config migration
- Mixed old/new keys
- Missing sections
- Corrupted config
- Both scripts functionality
- Language-specific configs (ar, en, etc.)

---

## ⚠️ Critical Requirements

1. **Empty Language Defaults:** Template must have empty `renaming_language_suffix` and `embedding_language_code`

2. **Backward Compatibility:** Old configs must auto-migrate seamlessly without user intervention

3. **Both Scripts Must Work:** Test renaming then embedding, and embedding then renaming with unified config

4. **All Code References:** Search for old key names and replace throughout both scripts

---

## 🧪 Testing Checklist

- [ ] Fresh unified config - both scripts work
- [ ] Old renaming config - migrates and both scripts work
- [ ] Old embedding config - migrates and both scripts work  
- [ ] Corrupted config - backs up and recreates
- [ ] Missing sections - auto-adds
- [ ] Language-specific (ar) - both scripts work with ar populated
- [ ] Language-specific (en) - both scripts work with en populated
- [ ] All existing tests still pass
- [ ] New migration tests pass

---

## 📊 Estimated Effort

**Implementation:** 1.5-2 hours  
**Testing:** 1-1.5 hours  
**Total:** 2.5-3.5 hours

---

## 🚀 Ready for Implementation

Story 3.1 is updated and ready for Task 13 implementation. All requirements are documented in the story file with comprehensive subtasks.

**Good luck, James!** The user is counting on you to make both scripts work seamlessly together! 💪

---

**Note for Future:** After this is complete, the analyst will rebrand from "Subtitle Renamer Tool [AR]" to **"SubFast"** to reflect broader language support.
