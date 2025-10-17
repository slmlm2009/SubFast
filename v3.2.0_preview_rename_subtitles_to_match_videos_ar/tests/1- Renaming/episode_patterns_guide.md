# Episode Pattern Recognition - All Supported Formats

This document lists all 30 naming patterns (98 regex variations + 1 contextual) supported by the pattern engine, ordered by priority (first match wins).

**Recent Updates (2025-01-17):**
- ✅ Pattern 5a: Fixed to allow space before episode number (`s2 ep 08`)
- ✅ Pattern 5b: Added for dot separator before EP (`s02.ep13`)
- ✅ Pattern 22 (19a): Added for `season## e##` format (`season2 e21`)
- ✅ Pattern 30: Added FINAL SEASON contextual matching (season inference)

---

## Pattern 1: S##E## Format
**Regex:** `[Ss](\d+)\s?[Ee](\d+)` and `[Ss](\d+)\s+[Ee]pisode\s+(\d+)`

**Description:** The most common format with 'S' followed by season number, 'E' followed by episode number. Supports optional space between S## and E##, and full 'Episode' word variation.

**Examples:**
- `S01E05` → Season 1, Episode 5
- `S2E10` → Season 2, Episode 10
- `s03e15` → Season 3, Episode 15
- `S02 E3` → Season 2, Episode 3 (space-separated)
- `s3 e2` → Season 3, Episode 2 (space-separated, lowercase)
- `S02 Episode 08` → Season 2, Episode 8 (full Episode word)
- `Show.Name.S01E01.720p.mkv`
- `ShowName.S02 E3.mkv` (space-separated variation)

---

## Pattern 2: ##x## Format
**Regex:** `(?:^|[._\s-])(\d{1,2})[xX](\d+)(?=[._\s-]|$)`

**Description:** Alternative format using 'x' as separator between season and episode.

**Examples:**
- `2x05` → Season 2, Episode 5
- `1x10` → Season 1, Episode 10
- `Show.Name.3X07.mkv`
- `Episode.12x03.srt`

**Note:** Requires word boundaries to avoid matching random 'x' in text.

---

## Pattern 3: S## - ## Format
**Regex:** `[Ss](\d{1,2})\s*-\s*(\d+)`

**Description:** Season with dash separator to episode number (no 'E').

**Examples:**
- `S01 - 05` → Season 1, Episode 5
- `S2 - 10` → Season 2, Episode 10
- `S03-15` → Season 3, Episode 15
- `s1 - 7` → Season 1, Episode 7

---

## Pattern 4: S## - E## Format (and variations)
**Regex:** `[Ss](\d{1,2})\s*-\s*[Ee](\d+)`, `[Ss](\d{1,2})\.E(\d+)`, `[Ss](\d{1,2})_[Ee](\d+)`

**Description:** Season with separator to 'E' + episode number. Supports dash, dot, and underscore separators.

**Examples:**
- `S01 - E05` → Season 1, Episode 5 (dash)
- `S2 - E10` → Season 2, Episode 10 (dash)
- `S03-E15` → Season 3, Episode 15 (dash, no space)
- `S02.E12` → Season 2, Episode 12 (dot separator)
- `S03_E07` → Season 3, Episode 7 (underscore separator)
- `s1 - e7` → Season 1, Episode 7

---

## Pattern 5: S## - EP## Format (and variations)
**Regex:** `[Ss](\d{1,2})\s*-\s*[Ee][Pp](\d+)`, `[Ss](\d{1,2})\s+[Ee][Pp]\s*(\d+)`, and `[Ss](\d{1,2})\.[Ee][Pp](\d+)` **[FIXED + NEW]**

**Description:** Season with separator to 'EP' + episode number. Supports dash, space, and dot separators. **Fixed to allow optional space before episode number** (e.g., `s2 ep 08`). **Added dot separator** (e.g., `s02.ep13`).

**Examples:**
- `S01 - EP05` → Season 1, Episode 5 (dash)
- `S2 - EP10` → Season 2, Episode 10 (dash)
- `S03-ep15` → Season 3, Episode 15 (dash, no space)
- `S01 EP15` → Season 1, Episode 15 (space, no dash)
- `s2 ep 08` → Season 2, Episode 8 (**space before episode** - fixed)
- `s02.ep13` → Season 2, Episode 13 (**dot separator** - new)
- `s1 - Ep7` → Season 1, Episode 7

---

## Pattern 6: 1st Season - ## Format
**Regex:** `(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s*-\s*(\d+)`

**Description:** Ordinal number format (1st, 2nd, 3rd, etc.) with 'Season' keyword.

