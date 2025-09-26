# Test Results for No-Season Pattern

## Sixth Test Run: ShowName - #### Pattern (No Season Specified)

### Background
Tested if the script properly handles the "ShowName - ####.mkv" pattern format, where no season number is specified and episodes are identified only by the number after the dash.

### How the Pattern Works
- The script's current regex `r'-\s*(\d+)'` matches the dash followed by digits anywhere in the filename
- For a file like "Show.Name - 1234.mkv", this detects episode 1234 and assumes season 1 (S01E1234)
- This allows matching with subtitles that follow the same episode number pattern

### Test Cases Conducted

#### Test 1: Basic No-Season Pattern
- **Files**: `Show.Name - 1234.mkv` and `subtitle - 1234.srt`
- **Pattern Analysis**:
  - Video detected as: S01E1234 (using the - 1234 part)
  - Subtitle detected as: S01E1234 (using the - 1234 part)
- **Result**: Successfully matched and renamed to `Show.Name - 1234.ar.srt`
- **Status**: ✅ PASSED

#### Test 2: Multiple No-Season Pattern Files
- **Files**:
  - `Show.Name - 01.mkv` (2-digit episode)
  - `Show.Name - 1234.mkv` (4-digit episode) 
  - `subtitle - 01.srt` (2-digit episode subtitle)
  - `other - 1234.ass` (4-digit episode subtitle)
- **Results**:
  - `subtitle - 01.srt` → `Show.Name - 01.ar.srt` (matched episode 01)
  - `other - 1234.ass` → `Show.Name - 1234.ar.ass` (matched episode 1234)
- **Status**: ✅ PASSED (No confusion between 2-digit and 4-digit numbers)

### Technical Analysis

The script successfully handles the "ShowName - ####" pattern because:

1. The `- ##` pattern detector (`r'-\s*(\d+)'`) finds the episode number regardless of its position in the filename
2. The episode number is extracted and formatted as "S01E####" (assuming season 1)
3. Matching works between video and subtitle files with the same episode number
4. The removal of `.zfill(2)` preserves actual digit counts

### Results Summary

- ✅ ShowName - #### pattern (no season) works correctly
- ✅ Multiple files with different episode lengths work without confusion  
- ✅ Mixed ShowName - ## and ShowName - #### patterns work together
- ✅ All previously tested functionality continues to work
- ✅ High episode number support continues to work

### Conclusion

The script successfully handles the "ShowName - ####.mkv" pattern where no season is specified. The existing pattern detection logic is flexible enough to identify episode numbers from dash-prefixed digits anywhere in the filename, then match them appropriately with subtitles that follow the same pattern. This is a natural extension of the existing "- ##" pattern functionality.