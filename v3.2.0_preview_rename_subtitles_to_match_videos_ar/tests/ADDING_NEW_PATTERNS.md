# Adding New Episode Patterns - Quick Guide

This document provides a simple 5-step workflow for adding new episode naming patterns to SubFast's pattern recognition system.

**Time to add a new pattern: < 10 minutes** (no test code changes needed!)

---

## 5-Step Workflow

### Step 1: Add Pattern Regex to Pattern Engine

**File:** `subfast/scripts/common/pattern_engine.py`

**Location:** Add to the `EPISODE_PATTERNS` list (order matters - first match wins!)

**Template:**
```python
# Pattern ##: <Your Pattern Name>
(
    '<Pattern Name>',
    re.compile(r'<your_regex_pattern>', re.IGNORECASE),
    lambda m: (int(m.group(1)), int(m.group(2)))
),
```

**Example - Adding "Episode.##.Season.##" format:**
```python
# Pattern 26: Episode.##.Season.## (reversed order)
(
    'Episode.##.Season.##',
    re.compile(r'[Ee]pisode[\s\._-]*(\d+)[\s\._-]*[Ss]eason[\s\._-]*(\d+)', re.IGNORECASE),
    lambda m: (int(m.group(2)), int(m.group(1)))  # Note: reversed - episode is group 1, season is group 2
),
```

---

### Step 2: Add Pattern Definition to JSON

**File:** `tests/fixtures/pattern_definitions.json`

**Location:** Add to the `patterns` array

**Template:**
```json
{
  "id": 26,
  "name": "Your Pattern Name",
  "description": "Brief description of the pattern format",
  "video_variations": [
    "Example.File.Name.1.mkv",
    "Another.Example.2.720p.mkv",
    "Third.Variation.3.mkv"
  ],
  "subtitle_variations": [
    "Example.File.Name.1.srt",
    "Another.Example.2.srt",
    "Third.Variation.3.srt"
  ],
  "expected_match": {
    "S##E##": ["Example.File.Name.1.mkv", "Example.File.Name.1.srt"],
    "S##E##": ["Another.Example.2.720p.mkv", "Another.Example.2.srt"],
    "S##E##": ["Third.Variation.3.mkv", "Third.Variation.3.srt"]
  }
}
```

**Actual Example - Adding "Episode.5.Season.2" format:**
```json
{
  "id": 26,
  "name": "Episode.#.Season.#",
  "description": "Reversed order - Episode number before Season (e.g., Episode.5.Season.2)",
  "video_variations": [
    "Show.Episode.5.Season.2.mkv",
    "Series.Episode.10.Season.3.720p.mkv",
    "Example.Episode.15.Season.1.BluRay.mkv"
  ],
  "subtitle_variations": [
    "Show.Episode.5.Season.2.srt",
    "Series.Episode.10.Season.3.srt",
    "Example.Episode.15.Season.1.srt"
  ],
  "expected_match": {
    "S02E05": ["Show.Episode.5.Season.2.mkv", "Show.Episode.5.Season.2.srt"],
    "S03E10": ["Series.Episode.10.Season.3.720p.mkv", "Series.Episode.10.Season.3.srt"],
    "S01E15": ["Example.Episode.15.Season.1.BluRay.mkv", "Example.Episode.15.Season.1.srt"]
  }
}
```

**Important JSON Fields:**
- `id`: Next sequential pattern number
- `name`: Short pattern name (used in test class names)
- `description`: Explain what the pattern matches
- `video_variations`: 3-5 example video filenames
- `subtitle_variations`: 3-5 example subtitle filenames (can differ from video)
- `expected_match`: Map each filename to its expected S##E## result

---

### Step 3: Regenerate Dummy Test Files

**Command:**
```bash
python tests/generate_test_files.py
```

**What happens:**
- Script reads `pattern_definitions.json`
- Automatically creates dummy files for your new pattern
- Creates new directory: `tests/fixtures/pattern_files/pattern_26_<name>/`
- Generates all video and subtitle variations

**Expected output:**
```
[OK] Pattern 26: Your Pattern Name  (3 videos, 3 subtitles)
...
Total files created: 160  (was 154, now 6 more files added)
```

---

### Step 4: Run Tests to Validate

**Command:**
```bash
python tests/run_tests.py
```

**What to check:**
- New tests automatically discovered for Pattern 26
- All tests pass (including your new pattern)
- Test count increased by 2 (video_variations + subtitle_variations)

**Expected output:**
```
TEST SCRIPT SUMMARY
| test_pattern_matching     | 61     | 61     | 0      | 100.00% | PASS   |
                              ^^^ was 59, now 61

Ran 85 tests in 0.062s  (was 83 tests)
OK
```

**If tests fail:**
- Check your regex in Step 1
- Verify expected_match values in Step 2
- Ensure pattern priority is correct (earlier patterns might match first)

---

### Step 5: Update Pattern Guide Documentation

**File:** `tests/1- Renaming/episode_patterns_guide.md`