**Examples:**
- `1st Season - 05` → Season 1, Episode 5
- `2nd Season - 10` → Season 2, Episode 10
- `3rd Season - 15` → Season 3, Episode 15
- `12th Season - 3` → Season 12, Episode 3

---

## Pattern 7: 1st Season Episode ## Format
**Regex:** `(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s+[Ee]pisode\s+(\d+)`

**Description:** Full ordinal format with both 'Season' and 'Episode' keywords.

**Examples:**
- `3rd Season Episode 8` → Season 3, Episode 8
- `1st Season Episode 1` → Season 1, Episode 1
- `2nd season episode 15` → Season 2, Episode 15
- `10th Season Episode 22` → Season 10, Episode 22

---

## Pattern 8: 1st Season E## Format
**Regex:** `(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s+[Ee]\s*(\d+)`

**Description:** Ordinal format with abbreviated 'E' for episode.

**Examples:**
- `2nd Season E10` → Season 2, Episode 10
- `1st Season E5` → Season 1, Episode 5
- `3rd season e7` → Season 3, Episode 7

---

## Pattern 9: 1st Season EP## Format
**Regex:** `(\d{1,2})(?:st|nd|rd|th)\s+[Ss]eason\s+[Ee][Pp]\s*(\d+)`

**Description:** Ordinal format with 'EP' for episode.

**Examples:**
- `2nd Season EP10` → Season 2, Episode 10
- `1st Season EP5` → Season 1, Episode 5
- `3rd season ep7` → Season 3, Episode 7

---

## Pattern 10: Season ## - ## Format
**Regex:** `[Ss]eason\s+(\d{1,2})\s*-\s*(\d+)`

**Description:** Full 'Season' word with space, followed by dash and episode number.

**Examples:**
- `Season 2 - 23` → Season 2, Episode 23
- `Season 12 - 103` → Season 12, Episode 103
- `season 1 - 5` → Season 1, Episode 5

---

## Pattern 11: Season## - ## Format
**Regex:** `[Ss]eason(\d{1,2})\s*-\s*(\d+)`

**Description:** 'Season' word without space before number, dash to episode.

**Examples:**
- `Season1 - 5` → Season 1, Episode 5
- `Season2 - 10` → Season 2, Episode 10
- `season3-15` → Season 3, Episode 15

---

## Pattern 12: Season.#.Episode.# Format
**Regex:** `[Ss]eason\.(\d+)[\s\._-]*[Ee]pisode\.(\d+)`

**Description:** Dot-separated format with full keywords.

**Examples:**
- `Season.1.Episode.5` → Season 1, Episode 5
- `Season.2.Episode.10` → Season 2, Episode 10
- `season.3_episode.7` → Season 3, Episode 7

---

## Pattern 13: S#.Ep.# Format
**Regex:** `[Ss](\d+)[\s\._-]*[Ee]p(?:isode)?\.(\d+)`

**Description:** Short 'S' with dot-separated 'Ep' or 'Episode'.

**Examples:**
- `S1.Ep.5` → Season 1, Episode 5
- `S2.Episode.10` → Season 2, Episode 10
- `s3_ep.7` → Season 3, Episode 7

---

## Pattern 14: S#Ep# Format
**Regex:** `[Ss](\d+)[Ee]p(?:isode)?(\d+)`

**Description:** Short 'S' followed by 'Ep' or 'Episode', no separators.

**Examples:**
- `S1Ep5` → Season 1, Episode 5
- `S2Episode10` → Season 2, Episode 10
- `s3ep7` → Season 3, Episode 7

---

## Pattern 15: Season # Episode # Format (and variations)
**Regex:** `[Ss]eason\s+(\d+)\s+[Ee]pisode\s+(\d+)` and `[Ss]eason\s*(\d+)[\s_]+[Ee]pisode\s*(\d+)`

**Description:** Full words with spaces throughout, plus variation with optional spaces and space/underscore separator.

**Examples:**
- `Season 1 Episode 5` → Season 1, Episode 5 (all spaces)
- `Season 2 Episode 10` → Season 2, Episode 10 (all spaces)
- `Season02 Episode 20` → Season 2, Episode 20 (concatenated season)
- `Season 01_Episode 05` → Season 1, Episode 5 (underscore separator)
- `Season01_Episode05` → Season 1, Episode 5 (no spaces, underscore)
- `season 3 episode 7` → Season 3, Episode 7

---

## Pattern 16: Season#Episode# Format
**Regex:** `[Ss]eason(\d+)[Ee]pisode(\d+)`

**Description:** Full words concatenated without spaces.

