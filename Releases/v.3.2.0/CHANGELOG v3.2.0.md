# SubFast v3.2.0 Changelog

## **SubFast v3.2.0** - Smarter. Faster. Better tested. 🚀
**Release Date:** 17-OCT-2025  
**From Version:** 3.1.0  (Internal release focusing on project directory restructure, refactoring and sub-moduleing)
**Major Focus:** Pattern recognition expansion and bug fixes + internal development comprehensive testing framework

---

## 🎯 Change Summary

Version 3.2.0 represents a major milestone in SubFast's maturity, delivering:
- **7 New Episode Patterns** - Expanded the total to 30 patterns
- **FINAL SEASON Logic** - Intelligent contextual matching for anime final seasons
- **Comprehensive Testing Infrastructure (For development)** - Complete test framework with seamless new pattern integratio
- **mkvmerge** updated to latest stable version (v.95)

---

## 🔄 Migration Notes

### From v3.0 to v3.2:

#### Just paste the `subfast` folder in in the root of C drive `C:\` and accept any file replacements

## 🚀 Major Features

### Adding 7 New Patterns + Enhancement for Existing Patterns

#### New Patterns Added:

**Pattern 23:** Season [space] Ep[space]number  
`Show Season 2 Ep 15`  

**Pattern 24:** Ep[number] (no season, defaults to S01)  
`Show Ep05` → S01E05  

**Pattern 25:** E[number] (no season, defaults to S01)  
`Show E10` → S01E10  

**Pattern 26:** [number] - [number] (season - episode, no prefix)  
`Show 2 - 15` → S02E15  

**Pattern 27:** [number]-[number] (season-episode, hyphen only)  
`Show 2-15` → S02E15  

**Pattern 28:** [square brackets][number][square brackets]  
`Show [15]` → S01E15  

**Pattern 29:** Underscore [number] (episode only, defaults to S01)  
`Show_09` → S01E09  


**Note: Patterns 24-29 are all low priority and only considered of there are no other matches before them**

---

### Supporting FINAL SEASON Contextual Matching ⭐ NEW
**Intelligent season inference for anime final seasons**

#### Problem Solved:
Anime final seasons often released with "FINAL SEASON" in filename but no season number:
```
Subtitle: Boku no Hero Academia FINAL SEASON - 01.ass  (defaults to S01E01)
Video:    My.Hero.Academia.S08E01.mkv                   (actual S08E01)
Result:   NO MATCH ❌ (S01 ≠ S08)
```

#### Solution - Pattern 30:
**Contextual matching with bidirectional season inference**

```
Subtitle: Boku no Hero Academia FINAL SEASON - 01.ass  (inferred from subtitle file S08E01)
Video:    My.Hero.Academia.S08E01.mkv                   (actual S08E01)
Result:   MATCH ✅
```


#### Bug Fixed and other Enhancements:
**Movie Mode Activation Bug**
- **Issue:** Movie mode activating incorrectly with multiple episode files
- **Fix:** Changed condition to check total files (not remaining)

#### Pattern - {XX} Hardening:
**Enhanced to support OnePiece-style long episode numbers (1000+)**

Pattern 25 now excludes:
- Years (1900-2099) to prevent false matches
- Resolution patterns (720p, 1080p, etc.)
- Codec patterns (x264, x265, AV1, etc.)

```python
# Enhanced regex with negative lookbehind
r'(?<!(?:19|20)\d{2})[\s._-](?P<episode>\d{3,})(?!p)(?!\s*(?:x264|x265|AV1|AAC))'
```

#### Existing Patterns Enhancements:
- **Pattern 1 (S[#]E[#]):** Added VAR4-VAR6 with flexible separators
- **Pattern 4 (S[#]-E[#]):** Added VAR4-VAR5 with underscore separator
- **Pattern 5 (S[#]-EP[#]):** Added VAR4-VAR6 with space variations

#### Pattern Reordering:
**Old Order:** Old original ID assignment (20, 21, 22...)  
**New Order:** By specificity (high to low)

**Reordering Rationale:**
- **High Specificity First:** Patterns with unique markers processed first
- **Prevent False Matches:** More specific patterns capture intent before generic ones


#### Pattern Hardening:
Applied to Patterns 26, 27, 28:
- Episode number range validation (1-9999)
- Season number validation (1-99)
- Prevents year/resolution false matches
