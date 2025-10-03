# Configuration System

### Customization

**Edit `config.ini` to customize behavior:**

```ini
[General]
enable_export = false          # Disable CSV report (14% faster)
language_suffix = en           # Use .en instead of .ar

[FileFormats]
video_extensions = mkv, mp4, avi, webm			# Adding .avi and .webm support in addition to default .mkv, .mp4
subtitle_extensions = srt, ass, ssa, sub	    # Adding .sub and .ssa support in addition to default .srt, .ass
```

**Re-run the script** - it will use your custom settings!

---

## Configuration Options

### Language Suffix
**What it does:** Sets the language tag added before file extension

**Default:** `ar` (Arabic)

**Examples:**
```ini
language_suffix = ar     # Show.S01E05.ar.srt
language_suffix = en     # Show.S01E05.en.srt
language_suffix = es     # Show.S01E05.es.srt
language_suffix =        # Show.S01E05.srt
```

**Constraints:**
- 1-10 characters
- Letters, numbers, hyphens, underscores only
- No dots (use `ar` not `.ar`)

### CSV Export Control
**What it does:** Enables/disables `renaming_report.csv` generation

**Default:** `true` (enabled)

**Values:** `true`, `false`, `yes`, `no`, `1`, `0`, `on`, `off`

**Performance:**
- Enabled: Full analysis report created
- Disabled: 14% faster execution (skips report)

### Video Extensions
**What it does:** Defines which video file types to process

**Default:** `mkv, mp4`

**Common formats:**
```ini
video_extensions = mkv, mp4                      # Default
video_extensions = mkv, mp4, avi, webm           # Add more formats
video_extensions = mkv, mp4, avi, mov, flv, m4v  # Maximum support
```

**Notes:**
- Comma-separated
- Case-insensitive (MKV = mkv)
- Dots optional (.mkv = mkv)

### Subtitle Extensions
**What it does:** Defines which subtitle file types to process

**Default:** `srt, ass`

**Common formats:**
```ini
subtitle_extensions = srt, ass                      # Default
subtitle_extensions = srt, ass, ssa, sub            # Add more formats
subtitle_extensions = srt, ass, ssa, sub, vtt, smi 	# Maximum support
```

---

## Example Use Cases

### Use Case 1: Arabic Subtitles
```ini
[General]
enable_export = true
language_suffix = ar

[FileFormats]
video_extensions = mkv, mp4
subtitle_extensions = srt
```

### Use Case 2: Batch Processing (Speed Priority)
```ini
[General]
enable_export = false          # Skip CSV for speed
language_suffix = ar
video_extensions = mkv, mp4
subtitle_extensions = srt, ass
```

### Use Case 3: Maximum Format Support
```ini
[General]
enable_export = true
language_suffix = ar
video_extensions = mkv, mp4, avi, webm, mov, flv, m4v
subtitle_extensions = srt, ass, sub, vtt, ssa, smi
```

---

## Error Handling

### Scenario: Missing config.ini
**Behavior:**
```
[INFO] config.ini not found - creating default configuration
Created default config.ini at: /path/to/script/config.ini
Edit this file to customize script behavior.
```
→ Creates default config, continues with defaults

### Scenario: Invalid Language Suffix
**Behavior:**
```
[WARNING] Invalid language_suffix: '???' (invalid characters)
[INFO] Using no suffix: 'none'
Valid characters: letters, numbers, hyphens, underscores only
```
→ Uses 'none', script continues

### Scenario: No Valid Extensions
**Behavior:**
```
[WARNING] No valid video extensions - using defaults: mkv, mp4
```
→ Falls back to defaults, script continues

### Scenario: Corrupted config.ini
**Behavior:**
```
[WARNING] Failed to parse config.ini: [error details]
[INFO] Using default configuration
```
→ Uses defaults, script continues

**All error scenarios allow the script to continue with safe defaults.**
