# Migration Guide: Option B (Scalable Structure)

**Date:** 2025-01-05  
**Architect:** Winston  
**Target Structure:** Option B with modified paths

---

## 📋 Overview

This guide provides step-by-step instructions for migrating the SubFast project from the current flat structure to the scalable Option B structure with branded script names.

---

## 🎯 Structural Changes

### Before (Current)

```
rename_subtitles_to_match_videos_ar/
├── rename_subtitles_to_match_videos_ar.py
├── embed_subtitles_to_match_videos_ar.py
├── mkvmerge.exe
├── config.ini
├── CONFIGURATION_README.md
├── Resources/
│   └── [logo will be here]
└── [old .reg files]
```

### After (Target)

```
subfast/
├── scripts/
│   ├── subfast_rename.py
│   └── subfast_embed.py
├── bin/
│   └── mkvmerge.exe
├── resources/
│   └── subfast_logo.ico
├── config.ini
├── add_subfast_menu.reg
├── remove_subfast_menu.reg
├── CONFIGURATION_README.md
└── README.md
```

---

## 🚀 Migration Steps

### Step 1: Backup Current State

```powershell
# Create backup of current folder
Copy-Item -Path "rename_subtitles_to_match_videos_ar" -Destination "rename_subtitles_to_match_videos_ar_BACKUP" -Recurse
```

### Step 2: Rename Main Folder

```powershell
# Rename main project folder
Rename-Item -Path "rename_subtitles_to_match_videos_ar" -NewName "subfast"
cd subfast
```

### Step 3: Create New Folder Structure

```powershell
# Create new folders
New-Item -Path "scripts" -ItemType Directory
New-Item -Path "bin" -ItemType Directory

# Rename Resources to resources (lowercase)
Rename-Item -Path "Resources" -NewName "resources"
```

### Step 4: Move and Rename Python Scripts

```powershell
# Rename and move scripts
Rename-Item -Path "rename_subtitles_to_match_videos_ar.py" -NewName "subfast_rename.py"
Rename-Item -Path "embed_subtitles_to_match_videos_ar.py" -NewName "subfast_embed.py"

# Move to scripts folder
Move-Item -Path "subfast_rename.py" -Destination "scripts\"
Move-Item -Path "subfast_embed.py" -Destination "scripts\"
```

### Step 5: Move Binary

```powershell
# Move mkvmerge to bin folder
Move-Item -Path "mkvmerge.exe" -Destination "bin\"
```

### Step 6: Update config.ini

Open `config.ini` and update the mkvmerge path:

```ini
[Embedding]
mkvmerge_path = bin\mkvmerge.exe
```

### Step 7: Update Scripts (Import Paths)

**CRITICAL:** Check if scripts have any relative imports that need updating.

Open both scripts and verify:
- `scripts/subfast_rename.py`
- `scripts/subfast_embed.py`

Update any relative path references to config.ini:

```python
# OLD (if it exists)
config_path = Path(__file__).parent / 'config.ini'

# NEW
config_path = Path(__file__).parent.parent / 'config.ini'
```

Update any relative path references to mkvmerge:

```python
# OLD (if hardcoded)
mkvmerge_path = Path(__file__).parent / 'mkvmerge.exe'

# NEW - Should use config.ini, but if needed:
mkvmerge_path = Path(__file__).parent.parent / 'bin' / 'mkvmerge.exe'
```

### Step 8: Archive Old Registry Files

```powershell
# Create archive folder
New-Item -Path "archive" -ItemType Directory

# Move old registry files
Move-Item -Path "add_embed_subtitle_menu.reg" -Destination "archive\" -ErrorAction SilentlyContinue
Move-Item -Path "add_subtitle_rename_menu.reg" -Destination "archive\" -ErrorAction SilentlyContinue
Move-Item -Path "remove_embed_subtitle_menu.reg" -Destination "archive\" -ErrorAction SilentlyContinue
Move-Item -Path "remove_subtitle_rename_menu.reg" -Destination "archive\" -ErrorAction SilentlyContinue
```

### Step 9: Verify New Registry Files

Confirm these files exist at root:
- `add_subfast_menu.reg` ✅
- `remove_subfast_menu.reg` ✅

Verify they contain correct paths to `scripts/` and `resources/`.

### Step 10: Clean Up Cache Files

```powershell
# Remove Python cache
Remove-Item -Path "__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "scripts\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue

# Remove any .pyc files
Get-ChildItem -Path . -Filter "*.pyc" -Recurse | Remove-Item -Force
```

---

## ✅ Testing Checklist

### Phase 1: File System Verification

- [ ] Main folder renamed to `subfast`
- [ ] `scripts/` folder exists with both .py files
- [ ] `bin/` folder exists with mkvmerge.exe
- [ ] `resources/` folder exists (lowercase)
- [ ] `config.ini` at root level
- [ ] Registry files at root level
- [ ] README.md at root level
- [ ] Old .reg files moved to archive

