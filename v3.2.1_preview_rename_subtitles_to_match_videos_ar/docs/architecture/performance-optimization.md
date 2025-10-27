# Performance Optimization

## Current Performance Metrics

**Renaming Performance:**
- **1000 files in <1 second** (v2.5.0 achievement)
- Episode number caching: 12x performance improvement over v2.0.0
- Regex compilation: Done once at startup
- CSV export disabled: +14% speed on large datasets

**Embedding Performance:**
- **Bottleneck:** mkvmerge execution time (seconds to minutes per file)
- **Disk I/O:** SSD significantly faster than HDD (10x+ improvement)
- **Parallelization:** Not implemented (risk of disk I/O contention)

## Optimization Strategies

### 1. Regex Compilation (Renaming)

**Implementation:**
```python
# At script startup (done once)
COMPILED_PATTERNS = [
    ('S##E##', re.compile(r'S(\d{1,2})E(\d{1,3})', re.IGNORECASE)),
    ('##x##', re.compile(r'(\d{1,2})x(\d{1,3})', re.IGNORECASE)),
    # ... all 25+ patterns
]

# Per-file (fast lookup)
for pattern_name, pattern in COMPILED_PATTERNS:
    match = pattern.search(filename)
    if match:
        return normalize_episode(match)
```

**Benefit:** Avoids recompiling regex for each filename (1000x reduction in regex compile time)

---

### 2. Episode Number Caching (Renaming)

**Implementation:**
```python
# Build cache: O(n) scan of all files
video_cache = {
    (season, episode): video_file 
    for video_file in videos 
    if video_file.episode_info
}

# Lookup: O(1) for each subtitle
for subtitle in subtitles:
    if subtitle.episode_info:
        season, episode = subtitle.episode_info
        matched_video = video_cache.get((season, episode))
```

**Benefit:** O(1) lookup instead of O(n) linear search per subtitle (12x speedup on 1000 files)

---

### 3. CSV Export Optionality (Both Scripts)

**Configuration:**
```ini
[Renaming]
renaming_report = false  # Disable for 14% speed gain

[Embedding]
embedding_report = false  # Minimal impact (embedding is I/O bound)
```

**Benefit:** Eliminates CSV file I/O overhead for speed-critical scenarios

---

### 4. Disk Space Pre-Check (Embedding)

**Implementation:**
```python
# Check once before processing
total_required = sum(video.size + subtitle.size for pair in matched_pairs)
available = shutil.disk_usage(base_path).free

if available < total_required * 1.1:  # 10% buffer
    console_error(f"Insufficient space: Need {total_required}, have {available}")
    sys.exit(2)
```

**Benefit:** Fails fast instead of mid-batch; prevents disk full errors during processing

---

### 5. Memory Efficiency (Both Scripts)

**Sequential Processing:**
```python
# Good: Process files one at a time
for matched_pair in matched_pairs:
    result = process_file(matched_pair)
    results.append(result)

# Bad: Load all file contents in memory
file_contents = [open(f).read() for f in all_files]  # Memory bloat!
```

**Benefit:** Constant memory usage regardless of batch size (42% memory reduction in v2.5.0)

---

## Performance Testing

**Benchmark Setup:**
```bash
# Create test dataset
python generate_test_files.py --count 1000 --mode mixed

# Benchmark renaming
time py scripts\subfast_rename.py "C:\test_dataset"

# Benchmark embedding (smaller dataset due to time)
time py scripts\subfast_embed.py "C:\test_dataset_small"
```

**Key Metrics:**
- Total execution time
- Files processed per second
- Memory usage (via Windows Task Manager)
- CSV generation overhead (enabled vs disabled)

---
