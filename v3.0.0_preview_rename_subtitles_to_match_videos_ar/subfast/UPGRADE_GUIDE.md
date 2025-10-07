# Quick Upgrade Guide: v2.x → v3.0.0

**Upgrading from SubFast v2.x to v3.0.0? Follow these steps.**

> **📖 Note:** This guide is available on the GitHub repository. The downloaded ZIP contains only the application files, not documentation.

---

## ⚡ Quick Steps (5 Minutes)

### **1. Remove Old Context Menu**

Navigate to your old folder: `C:\rename_subtitles_to_match_videos_ar\`

**If you have v2.5.0 or newer:**
- Double-click: `remove_subtitle_rename_menu.reg` → Click Yes
- Double-click: `remove_embed_subtitle_menu.reg` → Click Yes

**If you have older version:**
- Run your old removal registry files

---

### **2. Backup Your Settings (Optional)**

If you customized `config.ini`:
- Copy your language suffix and other custom settings
- Save for reference

---

### **3. Delete Old Installation**

Delete the entire folder:
```
C:\rename_subtitles_to_match_videos_ar\
```

**Note:** This only removes the tool. Your videos/subtitles are safe!

---

### **4. Install v3.0.0**

1. **Extract** SubFast v3.0.0 ZIP to:
   ```
   C:\subfast\
   ```
   ⚠️ **Must be exactly `C:\subfast`**

2. **Restore your settings** in `C:\subfast\config.ini`:
   ```ini
   [Renaming]
   renaming_language_suffix = ar    ← Your language
   
   [Embedding]
   embedding_language_code = ara    ← Your language code
   ```

3. **Install context menu:**
   - Double-click: `add_subfast_menu.reg`
   - Click "Yes"

---

### **5. Test**

Right-click in any folder → Look for **SubFast** menu with:
- Rename subtitles
- Embed subtitles

**✅ Done!**

---

## 📋 What Changed?

| Old (v2.x) | New (v3.0.0) |
|------------|--------------|
| `C:\rename_subtitles_to_match_videos_ar\` | `C:\subfast\` |
| Two separate context menu entries | One "SubFast" menu with 2 sub-items |
| `rename_subtitles_to_match_videos_ar.py` | `scripts/subfast_rename.py` |
| `embed_subtitles_to_match_videos_ar.py` | `scripts/subfast_embed.py` |
| Flat folder structure | Organized (scripts/, bin/, resources/) |

---

## ⚠️ Important Notes

- **NOT a drop-in replacement** - Must uninstall v2.x first
- **Config format changed** - Must update manually
- **Path must be `C:\subfast`** - Registry files require this exact path
- **Python 3.7+ still required** - No change from v2.x

---

## 📖 Need More Details?

See **CHANGELOG.md** on GitHub for:
- Complete feature list
- Detailed migration steps
- Configuration changes
- FAQ
- Known issues

See **README.md** on GitHub for:
- Installation guide
- Usage instructions
- Features overview
- Troubleshooting

---

## 💡 Quick Troubleshooting

**Context menu not appearing?**
→ Restart Windows Explorer or log out/in

**Python not found?**
→ Same as v2.x - ensure Python 3.7+ installed with `py.exe` launcher

**Old menu entries still there?**
→ Run old removal registry files again from v2.x folder

---

**Questions? Check GitHub for README.md, CHANGELOG.md, and this UPGRADE_GUIDE.md**
