# SubFast v3.1.0 Refactoring Checklist

## Phase 2 Implementation Guide

### ✅ Completed (Phase 1)
- [x] Created `scripts/common/config_loader.py`
- [x] Created `scripts/common/pattern_engine.py`
- [x] Created `scripts/common/csv_reporter.py`
- [x] Created `resources/data/mkvmerge_language_codes.json`
- [x] Updated refactoring guide

### 🔨 To Do (Phase 2)

#### subfast_rename.py Refactoring

**1. Update Imports (Lines 1-35)**
```python
#!/usr/bin/env python3
"""SubFast - Renaming Module v3.1.0"""

import sys
import csv
from pathlib import Path
from datetime import datetime
import time

# Import shared modules
from common import config_loader
from common import pattern_engine
from common import csv_reporter
```

**2. Delete These Sections:**
- Lines 38-67: Delete BANNER and CSV_BANNER
- Lines 71-83: Delete DEFAULT_CONFIG (now in config_loader)
- Lines 85-175: Delete all config functions (get_script_directory, create_default_config_file, validate_configuration, load_config)
- Lines 180-450: Delete ALL EPISODE_PATTERNS and pattern matching functions
- Lines 600-750: Delete CSV export functions

**3. Replace Function Calls:**
- Line ~210: `CONFIG = load_config()` → `CONFIG = config_loader.load_config()`
- Line ~350: `episode_num = get_episode_number_cached(filename)` → `episode_num = pattern_engine.get_episode_number_cached(filename)`
- Line ~600: Replace entire CSV export block with:
  ```python
  if CONFIG['enable_export']:
      results_list = [...]  # Build results list
      csv_reporter.generate_csv_report(results_list, csv_path, 'renaming')
      csv_reporter.print_summary(results_list, 'Renaming')
  ```

**4. Remove Development Artifacts:**
- Delete all `# Story X.Y` comments (search for "# Story")
- Delete all `# OLD:` comments
- Simplify banner to: `print(f"\nSubFast v3.1.0 - Renaming\n")`

#### subfast_embed.py Refactoring

**1. Update Imports**
```python
#!/usr/bin/env python3
"""SubFast - Embedding Module v3.1.0"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import time

# Import shared modules
from common import config_loader
from common import pattern_engine
from common import csv_reporter
```

**2. Add Language Code Loading (After imports)**
```python
def load_language_codes():
    """Load language codes from JSON."""
    json_path = Path(__file__).parent.parent / 'resources' / 'data' / 'mkvmerge_language_codes.json'
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[WARNING] Language codes file not found")
        return {'codes': {}, 'common_two_letter_codes': {}}

LANGUAGE_DATA = load_language_codes()
```

**3. Delete These Sections:**
- Hardcoded MKVMERGE_LANGUAGE_CODES dictionary (~50 lines)
- All config functions (same as rename script)
- Duplicated episode pattern functions
- Old CSV export logic

**4. Update Language Detection:**
Replace hardcoded dict checks with:
```python
def is_valid_language_code(lang):
    if not lang:
        return False
    code_lower = lang.lower()
    return (code_lower in LANGUAGE_DATA.get('codes', {}) or 
            code_lower in LANGUAGE_DATA.get('common_two_letter_codes', {}))
```

**5. Replace CSV Export:**
Same as rename script - use `csv_reporter.generate_csv_report()`

### 📊 Expected Line Count After Refactoring

**Before:**
- subfast_rename.py: 1,252 lines
- subfast_embed.py: ~1,400 lines

**After:**
- subfast_rename.py: ~650 lines (48% reduction)
- subfast_embed.py: ~700 lines (50% reduction)

### 🧪 Testing Checklist

After refactoring, test:
1. [ ] Config loads correctly
2. [ ] Pattern matching works (test S01E05, 2x10, etc.)
3. [ ] CSV export generates properly
4. [ ] Language detection from JSON works
5. [ ] All features work as before

### 🔍 Search & Replace Commands

Use your IDE's search & replace:

1. **Remove Story comments:**
   - Find: `# Story \d+\.\d+.*\n`
   - Replace: `` (empty)
   - Regex: ON

2. **Update config calls:**
   - Find: `load_config\(`
   - Replace: `config_loader.load_config(`

3. **Update pattern calls:**
   - Find: `get_episode_number_cached\(`
   - Replace: `pattern_engine.get_episode_number_cached(`

### ⚠️ Critical Don't Forget

1. Test with actual video/subtitle files
2. Verify imports work (`from common import ...`)
3. Check JSON path is correct (resources/data/)
4. Remove ALL development artifacts
5. Update version strings to v3.1.0

---

**Next:** Start with `subfast_rename.py`, test it, then do `subfast_embed.py`
