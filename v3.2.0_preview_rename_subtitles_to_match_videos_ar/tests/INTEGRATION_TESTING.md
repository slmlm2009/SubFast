# SubFast Pattern Integration Testing

## Overview

**TRUE Integration Testing** for SubFast pattern matching that validates the ENTIRE workflow:
1. Runs the REAL `subfast_rename.py` script
2. Uses actual dummy files with episode patterns
3. Parses generated CSV reports
4. Verifies extracted episodes match expected results
5. Validates video/subtitle pairing

This is NOT unit testing - this tests what users actually experience!

## Key Features

### VAR-Based File Naming
All dummy files are prefixed with `[VAR1]`, `[VAR2]`, etc. for stable reference:

```
[VAR1]-Show.Season 1.Ep 5.mkv  → Expected: S01E05
[VAR1]-Show.Season 1.Ep 5.srt  → Expected: S01E05
[VAR2]-Series.Season 2.Ep 10.mkv → Expected: S02E10
[VAR2]-Series.Season 2.Ep 10.srt → Expected: S02E10
```

**Benefits:**
- Users can rename files for manual testing
- VAR tag provides stable reference
- Tests verify actual extraction, not filename matching
- No naming collisions during renaming

### Integration Testing Approach
Tests run the ACTUAL renaming workflow:
```
1. Copy pattern files to temp directory
2. Copy real config.ini
3. Run subfast_rename.py
4. Parse generated renaming_report.csv
5. Verify extractions match expected VAR results
6. Verify video/subtitle pairing worked
```

## Running Tests

### Test All Patterns
```bash
python tests/run_pattern_integration_tests.py
```

### Test Specific Pattern
```bash
python tests/run_pattern_integration_tests.py --pattern 21
```

### Test Output Example
```
====================================================================================================
Pattern 01: S##E##
====================================================================================================

[VAR1] Expected: S01E05
  Video:    [VAR1]-Show.Name.S01E05.720p.mkv                   -> Extracted: S01E05   | [MATCH]
  Subtitle: [VAR1]-Show.Name.S01E05.srt                        -> Extracted: S01E05   | [MATCH]
  Pairing:  Video <-> Subtitle PAIRED               | Status: PASS
  ----------------------------------------------------------------------------------------------

[VAR2] Expected: S02E10
  Video:    [VAR2]-Series.S2E10.BluRay.mkv                     -> Extracted: S02E10   | [MATCH]
  Subtitle: [VAR2]-Different.S2E10.srt                         -> Extracted: S02E10   | [MATCH]
  Pairing:  Video <-> Subtitle PAIRED               | Status: PASS
  ----------------------------------------------------------------------------------------------

Pattern 01 Summary: 4/4 PASSED (100.0%)
====================================================================================================

====================================================================================================
FINAL SUMMARY
====================================================================================================
Total Patterns Tested:  25
Total Variations:       77
Passed:                 77 (100.0%)
Failed:                 0 (0.0%)
====================================================================================================
```

## Test Results (Latest Run)

**Test Date:** 2025-10-16  
**Total Patterns:** 25  
**Total Variations:** 77  
**Pass Rate:** 100.0%

All 25 patterns with all variations PASSED! ✅

## Manual Testing

You can manually test patterns by:

1. **Reset files to clean state:**
   ```bash
   python tests/reset_test_files.py
   ```

2. **Modify files for testing:**
   - Rename files however you want
   - VAR tags remain stable for test reference
   - Example: `[VAR1]-Show.Season 1.Ep 5.srt` → `[VAR1]-AnyName.You.Want.srt`

3. **Run pattern test:**
   ```bash
   python tests/run_pattern_integration_tests.py --pattern 21
   ```

4. **See what was extracted:**
   ```bash
   python tests/verify_pattern_extractions.py --pattern 21
   ```

## Architecture

### Core Components

**1. pattern_definitions.json**
- VAR-based structure
- Each variation has: `var_id`, `expected`, `video_template`, `subtitle_template`
- 25 patterns, 77 total variations

**2. generate_test_files.py**
- Generates 154 dummy files (77 videos + 77 subtitles)
- Adds [VAR#] prefix to all filenames
- Creates realistic 1KB MKV and SRT files

**3. run_pattern_integration_tests.py**
- Main integration test runner
- Runs actual subfast_rename.py script
- Parses CSV reports
- Beautiful formatted output

**4. csv_report_parser.py**
- Parses text-based CSV reports from subfast_rename.py
- Extracts MATCHED EPISODES section
- Maps VAR tags to extraction results

**5. reset_test_files.py**
- Deletes all dummy files
- Regenerates fresh 154 files
- Verifies file counts
- Cleans test artifacts

## Test Philosophy

### Why Integration Testing?

**Unit tests** would test pattern extraction in isolation:
```python
def test_pattern():
    assert get_episode_number("Show.S01E05.mkv") == "S01E05"
```

**Integration tests** test the REAL workflow:
```python
def test_pattern():
    # Run actual script
    run_subfast_rename(pattern_folder)
    
    # Check CSV report
    report = parse_csv("renaming_report.csv")
    
    # Verify results
    assert report[VAR1].extracted == "S01E05"
    assert report[VAR1].video_paired_with_subtitle
```

Integration testing catches:
- CSV report generation issues
- File reading/writing problems
- Video/subtitle pairing logic
- Config loading issues
- Real-world edge cases

### VAR Tags Enable Both

- **Automated testing:** Tests reference VAR tags for expected results
- **Manual testing:** Users can rename files, VAR tags stay stable
- **Flexibility:** Rename `[VAR1]-Show.S01E05.srt` → `[VAR1]-MyTest.srt`
- **Stability:** Tests still know VAR1 should extract S01E05

## Adding New Patterns

See `ADDING_NEW_PATTERNS.md` for detailed guide.

Quick steps:
1. Add pattern to `pattern_definitions.json` with VAR structure
2. Run `python tests/generate_test_files.py`
3. Run `python tests/run_pattern_integration_tests.py --pattern ##`
4. Verify all variations pass

## Troubleshooting

### Tests Fail After Manual Changes
```bash
# Reset to clean state
python tests/reset_test_files.py

# Verify files regenerated
python tests/verify_pattern_extractions.py
```

### CSV Report Not Generated
- Check `subfast/config.ini` has `renaming_report = true`
- Ensure script has write permissions
- Check STDOUT/STDERR for errors

### Pattern Not Matching
```bash
# See what's being extracted
python tests/verify_pattern_extractions.py --pattern ##

# Check pattern regex in subfast/scripts/common/pattern_engine.py
```

## Performance

Integration tests are FAST:
- **Single pattern:** ~0.08 seconds
- **All 25 patterns:** ~2 seconds
- **Total with setup:** ~3 seconds

Tests run in isolated temp directories, so they're safe and don't pollute fixtures.

## Continuous Integration

These tests are perfect for CI/CD:
```yaml
- name: Run Pattern Integration Tests
  run: python tests/run_pattern_integration_tests.py
```

Exit code 0 = all passed  
Exit code 1 = failures detected

## Summary

✅ **77 variations across 25 patterns**  
✅ **100% pass rate**  
✅ **TRUE integration testing** (not just unit tests)  
✅ **VAR-based stable references**  
✅ **Manual testing friendly**  
✅ **Beautiful formatted output**  
✅ **Fast execution** (~3 seconds for all patterns)

**This is production-ready testing infrastructure!** 🚀
