#!/usr/bin/env python3
"""Update CHANGELOG with bug fix"""

lines = open('CHANGELOG.md', 'r', encoding='utf-8').readlines()

# Find where to insert (before the first hotfix entry)
idx = next(i for i, l in enumerate(lines) if '- **Hotfix: ##x## Pattern Resolution Conflict**' in l)

# Insert bug fix entry
bugfix = '''- **Bug: Negative "Subtitles Missing Videos" Count in Movie Mode**
  - Added max(0, ...) to unmatched_subtitles calculation to prevent negative values
  - Occurred when movie subtitles were counted as both "renamed" and "unidentified"
  - Cosmetic issue in CSV report only, no impact on file renaming
  - Tested and verified on Movie_Test scenario

'''

lines.insert(idx, bugfix)

open('CHANGELOG.md', 'w', encoding='utf-8').writelines(lines)
print('[OK] Updated CHANGELOG.md with bug fix')
