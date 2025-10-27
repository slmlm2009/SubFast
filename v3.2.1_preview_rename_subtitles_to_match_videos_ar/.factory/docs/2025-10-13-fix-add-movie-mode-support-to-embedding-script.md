# Fix: Add Movie Mode Support to Embedding Script

## Problem Analysis

The refactored v3.1.0 embedding script is **missing movie mode functionality** that was present in v3.0.0. When processing a folder with a single movie file and single subtitle file (no episode patterns), the script:

1. ❌ Tries to match the subtitle based on episode pattern
2. ❌ Finds no episode pattern → marks as "no_match"
3. ❌ Aborts without attempting movie mode matching
4. ❌ Never embeds the subtitle even though it's the only pair

**v3.0.0 behavior (correct):**
- After episode matching completes
- If NO matches found AND exactly 1 video + 1 subtitle exist
- Activates movie mode (word overlap + year matching)
- Successfully embeds the pair

---

## Root Cause

The refactored script **completely removed** the movie mode matching logic:
- Missing: `match_movie_files()` function
- Missing: `extract_base_name()` helper
- Missing: Movie matching constants (`YEAR_PATTERN`, `COMMON_INDICATORS`, `BASE_NAME_CLEANUP`)
- Missing: Fallback logic to try movie mode after episode matching fails

---

## Solution Overview

Add movie mode support back to the refactored script while maintaining the clean v3.1.0 architecture.

---

## Implementation Plan

### **1. Add Movie Matching Constants** (Top of file, after imports)

**Location:** `subfast_embed.py` - After imports, before functions

**Add these constants from v3.0.0:**

```python
# Movie mode matching patterns and helpers
YEAR_PATTERN = re.compile(r'(?:19|20)\d{2}')
BASE_NAME_CLEANUP = re.compile(r'[._\-]+')

COMMON_INDICATORS = {
    '1080p', '720p', '480p', '2160p', '4k', 'bluray', 'web', 'dvd', 'hd', 'x264', 'x265',
    'h264', 'h265', 'avc', 'hevc', 'aac', 'ac3', 'dts', 'remux', 'proper', 'repack',
    'extended', 'theatrical', 'unrated', 'directors', 'cut', 'multi', 'sub', 'eng', 'en',
    'ara', 'ar', 'eng', 'fre', 'fr', 'ger', 'de', 'ita', 'es', 'spa', 'kor', 'jpn', 'ch',
    'chs', 'cht', 'internal', 'limited', 'xvid', 'divx', 'ntsc', 'pal', 'dc',
    'sync', 'syncopated', 'cc', 'sdh', 'hc', 'final', 'post', 'pre',
    'dub', 'dubbed'
}
```

---

### **2. Add Helper Functions**

**Location:** Before `build_episode_context()` function

#### **Function 1: `extract_base_name()`**

```python
def extract_base_name(filename):
    """
    Extract and clean base filename for movie comparison.
    Converts separators (., _, -) to spaces.
    
    Args:
        filename: The filename to process
        
    Returns:
        Cleaned base name with spaces
    """
    from pathlib import Path
    base_name = Path(filename).stem
    base_name = BASE_NAME_CLEANUP.sub(' ', base_name)
    return base_name.strip()
```

#### **Function 2: `match_movie_files()`**

```python
def match_movie_files(video_files, subtitle_files):
    """
    Match single movie file with single subtitle file based on title similarity.
    
    Uses two matching strategies:
    1. Year matching: If both files contain the same 4-digit year
    2. Word overlap: Compares common words after removing quality indicators
    
    Args:
        video_files: List of video Path objects
        subtitle_files: List of subtitle Path objects
        
    Returns:
        Tuple of (video_file, subtitle_file) if match found, None otherwise
    """
    if len(video_files) != 1 or len(subtitle_files) != 1:
        return None
    
    video_name = extract_base_name(video_files[0].name)
    subtitle_name = extract_base_name(subtitle_files[0].name)
    
    video_year_match = YEAR_PATTERN.search(video_files[0].name)
    subtitle_year_match = YEAR_PATTERN.search(subtitle_files[0].name)
    
    video_year = video_year_match.group() if video_year_match else None
    subtitle_year = subtitle_year_match.group() if subtitle_year_match else None
    
    video_words = set(video_name.lower().split()) - COMMON_INDICATORS
    subtitle_words = set(subtitle_name.lower().split()) - COMMON_INDICATORS
    
    common_words = video_words.intersection(subtitle_words)
    years_match = (video_year and subtitle_year and video_year == subtitle_year)
    
    if years_match:
        if len(common_words) > 0:
            return (video_files[0], subtitle_files[0])
    else:
        if len(video_words) > 0 and len(subtitle_words) > 0:
            match_ratio = len(common_words) / min(len(video_words), len(subtitle_words))
            if match_ratio >= 0.3 or len(common_words) > 0:
                return (video_files[0], subtitle_files[0])
    
    return None
```