**Examples:**
- `Season1Episode5` → Season 1, Episode 5
- `Season2Episode10` → Season 2, Episode 10
- `season3episode7` → Season 3, Episode 7

---

## Pattern 17: Season# Episode# Format
**Regex:** `[Ss]eason(\d+)\s+[Ee]pisode(\d+)`

**Description:** 'Season' concatenated with number, space before 'Episode'.

**Examples:**
- `Season1 Episode5` → Season 1, Episode 5
- `Season2 Episode10` → Season 2, Episode 10
- `season3 episode7` → Season 3, Episode 7

---

## Pattern 18: Season# Ep# Format
**Regex:** `[Ss]eason(\d+)\s+[Ee]p(?:isode)?(\d+)`

**Description:** 'Season' concatenated with number, space before 'Ep/Episode'.

**Examples:**
- `Season1 Ep5` → Season 1, Episode 5
- `Season2 Episode10` → Season 2, Episode 10
- `season3 ep7` → Season 3, Episode 7

---

## Pattern 19: Season#Ep# Format
**Regex:** `[Ss]eason(\d+)[Ee]p(?:isode)?(\d+)`

**Description:** Everything concatenated without spaces.

**Examples:**
- `Season1Ep5` → Season 1, Episode 5
- `Season2Episode10` → Season 2, Episode 10
- `season3ep7` → Season 3, Episode 7

---

## Pattern 19a: season## e## Format **[NEW]**
**Regex:** `[Ss]eason(\d+)\s+[Ee](\d+)`

**Description:** Lowercase 'season' concatenated with season number (no space), then space, then just 'e' (not 'ep') + episode number. **Added to fix issue with filenames like `Gintama season2 e21.srt`**.

**Examples:**
- `season2 e21` → Season 2, Episode 21 (**user-reported fix**)
- `Season3 E05` → Season 3, Episode 5
- `season1 e10` → Season 1, Episode 10

