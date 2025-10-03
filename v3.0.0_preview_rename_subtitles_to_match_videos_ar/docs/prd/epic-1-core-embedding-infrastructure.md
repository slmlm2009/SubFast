# Epic 1: Core Embedding Infrastructure

**Epic Goal:** Build the foundation for subtitle embedding using mkvmerge

**Epic Description:**
This epic establishes the core infrastructure for the subtitle embedding feature. It focuses on creating the base script structure, integrating with the mkvmerge command-line tool, implementing the embedding logic with intelligent language detection, and ensuring robust error handling throughout the process.

**Functional Requirements Covered:** FR1, FR3, FR4, NFR1, NFR4

**Non-Functional Requirements Covered:** NFR1 (mkvmerge dependency), NFR4 (error handling)

---

## Story 1.1: Create Base Script Structure and mkvmerge Integration

**Story:** 
As a developer, I want to create the foundational script structure with mkvmerge integration, so that we have a working base for subtitle embedding operations.

**Acceptance Criteria:**
1. A new Python script `embed_subtitles_to_match_videos_ar.py` is created
2. The script can locate and execute `mkvmerge.exe` from a configurable path
3. If no path is configured, the script assumes `mkvmerge.exe` is in the same directory
4. The script validates that `mkvmerge.exe` exists and is executable before proceeding
5. Basic command-line argument parsing is implemented to accept directory input
6. A simple test can be run to verify mkvmerge connectivity (e.g., `mkvmerge --version`)

---

## Story 1.2: Implement Subtitle Embedding Logic with Language Detection

**Story:**
As a user, I want the script to embed subtitles into MKV files with correct language tags, so that my media players can properly identify and display the subtitle tracks.

**Acceptance Criteria:**
1. The script generates correct mkvmerge commands to mux video, audio, and subtitle tracks
2. The new subtitle track is tagged as "default" unless configured otherwise
3. Language codes are extracted from subtitle filenames (e.g., `.ar.srt`, `.en.srt`, `.fr.srt`)
4. If no language code is found in the filename, the script falls back to a configured default language
5. If no default language is configured, no language tag is applied
6. The mkvmerge command preserves all original video and audio tracks without re-encoding
7. A single video-subtitle pair can be successfully merged into a new MKV file

---

## Story 1.3: Add Error Handling and Validation

**Story:**
As a user, I want the script to gracefully handle errors and provide clear feedback, so that I can understand what went wrong and take corrective action.

**Acceptance Criteria:**
1. The script validates that `mkvmerge.exe` exists before attempting any operations
2. Clear error messages are displayed if `mkvmerge.exe` is not found
3. The script checks file permissions before attempting to read/write files
4. Failed mkvmerge operations are caught and reported with the specific error
5. Partial failures during batch processing don't stop the entire operation
6. Each error includes the affected filename and a description of the problem
7. A summary of successful and failed operations is displayed at the end
8. The script returns appropriate exit codes (0 for success, non-zero for errors)