---

### **3. Modify `process_embedding()` Function**

**Current logic:**
```python
for subtitle_file in sorted(all_subtitle_files):
    # Try episode matching
    if target_video_name:
        # Embed
    else:
        # Mark as no_match
```

**New logic with movie mode fallback:**

Add this **AFTER** the main subtitle processing loop (after the for loop ends):

```python
    # Movie mode fallback - try if no embeddings succeeded
    if embedded_count == 0 and len(mkv_videos) == 1 and len(all_subtitle_files) == 1:
        print("\n" + "=" * 60)
        print("MOVIE MODE: Attempting title-based matching...")
        print("=" * 60)
        
        movie_match = match_movie_files(mkv_videos, all_subtitle_files)
        
        if movie_match:
            video_file, subtitle_file = movie_match
            
            print(f"\n[MOVIE MODE] Matched: '{video_file.name}' + '{subtitle_file.name}'")
            
            # Detect language
            language_code = detect_language_with_fallback(
                subtitle_file.name,
                config.get('embedding_language_code')
            )
            
            print(f"\nEMBEDDING: '{subtitle_file.name}' into '{video_file.name}'")
            if language_code:
                lang_name = LANGUAGE_DATA.get('codes', {}).get(language_code, {}).get('name', language_code)
                print(f"  Language: {lang_name} ({language_code})")
            else:
                print(f"  Language: (none detected)")
            
            # Embed subtitle
            success, error, backups_dir = embed_subtitle(
                video_file,
                subtitle_file,
                mkvmerge_path,
                language_code,
                config.get('default_flag', True),
                backups_dir,
                config
            )
            
            if success:
                print(f"  ✓ SUCCESS")
                embedded_count += 1
                
                # Update results - replace the 'no_match' entry with success
                results = [r for r in results if r.get('subtitle') != subtitle_file.name]
                results.append({
                    'subtitle': subtitle_file.name,
                    'video': video_file.name,
                    'episode': 'Movie',
                    'language': language_code or 'N/A',
                    'status': 'success'
                })
            else:
                print(f"  ✗ FAILED: {error}")
                failed_count += 1
                
                # Update results - replace the 'no_match' entry with failed
                results = [r for r in results if r.get('subtitle') != subtitle_file.name]
                results.append({
                    'subtitle': subtitle_file.name,
                    'video': video_file.name,
                    'episode': 'Movie',
                    'language': language_code or 'N/A',
                    'status': 'failed',
                    'error': error
                })
        else:
            print("\n[MOVIE MODE] No match found - files are too dissimilar")
```

**Integration point:** Add this block immediately before the final `print("\n" + "=" * 60)` summary line.

---

### **4. Update Summary Display**

The existing summary will automatically reflect the movie mode embedding because we update the `embedded_count` and `failed_count` counters.

No changes needed to the final summary print statements.

---

## Expected Behavior After Fix

### **Scenario 1: Single Movie + Single Subtitle (No Episode Patterns)**

**Before (broken):**
```
FILES FOUND: 1 MKV videos | 1 subtitles
==============================================================

PROCESSING EMBEDDINGS:
----------------------------------------

NO MATCH: 'Movie.2023.srt' -> episode (undetected)

==============================================================
COMPLETED: 0 embedded | 0 failed | 1 unmatched
==============================================================
```

**After (fixed):**
```
FILES FOUND: 1 MKV videos | 1 subtitles
==============================================================

PROCESSING EMBEDDINGS:
----------------------------------------

NO MATCH: 'Movie.2023.srt' -> episode (undetected)

==============================================================
MOVIE MODE: Attempting title-based matching...
==============================================================

[MOVIE MODE] Matched: 'Movie.2023.1080p.mkv' + 'Movie.2023.srt'

EMBEDDING: 'Movie.2023.srt' into 'Movie.2023.1080p.mkv'
  Language: (none detected)
  ✓ SUCCESS

==============================================================
COMPLETED: 1 embedded | 0 failed | 0 unmatched
==============================================================
```

---

### **Scenario 2: TV Show Episodes (Episode Patterns Present)**

