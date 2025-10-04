# Sprint Change Proposal: Story 3.1 Configuration Unification

**Date:** 2025-01-12  
**Prepared By:** Bob (Scrum Master)  
**Change Type:** Enhancement - Configuration Integration  
**Status:** Awaiting Approval

---

## Executive Summary

During Story 3.2 manual testing, a critical integration issue was discovered: the renaming and embedding scripts have incompatible `config.ini` structures, preventing them from coexisting in the same deployment folder. This proposal outlines reopening Story 3.1 to implement a unified configuration structure with backward compatibility and auto-migration.

**Impact:** Story 3.1 must be reopened and enhanced with Task 6  
**Estimated Effort:** 1-2 hours implementation + comprehensive testing  
**Risk Level:** Medium (code changes in both scripts, requires thorough testing)

---

## 1. Issue Analysis

### Triggering Event
**Story 3.2** (Windows Context Menu Integration) - Discovered during manual testing at deployment location `C:\rename_subtitles_to_match_videos_ar\`

### Core Problem
When both scripts are deployed to the same folder:
- **Renaming script** creates config with `[General]` and `[FileFormats]` sections
- **Embedding script** expects `[Embedding]` and `[Reporting]` sections
- When one config exists, the other script cannot read its required settings
- Scripts fail to auto-create config when file already exists (as designed)
- Result: Users must manually maintain separate incompatible configs

### Root Cause
Story 3.1 implemented configuration for embedding script without considering integration with existing renaming script configuration.

### Evidence
- Both scripts deployed to `C:\rename_subtitles_to_match_videos_ar\`
- Existing renaming script config.ini present
- Embedding script could not read configuration values
- Manual testing confirmed incompatibility

---

## 2. Epic & Story Impact

### Epic 3: User Experience & Configuration

**Story 3.1: Configuration File Handling**
- **Status Change:** DONE → In Progress
- **Action:** Add Task 6 (unified configuration)
- **New ACs:** 12-19 (unified structure requirements)

**Story 3.2: Windows Context Menu Integration**
- **Status:** Ready for Review
- **Action:** No changes needed

**Story 3.3: User Feedback and CSV Reporting**
- **Status:** Not started
- **Action:** No changes needed (will reference unified config)

### Future Epics
- **Impact:** None identified

---

## 3. Artifact Updates Required

### A. Story 3.1 Changes

#### New Task 6: Unify Configuration Structure

**Add complete Task 6 with subtasks covering:**

1. **Unified Structure Design** with improved naming:
   - `[General]` section: `detected_video_extensions`, `detected_subtitle_extensions`
   - `[Renaming]` section: `renaming_report`, `renaming_language_suffix`
   - `[Embedding]` section: `mkvmerge_path`, `embedding_language_code`, `default_flag`, `embedding_report`
   - **Default template:** Empty language values (for language-specific distributions)

2. **Backward Compatibility Migration:**
   - Auto-detect old key names
   - Migrate old → new key names
   - Preserve user's custom values
   - Save migrated config
   - Print migration messages

3. **Graceful Section Handling:**
   - Auto-add missing sections with defaults
   - Auto-add missing keys with defaults
   - Save updated config

4. **Corrupted Config Handling:**
   - Catch `MissingSectionHeaderError`
   - Backup to timestamped file
   - Recreate fresh config
   - User guidance messages

5. **Code Updates:**
   - Update `rename_subtitles_to_match_videos_ar.py` config loading and creation
   - Update `embed_subtitles_to_match_videos_ar.py` config loading and creation
   - Update all code references to use new key names
   - Maintain fallback defaults

6. **Documentation Updates:**
   - Update `CONFIGURATION_README.md` with new structure and naming
   - Document migration behavior
   - Note empty language defaults

7. **Comprehensive Testing:**
   - Fresh install scenario
   - Old renaming config migration
   - Old embedding config migration
   - Mixed old/new keys
   - Missing sections
   - Corrupted config
   - Both scripts functionality
   - Language-specific configs

#### New Acceptance Criteria (12-19)

**Add to Story 3.1:**

12. Configuration file uses unified structure with clearer naming (`detected_*`, `renaming_*`, `embedding_*` prefixes)
13. Shared settings in `[General]` section, script-specific in `[Renaming]` and `[Embedding]`
14. Default template has EMPTY language values (language-specific versions distributed separately)
15. Old configuration key names automatically migrate to new names on first run
16. If config missing sections, scripts auto-add with defaults
17. Corrupted configs (missing section headers) backed up and recreated
18. Both scripts fully compatible with unified config structure
19. Backward compatibility maintained: old configs automatically updated to new format

#### Status Update

**Change:** `Status: DONE` → `Status: In Progress`

---

### B. Code Changes Required

#### rename_subtitles_to_match_videos_ar.py

**Functions to Update:**
1. `load_configuration()`:
   - Add migration logic for old → new key names
   - Read from `[General]` section: `detected_video_extensions`, `detected_subtitle_extensions`
   - Read from `[Renaming]` section: `renaming_report`, `renaming_language_suffix`
   - Handle missing sections gracefully
   - Add corrupted config handling

2. `create_default_config_file()`:
   - Generate unified structure with all three sections
   - Use new key names
   - Leave `renaming_language_suffix` EMPTY
   - Include comprehensive comments

3. **All references to config keys throughout code:**
   - `enable_export` → `renaming_report`
   - `language_suffix` → `renaming_language_suffix`
   - `video_extensions` → `detected_video_extensions`
   - `subtitle_extensions` → `detected_subtitle_extensions`

#### embed_subtitles_to_match_videos_ar.py

**Functions to Update:**
1. `load_config()`:
   - Add migration logic for old → new key names
   - Read from `[General]`: `detected_video_extensions`, `detected_subtitle_extensions`
   - Read from `[Embedding]`: `mkvmerge_path`, `embedding_language_code`, `default_flag`, `embedding_report`
   - Handle missing sections gracefully
   - Add corrupted config handling

2. `create_default_config()`:
   - Generate unified structure with all three sections
   - Use new key names
   - Leave `embedding_language_code` EMPTY
   - Include comprehensive comments

3. **All references to config keys throughout code:**
   - `language` → `embedding_language_code`
   - `csv_export` → `embedding_report`
   - `default_track` → `default_flag`
   - Add references to `detected_video_extensions`, `detected_subtitle_extensions` from `[General]`

#### CONFIGURATION_README.md

**Updates Required:**
- Replace all old key names with new names throughout document
- Document unified structure with three sections
- Explain naming convention (detected_, renaming_, embedding_ prefixes)
- Document migration behavior and backward compatibility
- Note empty language defaults in template
- Update all example configurations
- Update troubleshooting section

---

### C. Testing Changes Required

**New Test Files/Cases:**
1. `test_config_migration.py` - Test backward compatibility
   - Test old renaming format migration
   - Test old embedding format migration
   - Test mixed old/new keys
   - Test corrupted config handling

2. Update existing config tests:
   - Update all test assertions to use new key names
   - Add tests for missing section handling
   - Add tests for graceful degradation

3. **Integration testing scenarios:**
   - Both scripts with fresh unified config
   - Renaming script with old config, embedding script uses it
   - Embedding script with old config, renaming script uses it
   - Both scripts run successfully in sequence

---

## 4. Migration Mapping Reference

### Old → New Key Name Changes

**Shared Settings (now in [General]):**
- `video_extensions` → `detected_video_extensions`
- `subtitle_extensions` → `detected_subtitle_extensions`

**Renaming Script (now in [Renaming]):**
- `enable_export` → `renaming_report`
- `language_suffix` → `renaming_language_suffix`

**Embedding Script (now in [Embedding]):**
- `language` → `embedding_language_code`
- `csv_export` → `embedding_report`
- `default_track` → `default_flag`

### Old → New Section Changes

- `[FileFormats]` → `[General]`
- `[Reporting]` → Merged into `[Embedding]`

---

## 5. Unified Config Template (New Format)

```ini
# ============================================================================
# Unified Configuration - Subtitle Tools [AR]
# ============================================================================
# This configuration is shared by both renaming and embedding scripts
# Note: Language values are empty by default for language-agnostic distribution
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

