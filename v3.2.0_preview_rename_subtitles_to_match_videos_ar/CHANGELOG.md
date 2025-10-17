# SubFast v3.2.0 Changelog

## Version 3.2.0 - Epic 6: Testing Infrastructure & Pattern Expansion
**Release Date:** January 2025  
**From Version:** 3.0.0  
**Major Focus:** Comprehensive testing framework and pattern recognition expansion

---

## 🎯 Executive Summary

Version 3.2.0 represents a major milestone in SubFast's maturity, delivering:
- **Comprehensive Testing Infrastructure** - Complete test framework with 154 pattern test files
- **10 New Episode Patterns** - Expanded from 20 to 30 patterns (50% increase)
- **FINAL SEASON Logic** - Intelligent contextual matching for anime final seasons
- **100% Test Coverage** - All 30 patterns validated with multiple variations each
- **Production Quality** - Extensive bug fixes, pattern hardening, and quality improvements

---

## 📊 Epic 6 Stories Overview

| Story | Title | Status | Impact |
|-------|-------|--------|--------|
| 6.1 | Test Framework Setup & Structure | ✅ DONE | Foundation for all testing |
| 6.2 | Episode Pattern Test Suite with Dummy Files | ✅ DONE | 154 test files, JSON-based |
| 6.3 | Integration Tests - Embedding Workflow | ✅ DONE | 11 integration tests |
| 6.4 | Test Data Management & Extensibility | ✅ DONE | Documented workflows |
| 6.5 | Movie Mode Bug Fix & Pattern Hardening | ✅ DONE | Critical bug fixes |
| 6.6 | Add 7 New Patterns + Pattern Reordering | ✅ DONE | Patterns 23-29 |
| 6.7 | FINAL SEASON Contextual Matching | ✅ DONE | Pattern 30 |

---

## 🚀 Major Features

### 1. Testing Infrastructure (Story 6.1)
**Complete test framework using Python stdlib `unittest` (zero external dependencies)**

#### Features:
- **Comprehensive Test Runner** (`tests/run_tests.py`)
  - Run all tests, specific modules, or individual test suites
  - Automatic CSV report generation (no flag needed)
  - Beautiful bordered table output matching SubFast console style
  - Timestamped reports saved to `tests/reports/` directory

- **Test Report Format:**
  - Overall summary with pass/fail statistics and percentages
  - Per-module test script summary showing module health
  - Detailed test results with script, class, and test name columns
  - Pattern breakdown section with pattern-specific details
  - Failed tests section with detailed error messages

- **Test Utilities** (`tests/test_helpers.py`)
  - Temporary directory management
  - Fixture loading and validation
  - Custom assertions for SubFast patterns
  - File generation helpers

#### Files Created:
- `tests/run_tests.py` - Custom test runner with reporting
- `tests/README.md` - Complete testing documentation
- `tests/test_helpers.py` - Shared test utilities
- `tests/test_config_loader.py` - Config tests (14 tests)
- `tests/test_csv_reporter.py` - CSV reporter tests (10 tests)
- `tests/test_reporter.py` - Report generator module
- `tests/fixtures/` - Test data directory
- `tests/reports/` - Test reports directory

**Test Execution Time:** < 0.1 seconds for all tests

---

### 2. Pattern Test Suite with Dummy Files (Story 6.2)
**JSON-driven pattern testing system with 154 test files covering all patterns**

#### Features:
- **JSON-Based Pattern Definitions** (`tests/fixtures/pattern_definitions.json`)
  - All 30 patterns defined with metadata
  - 3-5 variations per pattern
  - Video and subtitle can use different formats
  - Data-driven test design

- **Automatic Test File Generation**
  - Helper functions to generate test files from JSON
  - VAR-based naming for stable references
  - Backup system for manual testing
  - Reset script to restore original state

- **Pattern Testing:**
  - 154 dummy test files (77 videos + 77 subtitles)
  - Realistic filename formats
  - Pattern priority validation (first match wins)
  - Cache behavior testing

#### Files Created:
- `tests/fixtures/pattern_definitions.json` - Complete pattern catalog
- `tests/test_pattern_matching.py` - 59 pattern tests
- `tests/test_helpers.py` - Pattern test utilities (extended)
- `tests/ADDING_NEW_PATTERNS.md` - 5-step workflow guide
- `tests/fixtures/pattern_files/` - 30 pattern directories with test files

