# Sprint Change Proposal: Story 2.2 Backup Strategy Revision

**Date:** 2025-01-12  
**Proposed By:** User  
**Analyzed By:** Bob (Scrum Master)  
**Status:** ✅ APPROVED  
**Approved By:** User  
**Approval Date:** 2025-01-12

---

## Executive Summary

**Change Type:** Significant Enhancement - Backup Strategy Revision

**Original Approach:**
- Rename `video.mkv` → `video.original.mkv` (in-place backup)
- Create merged file as `video.mkv`
- User manually deletes `.original.mkv` files after verification

**Revised Approach:**
- Create temporary `video.embedded.mkv` during merge
- On success: Move originals to `backups/` directory
- Rename `video.embedded.mkv` → `video.mkv`
- Result: Clean working directory with only embedded videos, all originals in `backups/`

**Rationale for Change:**
✅ **Safer:** Original files never touched until merge succeeds  
✅ **Cleaner:** Working directory only contains final embedded videos  
✅ **Organized:** All backups centralized in one `backups/` directory  
✅ **Explicit:** Temporary `.embedded.mkv` makes process transparent  
✅ **Reversible:** Easy to restore from `backups/` directory

---

## Impact Analysis

### Affected Artifacts

| Artifact | Impact Level | Changes Required |
|----------|--------------|------------------|
| Story 2.2 | 🔴 HIGH | Complete rewrite of ACs, technical guidance, code examples, tasks |
| Epic 2 (PRD) | 🟡 MEDIUM | Update Story 2.2 section with new ACs |
| Architecture Doc | 🟡 MEDIUM | Update `file_manager` component, sequence diagram |
| Story 2.3 | 🟢 LOW | May reference backup behavior (verify during draft) |

### Scope Impact

**MVP Scope:** ✅ NO CHANGE
- Still delivers FR5 (Backup and Output File Management)
- Implementation approach changed, not the feature itself

**Timeline Impact:** ✅ MINIMAL
- Same complexity level (file operations)
- Possibly easier (no restore logic on failure)
- Estimated effort unchanged

**Risk Assessment:** ✅ REDUCED RISK
- Safer approach (originals untouched until success)
- Simpler error handling (just delete temp file)
- Better user experience (cleaner working directory)

---

## Detailed Changes

### 1. Story 2.2 Updates

**File:** `docs/stories/2.2.backup-and-output-file-management.md`

#### Story Statement
**FROM:**
> As a user, I want the script to create backups of my original files and generate new merged files safely, so that I don't lose any data if something goes wrong.

**TO:**
> As a user, I want the script to create embedded videos with temporary names, then safely move originals to a `backups/` directory after successful merge, so that I don't lose any data and my working directory only contains the final embedded videos.

#### Acceptance Criteria (Complete Replacement)
**OLD (7 ACs):** Focused on `.original.mkv` renaming approach

**NEW (9 ACs):** Focused on `backups/` directory approach
1. Create temporary `.embedded.mkv` file
2. Create `backups/` directory on successful merge
3. Move original video to `backups/`
4. Move original subtitle to `backups/`
5. Rename temp `.embedded.mkv` to original name
6. Delete temp file on failure
7. Check disk space before operations
8. Intelligent collision handling (check each file independently)
9. Users can restore from `backups/` directory

#### Technical Guidance Changes
- **Workflow:** Complete rewrite from rename-based to directory-based
- **Functions:** 5 new functions (ensure_backups_directory, backup_originals, safe_delete_subtitle, rename_embedded_to_final, cleanup_failed_merge)
- **Error Handling:** Simplified (no restore needed, just cleanup)
- **Code Examples:** All code snippets rewritten

#### Tasks Changes
**OLD:** 7 tasks focused on rename/restore workflow

**NEW:** 8 tasks focused on directory/move workflow
- Task 1: Disk space checking (updated calculation)
- Task 2: Backups directory management (NEW)
- Task 3: Intelligent backup logic (4 collision scenarios)
- Task 4: Safe subtitle deletion (NEW)
- Task 5: File renaming and cleanup (NEW)
- Task 6: Integration into batch processing
- Task 7: Console output messages
- Task 8: Test suite creation

#### Testing Changes
- **Unit Tests:** 10 tests (was 6)
  - Added: backups directory creation
  - Added: 4 collision scenarios
  - Added: safe subtitle deletion (2 tests)
  - Added: temp file cleanup
  - Removed: user prompt mocking tests
- **Integration Tests:** Enhanced to verify `backups/` directory, subtitle deletion, re-run behavior

---

### 2. Epic 2 (PRD) Updates

**File:** `docs/prd/epic-2-file-discovery-and-management.md`

#### Story 2.2 Section
**Changes:** Replace entire Story 2.2 section with updated story statement and 9 new acceptance criteria (same as Story 2.2 file)

**Impact:** Documentation alignment only, no functional change to Epic 2 overall goals

---

### 3. Architecture Document Updates

**File:** `docs/architecture/architecture-document-subtitle-renamer-tool-ar-subtitle-embedding-feature.md`

#### Component Breakdown - file_manager
**FROM:**
> Handles the file system operations as defined in the PRD (renaming the original video file).

**TO:**
> Handles file system operations for the backup and output workflow:
> - Creates `backups/` directory on first successful merge
> - Moves original video and subtitle files to `backups/` directory
> - Handles collision detection (skip backup if files already exist)
> - Renames `.embedded.mkv` temporary files to final `.mkv` names
> - Cleans up temporary `.embedded.mkv` files on merge failures
> - Removes subtitle files from working directory after successful backup

