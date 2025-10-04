# SubFast - Configuration Guide

**SubFast - Fast subtitle renaming and embedding for all languages**

Edit `config.ini` in the same folder as the scripts. Run either script once to auto-create it.

## Settings

```ini
[General]
detected_video_extensions = mkv, mp4          # Which video files to process "embedding only works with mkv"
detected_subtitle_extensions = srt, ass       # Which subtitle files to process

[Renaming]
renaming_language_suffix =                    # Language tag (ar, en, es) or empty for none
renaming_report =                             # true/false (default: true - unless invalid or empty)

[Embedding]
mkvmerge_path =                               # Full path or empty if in script folder
embedding_language_code =                     # Language code or empty to auto-detect
default_flag =                                # Mark embedded subtitle as default (true/false) - default: true
embedding_report =                            # true/false (default: true - unless invalid or empty)
```

## Examples

**English with reports:**
```ini
[Renaming]
renaming_language_suffix = en
renaming_report = true

[Embedding]
embedding_language_code = en
embedding_report = true
```

**More file types:**
```ini
[General]
detected_video_extensions = mkv, mp4, avi, webm
detected_subtitle_extensions = srt, ass, sub, ssa
```

---
