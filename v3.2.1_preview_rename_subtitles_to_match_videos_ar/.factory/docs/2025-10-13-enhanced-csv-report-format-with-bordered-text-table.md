# Enhanced CSV Report with Bordered Text Table

## Changes to Implement

### 1. Create Text Table Formatter
- **File**: `subfast/scripts/common/csv_reporter.py`
- **Add new function**: `format_text_table(file_rows)` 
- Generates bordered text table with dynamic column widths
- Column order: Original Filename | Detected Episode | Action | New Name
- Max width caps at 80 characters per column for readability

### 2. Update Report Generation
- **File**: `subfast/scripts/common/csv_reporter.py`
- **Function**: `generate_csv_report()`
- Replace CSV writer section with text table formatter
- Keep all header comments (banner, timestamp, summary stats)
- Keep matched episodes section at bottom
- File still named `renaming_report.csv` for backward compatibility

### 3. Key Features
- ✅ Dynamic column widths based on content
- ✅ Professional bordered table with `+`, `-`, `|` characters
- ✅ Left-aligned text with proper padding
- ✅ Better readability than CSV format
- ✅ No CSV parsing needed to read

### 4. Example Output
```
+-------------------------------------------------------+------------------+----------+-------------------------------------------------------+
| Original Filename                                     | Detected Episode | Action   | New Name                                              |
+-------------------------------------------------------+------------------+----------+-------------------------------------------------------+
| S01E02-Life in the Fast Lane [71D582F2].mkv          | S01E02           | --       | No Change                                             |
| [Celestial Dragons] Lazarus - 02 [1080p].ass         | S01E02           | RENAMED  | S01E02-Life in the Fast Lane [71D582F2].ar.ass       |
+-------------------------------------------------------+------------------+----------+-------------------------------------------------------+
```

## Files to Modify
- `subfast/scripts/common/csv_reporter.py` - Add formatter and update report generation