#### Sequence Diagram
**Changes:**
- Added FileSystem participant
- Replaced simple `rename_original_video()` with detailed workflow
- Added `alt` blocks for merge success/failure
- Added nested `alt` for backup collision handling
- Shows temp file creation, backup moves, final rename, cleanup
- Added user feedback at end

**Impact:** More accurate representation of the actual workflow

#### Source Tree
**NO CHANGES:** Per user request, `backups/` directory is situational (created in user's media location), not part of project source tree at `C:/rename_subtitles_to_match_videos_ar/`

---

## Change Workflow Details

### New Workflow Steps

```
1. Check disk space (video + subtitle + 10% overhead)
2. Create video.embedded.mkv via mkvmerge
3. If merge fails:
   → Delete video.embedded.mkv
   → Log error
   → Continue to next file
4. If merge succeeds:
   → Create backups/ directory (if doesn't exist)
   → Check backups/video.mkv exists? 
     → No: Move video.mkv → backups/video.mkv
     → Yes: Skip, log "Backup exists"
   → Check backups/subtitle.srt exists?
     → No: Move subtitle.srt → backups/subtitle.srt
     → Yes: Skip, log "Backup exists"
   → Delete subtitle from working dir (ONLY if in backups/)
   → Rename video.embedded.mkv → video.mkv
   → Log success
```

### Safety Features

**Before Deletion Check:**
- Subtitle is ONLY deleted if `backups/subtitle.srt` exists
- If not in backups/, subtitle remains in working directory with warning
- Prevents data loss from backup failures

**Collision Handling:**
- Each file checked independently
- Video and subtitle can have different backup states
- Allows re-running script safely (updates embedded version without losing backups)

---

## Configuration Changes

**Current Config (AC 6 removed):**
- No new configuration needed for basic functionality
- Future enhancement: Make backup directory name configurable

**No Config Changes Required for Story 2.2 Implementation**

---

## Testing Changes

### New Unit Tests (10 total)

1. `test_ensure_backups_directory_new` - Verify backups/ creation
2. `test_backup_originals_both_new` - Both files backed up
3. `test_backup_originals_video_exists` - Only subtitle backed up
4. `test_backup_originals_subtitle_exists` - Only video backed up
5. `test_backup_originals_both_exist` - Neither backed up
6. `test_safe_delete_subtitle_in_backups` - Subtitle deleted safely
7. `test_safe_delete_subtitle_not_in_backups` - Subtitle kept if not backed up
8. `test_cleanup_failed_merge` - Temp file deleted on failure
9. `test_disk_space_check_sufficient` - Sufficient space check
10. `test_disk_space_check_insufficient` - Insufficient space check

### Integration Test Enhancements

- Verify `backups/` directory created
- Verify original files moved to `backups/`
- Verify subtitles removed from working directory
- Verify `.embedded.mkv` files don't remain
- Test re-run behavior (backup collision)
- Test failure cleanup (temp file deletion)

---

## Risk Assessment

**Risks Mitigated by Change:**
1. ✅ Data loss during merge (originals untouched until success)
2. ✅ Cluttered working directory (cleaner final state)
3. ✅ Confusing file states (temp files clearly marked)

**New Risks Introduced:**
1. 🟡 Disk space requirement slightly higher (temp + original + embedded briefly)
   - **Mitigation:** Already checking disk space before operations
2. 🟢 Users might forget backups/ exists
   - **Mitigation:** Clear console message at end

**Overall Risk:** ✅ REDUCED (safer approach)

---

## Recommendation

**Path Forward:** ✅ **APPROVE CHANGE**

**Rationale:**
1. **Better user experience** - Cleaner working directory
2. **Safer implementation** - No data touched until success confirmed
3. **Simpler error handling** - Just delete temp file on failure
4. **Same development effort** - File operations complexity unchanged
5. **No timeline impact** - Story 2.2 not yet started

**Next Steps:**
1. ✅ Get user approval for this change proposal
2. ✅ All artifact updates already applied
3. Update Story 2.2 status from Draft → Ready for Development
4. Hand off to Dev agent for implementation

---

## Files Modified

✅ **Story 2.2:** `docs/stories/2.2.backup-and-output-file-management.md`
- Story statement updated
- 9 new acceptance criteria
- Complete technical guidance rewrite
- 8 revised tasks with subtasks
- 10 unit test scenarios
- Enhanced integration test requirements

✅ **Epic 2:** `docs/prd/epic-2-file-discovery-and-management.md`
- Story 2.2 section updated with new ACs

✅ **Architecture:** `docs/architecture/architecture-document-subtitle-renamer-tool-ar-subtitle-embedding-feature.md`
- file_manager component description enhanced
- Core workflow sequence diagram revised
- Source tree unchanged (per user request)

---

## Approval

**Scrum Master Assessment:** ✅ **RECOMMEND APPROVAL**

This change improves the feature without adding complexity or risk. The revised approach is safer, cleaner, and provides better user experience.

**Approved:** Changes finalized. Story 2.2 status updated to "Ready for Development"

---

## Implementation Authorization

✅ **APPROVED FOR IMPLEMENTATION**

All changes have been applied to:
- Story 2.2 documentation
- Epic 2 PRD
- Architecture document

Story 2.2 is now ready for Dev agent implementation.