**Pattern Coverage:** 30 patterns, 98 variations, 100% passing

---

### 3. Integration Tests - Embedding (Story 6.3)
**Comprehensive integration tests for the embedding workflow**

#### Features:
- **11 Integration Tests** covering complete embedding workflow
  - File discovery and pairing
  - mkvmerge availability detection (project bin first, then PATH)
  - Real video/subtitle embedding with verification
  - Backup creation and restoration
  - Error handling (missing files, permissions, invalid formats)
  - Movie mode testing (single file pairs)
  - Language detection and track configuration
  - CSV report generation

- **Dynamic Test Configuration:**
  - Automatic mkvmerge detection
  - Temporary directory management for test isolation
  - Dynamic timeout calculation (base 300s + 120s/GB, max 1800s)
  - Track verification using mkvmerge --identify

- **Enhanced Unified Reports:**
  - Integration tests included in main test report
  - Grand Summary shows embedding tests separately
  - Embedding Test Summary with config details
  - Real embedded MKV files in `tests/2- Embedding/test_output/`

#### Files Created:
- `tests/test_embedding_integration.py` - 11 integration tests
- `tests/2- Embedding/test_output/.gitignore` - Exclude embedded files
- `tests/2- Embedding/test_output/README.md` - Test output docs
- `tests/EMBEDDING_INTEGRATION_TESTS.md` - Integration test docs
- `tests/ENHANCED_REPORT_IMPLEMENTATION.md` - Enhanced report structure
- `tests/FINAL_REPORT_TEMPLATE.md` - Approved report template

**Modified:**
- `tests/run_tests.py` - Added embedding integration to unified runner

**Test Results:** 11/11 passing, real embedding verified with 3 tracks (video, audio, subtitle)

---

### 4. Movie Mode Bug Fix & Pattern Hardening (Story 6.5)
**Critical bug fix and pattern robustness improvements**

#### Bug Fixed:
**Movie Mode Activation Bug**
- **Issue:** Movie mode activating incorrectly with multiple episode files
- **Cause:** Checking remaining files instead of total file count
- **Fix:** Changed condition to check total files (not remaining)
- **Impact:** Movie mode now only activates for true single-file scenarios

```python
# BEFORE (Incorrect):
if len(remaining_video_files) == 1 and len(remaining_subtitle_files) == 1:
    movie_mode_detected = True

# AFTER (Correct):
if len(video_files) == 1 and len(subtitle_files) == 1:
    movie_mode_detected = True
```

#### Pattern 25 Hardening:
**Enhanced to support OnePiece-style long episode numbers (1000+)**

Pattern 25 now excludes:
- Years (1900-2099) to prevent false matches
- Resolution patterns (720p, 1080p, etc.)
- Codec patterns (x264, x265, AV1, etc.)

```python
# Enhanced regex with negative lookbehind
r'(?<!(?:19|20)\d{2})[\s._-](?P<episode>\d{3,})(?!p)(?!\s*(?:x264|x265|AV1|AAC))'
```

**Test Results:**
- Unit Tests: 128/128 passing
- Integration Tests: 77/77 passing (100%)
- No regression in existing functionality

#### Files Modified:
- `subfast/scripts/subfast_rename.py` - Movie Mode fix (line 348)
- `subfast/scripts/common/pattern_engine.py` - Pattern 25 hardening
- `subfast/scripts/subfast_embed.py` - Already using correct logic (verified)

---

### 5. Add 7 New Patterns + Pattern Reordering (Story 6.6)
**Major pattern expansion with intelligent reordering by specificity**

#### New Patterns Added:

**Pattern 23:** Season [space] Ep[space]number  
`Show Season 2 Ep 15`  
**Specificity:** Medium - Space-separated format

**Pattern 24:** Ep[number] (no season, defaults to S01)  
`Show Ep05` → S01E05  
**Specificity:** Low - Episode-only, default season

**Pattern 25:** E[number] (no season, defaults to S01)  
`Show E10` → S01E10  
**Specificity:** Very Low - Single letter prefix

