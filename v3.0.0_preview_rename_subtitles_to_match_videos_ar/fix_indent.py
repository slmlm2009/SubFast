"""Fix indentation in embed script for try-except-finally block"""

file_path = r'C:\Users\slmlm2009\Desktop\Github\rename_subtitles_to_match_videos_ar\v3.0.0_preview_rename_subtitles_to_match_videos_ar\rename_subtitles_to_match_videos_ar\embed_subtitles_to_match_videos_ar.py'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix indentation from line 1609 to 1708 (0-indexed: 1608 to 1707)
# ALL non-empty lines in this range need 4 more spaces (to be inside try block)
fixed_lines = []
for i, line in enumerate(lines):
    lnum = i + 1
    # Lines between 1609 and 1708 need to be indented by 4 more spaces
    if 1609 <= lnum <= 1708:
        # Add 4 spaces to any line that's not already a blank line
        if line.strip():  # If line has content
            fixed_lines.append('    ' + line)
        else:
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("Fixed indentation!")
