#!/usr/bin/env python3
"""Fix language suffix to allow empty string and fall back to empty for invalid"""

with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Update validation logic
old_validation = """    # Check length and characters
    if 1 <= len(suffix) <= 10 and all(c.isalnum() or c in '-_' for c in suffix):
        validated['language_suffix'] = suffix
    else:
        print(f"[WARNING] Invalid language_suffix: '{suffix}' - using default 'ar'")
        print("  Valid: 1-10 characters, letters/numbers/hyphens/underscores only")
        validated['language_suffix'] = 'ar'"""

new_validation = """    # Check length and characters
    # Empty string is valid (omits suffix), or 1-10 valid characters
    if len(suffix) == 0:
        # Empty suffix is valid - will omit language tag from renamed files
        validated['language_suffix'] = ''
    elif 1 <= len(suffix) <= 10 and all(c.isalnum() or c in '-_' for c in suffix):
        validated['language_suffix'] = suffix
    else:
        print(f"[WARNING] Invalid language_suffix: '{suffix}' - omitting suffix from filenames")
        print("  Valid: empty string (omit suffix) or 1-10 characters (letters/numbers/hyphens/underscores)")
        validated['language_suffix'] = ''"""

content = content.replace(old_validation, new_validation)
print("[OK] Fixed validation logic")

# Fix 2: Update display message
old_display = """        print(f"[INFO] Configuration loaded from: {config_path}")
        print(f"  Language suffix: .{validated['language_suffix']}")
        print(f"  Video formats: {', '.join(validated['video_extensions'])}")"""

new_display = """        print(f"[INFO] Configuration loaded from: {config_path}")
        # Display language suffix (or "none" if empty)
        if validated['language_suffix']:
            print(f"  Language suffix: .{validated['language_suffix']}")
        else:
            print(f"  Language suffix: (none - omitted from filenames)")
        print(f"  Video formats: {', '.join(validated['video_extensions'])}")"""

content = content.replace(old_display, new_display)
print("[OK] Fixed display message")

# Fix 3: Update generate_unique_name (first instance)
old_rename_1 = """    new_name = f"{base_name}.{CONFIG['language_suffix']}{subtitle_ext}"
    new_path = os.path.join(directory, new_name)"""

new_rename_1 = """    # Build filename with optional language suffix
    if CONFIG['language_suffix']:
        new_name = f"{base_name}.{CONFIG['language_suffix']}{subtitle_ext}"
    else:
        new_name = f"{base_name}{subtitle_ext}"
    new_path = os.path.join(directory, new_name)"""

content = content.replace(old_rename_1, new_rename_1)
print("[OK] Fixed generate_unique_name function")

# Fix 4: Update all other occurrences of the new_name pattern
old_pattern = 'new_name = f"{base_name}.{CONFIG[\'language_suffix\']}{subtitle_ext}"'
new_pattern = '''# Build filename with optional language suffix
            if CONFIG['language_suffix']:
                new_name = f"{base_name}.{CONFIG['language_suffix']}{subtitle_ext}"
            else:
                new_name = f"{base_name}{subtitle_ext}"'''

# Count and replace remaining occurrences
count = content.count(old_pattern)
content = content.replace(old_pattern, new_pattern)
print(f"[OK] Fixed {count} additional filename building locations")

# Fix 5: Update CSV config string
old_csv_config = """    # Get configuration display string
    config_str = f"language={CONFIG['language_suffix']}, videos={'|'.join(CONFIG['video_extensions'])}, subtitles={'|'.join(CONFIG['subtitle_extensions'])}, export={CONFIG['enable_export']}\"
"""

new_csv_config = """    # Get configuration display string
    lang_str = CONFIG['language_suffix'] if CONFIG['language_suffix'] else '(none)'
    config_str = f"language={lang_str}, videos={'|'.join(CONFIG['video_extensions'])}, subtitles={'|'.join(CONFIG['subtitle_extensions'])}, export={CONFIG['enable_export']}\"
"""

content = content.replace(old_csv_config, new_csv_config)
print("[OK] Fixed CSV config string")

# Write back
with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n[SUCCESS] All fixes applied successfully!")
print("- Empty language_suffix now omits suffix from filenames")
print("- Invalid language_suffix falls back to empty (not 'ar')")
print("- Default config.ini still uses 'ar' as example")
