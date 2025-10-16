# Enhanced CSV Report - Action Column Logic & Accurate Statistics

## Changes to Implement

### 1. Enhanced Action Column for Videos
**File:** `subfast/scripts/common/csv_reporter.py`
**Function:** `_write_renaming_report()`

**New Logic:**
- Video with matched subtitle → `MATCHED`
- Video with no matching subtitle → `NO MATCH`
- Video with unidentified episode → `--`
- Movie mode with match → `MATCHED`
- Movie mode without match → `NO MATCH`

### 2. Accurate Summary Statistics
**Replace hardcoded/incorrect values with accurate calculations:**
- Videos Missing Subtitles: Calculate from episode matching
- Subtitles Missing Videos: Calculate from episode matching  
- Videos Without Episode Pattern: Count unidentified videos
- Subtitles Without Episode Pattern: Already correct

### 3. Add Missing Report Sections (Option A)
**Add two sections after MATCHED EPISODES:**
- MISSING MATCHES section (episodes with only video OR subtitle)
- FILES WITHOUT EPISODE PATTERN section (unidentified files)

## Files to Modify
- `subfast/scripts/common/csv_reporter.py` - Update `_write_renaming_report()` function

## Expected Outcome
- Videos show informative MATCHED/NO MATCH actions
- All summary statistics accurately reflect table contents
- Complete v3.0.0 section compatibility
- Easy validation: summary numbers match table data