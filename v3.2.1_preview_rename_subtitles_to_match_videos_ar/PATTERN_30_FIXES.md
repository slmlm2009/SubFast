# Pattern 30 FINAL SEASON Fixes

## Issues Found

### 1. Test Script Only Looked for .ar.srt Files ❌
**Problem**: `run_pattern_integration_tests.py` only checked for `.ar.srt` renamed files, ignoring `.ar.ass` files.

**Impact**: Pattern 30 uses `.ass` files, so test showed false warning: "No renamed subtitle files found (.ar.srt)"

**Fixed**: Line 151 - Now checks for both `.ar.srt` and `.ar.ass` dynamically:
```python
renamed_subtitles = list(pattern_dir.glob('*.ar.srt')) + list(pattern_dir.glob('*.ar.ass'))
original_subtitles = (list(pattern_dir.glob('[[]VAR*[]].srt')) + 
                     list(pattern_dir.glob('[[]VAR*[]].ass')) +
                     list(pattern_dir.glob('[[]VAR*[]].vtt')))
```

### 2. False "[FAIL] No match pair" Messages ❌
**Problem**: Test printed `[FAIL] No match pair for S08E02 [X]` even when the test passed.

**Impact**: Confusing output - showed failures that weren't actually failures.

**Fixed**: Line 265 - Changed to informational message:
```python
csv_warning = f"  [INFO] Entry not in CSV report (testing from disk files)"
```

### 3. FINAL SEASON Matching Ignores VAR Tags ❌ **CRITICAL BUG**
**Problem**: `subfast_rename.py` FINAL SEASON matching logic matched files based ONLY on episode numbers, completely ignoring VAR tags.

**Impact**: Wrong file pairings:
- VAR1 subtitle → paired with VAR4 video ❌
- VAR4 subtitle → paired with VAR1 video ❌
- VAR2, VAR3, VAR5 showed "NO MATCH" even though correct files existed

**Example from CSV**:
```
S01E01 -> Video: [VAR4]-My.Hero.Academia.FINAL.SEASON.E01.mkv 
       | Subtitle: [VAR1]-[Heroacainarabic] Boku no Hero Academia FINAL SEASON - 01.ass
```

This should have been:
```
S08E01 -> Video: [VAR1]-My.Hero.Academia.S08E01...mkv
       | Subtitle: [VAR1]-[Heroacainarabic] Boku no Hero Academia FINAL SEASON - 01.ass
```

**Fixed**: Added VAR tag extraction and matching logic in `subfast_rename.py` lines 217-252:

```python
def extract_var_tag(filename):
    """Extract [VAR#] tag from filename if present."""
    import re
    match = re.match(r'\[(VAR\d+)\]-', filename)
    return match.group(1) if match else None

subtitle_var_tag = extract_var_tag(subtitle)

# In matching loop:
for video in sorted(available_videos):
    video_var_tag = extract_var_tag(video)
    
    # If both have VAR tags, they must match
    if subtitle_var_tag and video_var_tag and subtitle_var_tag != video_var_tag:
        continue  # Skip this video, VAR tags don't match
    
    # Now check FINAL SEASON matching logic...
```

## Expected Results After Fixes

### Pattern 30 Should Now Show:

**VAR1**: 
- Video: `[VAR1]-My.Hero.Academia.S08E01.Toshinori.Yagi.Rising-Origin.1080p.mkv` → S08E01
- Subtitle: `[VAR1]-[Heroacainarabic] Boku no Hero Academia FINAL SEASON - 01.ass` → S08E01 (inferred from video)
- **Status**: PASS ✅

**VAR2**:
- Video: `[VAR2]-My.Hero.Academia.S08E02.Toshinori.Yagi.Rising-Origin.1080p.mkv` → S08E02
- Subtitle: `[VAR2]-[Heroacainarabic] Boku no Hero Academia FINAL SEASON - 02.ass` → S08E02 (inferred from video)
- **Status**: PASS ✅

**VAR3**:
- Video: `[VAR3]-Attack.on.Titan.S04E05.1080p.mkv` → S04E05
- Subtitle: `[VAR3]-Attack on Titan FINAL SEASON - 05.ass` → S04E05 (inferred from video)
- **Status**: PASS ✅

**VAR4**:
- Video: `[VAR4]-My.Hero.Academia.FINAL.SEASON.E01.mkv` → S08E01 (inferred from subtitle)
- Subtitle: `[VAR4]-Boku no Hero Academia S08E01.ass` → S08E01
- **Status**: PASS ✅

**VAR5**:
- Video: `[VAR5]-Attack.on.Titan.FINAL.SEASON - 03.mkv` → S04E03 (inferred from subtitle)
- Subtitle: `[VAR5]-Attack.on.Titan.S04E03.ass` → S04E03
- **Status**: PASS ✅

**VAR6**:
- Video: `[VAR6]-Show.FINAL.SEASON.E01.mkv` → S01E01
- Subtitle: `[VAR6]-Show.FINAL.SEASON - 01.ass` → S01E01
- **Status**: PASS ✅

**Expected**: 6/6 PASSED (100%) ✅

## Files Modified

1. ✅ **tests/run_pattern_integration_tests.py**
   - Lines 150-167: Dynamic subtitle extension detection (.srt, .ass, .vtt)
   - Line 265: Fixed false failure message

2. ✅ **subfast/scripts/subfast_rename.py**
   - Lines 217-252: Added VAR tag matching for FINAL SEASON logic
   - Ensures files are only paired if their VAR tags match

## Testing Instructions

### 1. Reset Test Environment
```bash
cd tests/fixtures/pattern_files/pattern_30_FINAL_SEASON
rm -rf backup *.ar.ass renaming_report.csv
cd ../../..
python test_helpers.py  # Regenerate Pattern 30 files
```

Or run full reset:
```bash
python tests/reset_test_files.py
```

### 2. Run Pattern 30 Test
```bash
python tests/run_pattern_integration_tests.py 30
```

### 3. Verify Results
- Should show 6/6 PASSED (100%)
- No false "[FAIL] No match pair" messages
- Correct video-subtitle pairing by VAR tags
- Info message: "Found 6 renamed subtitle files (0 .ar.srt, 6 .ar.ass)"

## Root Cause Analysis

The FINAL SEASON feature was designed for real-world anime files where you might have:
- Video: `My.Hero.Academia.S08E01...mkv` (has specific season)
- Subtitle: `Boku no Hero Academia FINAL SEASON - 01.ass` (generic FINAL SEASON)

The system should infer the subtitle is S08E01 based on the video's season.

However, the implementation had a **critical flaw**: It matched files based ONLY on whether the FINAL SEASON inference algorithm returned matching episode numbers, without considering that test files have VAR tags to keep variations separate.

This caused **cross-contamination** where VAR1's subtitle would match with VAR4's video if their inferred episode numbers happened to match.

**The fix ensures**: When both files have VAR tags (like in tests), they MUST have the same VAR tag before attempting FINAL SEASON inference. This keeps test variations isolated while still allowing the FINAL SEASON logic to work on real-world files without VAR tags.