# ============================================================================
# NOTE: For language-specific distributions, pre-populate:
#   - renaming_language_suffix (e.g., 'ar' for Arabic version)
#   - embedding_language_code (e.g., 'ar' for Arabic version)
# ============================================================================
```

---

## 6. Implementation Plan

### Phase 1: Update Story 3.1
- [ ] Add Task 6 with complete subtasks
- [ ] Add Acceptance Criteria 12-19
- [ ] Change status: DONE → In Progress
- [ ] Add change log entry documenting reopening

### Phase 2: Implement Code Changes
- [ ] Update `rename_subtitles_to_match_videos_ar.py`
- [ ] Update `embed_subtitles_to_match_videos_ar.py`
- [ ] Implement migration functions
- [ ] Implement section handling
- [ ] Implement corrupted config handling

### Phase 3: Update Documentation
- [ ] Update `CONFIGURATION_README.md` with new structure

### Phase 4: Comprehensive Testing
- [ ] Test all migration scenarios
- [ ] Test backward compatibility
- [ ] Test both scripts in sequence
- [ ] Verify all acceptance criteria met

### Phase 5: Story Completion
- [ ] Mark Task 6 complete
- [ ] Update File List
- [ ] Set status: Ready for Review
- [ ] Hand off for QA review

---

## 7. Risk Assessment

### Implementation Risks

**Risk 1: Breaking Existing Configs**
- **Mitigation:** Backward compatibility with auto-migration
- **Verification:** Test with all old config formats

**Risk 2: Migration Logic Bugs**
- **Mitigation:** Comprehensive test coverage
- **Verification:** Test mixed old/new scenarios

**Risk 3: Performance Impact**
- **Mitigation:** Migration happens once, cached after
- **Verification:** Benchmark config loading time

### Rollback Plan
- Migration preserves old values
- If issues found, users can manually edit config
- Documentation provides clear structure reference

---

## 8. Success Criteria

**Story 3.1 Enhancement Complete When:**
- [ ] Unified config structure implemented
- [ ] Both scripts read from unified config correctly
- [ ] Old configs auto-migrate to new format
- [ ] All backward compatibility scenarios tested
- [ ] Documentation updated and accurate
- [ ] Both scripts function correctly with unified config
- [ ] All 19 acceptance criteria met

---

## 9. Next Steps & Handoff

### Immediate Actions (Scrum Master - Bob)
1. **Obtain user approval** for this Sprint Change Proposal
2. **Update Story 3.1** with Task 6 and new ACs
3. **Change Story 3.1 status** to In Progress
4. **Hand off to Developer** (James) for implementation

### Developer Actions (After Approval)
1. Implement Task 6 following the detailed subtasks
2. Update both Python scripts with new key names
3. Implement migration and section handling logic
4. Update documentation
5. Execute comprehensive test suite
6. Mark story Ready for Review

### Future Work (Noted for Analyst)
**Rebranding:** The analyst will rebrand from "Subtitle Renamer Tool [AR]" to "SubFast" throughout all project documentation, reflecting broader language focus and expanded functionality.

---

## 10. Approval Required

**User Approval Checkpoint:**

I need your explicit approval to proceed with:
- [ ] Reopening Story 3.1 (status: DONE → In Progress)
- [ ] Adding Task 6 (unified configuration)
- [ ] Adding Acceptance Criteria 12-19
- [ ] Implementing code changes in both scripts
- [ ] All proposed changes documented above

**Do you approve this Sprint Change Proposal?**

Once approved, I will:
1. Update Story 3.1 immediately
2. Hand off to Developer (James) for implementation
3. Track progress through to completion

---

**Please confirm: Do you approve these changes?**
