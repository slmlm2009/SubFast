# Episode Pattern Recognition - All Supported Formats

This document lists all 26 naming patterns supported by the pattern engine, ordered by priority (first match wins).

---

## Pattern 1: S##E## Format
**Regex:** `[Ss](\d+)\s?[Ee](\d+)`

**Description:** The most common format with 'S' followed by season number, 'E' followed by episode number. Supports optional space between S## and E##.

**Examples:**
- `S01E05` → Season 1, Episode 5
- `S2E10` → Season 2, Episode 10
- `s03e15` → Season 3, Episode 15
- `S02 E3` → Season 2, Episode 3 (space-separated)
- `s3 e2` → Season 3, Episode 2 (space-separated, lowercase)
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

## Pattern 4: S## - E## Format
**Regex:** `[Ss](\d{1,2})\s*-\s*[Ee](\d+)`

**Description:** Season with dash separator to 'E' + episode number.

**Examples:**
- `S01 - E05` → Season 1, Episode 5
- `S2 - E10` → Season 2, Episode 10
- `S03-E15` → Season 3, Episode 15
- `s1 - e7` → Season 1, Episode 7

---

## Pattern 5: S## - EP## Format
**Regex:** `[Ss](\d{1,2})\s*-\s*[Ee][Pp](\d+)`

**Description:** Season with dash separator to 'EP' + episode number.

**Examples:**
- `S01 - EP05` → Season 1, Episode 5
- `S2 - EP10` → Season 2, Episode 10
- `S03-ep15` → Season 3, Episode 15
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

## Pattern 15: Season # Episode # Format
**Regex:** `[Ss]eason\s+(\d+)\s+[Ee]pisode\s+(\d+)`

**Description:** Full words with spaces throughout.

**Examples:**
- `Season 1 Episode 5` → Season 1, Episode 5
- `Season 2 Episode 10` → Season 2, Episode 10
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

## Pattern 20: E## Format (Assumes Season 1)
**Regex:** `(?:^|[._\s-])[Ee](\d+)(?=[._\s-]|$)`

**Description:** Just episode number with 'E' prefix. Assumes Season 1.

**Examples:**
- `E05` → Season 1, Episode 5
- `E10` → Season 1, Episode 10
- `Show.Name.E07.mkv` → Season 1, Episode 7

**Note:** Requires word boundaries to avoid false matches.

---

## Pattern 21: Season #.Ep # Format
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

## Pattern 23: Ep## Format (Assumes Season 1)
**Regex:** `(?:^|[._\s-])[Ee]p(?:isode)?\s*(\d+)(?=[._\s-]|$)`

**Description:** Just 'Ep' or 'Episode' with number. Assumes Season 1.

**Examples:**
- `Ep05` → Season 1, Episode 5
- `Episode10` → Season 1, Episode 10
- `Show.Name.ep07.mkv` → Season 1, Episode 7

**Note:** Requires word boundaries to avoid false matches.

---

## Pattern 24: Season # Ep # Format
**Regex:** `[Ss]eason\s+(\d+)\s+[Ee]p(?:isode)?\s*(\d+)`

**Description:** Full words with consistent spacing.

**Examples:**
- `Season 1 Ep 5` → Season 1, Episode 5
- `Season 2 Episode 10` → Season 2, Episode 10
- `season 3 ep 7` → Season 3, Episode 7

---

## Pattern 25: ## - ## Format
**Regex:** `(?<![0-9])(\d{1,2})\s*-\s*(\d{1,2})(?![a-zA-Z0-9])`

**Description:** Season and episode numbers separated by dash, no S/E prefix. Optional spaces around dash. Supports 1-99 for both season and episode.

**Examples:**
- `Show 3 - 04` → Season 3, Episode 4
- `Series 2-10` → Season 2, Episode 10
- `Example 1 - 25.mkv` → Season 1, Episode 25
- `[Moozzi2] Re Zero 3 - 04 [x265].mkv` → Season 3, Episode 4

**Note:** Uses negative lookahead/lookbehind to avoid matching years or resolution numbers.

---

## Pattern 26: - ## Format (Assumes Season 1)
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
