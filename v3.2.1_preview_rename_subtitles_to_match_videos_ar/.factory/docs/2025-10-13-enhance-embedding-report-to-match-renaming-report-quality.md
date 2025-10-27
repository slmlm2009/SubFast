# Enhancement: Comprehensive Embedding Report

## Problem
Current refactored embedding report (`csv_reporter._write_embedding_report()`) generates only a basic CSV table with no header sections, statistics, or human-readable summaries. This is a significant regression from v3.0.0 which had:
- SubFast ASCII banner
- Configuration summary
- Detailed statistics with execution time
- Successfully embedded pairs section
- Failed operations with error details
- Unmatched videos/subtitles sections
- Comprehensive CSV table

The current basic format doesn't match the quality of the enhanced renaming report.

---

## Solution Overview
Transform the embedding report to match the comprehensive, professional format of the renaming report while preserving embedding-specific information.

---

## Implementation Plan

### **1. Update `csv_reporter.py` - Enhance `_write_embedding_report()`**

**Current signature:**
```python
def _write_embedding_report(file_handle, results: List[Dict[str, Any]]) -> None:
```

**New signature:**
```python
def _write_embedding_report(
    file_handle,
    results: List[Dict[str, Any]],
    output_path: Path,
    config: Optional[Dict] = None,
    execution_time_str: Optional[str] = None,
    elapsed_seconds: Optional[float] = None,
    all_videos: Optional[List[str]] = None,
    all_subtitles: Optional[List[str]] = None
) -> None:
```

**New report structure:**

#### **Section 1: SubFast ASCII Banner**
- Reuse the banner from renaming report

#### **Section 2: Report Header**
```
# SubFast Embedding Report
# Generated: 2025-01-15 14:30:00
# Directory: C:\path\to\directory
```

#### **Section 3: Configuration Summary**
```
# CONFIGURATION:
# mkvmerge path: C:\path\to\mkvmerge.exe (or: default - bin/mkvmerge.exe)
# Language code: ar (or: none)
# Default flag: yes
# Embedding report: enabled
```

#### **Section 4: Statistics Summary**
```
# STATISTICS:
# Total Videos: 10
# Total Subtitles: 8
# Pairs Matched: 7
# Successfully Embedded: 7
# Failed: 0
# Videos Without Subtitles: 3
# Subtitles Without Videos: 1
# Success Rate: 100.0%
# Total Execution Time: 2m 15.5s
# Average Time Per File: 19.4s
```

**Statistics Calculation Logic:**
- **Total Videos:** Count from `all_videos` list
- **Total Subtitles:** Count from `all_subtitles` list
- **Pairs Matched:** Count of results with `status='success'` or `'failed'` (video matched)
- **Successfully Embedded:** Count of results with `status='success'`
- **Failed:** Count of results with `status='failed'`
- **Videos Without Subtitles:** Count of videos not in embedded results
- **Subtitles Without Videos:** Count of results with `status='no_match'`
- **Success Rate:** (Successfully Embedded / Pairs Matched) * 100

#### **Section 5: Bordered Text Table**
Format similar to renaming report:
```
+------------------+------------------+----------+----------+------------------+
| Video File       | Subtitle File    | Episode  | Language | Status           |
+------------------+------------------+----------+----------+------------------+
| Episode.S01E01.. | Subtitle.ar.srt  | S01E01   | ar       | EMBEDDED         |
| Episode.S01E02.. | Subtitle.srt     | S01E02   | none     | EMBEDDED         |
| Episode.S01E03.. | (no match)       | S01E03   | --       | NO SUBTITLE      |
| (no match)       | Orphan.srt       | N/A      | --       | NO VIDEO         |
| Episode.S01E04.. | Failed.srt       | S01E04   | en       | FAILED           |
+------------------+------------------+----------+----------+------------------+
```

**Column Logic:**
- **Video File:** Video filename (or "(no match)" for subtitles without videos)
- **Subtitle File:** Subtitle filename (or "(no match)" for videos without subtitles)
- **Episode:** Detected episode pattern (S01E01 format) or "N/A"
- **Language:** Detected language code or "--"
- **Status:** EMBEDDED | FAILED | NO SUBTITLE | NO VIDEO

**Table Construction:**
1. Build rows from `results` list (matched pairs + no_match subtitles)
2. Add rows for unmatched videos (videos not in results)
3. Sort by video filename, then subtitle filename

#### **Section 6: Successfully Embedded Pairs**
```
# SUCCESSFULLY EMBEDDED PAIRS:
# S01E01 -> Video: Episode.S01E01.mkv | Subtitle: Subtitle.S01E01.ar.srt | Language: ar
# S01E02 -> Video: Episode.S01E02.mkv | Subtitle: Subtitle.S01E02.srt | Language: none
# (7 total)
```

#### **Section 7: Failed Operations**
```
# FAILED OPERATIONS:
# S01E04 -> Video: Episode.S01E04.mkv | Subtitle: Failed.srt
#   Error: mkvmerge failed: insufficient disk space
# (1 total)
```
- Only show if there are failures
- Include full error message

#### **Section 8: Unmatched Videos**
```
# VIDEOS WITHOUT MATCHING SUBTITLES:
# S01E03 -> Episode.S01E03.mkv
# S01E05 -> Episode.S01E05.mkv
# (2 total)
```

