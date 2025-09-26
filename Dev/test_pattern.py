import re

# Test the S##Ep## pattern
filename = "Program S02Ep15.mkv"
pattern = r'[Ss](\d+)[Ee]p(?:isode)?(\d+)'
match = re.search(pattern, filename, re.IGNORECASE)

if match:
    print(f"Pattern matched for: {filename}")
    season = match.group(1).zfill(2)  # Ensure 2 digits for season
    episode = match.group(2)  # Keep original episode digits
    result = f"S{season}E{episode}"
    print(f"Detected episode: {result}")
else:
    print(f"Pattern did not match: {filename}")

# Test single digit season
filename2 = "Program S2Ep10.mkv"
match2 = re.search(pattern, filename2, re.IGNORECASE)

if match2:
    print(f"Pattern matched for: {filename2}")
    season = match2.group(1).zfill(2)  # Ensure 2 digits for season
    episode = match2.group(2)  # Keep original episode digits
    result = f"S{season}E{episode}"
    print(f"Detected episode: {result}")
else:
    print(f"Pattern did not match: {filename2}")