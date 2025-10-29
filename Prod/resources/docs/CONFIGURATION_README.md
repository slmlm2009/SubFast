# SubFast - Configuration Guide

**SubFast - Fast subtitle renaming and embedding for all languages**

This guide provides detailed configuration options for SubFast features accessible through the unified context menu.

## Quick Start

Edit `config.ini` in the same folder as the scripts. Run either script once to auto-create it, or create it manually using the examples below.

## Settings

```ini
[General]
detected_video_extensions = mkv, mp4          # Which video files to process "embedding only works with mkv"
detected_subtitle_extensions = srt, ass       # Which subtitle files to process
keep_console_open = false                     # Keep console open until keypress (true/false)
                                               # false = smart behavior (auto-close on success, stay open on errors)
                                               # true = always wait for keypress

[Renaming]
renaming_language_suffix =                    # Language tag (ar, en, es, etc...) or empty for none
renaming_report =                             # true/false (default: true - unless invalid or empty)

[Embedding]
mkvmerge_path = bin\mkvmerge.exe              # Relative path from config.ini location, or full path
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
mkvmerge_path = bin\mkvmerge.exe
embedding_language_code = en
embedding_report = true
```
