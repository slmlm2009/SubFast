# Deployment and Distribution

## Installation Process

**User Installation Steps:**

1. **Extract ZIP:**
   ```
   User downloads SubFast-v3.0.0.zip
   Extract to C:\subfast\
   ```

2. **Verify Structure:**
   ```
   Ensure exact path: C:\subfast\
   Required files:
   - scripts\subfast_rename.py
   - scripts\subfast_embed.py
   - bin\mkvmerge.exe
   - config.ini
   - add_subfast_menu.reg
   ```

3. **Install Context Menu:**
   ```
   Double-click: add_subfast_menu.reg
   Click "Yes" when prompted
   Approve UAC if requested
   ```

4. **Verify Installation:**
   ```
   Right-click in any folder
   Look for "SubFast" cascading menu
   Should show: Rename subtitles, Embed subtitles
   ```

## Distribution Variants

**1. Standard Package:**
- Default config.ini (no language suffix)
- Latest mkvmerge.exe bundled
- Complete documentation
- For international users

**2. Arabic-Preconfigured Package:**
- config.ini with `renaming_language_suffix = ar`
- config.ini with `embedding_language_code = ara`
- Same mkvmerge.exe
- Arabic user guide included
- For Arabic subtitle management

## Uninstallation

**Steps:**
```bash
# 1. Remove context menu
Double-click: C:\subfast\remove_subfast_menu.reg

# 2. Verify removal
Right-click in folder → "SubFast" should be gone

# 3. Delete installation
Delete C:\subfast\ folder

# 4. Clean up user data (optional)
# User-generated backups/ and CSV reports remain in user directories
# Delete manually if desired
```

## Update Process

**In-Place Update:**
```bash
# 1. Download new version
# 2. Extract to temporary location
# 3. Close any running SubFast operations
# 4. Copy new files to C:\subfast\ (overwrite old)
# 5. Preserve user config.ini or merge changes
# 6. Registry unchanged (no need to re-run .reg files)
```

**Clean Update (Recommended):**
```bash
# 1. Backup user config.ini
# 2. Run remove_subfast_menu.reg
# 3. Delete C:\subfast\
# 4. Extract new version to C:\subfast\
# 5. Restore/merge config.ini
# 6. Run add_subfast_menu.reg
```

---
