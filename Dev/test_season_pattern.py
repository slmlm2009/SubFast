import re

def test_new_pattern():
    # Test the new Season X Episode Y pattern
    filename = "Show Name Season 1 Episode 5.mkv"
    
    # Pattern: Show Name Season X Episode Y (with spaces)
    match = re.search(r'[Ss]eason\s+(\d+)\s+[Ee]pisode\s+(\d+)', filename, re.IGNORECASE)
    
    if match:
        print(f"Pattern matched for: {filename}")
        season = match.group(1).zfill(2)  # Ensure 2 digits for season
        episode = match.group(2)  # Keep original episode digits
        result = f"S{season}E{episode}"
        print(f"Detected episode: {result}")
        return result
    else:
        print(f"Pattern did not match: {filename}")
        return None

def test_new_pattern2():
    # Test with 2-digit season
    filename = "Show Name Season 12 Episode 105.mkv"
    
    # Pattern: Show Name Season X Episode Y (with spaces)
    match = re.search(r'[Ss]eason\s+(\d+)\s+[Ee]pisode\s+(\d+)', filename, re.IGNORECASE)
    
    if match:
        print(f"Pattern matched for: {filename}")
        season = match.group(1).zfill(2)  # Ensure 2 digits for season
        episode = match.group(2)  # Keep original episode digits
        result = f"S{season}E{episode}"
        print(f"Detected episode: {result}")
        return result
    else:
        print(f"Pattern did not match: {filename}")
        return None

if __name__ == "__main__":
    print("Testing Season X Episode Y pattern:")
    test_new_pattern()
    test_new_pattern2()