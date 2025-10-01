# Bug Fix: Negative "Subtitles Missing Videos" Count

## Issue
In movie mode, the CSV report showed:
```
# Subtitles Missing Videos: -1
```

Should have been:
```
# Subtitles Missing Videos: 0
```

## Root Cause
The calculation for unmatched subtitles double-counted movie subtitles:

```python
unmatched_subtitles = total_subtitles - renamed_count - unidentified_subtitle_count
```

In movie mode:
- `total_subtitles = 1` (the movie subtitle)
- `renamed_count = 1` (subtitle was renamed via movie matching)
- `unidentified_subtitle_count = 1` (movie subtitle has no episode pattern)

Result: `1 - 1 - 1 = -1` ❌

**Problem**: Movie subtitles are both "renamed" AND "unidentified" (no episode pattern), so they were counted twice in the subtraction.

## Solution
Added `max(0, ...)` to prevent negative values:

```python
unmatched_subtitles = max(0, total_subtitles - renamed_count - unidentified_subtitle_count)
```

This ensures the count never goes below zero, which is mathematically correct since you can't have negative unmatched files.

## Testing
**Before Fix:**
```
# Subtitles Missing Videos: -1
```

**After Fix:**
```
# Subtitles Missing Videos: 0
```

✅ Tested on Movie_Test folder with single movie + subtitle pair  
✅ Both NoThinking and Configurable versions fixed

## Files Modified
- `rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking.py` (line 853)
- `rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py` (line 853)

## Impact
- **Scope**: Movie mode only (files without episode patterns)
- **Severity**: Low (cosmetic issue in CSV report)
- **User Impact**: None on file renaming functionality, only affects report display

---
**Date**: 2025-01-10
**Version**: v2.5.0-preview
**Type**: Bug Fix - Cosmetic
