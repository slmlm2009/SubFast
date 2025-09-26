import re

def debug_pattern_matching(filename):
    print(f\"Debugging pattern matching for: {filename}\")
    
    # Pattern 1: S##E##
    pattern = r'[Ss](\\d+)[Ee](\\d+)'
    match = re.search(pattern, filename)
    if match:
        print(f\"  1. S##E## matched: {match.group(0)}\")
        return f\"S{match.group(1).zfill(2)}E{match.group(2)}\"
    else:
        print(\"  1. S##E##: no match\")
    
    # Pattern 2: 2x05
    pattern = r'(?:^|[._\\s-])(\\d+)[xX](\\d+)(?=[._\\s-]|$)'
    match = re.search(pattern, filename)
    if match:
        print(f\"  2. 2x05 matched: {match.group(0)}\")
        return f\"S{match.group(1).zfill(2)}E{match.group(2)}\"
    else:
        print(\"  2. 2x05: no match\")
    
    # Pattern 3: Season.Episode
    pattern = r'[Ss]eason\\.(\\d+)[\\s\\._-]*[Ee]pisode\\.(\\d+)'
    match = re.search(pattern, filename, re.IGNORECASE)
    if match:
        print(f\"  3. Season.Episode matched: {match.group(0)}\")
        return f\"S{match.group(1).zfill(2)}E{match.group(2)}\"
    else:
        print(\"  3. Season.Episode: no match\")
    
    # Pattern 4: S##.Ep.##
    pattern = r'[Ss](\\d+)[\\s\\._-]*[Ee]p(?:isode)?\\.(\\d+)'
    match = re.search(pattern, filename, re.IGNORECASE)
    if match:
        print(f\"  4. S##.Ep.## matched: {match.group(0)}\")
        return f\"S{match.group(1).zfill(2)}E{match.group(2)}\"
    else:
        print(\"  4. S##.Ep.##: no match\")
    
    # Pattern 5: Season X Episode Y
    pattern = r'[Ss]eason\\s+(\\d+)\\s+[Ee]pisode\\s+(\\d+)'
    match = re.search(pattern, filename, re.IGNORECASE)
    if match:
        print(f\"  5. Season X Episode Y matched: {match.group(0)}\")
        return f\"S{match.group(1).zfill(2)}E{match.group(2)}\"
    else:
        print(\"  5. Season X Episode Y: no match\")
    
    # Pattern 6: ShowNameSeasonXEpisodeY
    pattern = r'[Ss]eason(\\d+)[Ee]pisode(\\d+)'
    match = re.search(pattern, filename, re.IGNORECASE)
    if match:
        print(f\"  6. ShowNameSeasonXEpisodeY matched: {match.group(0)}\")
        return f\"S{match.group(1).zfill(2)}E{match.group(2)}\"
    else:
        print(\"  6. ShowNameSeasonXEpisodeY: no match\")
    
    # Pattern 7: ShowNameSeasonX EpisodeY
    pattern = r'[Ss]eason(\\d+)\\s+[Ee]pisode(\\d+)'
    match = re.search(pattern, filename, re.IGNORECASE)
    if match:
        print(f\"  7. ShowNameSeasonX EpisodeY matched: {match.group(0)}\")
        return f\"S{match.group(1).zfill(2)}E{match.group(2)}\"
    else:
        print(\"  7. ShowNameSeasonX EpisodeY: no match\")
    
    # Pattern 8: E####
    pattern = r'(?:^|[._\\s-])[Ee](\\d{2,})(?=[._\\s-]|$)'
    match = re.search(pattern, filename)
    if match:
        print(f\"  8. E#### matched: {match.group(0)}\")
        return f\"S01E{match.group(1)}\"
    else:
        print(\"  8. E####: no match\")
    
    # Pattern 9: Ep#### 
    pattern = r'(?:^|[._\\s-])[Ee]p(?:isode)?(\\d{2,})(?=[._\\s-]|$)'
    match = re.search(pattern, filename, re.IGNORECASE)
    if match:
        print(f\"  9. Ep#### matched: {match.group(0)}\")
        return f\"S01E{match.group(1)}\"
    else:
        print(\"  9. Ep####: no match\")
    
    # Pattern 10: S##Ep## (the one we expect to match)
    pattern = r'[Ss](\\d+)[Ee]p(?:isode)?(\\d+)'
    match = re.search(pattern, filename, re.IGNORECASE)
    if match:
        print(f\" 10. S##Ep## matched: {match.group(0)}\")
        return f\"S{match.group(1).zfill(2)}E{match.group(2)}\"
    else:
        print(\" 10. S##Ep##: no match\")
    
    # Pattern 11: - ##
    pattern = r'-\\s*(\\d+)'
    match = re.search(pattern, filename)
    if match:
        print(f\" 11. - ## matched: {match.group(0)}\")
        return f\"S01E{match.group(1)}\"
    else:
        print(\" 11. - ##: no match\")
        
    print(\"  No patterns matched\")
    return None


# Test the problematic file
result = debug_pattern_matching(\"Program S02Ep15.mkv\")
print(f\"\nFinal result: {result}\")