# Fix Console Auto-Close on Fatal Errors

## Bug
When `keep_console_open = true` in config but script encounters fatal error (mkvmerge not found, invalid directory, etc.), console auto-closes before user can read error message.

**Root Cause:** Early `return EXIT_FATAL_ERROR` statements bypass the end-of-main console handling logic.

## Expected Behavior (Story 3.3)
- **Fatal Errors** → ALWAYS keep console open (so user can read error)
- **Success + keep_console_open=true** → Keep open
- **Success + keep_console_open=false** → Auto-close

## Solution: Refactor to Never Return Early

**Strategy:** Use exit_code variable instead of early returns, ensure console logic ALWAYS executes at end of main().

### Changes Required

**File:** `subfast/scripts/subfast_embed.py`

1. **Add helper function for console handling:**
```python
def handle_console_exit(exit_code, config):
    """Smart console behavior - always show errors to user."""
    keep_console_open = config.get('keep_console_open', False)
    
    # Stay open if: fatal error OR config says so
    if exit_code != EXIT_SUCCESS or keep_console_open:
        input("\nPress Enter to close this window...")
    
    sys.exit(exit_code)
```

2. **Refactor main() to never return early:**
   - Change `return EXIT_FATAL_ERROR` → set `exit_code = EXIT_FATAL_ERROR` and jump to end
   - OR wrap in try/except and ensure cleanup always runs
   - Console handling at end ALWAYS executes

3. **Apply same fix to renaming script** if it has similar early returns

## Benefit
✅ Users can always read error messages when keep_console_open=true
✅ Matches Story 3.3 smart console behavior requirements
✅ Better UX - no more mysterious silent failures