### Phase 2: Script Functionality

```powershell
# Test scripts can find config.ini
python scripts\subfast_rename.py --help
# Should not error on config loading

python scripts\subfast_embed.py --help
# Should not error on config/mkvmerge loading
```

### Phase 3: Context Menu Installation

```powershell
# Install context menu
# Right-click add_subfast_menu.reg → Merge
# Verify no errors
```

- [ ] Context menu installs without errors
- [ ] SubFast menu appears in Windows Explorer
- [ ] Icon displays correctly
- [ ] "Rename Subtitles" is first option
- [ ] "Embed Subtitles" is second option

### Phase 4: Functional Testing

**Test Renaming:**
1. Navigate to test folder with videos and subtitles
2. Right-click → SubFast → Rename Subtitles
3. Verify script executes correctly
4. Check renaming works as expected

**Test Embedding:**
1. Navigate to test folder with MKV and subtitles
2. Right-click → SubFast → Embed Subtitles
3. Verify script executes correctly
4. Check embedding works as expected

### Phase 5: CSV Reports

- [ ] Renaming generates `renaming_report.csv`
- [ ] Embedding generates `embedding_report.csv`
- [ ] Reports contain correct data

---

## 🐛 Troubleshooting

### Issue: "config.ini not found"

**Cause:** Scripts can't find config.ini at root level

**Fix:**
```python
# In both scripts, verify this line:
config_path = Path(__file__).parent.parent / 'config.ini'
```

### Issue: "mkvmerge not found"

**Cause:** Path in config.ini is wrong

**Fix:** Update `config.ini`:
```ini
[Embedding]
mkvmerge_path = bin\mkvmerge.exe
```

### Issue: Context menu shows error

**Cause:** Registry paths are incorrect

**Fix:**
1. Run `remove_subfast_menu.reg`
2. Verify paths in `add_subfast_menu.reg`:
   - `scripts\\subfast_rename.py`
   - `scripts\\subfast_embed.py`
   - `resources\\subfast_logo.ico`
3. Run `add_subfast_menu.reg` again

### Issue: Icon doesn't display

**Cause 1:** Icon file missing  
**Fix:** Place `subfast_logo.ico` in `resources/` folder

**Cause 2:** Icon path wrong in registry  
**Fix:** Verify registry shows: `resources\\subfast_logo.ico`

### Issue: Scripts work from command line but not from context menu

**Cause:** Python not in PATH or paths in .reg file incorrect

**Fix 1:** Verify Python in PATH:
```powershell
python --version
# Should show Python version
```

**Fix 2:** Use absolute path in .reg file:
```registry
@="C:\\Python311\\python.exe \"%~dp0scripts\\subfast_rename.py\" \"%V\""
```

---

## 📝 Post-Migration Updates

### Update Documentation

- [ ] Update `docs/architecture/project-structure.md`
- [ ] Update any references in PRD or stories
- [ ] Update README.md if needed
- [ ] Close Story 3.4 as Done

### Git Commit

```bash
git add .
git commit -m "Restructure project to Option B (scalable) with branded script names

- Renamed main folder to 'subfast'
- Organized scripts into scripts/ folder
- Renamed scripts to subfast_rename.py and subfast_embed.py
- Moved mkvmerge.exe to bin/ folder
- Renamed Resources to resources (lowercase)
- Updated all paths in registry files and documentation
- Archived old individual registry files

Fixes #[story-number] - Story 3.4 Unified Context Menu"
```

---

## 🎉 Success Criteria

Migration is complete when:

✅ All files in correct locations  
✅ Scripts execute from context menu  
✅ Icon displays in menu  
✅ Config.ini is properly loaded  
✅ mkvmerge is found by embedding script  
✅ CSV reports generate correctly  
✅ No Python import errors  
✅ Context menu installs/uninstalls cleanly  
✅ Documentation updated  

---

## 🔄 Rollback Plan

If migration fails:

```powershell
# Remove new structure
cd ..
Remove-Item -Path "subfast" -Recurse -Force

# Restore backup
Copy-Item -Path "rename_subtitles_to_match_videos_ar_BACKUP" -Destination "rename_subtitles_to_match_videos_ar" -Recurse

# Remove context menu if installed
# Run the backup's remove_subtitle_rename_menu.reg and remove_embed_subtitle_menu.reg
```

---

## 📊 Before/After Comparison

| Aspect | Before (Flat) | After (Option B) |
|--------|---------------|-------------------|
| Main folder | `rename_subtitles_to_match_videos_ar` | `subfast` |
| Scripts | Root level, long names | `scripts/` folder, branded names |
| Binary | Root level | `bin/` folder |
| Assets | `Resources/` | `resources/` (lowercase) |
| Context menu | 2 separate entries | 1 unified cascading menu |
| Scalability | Limited | High |
| Professionalism | Good | Excellent |

---

**Migration prepared by Winston (Architect) - Ready for Dev execution** 🏗️
