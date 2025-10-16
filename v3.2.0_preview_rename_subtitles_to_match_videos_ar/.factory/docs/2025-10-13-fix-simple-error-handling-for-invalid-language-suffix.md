# Fix: Simple Error Handling for Invalid Language Suffix

## Problem
When renaming script encounters invalid language suffix (spaces or special characters), it:
1. ❌ Crashes during filename generation
2. ❌ Console closes immediately (even with `keep_console_open = true`)
3. ❌ No fallback to defaults
4. ❌ User sees no error message

## Solution (Simple)
1. **Validate language suffix** - reject if has spaces or invalid filename characters
2. **Fall back to empty string** (no suffix mode) if invalid
3. **Catch all crashes** with try-except wrapper
4. **Keep console open** on crashes OR when flag is set

---

## Implementation

### **1. Add Simple Validation Function**

**Location:** `subfast/scripts/subfast_rename.py` (before `main()` function)

```python
def is_valid_language_suffix(suffix):
    """
    Check if language suffix is valid for use in filenames.
    
    Args:
        suffix: Language suffix from config
        
    Returns:
        bool: True if valid (no spaces or special chars), False otherwise
    """
    if not suffix:
        return True  # Empty is valid (no suffix mode)
    
    # Invalid filename characters for Windows/Linux
    invalid_chars = {'\\', '/', ':', '*', '?', '"', '<', '>', '|', ' ', '\t', '\n'}
    
    # Check if any invalid character exists
    return not any(c in invalid_chars for c in suffix)
```

---

### **2. Update main() - Validate and Fallback**

**Location:** In `main()` function, after loading config

**Add this validation:**

```python
def main():
    """Main entry point."""
    print("\n" + "=" * 60)
    print("SubFast v3.1.0 - Subtitle Renaming")
    print("=" * 60 + "\n")
    
    # Load configuration
    config = config_loader.load_config()
    global CONFIG
    CONFIG = config
    
    # Validate language suffix - fall back to empty if invalid
    language_suffix = config.get('language_suffix', '')
    if language_suffix and not is_valid_language_suffix(language_suffix):
        print(f"[ERROR] Invalid language suffix in config.ini: '{language_suffix}'")
        print(f"        Language suffix cannot contain spaces or special characters")
        print(f"[INFO] Falling back to no suffix mode")
        print()
        config['language_suffix'] = ''
    
    # Track execution time
    start_time = time.time()
    
    # ... rest of main() continues normally
```

---

### **3. Add Try-Except Wrapper + Fix Console Handling**

**Location:** Replace `if __name__ == "__main__":` block

**Current:**
```python
if __name__ == "__main__":
    main()
```

**New:**
```python
if __name__ == "__main__":
    exit_code = 0
    config = None
    
    try:
        exit_code = main()
    except Exception as e:
        print(f"\n[FATAL ERROR] Unexpected error: {type(e).__name__}: {e}")
        print("\nPlease check config.ini settings and try again")
        exit_code = 1
    finally:
        # Console handling - ALWAYS runs even if crash occurred
        try:
            if config is None:
                config = config_loader.load_config()
        except:
            config = {'keep_console_open': False}
        
        keep_console_open = config.get('keep_console_open', False)
        
        # Keep console open on crashes OR when flag is set
        if exit_code != 0 or keep_console_open:
            input("\nPress Enter to close this window...")
    
    sys.exit(exit_code)
```

---

### **4. Update main() to Return Exit Code**

**Location:** Bottom of `main()` function

**Change from:**
```python
    # Smart console behavior
    keep_console_open = config.get('keep_console_open', False)
    if keep_console_open:
        input("\nPress Enter to close this window...")
    
    sys.exit(0)
```

**To:**
```python
    return 0  # Success - console handling moved to if __name__ block
```

---

## Example Outputs

### **Invalid Suffix (with spaces):**
```ini
renaming_language_suffix = ar test
```

**Console:**
```
============================================================
SubFast v3.1.0 - Subtitle Renaming
============================================================

[ERROR] Invalid language suffix in config.ini: 'ar test'
        Language suffix cannot contain spaces or special characters
[INFO] Falling back to no suffix mode

PROCESSING SUBTITLES:
----------------------------------------
RENAMED: 'Show.S01E01.srt' -> 'Show.S01E01.srt'  (no suffix added)
```

---

### **Crash During Processing:**
```
[FATAL ERROR] Unexpected error: OSError: No space left on device

Please check config.ini settings and try again

Press Enter to close this window...
```
*(Console stays open!)*

---

## Summary of Changes

**File:** `subfast/scripts/subfast_rename.py`

1. **Add function** `is_valid_language_suffix()` (~15 lines)
   - Simple check for spaces and special characters
   
2. **Update `main()`** (~8 lines)
   - Call validation after loading config
   - Print error and fall back to '' if invalid
   - Change `sys.exit(0)` to `return 0`

3. **Replace `if __name__ == "__main__":` block** (~20 lines)
   - Add try-except-finally wrapper
   - Catch all exceptions
   - Move console handling to finally block
   - Keep console open on crashes OR when flag is set

**Total:** ~40 lines added/modified

---

## Benefits
✅ Invalid suffix → automatic fallback to no suffix  
✅ Script continues working instead of crashing  
✅ Console respects keep_console_open flag  
✅ Console stays open on ANY crash  
✅ Clear error message tells user what's wrong  
✅ Simple implementation, no over-engineering