#### **Section 9: Unmatched Subtitles**
```
# SUBTITLES WITHOUT MATCHING VIDEOS:
# S01E10 -> Orphan.S01E10.srt
# (1 total)
```

---

### **2. Update `subfast_embed.py` - Pass Additional Context**

**Modify `process_embedding()` to return additional data:**
```python
def process_embedding(folder_path, config, mkvmerge_path):
    # ... existing code ...
    
    # Return results plus additional context for reporting
    return {
        'results': results,
        'all_videos': [v.name for v in mkv_videos],
        'all_subtitles': [s.name for s in all_subtitle_files]
    }
```

**Update `main()` to pass enhanced parameters:**
```python
def main():
    # ... existing code ...
    
    # Process embeddings
    process_data = process_embedding(folder_path, config, mkvmerge_path)
    results = process_data['results']
    all_videos = process_data['all_videos']
    all_subtitles = process_data['all_subtitles']
    
    # Calculate execution time
    elapsed_time = time.time() - start_time
    time_str = csv_reporter.format_execution_time(elapsed_time)
    
    # Export CSV if enabled
    if config.get('embedding_report', False):
        csv_path = folder_path / 'embedding_report.csv'
        csv_reporter.generate_csv_report(
            results=results,
            output_path=csv_path,
            operation_type='embedding',
            config=config,
            execution_time_str=time_str,
            all_videos=all_videos,
            all_subtitles=all_subtitles,
            elapsed_seconds=elapsed_time
        )
```

---

### **3. Helper Functions in `csv_reporter.py`**

**Add helper to format embedding text table:**
```python
def format_embedding_text_table(
    results: List[Dict],
    all_videos: List[str],
    all_subtitles: List[str]
) -> str:
    """
    Format embedding results as bordered text table.
    
    Combines matched pairs, unmatched videos, and unmatched subtitles
    into a unified table view.
    """
    # Build comprehensive row list...
```

**Add helper to calculate embedding statistics:**
```python
def calculate_embedding_statistics(
    results: List[Dict],
    all_videos: List[str],
    all_subtitles: List[str]
) -> Dict[str, Any]:
    """Calculate comprehensive embedding statistics."""
    # Return dict with all stats...
```

---

## Expected Output Example

```
# ==========================================
#    ____        _     _____          _   
#   / ___| _   _| |__ |  ___|_ _  ___| |_ 
#   \___ \| | | | '_ \| |_ / _` |/ __| __|
#    ___) | |_| | |_) |  _| (_| |\__ \ |_ 
#   |____/ \__,_|_.__/|_|  \__,_||___/\__|
#                                         
#    Fast subtitle renaming and embedding
# 
# ==========================================
#
# SubFast Embedding Report
# Generated: 2025-01-15 14:30:00
# Directory: C:\Users\user\Videos\Show
#
# CONFIGURATION:
# mkvmerge path: default - bin/mkvmerge.exe
# Language code: ar
# Default flag: yes
# Embedding report: enabled
#
# STATISTICS:
# Total Videos: 10
# Total Subtitles: 8
# Pairs Matched: 7
# Successfully Embedded: 7
# Failed: 0
# Videos Without Subtitles: 3
# Subtitles Without Videos: 1
# Success Rate: 100.0%
# Total Execution Time: 2m 15.5s
# Average Time Per File: 19.4s
#
+------------------------------+------------------------------+----------+----------+--------------+
| Video File                   | Subtitle File                | Episode  | Language | Status       |
+------------------------------+------------------------------+----------+----------+--------------+
| Show.S01E01.1080p.mkv        | Show.S01E01.ar.srt          | S01E01   | ar       | EMBEDDED     |
| Show.S01E02.1080p.mkv        | Show.S01E02.ar.srt          | S01E02   | ar       | EMBEDDED     |
| Show.S01E03.1080p.mkv        | (no match)                   | S01E03   | --       | NO SUBTITLE  |
+------------------------------+------------------------------+----------+----------+--------------+
#
# SUCCESSFULLY EMBEDDED PAIRS:
# S01E01 -> Video: Show.S01E01.1080p.mkv | Subtitle: Show.S01E01.ar.srt | Language: ar
# S01E02 -> Video: Show.S01E02.1080p.mkv | Subtitle: Show.S01E02.ar.srt | Language: ar
# (2 total)
#
# FAILED OPERATIONS:
# (None)
#
# VIDEOS WITHOUT MATCHING SUBTITLES:
# S01E03 -> Show.S01E03.1080p.mkv
# (1 total)
#
# SUBTITLES WITHOUT MATCHING VIDEOS:
# (None)
#
```

---

## Benefits

1. **Feature Parity:** Matches v3.0.0 embedding report quality
2. **Consistency:** Aligns with enhanced renaming report format
3. **Comprehensive:** Shows all relevant information in one place
4. **Human-Readable:** Bordered tables and clear sections
5. **Actionable:** Easy to identify what worked, what failed, and what's missing

---

## Files Modified

1. **`subfast/scripts/common/csv_reporter.py`**
   - Enhance `_write_embedding_report()` signature and implementation
   - Add `format_embedding_text_table()` helper
   - Add `calculate_embedding_statistics()` helper

2. **`subfast/scripts/subfast_embed.py`**
   - Modify `process_embedding()` to return dict with results + context
   - Update `main()` to pass enhanced parameters to `generate_csv_report()`