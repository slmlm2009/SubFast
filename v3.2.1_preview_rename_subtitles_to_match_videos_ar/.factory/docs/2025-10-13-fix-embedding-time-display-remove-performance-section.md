# Fix Embedding Time Display - Remove Performance Section & Add Average

## Problem
The embedding script shows execution time in TWO places with potentially different values:
1. **PERFORMANCE section** (always shown) - Shows actual measured time
2. **Embedding Summary** (only shown if embedding_report enabled) - May show different calculation

**User wants:**
- ❌ Remove PERFORMANCE section entirely
- ✅ Keep accurate time in summary section (always show it)
- ✅ Add "Average time per file" below "Total Execution Time"

---

## Implementation Plan

### 1. Update `subfast_embed.py` main() function

**File:** `subfast/scripts/subfast_embed.py` (Lines 601-620)

#### **Remove PERFORMANCE Section:**
```python
# DELETE THESE LINES (607-612):
# Display performance
print("\nPERFORMANCE:")
print("=" * 60)
print(f"Total Execution Time: {time_str}")
print(f"Operations: {len(results)} total")
print("=" * 60)
```

#### **Always Call print_summary:**
```python
# CHANGE FROM (conditional):
if config.get('embedding_report', False):
    csv_path = folder_path / 'embedding_report.csv'
    csv_reporter.generate_csv_report(results, csv_path, 'embedding')
    csv_reporter.print_summary(results, 'Embedding')

# CHANGE TO (always show summary):
# Export CSV if enabled
if config.get('embedding_report', False):
    csv_path = folder_path / 'embedding_report.csv'
    csv_reporter.generate_csv_report(results, csv_path, 'embedding')

# Always display summary with accurate timing
csv_reporter.print_summary(
    results, 
    'Embedding',
    execution_time=time_str,
    total_files=len(results),
    elapsed_seconds=elapsed_time  # NEW: Pass raw seconds for average calculation
)
```

---

### 2. Update `csv_reporter.py` print_summary() function

**File:** `subfast/scripts/common/csv_reporter.py` (Lines 423-468)

#### **Add elapsed_seconds parameter:**
```python
def print_summary(
    results: List[Dict[str, Any]], 
    operation_name: str = 'Operation',
    execution_time: str = None,
    renamed_count: int = None,
    total_subtitles: int = None,
    total_files: int = None,
    elapsed_seconds: float = None  # NEW: Raw seconds for average calculation
) -> None:
```

#### **Add "Average time per file" after "Total Execution Time":**
```python
# Around line 463-467, CHANGE FROM:
if execution_time:
    print(f"Total Execution Time: {execution_time}")
else:
    print(f"Total time: {format_execution_time(stats['total_time'])}")

# CHANGE TO:
if execution_time:
    print(f"Total Execution Time: {execution_time}")
    # NEW: Add average time per file
    if elapsed_seconds and stats['total'] > 0:
        avg_per_file = elapsed_seconds / stats['total']
        avg_str = format_execution_time(avg_per_file)
        print(f"Average time per file: {avg_str}")
else:
    print(f"Total time: {format_execution_time(stats['total_time'])}")
```

---

## Expected Output

### **Before (Two sections with potentially different times):**
```
PERFORMANCE:
============================================================
Total Execution Time: 2m 35.5s
Operations: 10 total
============================================================

[Only if embedding_report enabled:]
============================================================
Embedding Summary
============================================================
Total files processed: 10
Successful: 8
Failed: 2
Success rate: 80.0%
Total time: 2m 30.0s    <- Different time!
============================================================
```

### **After (Single accurate section with average):**
```
============================================================
Embedding Summary
============================================================
Total files processed: 10
Successful: 8
Failed: 2
Success rate: 80.0%
Total Execution Time: 2m 35.5s
Average time per file: 15.6s
============================================================

Tip: Verify merged files before manually deleting backups directory
     Backups location: C:\path\to\backups
```

---

## Benefits

### ✅ **Accuracy:**
- Single source of truth for execution time
- Uses actual measured time from `time.time()`
- No discrepancies between sections

### ✅ **Useful Information:**
- Average time per file helps users estimate future operations
- Example: "10 files took 15.6s each = plan accordingly for 100 files"

### ✅ **Always Visible:**
- Summary always shown (not dependent on embedding_report setting)
- Users always see execution statistics

### ✅ **Cleaner Output:**
- Removed redundant PERFORMANCE section
- Single, comprehensive summary section

---

## Files Modified

1. **`subfast/scripts/subfast_embed.py`**
   - Remove PERFORMANCE section (6 lines)
   - Move print_summary outside conditional (always call it)
   - Pass execution_time and elapsed_seconds parameters

2. **`subfast/scripts/common/csv_reporter.py`**
   - Add elapsed_seconds parameter to print_summary()
   - Add "Average time per file" calculation and display

---

## Testing Checklist

- [ ] Run embedding with no files (summary shows 0 files)
- [ ] Run embedding with files (summary shows accurate time)
- [ ] Verify "Average time per file" calculates correctly
- [ ] Verify summary shows even when embedding_report=false
- [ ] Verify no PERFORMANCE section appears
- [ ] Verify time format matches (e.g., "2m 35.5s")

---

**Result:** Embedding summary will always show with accurate timing from actual execution, plus helpful average time per file statistic.