**Behavior:** Movie mode is **NOT** activated, episode matching works as normal
```
FILES FOUND: 3 MKV videos | 3 subtitles
==============================================================

PROCESSING EMBEDDINGS:
----------------------------------------

EMBEDDING: 'Show.S01E01.srt' into 'Show.S01E01.mkv'
  ✓ SUCCESS

EMBEDDING: 'Show.S01E02.srt' into 'Show.S01E02.mkv'
  ✓ SUCCESS

EMBEDDING: 'Show.S01E03.srt' into 'Show.S01E03.mkv'
  ✓ SUCCESS

==============================================================
COMPLETED: 3 embedded | 0 failed | 0 unmatched
==============================================================
```

---

### **Scenario 3: Multiple Movies (Movie Mode Not Applicable)**

**Behavior:** Movie mode only works with exactly 1 video + 1 subtitle
```
FILES FOUND: 3 MKV videos | 2 subtitles
==============================================================

PROCESSING EMBEDDINGS:
----------------------------------------

NO MATCH: 'Movie1.srt' -> episode (undetected)
NO MATCH: 'Movie2.srt' -> episode (undetected)

==============================================================
COMPLETED: 0 embedded | 0 failed | 2 unmatched
==============================================================

(Movie mode not attempted - requires exactly 1 video + 1 subtitle)
```

---

## Movie Matching Algorithm

**Step 1: Year Matching (Higher Priority)**
- Extract 4-digit year from both filenames using `YEAR_PATTERN`
- If both have same year AND have at least 1 common word → MATCH

**Step 2: Word Overlap (Fallback)**
- Clean filenames: convert separators to spaces, remove quality indicators
- Calculate word overlap ratio
- If ratio ≥ 0.3 OR any common words exist → MATCH

**Examples:**

| Video | Subtitle | Match? | Reason |
|-------|----------|--------|--------|
| `The.Matrix.1999.1080p.mkv` | `The.Matrix.1999.srt` | ✅ YES | Same year (1999) + common words ("matrix") |
| `Inception.2010.BluRay.mkv` | `Inception.srt` | ✅ YES | Common word "inception" |
| `Avatar.2009.mkv` | `Titanic.1997.srt` | ❌ NO | Different years, no common words |
| `Movie.mkv` | `Film.srt` | ❌ NO | No common words, no years |

---

## Files Modified

1. **`subfast/scripts/subfast_embed.py`**
   - Add movie matching constants (3 items: YEAR_PATTERN, BASE_NAME_CLEANUP, COMMON_INDICATORS)
   - Add `extract_base_name()` helper function
   - Add `match_movie_files()` function
   - Add movie mode fallback logic in `process_embedding()`

---

## Testing Strategy

### **Test 1: Single Movie File**
```
Directory:
  - The.Matrix.1999.1080p.mkv
  - The.Matrix.1999.srt

Expected: Movie mode activates, subtitle successfully embedded
```

### **Test 2: TV Show (No Regression)**
```
Directory:
  - Show.S01E01.mkv
  - Show.S01E01.srt
  - Show.S01E02.mkv
  - Show.S01E02.srt

Expected: Episode mode works as normal, movie mode not triggered
```

### **Test 3: Dissimilar Movie Names**
```
Directory:
  - Avatar.2009.mkv
  - Titanic.1997.srt

Expected: Movie mode attempts but finds no match
```

---

## Benefits

1. **✅ Feature Parity:** Restores v3.0.0 movie mode functionality
2. **✅ No Breaking Changes:** TV show embedding continues to work exactly as before
3. **✅ Smart Fallback:** Only activates when episode matching produces no results
4. **✅ User-Friendly:** Clear console messages indicate when movie mode is active
5. **✅ Accurate Reporting:** Results correctly show 'Movie' as episode for movie files

---

## Validation Checklist

- [ ] Movie mode constants added (YEAR_PATTERN, COMMON_INDICATORS, BASE_NAME_CLEANUP)
- [ ] `extract_base_name()` function added
- [ ] `match_movie_files()` function added
- [ ] Movie mode fallback logic added to `process_embedding()`
- [ ] Movie mode only activates when exactly 1 video + 1 subtitle with 0 embeddings
- [ ] Results properly updated when movie mode succeeds/fails
- [ ] Console messages clearly indicate movie mode activation
- [ ] Test with single movie file succeeds
- [ ] Test with TV show episodes (no regression)
- [ ] Test with multiple movies (movie mode not triggered)