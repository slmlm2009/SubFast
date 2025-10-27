# Restore v3.0.0 Embedding Workflow to Refactored Script

## Problem Analysis

The refactored v3.1.0 embedding script has a **completely different workflow** than v3.0.0:

### Current (Wrong) Workflow:
1. Creates `.temp.mkv` file
2. Creates `.original.mkv` backup in same directory  
3. Deletes original video
4. Renames `.temp.mkv` to original name
5. **Doesn't properly handle subtitle cleanup**

### v3.0.0 (Correct) Workflow:
1. Creates temporary `.embedded.mkv` file
2. On success:
   - Creates `backups/` directory
   - **Moves BOTH original video AND subtitle to backups/ folder**
   - Renames `.embedded.mkv` to original video name
   - Deletes subtitle from working directory only if safely backed up
3. On failure:
   - Cleans up `.embedded.mkv` temp file
   - Original files remain untouched

---

## Implementation Plan

### 1. Replace `create_backup()` function

**Remove:** Current `create_backup()` that creates `.original.mkv` files

**Add:** Five v3.0.0 backup management functions:
- `ensure_backups_directory()` - Creates backups/ folder
- `backup_originals()` - Moves video + subtitle to backups/ with existence checks
- `safe_delete_subtitle()` - Deletes subtitle only if backup exists
- `rename_embedded_to_final()` - Renames .embedded.mkv to final name
- `cleanup_failed_merge()` - Cleanup on failure

### 2. Rewrite `embed_subtitle()` function

**Key Changes:**
```python
# Before (wrong):
output_path = video_path.with_suffix('.temp.mkv')
# ... on success:
backup_path = create_backup(video_path)
video_path.unlink()
output_path.rename(video_path)

# After (correct - v3.0.0):
embedded_file = video_path.parent / f"{video_path.stem}.embedded.mkv"
# ... on success:
backups_dir = ensure_backups_directory(video_path.parent)
backup_originals(video_path, subtitle_path, backups_dir)
safe_delete_subtitle(subtitle_path, backups_dir)
rename_embedded_to_final(embedded_file, video_path)
```

**New signature:** Add `backups_dir` parameter and return it for batch reuse

### 3. Update `process_embedding()` caller

**Track backups_dir:** Maintain across iterations to avoid recreating

```python
# Add before loop:
backups_dir = None

# Update embed_subtitle call:
success, error, backups_dir = embed_subtitle(
    target_video_path,
    subtitle_file, 
    mkvmerge_path,
    language_code,
    config.get('default_flag', True),
    backups_dir  # Pass existing backups_dir
)
```

---

## Expected Behavior After Fix

### Successful Embedding:
```
EMBEDDING: 'episode.srt' into 'episode.mkv'
  Language: Arabic (ar)
[INFO] Creating backups/ directory...
[BACKUP] Moved episode.mkv -> backups/
[BACKUP] Moved episode.srt -> backups/
[CLEANUP] Removed subtitle from working dir: episode.srt
[SUCCESS] Created: episode.mkv
```

### Failed Embedding:
```
EMBEDDING: 'episode.srt' into 'episode.mkv'
  Language: Arabic (ar)
[CLEANUP] Removed temporary file: episode.embedded.mkv
✗ FAILED: mkvmerge error message
```

### Directory Structure After Success:
```
working_directory/
├── episode.mkv              (new embedded version)
└── backups/
    ├── episode.mkv          (original video)
    └── episode.srt          (original subtitle)
```

---

## Testing Checklist

- [ ] Single file embedding creates backups/ folder
- [ ] Both video and subtitle moved to backups/
- [ ] .embedded.mkv renamed to original video name
- [ ] Subtitle deleted from working directory only if in backups/
- [ ] Batch processing reuses existing backups/ folder
- [ ] Failed merge cleans up .embedded.mkv
- [ ] Failed merge leaves originals untouched
- [ ] No .temp.mkv or .original.mkv files created

---

## Files Modified

**File:** `subfast/scripts/subfast_embed.py`

**Functions replaced:**
- `create_backup()` → 5 new backup management functions
- `embed_subtitle()` → Rewritten with v3.0.0 workflow

**Functions updated:**
- `process_embedding()` → Track backups_dir parameter

**Lines affected:** ~100 lines (functions at lines 168-233)