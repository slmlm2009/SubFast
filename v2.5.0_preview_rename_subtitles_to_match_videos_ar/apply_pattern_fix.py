#!/usr/bin/env python3
"""Apply pattern ordering fix"""

# Read file
with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the line numbers
start_idx = None
ordinal_start = None
ordinal_end = None
end_idx = None

for i, line in enumerate(lines):
    if '# NEW: S## - EP## format' in line:
        start_idx = i
    if '# NEW: Ordinal Season patterns' in line:
        ordinal_start = i
    if ordinal_start and 'Pattern: 3rd Season EP8' in line:
        # Find the closing of this pattern
        for j in range(i, min(i+5, len(lines))):
            if '),' in lines[j]:
                ordinal_end = j
                break
    if '# Pre-compiled utility regex patterns' in line:
        end_idx = i
        break

if not all([start_idx, ordinal_start, ordinal_end, end_idx]):
    print(f"ERROR: Could not find markers: start={start_idx}, ordinal_start={ordinal_start}, ordinal_end={ordinal_end}, end={end_idx}")
    exit(1)

# Extract ordinal patterns
ordinal_patterns = lines[ordinal_start:ordinal_end+1]

# Build new pattern list
new_lines = []
new_lines.extend(lines[:start_idx+2])  # Up to and including S## - EP## pattern closing

# Add ordinal patterns (moved here)
new_lines.append('    # NEW: Ordinal Season patterns (MOVED HERE - must come BEFORE general E##/EP## patterns)\n')
new_lines.append('    # Pattern: 2nd Season EP8 → S02E08 (most specific first)\n')
new_lines.append('    (re.compile(r\'(\\d{1,2})(?:st|nd|rd|th)\\s+[Ss]eason\\s+[Ee][Pp]\\s*(\\d+)\', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),\n')
new_lines.append('    # Pattern: 2nd Season E10 or 2nd Season Episode 10 → S02E10\n')
new_lines.append('    (re.compile(r\'(\\d{1,2})(?:st|nd|rd|th)\\s+[Ss]eason\\s+[Ee](?:pisode)?\\s*(\\d+)\', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),\n')
new_lines.append('    # Pattern: 1st Season - 05 → S01E05\n')
new_lines.append('    (re.compile(r\'(\\d{1,2})(?:st|nd|rd|th)\\s+[Ss]eason\\s*-\\s*(\\d+)\', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),\n')

# Add new Season ## - ## patterns
new_lines.append('    # NEW: Season ## - ## patterns (CRITICAL - must come BEFORE general patterns)\n')
new_lines.append('    # Pattern: Season 2 - 23 → S02E23 (with space before number)\n')
new_lines.append('    (re.compile(r\'[Ss]eason\\s+(\\d{1,2})\\s*-\\s*(\\d+)\', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),\n')
new_lines.append('    # Pattern: Season12 - 103 → S12E103 (without space before number)\n')
new_lines.append('    (re.compile(r\'[Ss]eason(\\d{1,2})\\s*-\\s*(\\d+)\', re.IGNORECASE), lambda m: (m.group(1).zfill(2), m.group(2))),\n')

# Add remaining patterns (skip ordinal section)
# Find the next pattern after the S## - EP## pattern
next_pattern_idx = start_idx + 2
while next_pattern_idx < ordinal_start and not lines[next_pattern_idx].strip().startswith('(re.compile'):
    next_pattern_idx += 1

new_lines.extend(lines[next_pattern_idx:ordinal_start])  # Patterns between S## and ordinals

# Skip ordinal patterns (already added above)
# Continue after ordinal patterns to closing bracket
new_lines.extend(lines[ordinal_end+1:end_idx])  # Rest of patterns and closing

new_lines.extend(lines[end_idx:])  # Rest of file

# Write back
with open('rename_subtitles_to_match_videos_ar_optimized_Sonnet4_NoThinking_configurable.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Pattern fix applied successfully!")
print(f"  - Moved ordinal patterns from line {ordinal_start} to line {start_idx+2}")
print(f"  - Added 2 new Season dash patterns")
print(f"  - Total patterns: 27 (was 25)")