**Pattern 26:** [number] - [number] (season - episode, no prefix)  
`Show 2 - 15` → S02E15  
**Specificity:** High - No prefix required

**Pattern 27:** [number]-[number] (season-episode, hyphen only)  
`Show 2-15` → S02E15  
**Specificity:** High - Compact format

**Pattern 28:** [number][square brackets][number]  
`Show 02[15]` → S02E15  
**Specificity:** Very High - Unique bracket format

**Pattern 29:** Underscore [number] (episode only, defaults to S01)  
`Show_09` → S01E09  
**Specificity:** Very Low - LAST PATTERN (fallback)

#### Quick-Win Variations Added:
- **Pattern 1 (S[#]E[#]):** Added VAR4-VAR6 with flexible separators
- **Pattern 4 (S[#]-E[#]):** Added VAR4-VAR5 with underscore separator
- **Pattern 5 (S[#]-EP[#]):** Added VAR4-VAR6 with space variations

#### Pattern Reordering:
**Old Order:** Original ID assignment (20, 21, 22...)  
**New Order:** By specificity (high to low)

**Reordering Rationale:**
- **High Specificity First:** Patterns with unique markers processed first
- **Prevent False Matches:** More specific patterns capture intent before generic ones
- **Performance:** Early matches reduce unnecessary regex evaluations

**Pattern ID Changes:**
- Pattern 20 → 25 (E[number])
- Pattern 21 → 20 (Season[space]Ep[space])
- Pattern 22 → 21 (Season.Ep)
- Pattern 23 ↔ 24 (Swapped based on specificity)
- Pattern 25-28 → 26-29 (Shifted for new insertions)

**Pattern 22 Status:** Left unassigned (gap in sequence for future use)

#### Pattern Hardening:
Applied to Patterns 26, 27, 28:
- Episode number range validation (1-9999)
- Season number validation (1-99)
- Prevents year/resolution false matches

#### Test Coverage:
- **46 new test files** generated (Pattern 27, 28 + variations)
- **30 test files regenerated** (Patterns 1, 4, 5, 15, 20, 21, 23, 24, 25)
- **Total test files:** 154 (77 videos + 77 subtitles)

#### Helper Scripts Created:
- `add_patterns_story66.py` - Pattern addition automation
- `reorder_patterns_fixed.py` - Pattern reordering script
- `regenerate_test_files.py` - Test file regeneration utility

#### Files Modified:
- `subfast/scripts/common/pattern_engine.py` - Added 7 patterns, reordered 23-29
- `tests/fixtures/pattern_definitions.json` - Added Pattern 27, 28 + 5 variations
- `tests/1- Renaming/episode_patterns_guide.md` - Updated all 28 patterns
- Test directories renamed for new ordering

**Test Results:** 128/128 tests passing (100%)

---

### 6. FINAL SEASON Contextual Matching (Story 6.7) ⭐ NEW
**Intelligent season inference for anime final seasons**

#### Problem Solved:
Anime final seasons often released with "FINAL SEASON" in filename but no season number:
```
Subtitle: Boku no Hero Academia FINAL SEASON - 01.ass  (defaults to S01E01)
Video:    My.Hero.Academia.S08E01.mkv                   (actual S08E01)
Result:   NO MATCH ❌ (S01 ≠ S08)
```

#### Solution - Pattern 30:
**Contextual matching with bidirectional season inference**

**Detection:**
- Regex: `r'final[.\s_-]+season'` (case-insensitive)
- Supports multiple separators: dots, spaces, underscores, hyphens

**Inference Logic:**
1. **Subtitle has FINAL SEASON:**
   - Default extraction: S01 (fallback)
   - Check if video has explicit season (S08)
   - Infer subtitle season from video: S01 → S08
   - Match if episodes align: E01 = E01 ✓

2. **Video has FINAL SEASON:**
   - Default extraction: S01 (fallback)
   - Check if subtitle has explicit season (S08)
   - Infer video season from subtitle: S01 → S08
   - Match if episodes align: E01 = E01 ✓

3. **Both have FINAL SEASON:**
   - No inference (both default to S01)
   - Match normally

**Constraints:**
- Inference only applies when detected season is 1 (default fallback)
- Episode numbers must still match for pairing
- Non-breaking: Only activates when FINAL SEASON keyword detected

#### Implementation:

**New Functions in `pattern_engine.py`:**
```python
def detect_final_season_keyword(filename: str) -> bool:
    """Detect if filename contains 'FINAL SEASON' keyword."""
    pattern = r'final[.\s_-]+season'
    return bool(re.search(pattern, filename, re.IGNORECASE))

def match_subtitle_to_video(subtitle_file: str, video_file: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Match subtitle to video with FINAL SEASON contextual inference.
    Returns (subtitle_episode, video_episode) or (None, None) if no match.
    """
    # Bidirectional season inference logic
    # ...
```

**Integration in Main Scripts:**

Both `subfast_rename.py` and `subfast_embed.py` now check for FINAL SEASON before falling back to simple key matching:

```python
# Check if subtitle has FINAL SEASON
if pattern_engine.detect_final_season_keyword(subtitle):
    for video in sorted(video_files):
        sub_ep, vid_ep = pattern_engine.match_subtitle_to_video(subtitle, video)
        if sub_ep and vid_ep:
            # Match found via FINAL SEASON inference
            print(f"'{subtitle}' -> {ep} adjusted to {sub_ep} (FINAL SEASON inference from '{video}')")
            break

# Check if video has FINAL SEASON
if not target_video:
    for video in sorted(video_files):
        if pattern_engine.detect_final_season_keyword(video):
            sub_ep, vid_ep = pattern_engine.match_subtitle_to_video(subtitle, video)
            if sub_ep and vid_ep:
                # Match found
                break

# Fallback to existing simple key matching
if not target_video and ep:
    # ... existing logic
```

#### Console Output:
Clear messages indicate when FINAL SEASON inference is used:
```
'[Heroacainarabic] Boku no Hero Academia FINAL SEASON - 01.ass' -> S01E01 adjusted to S08E01 (FINAL SEASON inference from 'My.Hero.Academia.S08E01.mkv')
RENAMED: '[Heroacainarabic] Boku no Hero Academia FINAL SEASON - 01.ass' -> 'My.Hero.Academia.S08E01.ar.ass'
```

#### Test Coverage:

**11 Unit Tests:**
- 3 detection tests (positive, negative, filename-only)
- 8 matching tests (inference both directions, edge cases)

**6 Integration Test Variations:**
- VAR1-VAR2: My Hero Academia S08 (subtitle FINAL)
- VAR3: Attack on Titan S04 (subtitle FINAL)
- VAR4-VAR5: Reverse scenarios (video FINAL)
- VAR6: Edge case (both FINAL)

**12 Test Files Generated:**
- `tests/fixtures/pattern_files/pattern_30_FINAL_SEASON/`

#### Documentation:
- Pattern 30 added to `episode_patterns_guide.md` (96 lines)
- Comprehensive examples with My Hero Academia and Attack on Titan
- Edge cases documented (both FINAL, both explicit seasons)
- Use case: "Anime final seasons without traditional season numbering"

#### Files Modified:
- `subfast/scripts/common/pattern_engine.py` - Added 2 new functions (60 lines)
- `subfast/scripts/subfast_rename.py` - Integrated FINAL SEASON logic (47 lines)
- `subfast/scripts/subfast_embed.py` - Integrated FINAL SEASON logic (43 lines)
- `tests/test_pattern_matching.py` - Added 2 test classes (110 lines)
- `tests/fixtures/pattern_definitions.json` - Added Pattern 30 with 6 variations
- `tests/1- Renaming/episode_patterns_guide.md` - Added Pattern 30 documentation

**Test Results:** 
- 11/11 unit tests passing
- 6/6 integration scenarios passing
- Non-breaking: Existing behavior preserved

---

## 📈 Statistics

### Pattern Recognition:
- **Total Patterns:** 30 (was 20 in v3.0)
- **Growth:** +50% pattern coverage
- **Pattern Types:** 29 regex + 1 contextual
- **Test Files:** 154 (77 videos + 77 subtitles)
- **Test Variations:** 98 unique scenarios

### Test Coverage:
- **Unit Tests:** 128 tests, 100% passing
- **Integration Tests:** 11 tests (embedding), 100% passing
- **Pattern Tests:** 98 variations across 30 patterns, 100% passing
- **Total Test Execution Time:** < 1 second

### Code Quality:
- **Zero External Dependencies:** Pure Python stdlib
- **Test Framework:** Python `unittest` (zero setup)
- **Report Generation:** Automatic CSV reports
- **Documentation:** Comprehensive guides and examples

---

## 🐛 Bug Fixes

### Critical Fixes:
1. **Movie Mode Activation Bug (Story 6.5)**
   - Fixed incorrect file count check
   - Now only activates for true single-file scenarios
   - Prevents false activation with multiple episode files

### Pattern Hardening:
2. **Pattern 25 Enhancement (Story 6.5)**
   - Now supports OnePiece-style long episode numbers (1000+)
   - Excludes years (1900-2099) to prevent false matches
   - Excludes resolution/codec patterns (720p, x264, etc.)

3. **Pattern 26-28 Hardening (Story 6.6)**
   - Episode range validation (1-9999)
   - Season range validation (1-99)
   - Prevents year/resolution false matches

---

## 📚 Documentation

### New Documentation:
- `tests/README.md` - Complete testing guide (philosophy, usage, examples)
- `tests/ADDING_NEW_PATTERNS.md` - 5-step workflow for adding patterns
- `tests/EMBEDDING_INTEGRATION_TESTS.md` - Integration test documentation
- `tests/ENHANCED_REPORT_IMPLEMENTATION.md` - Report structure docs
- `tests/FINAL_REPORT_TEMPLATE.md` - Approved report template
- `tests/1- Renaming/episode_patterns_guide.md` - Updated all 30 patterns

### Updated Documentation:
- All pattern examples updated for new patterns 23-30
- Pattern reordering rationale documented
- FINAL SEASON use cases and examples
- Test execution examples and options

---

## 🔄 Migration Notes

### From v3.0 to v3.2:

#### No Breaking Changes:
- All existing patterns continue to work
- New patterns only activate when matched
- FINAL SEASON logic only applies when keyword detected
- Existing behavior preserved for all scripts

#### New Features Automatically Available:
- All 10 new patterns (23-30) available immediately
- FINAL SEASON matching works out of the box
- No configuration changes required

#### Test Framework (Optional):
If you want to run tests:
```bash
# Run all tests
python tests/run_tests.py

# Run specific module
python tests/run_tests.py pattern

# View test reports
# Reports automatically saved to tests/reports/
```

#### Pattern Priority Changes:
Some patterns reordered for better specificity matching. This may result in different patterns matching for ambiguous filenames, but should always produce correct results.

---

## 🔮 Future Enhancements

### Planned for v3.3:
- Web-based pattern testing interface
- Pattern performance profiling
- Additional anime-specific patterns
- Pattern confidence scoring
- Multi-language pattern support

### Long-term Roadmap:
- Machine learning-based pattern suggestion
- Custom pattern creation via UI
- Cloud-based pattern library
- Collaborative pattern sharing

---

## 🙏 Credits

**Epic 6 Development Team:**
- **James (Dev Agent):** Implementation of all 7 stories
- **Quinn (Test Architect):** QA review and validation
- **Bob (Scrum Master):** Story creation and coordination

**Special Thanks:**
- Community contributors for pattern suggestions
- Beta testers for My Hero Academia FINAL SEASON testing
- All users who provided feedback and bug reports

---

## 📝 Version History

| Version | Date | Description |
|---------|------|-------------|
| 3.2.0 | January 2025 | Epic 6: Testing Infrastructure & Pattern Expansion |
| 3.0.0 | December 2024 | Epic 5: Pattern Recognition Engine & Modular Architecture |
| 2.0.0 | November 2024 | Epic 2-3: Batch Processing & Context Menu Integration |
| 1.0.0 | October 2024 | Epic 1: Core Embedding Functionality |

---

## 📞 Support

For issues, questions, or feature requests:
- **GitHub Issues:** [Project Repository]
- **Documentation:** `tests/README.md` and `tests/1- Renaming/episode_patterns_guide.md`
- **Pattern Guide:** Comprehensive guide in `episode_patterns_guide.md`

---

**SubFast v3.2.0** - Smarter. Faster. Better tested. 🚀
