import re

def get_episode_number(filename):
    print(f\"Checking file: {filename}\")
    
    # Try to match S##E## pattern (for video files like S01E01)
    match = re.search(r'[Ss](\\d+)[Ee](\\d+)', filename)
    if match:
        print(f\"  S##E## pattern matched: {match.group(0)} -> season: {match.group(1)}, episode: {match.group(2)}\")
        season = match.group(1).zfill(2)  # Ensure 2 digits for season
        episode = match.group(2)  # Keep original episode digits (for 100+ episodes)
        return f\"S{season}E{episode}\"
    
    print(\"  S##E## pattern: no match\")
    
    # Try to match season.episode pattern (for files like Show.Name.2x05)
    match = re.search(r'(?:^|[._\\s-])(\\d+)[xX](\\d+)(?=[._\\s-]|$)', filename)
    if match:
        print(f\"  2x05 pattern matched: {match.group(0)} -> season: {match.group(1)}, episode: {match.group(2)}\")
        season = match.group(1).zfill(2)  # Ensure 2 digits for season
        episode = match.group(2)  # Keep original episode digits (for 100+ episodes)
        return f\"S{season}E{episode}\"
    
    print(\"  2x05 pattern: no match\")
    
    # Try to match Season/Episode words pattern (for files like Show.Name.Season.1.Episode.05)
    match = re.search(r'[Ss]eason\\.(\\d+)[\\s\\._-]*[Ee]pisode\\.(\\d+)', filename, re.IGNORECASE)
    if match:
        print(f\"  Season.Episode pattern matched: {match.group(0)} -> season: {match.group(1)}, episode: {match.group(2)}\")
        season = match.group(1).zfill(2)  # Ensure 2 digits for season
        episode = match.group(2)  # Keep original episode digits (for 100+ episodes)
        return f\"S{season}E{episode}\"
    
    print(\"  Season.Episode pattern: no match\")
    
    # Alternative pattern: Show.Name.S01.Ep.05
    match = re.search(r'[Ss](\\d+)[\\s\\._-]*[Ee]p(?:isode)?\\.(\\d+)', filename, re.IGNORECASE)
    if match:
        print(f\"  S##.Ep.## pattern matched: {match.group(0)} -> season: {match.group(1)}, episode: {match.group(2)}\")
        season = match.group(1).zfill(2)  # Ensure 2 digits for season
        episode = match.group(2)  # Keep original episode digits (for 100+ episodes)
        return f\"S{season}E{episode}\"
    
    print(\"  S##.Ep.## pattern: no match\")
    
    # NEW PATTERN: Show Name Season X Episode Y (with spaces)
    match = re.search(r'[Ss]eason\\s+(\\d+)\\s+[Ee]pisode\\s+(\\d+)', filename, re.IGNORECASE)
    if match:
        print(f\"  Season X Episode Y pattern matched: {match.group(0)} -> season: {match.group(1)}, episode: {match.group(2)}\")
        season = match.group(1).zfill(2)  # Ensure 2 digits for season
        episode = match.group(2)  # Keep original episode digits (for 100+ episodes)
        return f\"S{season}E{episode}\"
    
    print(\"  Season X Episode Y pattern: no match\")
    
    # NEW PATTERN: ShowNameSeasonXEpisodeY (without any spaces)
    match = re.search(r'[Ss]eason(\\d+)[Ee]pisode(\\d+)', filename, re.IGNORECASE)
    if match:
        print(f\"  ShowNameSeasonXEpisodeY pattern matched: {match.group(0)} -> season: {match.group(1)}, episode: {match.group(2)}\")
        season = match.group(1).zfill(2)  # Ensure 2 digits for season
        episode = match.group(2)  # Keep original episode digits (for 100+ episodes)
        return f\"S{season}E{episode}\"
    
    print(\"  ShowNameSeasonXEpisodeY pattern: no match\")
    
    # NEW PATTERN: ShowNameSeasonX EpisodeY (space only between Season and Episode)
    match = re.search(r'[Ss]eason(\\d+)\\s+[Ee]pisode(\\d+)', filename, re.IGNORECASE)
    if match:
        print(f\"  ShowNameSeasonX EpisodeY pattern matched: {match.group(0)} -> season: {match.group(1)}, episode: {match.group(2)}\")
        season = match.group(1).zfill(2)  # Ensure 2 digits for season
        episode = match.group(2)  # Keep original episode digits (for 100+ episodes)
        return f\"S{season}E{episode}\"
    
    print(\"  ShowNameSeasonX EpisodeY pattern: no match\")
    
    # Try to match E## pattern (for files like Show.Name.E1234)
    # Use word boundary or separators to avoid matching within words like \"Title.2023\"
    match = re.search(r'(?:^|[._\\s-])[Ee](\\d{2,})(?=[._\\s-]|$)', filename)  
    if match:
        print(f\"  E#### pattern matched: {match.group(0)} -> episode: {match.group(1)}\")
        episode = match.group(1)  # Keep original episode digits
        return f\"S01E{episode}\"  # Assume season 1
    
    print(\"  E#### pattern: no match\")
    
    # NEW PATTERN: Try to match Ep#### pattern (for files like Show.Name.Ep1234)
    # Use word boundary or separators to avoid matching within other words
    match = re.search(r'(?:^|[._\\s-])[Ee]p(?:isode)?(\\d{2,})(?=[._\\s-]|$)', filename, re.IGNORECASE)  
    if match:
        print(f\"  Ep#### pattern matched: {match.group(0)} -> episode: {match.group(1)}\")
        episode = match.group(1)  # Keep original episode digits
        return f\"S01E{episode}\"  # Assume season 1
    
    print(\"  Ep#### pattern: no match\")
    
    # NEW PATTERN: S##Ep## (without dots)
    match = re.search(r'[Ss](\\d+)[Ee]p(?:isode)?(\\d+)', filename, re.IGNORECASE)
    if match:
        print(f\"  S##Ep## pattern matched: {match.group(0)} -> season: {match.group(1)}, episode: {match.group(2)}\")
        season = match.group(1).zfill(2)  # Ensure 2 digits for season
        episode = match.group(2)  # Keep original episode digits (for 100+ episodes)
        return f\"S{season}E{episode}\"
    
    print(\"  S##Ep## pattern: no match\")
    
    # Try to match - ## pattern (for subtitle files like - 01, - 02)
    match = re.search(r'-\\s*(\\d+)', filename)
    if match:
        print(f\"  - ## pattern matched: {match.group(0)} -> episode: {match.group(1)}\")
        episode_num = match.group(1)  # Keep original episode digits (for 100+ episodes)
        return f\"S01E{episode_num}\"  # Assume season 1
    
    print(\"  - ## pattern: no match\")
    
    print(\"  No patterns matched\")
    return None

# Test the problematic files
test_files = [
    \"Program S02Ep15.mkv\",
    \"Program S2Ep10.mkv\"
]

for filename in test_files:
    result = get_episode_number(filename)
    print(f\"Result: {result}\\n\")