**Note:** This pattern matches BEFORE Pattern 25 (E##) to capture the season number instead of assuming Season 1.

---

## Pattern 20: Season #.Ep # Format
**Regex:** `[Ss]eason\s+(\d+)[\s\._-]*[Ee]p(?:isode)?\s*(\d+)`

**Description:** 'Season' with space, flexible separator to 'Ep/Episode'.

**Examples:**
- `Season 1.Ep 5` → Season 1, Episode 5
- `Season 2_Episode 10` → Season 2, Episode 10
- `season 3-ep 7` → Season 3, Episode 7

---

## Pattern 22: Season#.Ep# Format
**Regex:** `[Ss]eason(\d+)[\s\._-]*[Ee]p(?:isode)?(\d+)`

**Description:** 'Season' without space, flexible separator to 'Ep/Episode'.

**Examples:**
- `Season1.Ep5` → Season 1, Episode 5
- `Season2_Episode10` → Season 2, Episode 10
- `season3-ep7` → Season 3, Episode 7

---

## Pattern 22: season## e## Format **[NEW - USER FIX]**
**Regex:** `[Ss]eason(\d+)\s+[Ee](\d+)`

**Description:** Lowercase 'season' concatenated with season number (no space after 'season'), then space, then just 'e' (not 'ep') followed by episode number. **Added to fix user-reported issue** with filenames like `Gintama season2 e21.srt`. This pattern matches BEFORE Pattern 25 (E##) to capture the season number instead of assuming Season 1.

**Also Known As:** Pattern 19a in the engine (inserted after Pattern 19)

**Examples:**
- `season2 e21` → Season 2, Episode 21 (**user-reported fix** ✅)
- `Gintama season2 e21.srt` → Season 2, Episode 21
- `Season3 E05` → Season 3, Episode 5
- `season1 e10` → Season 1, Episode 10

**Note:** This pattern is different from Pattern 18 (Season# Ep#) which requires 'ep' or 'episode', not just 'e'.

---

## Pattern 23: Season # Ep # Format (REORDERED for specificity)
**Regex:** `[Ss]eason\s+(\d+)\s+[Ee]p(?:isode)?\s*(\d+)`

**Description:** Full words with consistent spacing. **Moved before Pattern 24 for better specificity** (Season keyword makes it more specific than just Ep##).

**Examples:**
- `Season 1 Ep 5` → Season 1, Episode 5
- `Season 2 Episode 10` → Season 2, Episode 10
- `season 3 ep 7` → Season 3, Episode 7

---

## Pattern 24: Ep## Format (Assumes Season 1) (REORDERED)
**Regex:** `(?:^|[._\s-])[Ee]p(?:isode)?\s*(\d+)(?=[._\s-]|$)`

**Description:** Just 'Ep' or 'Episode' with number. Assumes Season 1. **Swapped with Pattern 23** for better pattern matching order.

**Examples:**
- `Ep05` → Season 1, Episode 5
- `Episode10` → Season 1, Episode 10
- `Show.Name.ep07.mkv` → Season 1, Episode 7

**Note:** Requires word boundaries to avoid false matches.

---

## Pattern 25: E## Format (Assumes Season 1) (MOVED from Pattern 20)
**Regex:** `(?:^|[._\s-])[Ee](\d+)(?=[._\s-]|$)`

**Description:** Just episode number with 'E' prefix. Assumes Season 1. **Moved from Pattern 20 for better specificity ordering** (more generic patterns moved to end).

**Examples:**
- `E05` → Season 1, Episode 5
- `E10` → Season 1, Episode 10
- `Show.Name.E07.mkv` → Season 1, Episode 7

**Note:** Requires word boundaries to avoid false matches.

---

## Pattern 26: ## - ## Format
**Regex:** `(?<![0-9])(\d{1,2})\s*-\s*(\d{1,2})(?![a-zA-Z0-9])`

**Description:** Season and episode numbers separated by dash, no S/E prefix. Optional spaces around dash. Supports 1-99 for both season and episode.

**Examples:**
- `Show 3 - 04` → Season 3, Episode 4
- `Series 2-10` → Season 2, Episode 10
- `Example 1 - 25.mkv` → Season 1, Episode 25
- `[Moozzi2] Re Zero 3 - 04 [x265].mkv` → Season 3, Episode 4

**Note:** Uses negative lookahead/lookbehind to avoid matching years or resolution numbers.

---

## Pattern 27: - ## Format (Assumes Season 1)
**Regex:** `-\s*(?:1[0-8]\d{2}|\d{1,3})(?![a-zA-Z0-9])`

**Description:** Just a dash followed by episode number. Assumes Season 1. **Hardened** to avoid common false positives.

**Hardening Features:**
- Supports episodes 1-1899 (covers all realistic episode counts)
- Blocks years 1900+ (avoids matching `Show - 2024.mkv`)
- Blocks resolution/codec suffixes (avoids matching `Show-1080p.mkv`, `Video-x264.mkv`)
- Uses negative lookahead to prevent matching letter/number combinations

**Examples:**
- `Show - 15` → Season 1, Episode 15
- `Series - 3` → Season 1, Episode 3
- `Name - 08.mkv` → Season 1, Episode 8
- `Example - 1234` → Season 1, Episode 1234

**Won't Match (Protected):**
- `Show - 2024.mkv` ❌ (year, blocked)
- `Video-1080p.mkv` ❌ (resolution, blocked)
- `Movie-x264.mkv` ❌ (codec, blocked)

**Warning:** This is the most permissive pattern but has been hardened to reduce false positives.

---

## Pattern 28: [##] Format (Assumes Season 1)
**Regex:** `\[(\d{1,2})\](?![a-zA-Z0-9])`

**Description:** Bracket-enclosed episode number. Assumes Season 1. **Hardened** to avoid matching codec/quality tags.

**Hardening Features:**
- Supports episodes 1-99
- Blocks letter/number suffixes (prevents matching [10bit], [1080p], [x265])
- Uses negative lookahead to prevent matching [10bit], [x265], etc.

**Examples:**
- `[VCB-Studio] IS [07].mkv` → Season 1, Episode 7
- `Show.[12].720p.mkv` → Season 1, Episode 12
- `Series [5] Episode.mkv` → Season 1, Episode 5

**Won't Match (Protected):**
- `Show[10bit].mkv` ❌ (codec tag, blocked)
- `Video[1080p].mkv` ❌ (resolution tag, blocked)
- `Movie[x265].mkv` ❌ (codec tag, blocked)

---

## Pattern 29: _## Format (Assumes Season 1) - LAST PATTERN
**Regex:** `_(?:1[0-8]\d{2}|\d{1,3})(?![a-zA-Z0-9])`

**Description:** Underscore with episode number. Assumes Season 1. **Hardened** same as Pattern 26. **This is the LAST pattern** - most permissive.

**Hardening Features:**
- Supports episodes 1-1899 (same as Pattern 26)
- Blocks years 1900+ and resolution/codec suffixes
- Uses negative lookahead to prevent matching letter/number combinations

**Examples:**
- `[DB]Maoyuu_09.mkv` → Season 1, Episode 9
- `Show_15.mkv` → Season 1, Episode 15
- `Example_3.720p.mkv` → Season 1, Episode 3

**Won't Match (Protected):**
- `Video_1080p.mkv` ❌ (resolution, blocked)
- `Show_x264.mkv` ❌ (codec, blocked)

**Warning:** This is the MOST permissive pattern (last in order) but has been hardened to reduce false positives.

---

## Pattern 30: FINAL SEASON (Contextual Matching) - NOT A REGEX PATTERN
**Type:** Contextual Enhancement (not a traditional regex pattern)

**Description:** Pattern 29 is a **contextual matching enhancement** that enables season inference when the "FINAL SEASON" keyword is detected in filenames. This is NOT a regex pattern that extracts episode numbers - instead, it modifies the matching logic to infer season numbers from paired files.

**How It Works:**

When matching subtitle and video files:

1. **Case 1 - Subtitle has "FINAL SEASON":**
   - Subtitle filename contains "FINAL SEASON" keyword
   - Subtitle pattern extraction defaults to Season 1 (no explicit season)
   - Video filename has explicit season (e.g., S08)
   - **Result:** Subtitle season is inferred from video season

2. **Case 2 - Video has "FINAL SEASON":**
   - Video filename contains "FINAL SEASON" keyword
   - Video pattern extraction defaults to Season 1 (no explicit season)
   - Subtitle filename has explicit season (e.g., S08)
   - **Result:** Video season is inferred from subtitle season

**Keyword Detection:**
- Regex: `r'final[.\s_-]+season'` (case insensitive)
- Matches "FINAL SEASON", "Final.Season", "final_season", etc.
- Must be in filename only (not directory path)

**Examples:**

**Example 1 - Subtitle has FINAL SEASON:**
```
Files in folder:
- My.Hero.Academia.S08E01.Toshinori.Yagi.Rising-Origin.1080p.mkv
- [Heroacainarabic] Boku no Hero Academia FINAL SEASON - 01.ass

Processing:
1. Video extracts as: S08E01
2. Subtitle extracts as: S01E01 (defaults to S01)
3. Subtitle has "FINAL SEASON": True
4. Inference: Subtitle → S08E01 (infer S08 from video)
5. Match: S08E01 == S08E01 ✅

Result: Files matched correctly at S08E01
```

**Example 2 - Video has FINAL SEASON:**
```
Files in folder:
- My.Hero.Academia.FINAL.SEASON.E01.mkv
- Boku no Hero Academia S08E01.ass

Processing:
1. Video extracts as: S01E01 (defaults to S01)
2. Subtitle extracts as: S08E01
3. Video has "FINAL SEASON": True
4. Inference: Video → S08E01 (infer S08 from subtitle)
5. Match: S08E01 == S08E01 ✅

Result: Files matched correctly at S08E01
```

**Edge Cases:**

**Both have FINAL SEASON:**
```
- FINAL SEASON - 01.mkv → S01E01
- FINAL.SEASON.E01.ass → S01E01
Result: Both default to S01, matched at S01E01
(User needs explicit season in one file for correct inference)
```

**Both have explicit seasons:**
```
- Show.S08E01.mkv → S08E01
- Show.S08E01.ass → S08E01
Result: Normal matching (no inference needed)
```

**Neither has FINAL SEASON:**
```
- Attack.on.Titan.S04E01.mkv → S04E01
- Attack.on.Titan.S04E01.ass → S04E01
Result: Normal matching (no inference applied)
```

**Important Notes:**
- Inference only applies when detected season is 1 (the default fallback)
- Episode numbers must still match for files to pair
- This is NOT a traditional pattern - it's a matching enhancement
- Implemented in `match_subtitle_to_video()` function
- Does not modify the pattern recognition engine itself

**Use Case:**
This pattern is specifically designed for anime where the final season is released without traditional season numbering in subtitle releases, but the video files have proper season numbers (or vice versa).

---

## Key Design Features

### Pattern Priority
Patterns are evaluated in order. The **first match wins**, so more specific patterns are placed before general ones to avoid incorrect matches.

### Case Insensitivity
All patterns use `re.IGNORECASE` or explicit `[Ss]`, `[Ee]` character classes for case-insensitive matching.

### Word Boundaries
Critical patterns (like `##x##`, `E##`, `Ep##`) use lookahead/lookbehind assertions to ensure they match complete tokens, not substrings.

### Flexible Separators
Many patterns accept `[\s\._-]*` allowing dots, underscores, hyphens, or spaces as separators.

### Output Format
All patterns normalize to `S##E##` format (e.g., `S01E05` or `S2E10`) for consistent processing.
