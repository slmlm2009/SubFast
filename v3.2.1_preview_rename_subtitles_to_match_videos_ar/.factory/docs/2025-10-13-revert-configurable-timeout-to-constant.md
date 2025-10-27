# Revert Configurable Timeout to Constant

## Summary
Revert the `merge_timeout_seconds` from being a user-configurable setting to a **hardcoded constant** in the code. The dynamic timeout calculation remains, but the maximum cap is no longer user-configurable.

---

## Changes Required

### 1. **Remove from config_loader.py**

**File:** `subfast/scripts/common/config_loader.py`

#### **A. Remove from DEFAULT_CONFIG** (Line 25)
```python
# REMOVE THIS LINE:
'merge_timeout_seconds': 1800  # Default 30 minutes for large files
```

#### **B. Remove from config.ini template** (Lines 79-82)
```python
# REMOVE THESE LINES:
# Maximum timeout for mkvmerge operations in seconds (minimum: 60)
# Dynamic timeout is calculated: 300s base + 120s per GB, capped by this value
# Default: 1800 (30 minutes)
merge_timeout_seconds = 1800
```

#### **C. Remove parsing logic** (Lines 205-219)
```python
# REMOVE THIS ENTIRE BLOCK:
# Optional timeout override (minimum 60 seconds)
timeout_raw = config.get('Embedding', 'merge_timeout_seconds', fallback='1800').strip()
if timeout_raw:
    try:
        timeout_val = int(timeout_raw)
        if timeout_val >= 60:
            config_dict['merge_timeout_seconds'] = timeout_val
        else:
            print("[WARNING] merge_timeout_seconds must be >= 60; using default 1800s")
            config_dict['merge_timeout_seconds'] = DEFAULT_CONFIG['merge_timeout_seconds']
    except ValueError:
        print("[WARNING] Invalid merge_timeout_seconds; using default 1800s")
        config_dict['merge_timeout_seconds'] = DEFAULT_CONFIG['merge_timeout_seconds']
else:
    config_dict['merge_timeout_seconds'] = DEFAULT_CONFIG['merge_timeout_seconds']
```

#### **D. Remove from exception handler** (Line 226)
```python
# REMOVE THIS LINE:
config_dict['merge_timeout_seconds'] = DEFAULT_CONFIG['merge_timeout_seconds']
```

---

### 2. **Update subfast_embed.py**

**File:** `subfast/scripts/subfast_embed.py`

#### **A. Add constant at module level** (After imports, ~line 20)
```python
# Timeout constants
TIMEOUT_BASE = 300  # 5 minutes minimum
TIMEOUT_PER_GB = 120  # 2 minutes per GB
TIMEOUT_MAX = 1800  # 30 minutes maximum cap
```

#### **B. Simplify dynamic timeout calculation** (Lines 319-323)
```python
# CHANGE FROM:
max_cfg = config.get('merge_timeout_seconds', 1800) if config else 1800
timeout_seconds = max(300, min(max_cfg, dyn_timeout))

# CHANGE TO:
timeout_seconds = max(TIMEOUT_BASE, min(TIMEOUT_MAX, dyn_timeout))
```

#### **C. Update comment** (Line 319)
```python
# CHANGE FROM:
# Dynamic timeout: base 300s + 120s per GB, capped by config

# CHANGE TO:
# Dynamic timeout: base 300s + 120s per GB, capped at 1800s (30 min)
```

---

## Result After Changes

### **Dynamic Timeout Calculation:**
```python
# At module level (constants)
TIMEOUT_BASE = 300  # 5 minutes minimum
TIMEOUT_PER_GB = 120  # 2 minutes per GB
TIMEOUT_MAX = 1800  # 30 minutes maximum cap

# In embed_subtitle() function
try:
    total_bytes = video_path.stat().st_size + subtitle_path.stat().st_size
except Exception:
    total_bytes = 0

# Dynamic timeout: base 300s + 120s per GB, capped at 1800s (30 min)
gb = total_bytes / (1024 ** 3)
dyn_timeout = TIMEOUT_BASE + int(max(0, gb) * TIMEOUT_PER_GB)
timeout_seconds = max(TIMEOUT_BASE, min(TIMEOUT_MAX, dyn_timeout))
```

---

## Benefits of This Approach

### ✅ **Simplicity:**
- No user configuration needed
- Constants are clear and easy to find in code
- Less complexity in config_loader.py

### ✅ **Dynamic Scaling Still Works:**
- Small files: ~5-10 minutes
- Medium files: ~15-20 minutes  
- Large files: Capped at 30 minutes

### ✅ **Easy to Modify:**
- Developers can change constants in code
- Clear module-level constants
- No config file parsing complexity

---

## Files Modified

1. **`subfast/scripts/common/config_loader.py`**
   - Remove `merge_timeout_seconds` from DEFAULT_CONFIG
   - Remove from config.ini template
   - Remove parsing logic
   - Remove from exception handler

2. **`subfast/scripts/subfast_embed.py`**
   - Add timeout constants at module level
   - Simplify dynamic timeout calculation
   - Remove config dependency for timeout

---

## Testing Checklist

After changes:
- [ ] Config loads without errors
- [ ] Embedding works with dynamic timeout
- [ ] Small files use shorter timeout
- [ ] Large files capped at 1800s
- [ ] No references to `merge_timeout_seconds` in config

---

**Result:** Dynamic timeout system remains functional, but maximum cap is now a simple constant in the code instead of a user-configurable setting.