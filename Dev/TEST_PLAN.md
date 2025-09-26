# Test Plan for Subtitle Renaming Script

## Overview
This document outlines the test plan for the `rename_subtitles_to_match_videos_ar.py` script. The script is designed to rename subtitle files to match corresponding video files based on episode numbers detected in filenames.

## Test Environment Setup
- Create a test directory with controlled file sets
- Ensure Python 3 and required dependencies are available
- Create test scenarios with various naming patterns
- Implement before/after state verification

## Test Categories

### 1. Episode Detection Tests

#### 1.1 S##E## Pattern Tests
- **Test 1.1.1**: Basic S##E## pattern
  - Input: `show.S01E01.mkv` and `subtitle.S01E01.srt`
  - Expected: `subtitle.S01E01.srt` → `show.S01E01.ar.srt`

- **Test 1.2**: S##E## with single digit episodes (should be zero-padded)
  - Input: `show.S01E5.mkv` and `subtitle.S01E5.srt`
  - Expected: `subtitle.S01E5.srt` → `show.S01E05.ar.srt`

- **Test 1.3**: S##E## with single digit seasons (should be zero-padded)
  - Input: `show.S1E05.mkv` and `subtitle.S1E05.srt`
  - Expected: `subtitle.S1E05.srt` → `show.S01E05.ar.srt`

- **Test 1.4**: Mixed case S##E## patterns
  - Input: `show.s01e01.mkv`, `show.S01e02.mkv`, `show.s01E03.mkv`
  - Expected: All patterns should be detected correctly

- **Test 1.5**: S##E## with additional text
  - Input: `show.name.S01E01.other.text.mkv` and `subtitle.name.S01E01.srt`
  - Expected: Should correctly match based on episode number

#### 1.2 "- ##" Pattern Tests
- **Test 1.2.1**: Basic "- ##" pattern
  - Input: `show.S01E01.mkv` and `subtitle - 01.srt`
  - Expected: `subtitle - 01.srt` → `show.S01E01.ar.srt` (assumes S01E01)

- **Test 1.2.2**: "- ##" with single digit numbers (should be zero-padded)
  - Input: `show.S01E05.mkv` and `subtitle - 5.srt`
  - Expected: `subtitle - 5.srt` → `show.S01E05.ar.srt`

- **Test 1.2.3**: "- ##" with spaces
  - Input: `show.S01E01.mkv` and `subtitle- 01.srt` (space before number)
  - Expected: Should detect the episode number

- **Test 1.2.4**: "- ##" with text after numbers
  - Input: `show.S01E01.mkv` and `subtitle - 01 extra.mkv`
  - Expected: Should detect episode 01

#### 1.3 Pattern Recognition Edge Cases
- **Test 1.3.1**: Invalid S##E## patterns
  - Input: `file.S1E1.txt` (not zero-padded)
  - Expected: Should detect as S01E01

- **Test 1.3.2**: Non-matching episode numbers
  - Input: `show.S01E01.mkv` and `other.S01E02.srt`
  - Expected: Files should not be renamed

- **Test 1.3.3**: No episode pattern in filename
  - Input: `movie file name.mkv` and `**any matching word of the movie file name**.srt`
  - Expected: Assuming a movie file and it's subtitle files  **any matching word of the movie file name**.srt will be renamed to "movie file name.srt"

### 2. File Extension Tests

#### 2.1 Video Format Support
- **Test 2.1.1**: MKV video files
  - Input: `show.S01E01.mkv` and `subtitle.S01E01.srt`
  - Expected: Successful rename

- **Test 2.1.2**: MP4 video files
  - Input: `show.S01E01.mp4` and `subtitle.S01E01.srt`
  - Expected: Successful rename

- **Test 2.1.3**: Multiple video formats in same directory
  - Input: `show.S01E01.mkv`, `show.S01E02.mp4`, `subtitle.S01E01.srt`, `subtitle.S01E02.ass`
  - Expected: Both subtitles should be renamed appropriately

#### 2.2 Subtitle Format Support
- **Test 2.2.1**: SRT subtitle files
  - Input: `show.S01E01.mkv` and `subtitle.S01E01.srt`
  - Expected: `subtitle.S01E01.srt` → `show.S01E01.ar.srt`

