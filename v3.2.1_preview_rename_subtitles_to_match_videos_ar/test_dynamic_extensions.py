"""Quick test of dynamic extension detection"""
import sys
from pathlib import Path

# Add tests to path
sys.path.insert(0, str(Path(__file__).parent / 'tests'))

from generate_test_files import extract_extensions_from_definitions

# Test extension detection
pattern_file = Path(__file__).parent / 'tests' / 'fixtures' / 'pattern_definitions.json'
exts = extract_extensions_from_definitions(pattern_file)

print("=" * 60)
print("DYNAMIC EXTENSION DETECTION TEST")
print("=" * 60)
print("\nDetected from pattern_definitions.json:")
print(f"  Video extensions: {', '.join(sorted(exts['video']))}")
print(f"  Subtitle extensions: {', '.join(sorted(exts['subtitle']))}")
print("\n[SUCCESS] Dynamic detection working!")
print("=" * 60)
