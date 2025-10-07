ARCHIVED FILES - DO NOT SHIP
=============================

This folder contains files from development/testing that are NOT included in v3.0.0 production release.

ARCHIVED REGISTRY FILES (v2.x - Deprecated)
--------------------------------------------
- add_embed_subtitle_menu.reg (old individual menu)
- add_subtitle_rename_menu.reg (old individual menu)
- remove_embed_subtitle_menu.reg (old removal)
- remove_subtitle_rename_menu.reg (old removal)

Why Deprecated: v3.0.0 uses unified cascading menu under "SubFast" parent.

ARCHIVED INSTALLERS (Development Only - NOT Shipped)
----------------------------------------------------
- INSTALL_CONTEXT_MENU.bat
- UNINSTALL_CONTEXT_MENU.bat
- install_context_menu.ps1
- uninstall_context_menu.ps1

Why Not Shipped: Registry files (.reg) are simpler and more robust for C:\subfast installation.
Batch/PowerShell installers introduced complexity and are not needed for standard installation.

CURRENT APPROACH (v3.0.0 Production)
-------------------------------------
Use the registry files in the parent folder:
- add_subfast_menu.reg (for installation at C:\subfast)
- remove_subfast_menu.reg (for uninstallation)

Requirements: Extract to C:\subfast, double-click .reg file. Simple and reliable.

FOR REFERENCE ONLY - DO NOT DISTRIBUTE THESE ARCHIVED FILES
