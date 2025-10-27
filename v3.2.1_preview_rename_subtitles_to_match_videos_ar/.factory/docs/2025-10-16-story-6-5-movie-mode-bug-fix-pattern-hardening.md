## Story 6.5: Fix Movie Mode Bug & Harden Pattern 25

### Implementation Plan

**Task 1: Fix Movie Mode Activation Bug**
- Modify `subfast/scripts/subfast_rename.py` line ~347
  - Change condition from `len(remaining_video_files)` to `len(video_files)` 
  - Change condition from `len(remaining_subtitle_files)` to `len(subtitle_files)`
- Apply identical fix to `subfast/scripts/subfast_embed.py`
- Ensures Movie Mode ONLY activates with total count = 1 video + 1 subtitle

**Task 2: Harden Pattern 25 `-##`**
- Update `subfast/scripts/common/pattern_engine.py`
- Locate Pattern 25 in `EPISODE_PATTERNS` list
- Replace regex:
  - From: `r'-(\d{1,3})\b'`
  - To: `r'-(?:1[0-8]\d{2}|\d{1,3})(?![a-zA-Z])'`
- Update lambda to: `lambda m: (1, int(m.group(0)[1:]))`
- Supports episodes 1-1899, blocks years 1900+, blocks resolution/codec suffixes

**Task 3: Validation**
- Run existing test suite (all 114 tests must pass)
- Manually verify Movie Mode behavior
- Test Pattern 25 edge cases (1080, 1899, 1080p rejection)

### Expected Results
✅ Movie Mode only activates with single video + single subtitle  
✅ Pattern 25 matches episodes 1-1899  
✅ Blocks resolutions (1080p), codecs (x264), years (2023)  
✅ No regression in existing functionality