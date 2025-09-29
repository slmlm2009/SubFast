<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# So you have analyzed the code will. Please look at all the naming patterns it supports for both video and subtitle files and suggest a comprehensive test to test all possible scenarios. (how many scenarios as well?).

Here is a comprehensive analysis of all **naming patterns** supported by your script (for both video and subtitle files) and a recommended **test plan** that covers all possible scenarios.

***

## Supported Naming Patterns

### The script tries to extract episode information from filenames using multiple regex patterns. Based on the code and summaries, here are the main patterns supported (explicit or implicit):

#### **TV Episode Patterns (Season/Episode Logic)**

1. **S01E02 / s01e02 / S1E2**
    - e.g. `Show.Name.S01E02.mkv`
2. **2x05 / 2X05**
    - e.g. `Show.Name.2x05.srt`
3. **Season.1.Episode.05**
    - e.g. `Show.Name.Season.1.Episode.05.ass`
4. **S01.Ep.05 / S1.Ep.5**
    - e.g. `Show.Name.S01.Ep.05.srt`
5. **S01Ep05 / S1Ep05**
    - e.g. `Show.Name.S01Ep05.mkv`
6. **Season 1 Episode 5 / Season 1 Ep 5**
    - e.g. `Show.Name.Season 1 Episode 5.mkv`
7. **Season1Episode05**
    - e.g. `Show.Name.Season1Episode05.ass`
8. **Season1 Ep05 / Season1Ep05**
    - e.g. `Show.Name.Season1 Ep05.mkv`
9. **Season 1 Ep 5**
    - e.g. `Show.Name Season 1 Ep 5.mkv`
10. **Season2.Ep160 / Season2.Ep05**
    - e.g. `Show.Name.Season2.Ep160.srt`
11. **Season2Ep15 / Season2Ep5**
    - e.g. `Show.Name Season2Ep15.mkv`
12. **S4E3 / s4e3**
    - e.g. `Show.S4E3.txt`
13. **Season2 Episode2**
    - e.g. `Show Season2 Episode2.ass`

#### **Episode Only Patterns**

14. **E05, Ep05**
    - e.g. `Show.Name.E05.srt` (assumes Season 1)
15. **- 5 or -05 (dash in filename)**
    - e.g. `Show.Name - 5.srt` (assumes Season 1)

#### **Alternative/Edge Cases**

16. **Year-matching \& fuzzy matching for movies (not series)**
    - e.g. `Title.2021.mkv` and `Title.2021.srt` should be matched by year and fuzziness (Movie mode)

#### **Subtitle and Video Extensions Supported**

- **Videos:** `.mkv`, `.mp4`
- **Subtitles:** `.srt`, `.ass`

***

## Test Scenarios Breakdown

Each regex pattern above represents a distinct case. For thorough coverage, you should test:

### For each pattern:

- **Video only:** File named with that pattern, no subtitle
- **Subtitle only:** File named with that pattern, no video
- **Video and subtitle:** Both files present, same pattern
- **Mixed pattern:** Video and subtitle use different patterns for the same episode/season (tests normalization)


### Edge \& Error Cases

- **Multiple matching files with different extensions**
- **Non-matching subtitles/videos (should stay unchanged)**
- **Patterns that almost match but not quite (should NOT be matched)**
- **Movie matching (year based, no S/E logic)**
- **File with no season/episode info (should be marked unidentified)**

***

## **Comprehensive Test Suite Proposal**

### **Main Test Scenarios**

1. S\#\#E\#\# (e.g., S01E02)
2. \#x\#\# (e.g., 2x05)
3. Season.\#.Episode.\#\#
4. S\#\#.Ep.\#\#
5. S\#\#Ep\#\#
6. Season \# Episode \#
7. Season\#Episode\#\#
8. Season\# Ep\#\#
9. Season \# Ep \#
10. Season\#.Ep\#\#
11. Season\#Ep\#
12. S\#E\#
13. Season\# Episode\#
14. E\#\#/Ep\#\#
15. Dash episode (`- 5`)
16. Movie matching: Same year and fuzzy match

#### **Each scenario tested for:**

- Match video file only
- Match subtitle file only
- Match video \& subtitle (same pattern)
- Video \& subtitle with different patterns but equivalent episode/season pair
- Non-matching example
- Edge cases (multi-digit episode, extra spaces, alternate separators)


#### **Edge/Complex Additional Scenarios**

- File names with extra/common indicators: `720p`, `WEB`, `HD`, `x264`, etc.
- Multi-season, multi-episode in one folder
- Multiple videos and subtitles for the same episode (renaming collision/conflict resolution)

***

### **Total Scenario Count**

You have at least **16 base patterns**, each tested for 4 core scenarios (**video only, subtitle only, matched, mixed**) and with additional edge/error/fuzz tests.

- **Core scenarios:** 16 patterns × 4 = **64**
- **Add ~10 edge/error/fuzzy scenarios:** For mixed/non-match, collisions, etc.
- **Movie scenario:** 1 (but test with different fuzzy year-matching)

**A realistic suite is around**:
**70–80 explicit test cases** for full functional coverage and confidence.

***

## **Example Test Case Table**

| \# | Filename / Pattern | File Type | Scenario | Expected Outcome |
| :-- | :-- | :-- | :-- | :-- |
| 1 | Show.Name.S01E02.mkv | Video | Base Pattern | Recognized S01E02 |
| 2 | Show.Name.S01E02.srt | Subtitle | Base Pattern | Recognized S01E02 |
| 3 | Show.Name.2x05.mkv | Video | Alternate Pattern | Recognized S02E05 |
| ... | ... | ... | ... | ... |
| 70 | MovieTitle.2020.mp4 + .2020.srt | Video+Sub | Fuzzy movie matching by year | Succeed if close/fuzzy match |
| 71 | Show.Name.Season1Ep5.mp4 + Ep05.srt | Video+Sub | Mixed pattern, same logical pair | Recognized S01E05 |
| 72 | Show.Name - 5.ass | Subtitle | Dash separator, fallback episode | Recognized S01E05 (Season 1 assumed) |
| ... | ... | ... | ... | ... |


***

## **Conclusion**

- You should have **16+ distinct pattern scenarios**.
- **Core cases** × **video/subtitle/match/mixed** = ~64
- With **movie logic, edge, error, collision, fuzz**, add ~10–15 more
- **Full test suite:** **70–80 scenarios**.

**Running these will give you nearly complete confidence in your code’s correctness against realistic real-world filename conventions for TV episodes and movies.**
<span style="display:none">[^1]</span>

<div align="center">⁂</div>

[^1]: rename_subtitles_to_match_videos_ar.py

