#!/usr/bin/env python3
"""Fix language suffix to allow empty string and fall back to empty for invalid"""

with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

changes_made = []

# Fix 1: Update validation logic (around line 127-139)
for i in range(len(lines)):
    if "    # Check length and characters" in lines[i]:
        # Found the validation section
        if i + 6 < len(lines) and "validated['language_suffix'] = 'ar'" in lines[i + 6]:
            # Replace the validation logic
            lines[i] = "    # Check length and characters\n"
            lines[i + 1] = "    # Empty string is valid (omits suffix), or 1-10 valid characters\n"
            lines[i + 2] = "    if len(suffix) == 0:\n"
            lines[i + 3] = "        # Empty suffix is valid - will omit language tag from renamed files\n"
            lines[i + 4] = "        validated['language_suffix'] = ''\n"
            lines[i + 5] = "    elif 1 <= len(suffix) <= 10 and all(c.isalnum() or c in '-_' for c in suffix):\n"
            lines[i + 6] = "        validated['language_suffix'] = suffix\n"
            lines[i + 7] = "    else:\n"
            lines[i + 8] = "        print(f\"[WARNING] Invalid language_suffix: '{suffix}' - omitting suffix from filenames\")\n"
            lines[i + 9] = "        print(\"  Valid: empty string (omit suffix) or 1-10 characters (letters/numbers/hyphens/underscores)\")\n"
            lines[i + 10] = "        validated['language_suffix'] = ''\n"
            changes_made.append("Fixed validation logic")
            break

# Fix 2: Update display message (around line 199)
for i in range(len(lines)):
    if '        print(f"  Language suffix: .{validated[' in lines[i]:
        # Replace with conditional display
        lines[i] = "        # Display language suffix (or \"none\" if empty)\n"
        lines.insert(i + 1, "        if validated['language_suffix']:\n")
        lines.insert(i + 2, "            print(f\"  Language suffix: .{validated['language_suffix']}\")\n")
        lines.insert(i + 3, "        else:\n")
        lines.insert(i + 4, "            print(f\"  Language suffix: (none - omitted from filenames)\")\n")
        changes_made.append("Fixed display message")
        break

# Fix 3: Update generate_unique_name function (around line 398)
for i in range(len(lines)):
    if '    new_name = f"{base_name}.{CONFIG[\'language_suffix\']}{subtitle_ext}"\n' == lines[i]:
        if i > 0 and 'def generate_unique_name' in ''.join(lines[max(0, i-20):i]):
            # This is in generate_unique_name function
            lines[i] = "    # Build filename with optional language suffix\n"
            lines.insert(i + 1, "    if CONFIG['language_suffix']:\n")
            lines.insert(i + 2, "        new_name = f\"{base_name}.{CONFIG['language_suffix']}{subtitle_ext}\"\n")
            lines.insert(i + 3, "    else:\n")
            lines.insert(i + 4, "        new_name = f\"{base_name}{subtitle_ext}\"\n")
            changes_made.append("Fixed generate_unique_name function")
            break

# Fix 4: Update CSV config string (around line 842)
for i in range(len(lines)):
    if '    config_str = f"language={CONFIG[\'language_suffix\']}, videos=' in lines[i]:
        # Insert lang_str line before config_str
        lines.insert(i, "    lang_str = CONFIG['language_suffix'] if CONFIG['language_suffix'] else '(none)'\n")
        # Update the config_str line
        lines[i + 1] = lines[i + 1].replace("language={CONFIG['language_suffix']}", "language={lang_str}")
        changes_made.append("Fixed CSV config string")
        break

# Fix 5: Update all remaining filename building locations (careful with indentation)
replacements_made = 0
for i in range(len(lines)):
    # Look for the pattern with proper context
    if '            new_name = f"{base_name}.{CONFIG[\'language_suffix\']}{subtitle_ext}"\n' == lines[i]:
        # Check if this is in a context that needs fixing (not already fixed)
        if i > 0 and '# Build filename with optional language suffix' not in lines[i-1]:
            # Replace this single line with conditional block
            indent = "            "  # 12 spaces
            lines[i] = f"{indent}# Build filename with optional language suffix\n"
            lines.insert(i + 1, f"{indent}if CONFIG['language_suffix']:\n")
            lines.insert(i + 2, f"{indent}    new_name = f\"{{base_name}}.{{CONFIG['language_suffix']}}{{subtitle_ext}}\"\n")
            lines.insert(i + 3, f"{indent}else:\n")
            lines.insert(i + 4, f"{indent}    new_name = f\"{{base_name}}{{subtitle_ext}}\"\n")
            replacements_made += 1

if replacements_made > 0:
    changes_made.append(f"Fixed {replacements_made} additional filename building locations")

# Write back
with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("[SUCCESS] All fixes applied successfully!")
for change in changes_made:
    print(f"  - {change}")
print("\nKey changes:")
print("- Empty language_suffix now omits suffix from filenames")
print("- Invalid language_suffix falls back to empty (not 'ar')")
print("- Default config.ini still uses 'ar' as example")
