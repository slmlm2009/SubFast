import re

# Test only the S##Ep## pattern
filename = "Program S02Ep15.mkv"
pattern = r'[Ss](\d+)[Ee]p(?:isode)?(\d+)'
match = re.search(pattern, filename, re.IGNORECASE)

if match:
    print(f"Pattern matched for: {filename}")
    print(f"Full match: {match.group(0)}")
    print(f"Season group: {match.group(1)}")
    print(f"Episode group: {match.group(2)}")
    
    season = match.group(1).zfill(2)  # Ensure 2 digits for season
    episode = match.group(2)  # Keep original episode digits
    result = f"S{season}E{episode}"
    print(f"Detected episode: {result}")
else:
    print(f"Pattern did not match: {filename}")