**Location:** Add new section at the end (before priority was important, but for docs just append)

**Template:**
```markdown
## Pattern ##: <Your Pattern Name> Format
**Regex:** `<your_regex_pattern>`

**Description:** <Detailed explanation of what this pattern matches>

**Examples:**
- `<example1>` → Season #, Episode #
- `<example2>` → Season #, Episode #
- `<example3>` → Season #, Episode #

---
```

**Actual Example:**
```markdown
## Pattern 26: Episode.#.Season.# Format
**Regex:** `[Ee]pisode[\s\._-]*(\d+)[\s\._-]*[Ss]eason[\s\._-]*(\d+)`

**Description:** Reversed episode/season order with episode number appearing before season number. Uses dot separators.

**Examples:**
- `Episode.5.Season.2` → Season 2, Episode 5
- `Episode.10.Season.3` → Season 3, Episode 10
- `Show.Episode.15.Season.1.mkv` → Season 1, Episode 15

**Note:** Episode number comes FIRST, season number comes SECOND (reversed from typical).

---
```

---

## ✅ That's It!

Your new pattern is now:
- ✅ Recognized by the pattern engine
- ✅ Tested with realistic dummy files
- ✅ Validated by automated tests
- ✅ Documented for other developers

**Total time:** < 10 minutes for simple patterns

---

## Common Pitfalls & Troubleshooting

### Pitfall 1: Pattern Priority

**Problem:** Your pattern never matches because an earlier pattern catches it first.

**Solution:** 
- Patterns are tried in order (first match wins)
- More specific patterns should come BEFORE generic patterns
- Example: `S01E05` (Pattern 1) should come before `Season 1 Episode 5` (Pattern 15)
- Consider adding your pattern earlier in the list if needed

### Pitfall 2: Regex Group Order

**Problem:** Season and episode numbers are swapped in results.

**Solution:**
- The lambda function expects: `lambda m: (season, episode)`
- Ensure `m.group(1)` and `m.group(2)` map correctly
- For reversed order patterns, swap them: `lambda m: (int(m.group(2)), int(m.group(1)))`

### Pitfall 3: Case Sensitivity

**Problem:** Pattern doesn't match lowercase/uppercase variations.

**Solution:**
- Always use `re.IGNORECASE` flag in your regex compile
- Use character classes: `[Ss]` instead of just `s` or `S`
- Test both uppercase and lowercase examples

### Pitfall 4: Word Boundaries

**Problem:** Pattern matches random text (e.g., "2x3" in "text12x3text").

**Solution:**
- Use word boundary anchors: `(?:^|[._\s-])` before and `(?=[._\s-]|$)` after
- Example from Pattern 2: `(?:^|[._\s-])(\d{1,2})[xX](\d+)(?=[._\s-]|$)`

### Pitfall 5: JSON Syntax Errors

**Problem:** Tests fail to load pattern_definitions.json.

**Solution:**
- Validate JSON syntax (use online JSON validator)
- Check for trailing commas (not allowed in JSON)
- Ensure all strings use double quotes (not single quotes)
- Verify brackets and braces are balanced

---

## Testing Your Pattern in Isolation

**Quick test without running full suite:**

```python
from subfast.scripts.common.pattern_engine import get_episode_number_cached

# Test your pattern
result = get_episode_number_cached("Your.Test.File.Name.mkv")
print(f"Result: {result}")  # Should print: S##E##
```

**Check which pattern matched:**

```python
from subfast.scripts.common.pattern_engine import extract_episode_info

season, episode = extract_episode_info("Your.Test.File.Name.mkv")
print(f"Season: {season}, Episode: {episode}")
```

---

## Pattern Template (Copy-Paste Ready)

### For pattern_engine.py:
```python
# Pattern ##: <NAME>
(
    '<Pattern.Name>',
    re.compile(r'<regex>', re.IGNORECASE),
    lambda m: (int(m.group(1)), int(m.group(2)))
),
```

### For pattern_definitions.json:
```json
{
  "id": ##,
  "name": "Pattern Name",
  "description": "Description here",
  "video_variations": [
    "File1.mkv",
    "File2.mkv",
    "File3.mkv"
  ],
  "subtitle_variations": [
    "File1.srt",
    "File2.srt",
    "File3.srt"
  ],
  "expected_match": {
    "S##E##": ["File1.mkv", "File1.srt"],
    "S##E##": ["File2.mkv", "File2.srt"],
    "S##E##": ["File3.mkv", "File3.srt"]
  }
}
```

---

## Need Help?

1. **Check existing patterns** in `pattern_engine.py` for similar examples
2. **Test your regex** at https://regex101.com/ (use Python flavor)
3. **Review the pattern guide** at `tests/1- Renaming/episode_patterns_guide.md`
4. **Run reset script** if test files get corrupted: `python tests/reset_test_files.py`

---

**Last updated:** v3.2.0  
**Tested with:** Python 3.10+, SubFast v3.2.0