- **Test 2.2.2**: ASS subtitle files
  - Input: `show.S01E01.mkv` and `subtitle.S01E01.ass`
  - Expected: `subtitle.S01E01.ass` → `show.S01E01.ar.ass`

- **Test 2.2.3**: Mixed subtitle formats
  - Input: `show.S01E01.mkv`, `subtitle.S01E01.srt`, `other.S01E01.ass`
  - Expected: Both subtitles renamed to match video

#### 2.3 Non-Supported Formats
- **Test 2.3.1**: Non-video files mixed with supported formats
  - Input: `show.S01E01.txt`, `show.S01E01.mkv`, `subtitle.S01E01.srt`
  - Expected: Only .mkv should be treated as video, .txt ignored

### 3. Error Handling Tests

#### 3.1 Missing Files
- **Test 3.1.1**: No video files present
  - Input: Only subtitle files in directory
  - Expected: No files renamed, appropriate message

- **Test 3.1.2**: No subtitle files present
  - Input: Only video files in directory
  - Expected: No files renamed, appropriate message

- **Test 3.1.3**: No matching episode numbers
  - Input: `show.S01E01.mkv` and `other.S02E01.srt`
  - Expected: No rename, message indicating no match found

#### 3.2 File Permissions
- **Test 3.2.1**: Read-only subtitle files
  - Input: `show.S01E01.mkv` and read-only `subtitle.S01E01.srt`
  - Expected: Appropriate error handling

#### 3.3 Edge Cases
- **Test 3.3.1**: Files with special characters
  - Input: `show.S01E01!.mkv` and `subtitle.S01E01@.srt`
  - Expected: Should handle special characters properly

- **Test 3.3.2**: Very long filenames
  - Input: Long filename with S##E## pattern
  - Expected: Should handle without errors

- **Test 3.3.3**: Duplicate episode numbers in subtitles
  - Input: `show.S01E01.mkv`, `subtitle1.S01E01.srt`, `subtitle2.S01E01.srt`
  - Expected: Both subtitles match the same video, but only one can be renamed to the target name (this is an inherent limitation of the script)

### 4. Special Case Tests

#### 4.1 Multiple Seasons
- **Test 4.1.1**: Multi-season directory
  - Input: `show.S01E01.mkv`, `show.S02E01.mkv`, `subtitle1.S01E01.srt`, `subtitle2.S02E01.srt`
  - Expected: Each subtitle should match its corresponding season/episode

#### 4.2 Partial Matches
- **Test 4.2.1**: Partial episode matches
  - Input: `show.S01E01.mkv` and `subtitle.S01E01.part1.srt`
  - Expected: Should detect episode and rename appropriately

#### 4.3 File Overwrites
- **Test 4.3.1**: Target filename already exists
  - Input: `show.S01E01.mkv`, `show.S01E01.ar.srt` (existing), `subtitle.S01E01.srt`
  - Expected: Appropriate error handling or skip

### 5. Functional Tests

#### 5.1 Complete Workflow
- **Test 5.1.1**: Full directory processing
  - Input: Mix of video and subtitle files with various patterns
  - Expected: All matching files are renamed correctly

- **Test 5.1.2**: Directory with no matches
  - Input: Unrelated files with no matching patterns
  - Expected: No files renamed, appropriate messages

#### 5.2 Console Output Verification
- **Test 5.2.1**: Verify output messages
  - Expected: Script outputs directory, file counts, detected episodes, and rename operations

## Test Execution Methodology

### Pre-test Setup
1. Create a clean test directory
2. Copy original script to test environment
3. Prepare test file sets according to test cases
4. Document initial state of test directory

### Test Execution
1. Run script in test directory
2. Capture console output
3. Document final state of test directory
4. Compare actual results with expected results
5. Record pass/fail status for each test
6. Log any errors or unexpected behavior

### Post-test Cleanup
1. Restore test environment to initial state
2. Remove test files and directories
3. Document any issues found for bug reporting

## Success Criteria
- All matching subtitle files are correctly renamed to match video files
- New filenames include .ar suffix and maintain original subtitle extension
- Episode numbers are properly detected and zero-padded
- Non-matching files remain unchanged
- Appropriate console messages are displayed
- No errors occur during normal operation

## Expected Output Format
The script should output:
- Current directory being processed
- Count of video and subtitle files found
- Detected episode numbers
- Rename operations performed
- Final count of renamed files