# SubFast v3.0.0 - Distribution Plan

## 📦 Two-Tier Distribution Strategy

SubFast v3.0.0 uses a **minimal ZIP + GitHub docs** approach for optimal distribution.

---

## 🎯 What Goes Where

### **ZIP Package (SubFast-v3.0.0.zip)**
**Purpose:** Operational files only - what users need to run SubFast

```
subfast/
├── config.ini                    ✅ Essential configuration
├── add_subfast_menu.reg          ✅ Installer
├── remove_subfast_menu.reg       ✅ Uninstaller
├── scripts/
│   ├── subfast_rename.py         ✅ Core functionality
│   └── subfast_embed.py          ✅ Core functionality
├── bin/
│   └── mkvmerge.exe              ✅ Required binary
└── resources/
    ├── subfast_logo.ico          ✅ Context menu icon
    └── doc/
        └── CONFIGURATION_README.md ✅ Configuration reference
```

**Size:** ~16.5 MB (mostly mkvmerge.exe)  
**User Benefit:** Fast download, clean installation, no documentation clutter

---

### **GitHub Repository**
**Purpose:** Full documentation, release notes, guides

**Root Level:**
- `README.md` - Displays on GitHub homepage, complete installation guide
- `CHANGELOG.md` - Full v3.0.0 release notes with migration guide
- `UPGRADE_GUIDE.md` - Quick reference for v2.x upgraders

**In Repository:**
- `resources/doc/README.md` - Detailed user guide (source file)
- `resources/doc/CONFIGURATION_README.md` - Configuration guide (also in ZIP)
- All ZIP contents (for reference and issue debugging)

**GitHub Releases Section:**
- Release title and description (from CHANGELOG.md)
- Attached ZIP file
- Link to full CHANGELOG.md
- Link to UPGRADE_GUIDE.md

---

## 🎯 User Journey

### **New Users:**
1. **Visit GitHub repository** → Read README.md
2. **Download** SubFast-v3.0.0.zip from Releases
3. **Extract** to C:\subfast
4. **Install** context menu (double-click .reg)
5. **Use** SubFast from right-click menu
6. **Reference** CONFIGURATION_README.md for config changes

### **Upgrading Users (from v2.x):**
1. **Visit GitHub repository** → Read UPGRADE_GUIDE.md
2. **Remove** old v2.x context menu
3. **Delete** old installation folder
4. **Download** SubFast-v3.0.0.zip from Releases
5. **Extract** to C:\subfast
6. **Install** new context menu
7. **Restore** settings in config.ini

---

## 📊 Benefits of This Approach

### **For Users:**
- ✅ Smaller download size
- ✅ Cleaner installation folder
- ✅ Up-to-date docs always on GitHub
- ✅ Essential reference (CONFIGURATION_README.md) included locally

### **For Maintainers:**
- ✅ Update docs without re-releasing ZIP
- ✅ Single source of truth (GitHub)
- ✅ Version-specific CHANGELOG in Releases
- ✅ Easier to maintain and update

### **For Support:**
- ✅ Users reference GitHub docs (always current)
- ✅ Issues link to specific versions
- ✅ Clear migration guides for upgraders
- ✅ FAQ and troubleshooting always accessible

---

## 📋 Release Checklist

### **1. Prepare ZIP Package:**
- [ ] Create clean `subfast/` folder with only essential files
- [ ] Verify structure matches plan above
- [ ] Test installation from ZIP
- [ ] Create `SubFast-v3.0.0.zip`

### **2. Prepare GitHub Repository:**
- [ ] Update root `README.md` for v3.0.0
- [ ] Ensure `CHANGELOG.md` is complete
- [ ] Ensure `UPGRADE_GUIDE.md` is clear
- [ ] Commit all documentation

### **3. Create GitHub Release:**
- [ ] Tag: `v3.0.0`
- [ ] Title: "SubFast v3.0.0 - Unified Branding & Professional Structure"
- [ ] Description: Summary from CHANGELOG.md
- [ ] Attach: `SubFast-v3.0.0.zip`
- [ ] Link to: Full CHANGELOG.md in repo
- [ ] Link to: UPGRADE_GUIDE.md in repo

### **4. Verify Links:**
- [ ] README.md displays on GitHub homepage
- [ ] CHANGELOG.md accessible in repo
- [ ] UPGRADE_GUIDE.md accessible in repo
- [ ] Release ZIP downloads correctly
- [ ] All documentation links work

---

## 🎉 Result

Users get:
- ✅ Minimal, clean application package (ZIP)
- ✅ Comprehensive documentation (GitHub)
- ✅ Clear upgrade path (UPGRADE_GUIDE.md)
- ✅ Essential reference included (CONFIGURATION_README.md)
- ✅ Professional distribution experience

**Perfect balance of simplicity and completeness!** 🚀
