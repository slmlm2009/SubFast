# Next Steps

## UX Expert Prompt

SubFast v3.0.0 is primarily a command-line utility with Windows Explorer context menu integration. However, if you're considering adding a GUI configuration tool or installer wizard in the future:

**Prompt for UX Expert:**
"Review the SubFast PRD and consider UX improvements for:
1. Configuration management (potential GUI for config.ini editing)
2. Installation wizard to simplify setup process
3. Progress visualization for large batch operations
4. Error reporting and recovery flows
Please create a UI/UX specification if GUI components are desired for future versions."

## Architect Prompt

**Prompt for Architect:**
"Using this SubFast v3.0.0 PRD as input, create a comprehensive architecture document that covers:

1. **Current v3.0.0 Architecture:**
   - Detailed component breakdown for `subfast_rename.py` and `subfast_embed.py`
   - Module architecture and function responsibilities
   - Data flow diagrams for both renaming and embedding workflows
   - Configuration loading and validation architecture
   - File matching engine architecture with caching strategy
   - Subprocess management for mkvmerge integration
   - Error handling and recovery architecture

2. **Technical Implementation Details:**
   - Python module organization and imports
   - Windows Registry integration specifics
   - mkvmerge command building with list-based subprocess pattern
   - Backup management and atomic file operations
   - Performance optimization strategies (regex compilation, caching)
   - CSV reporting architecture

3. **Deployment and Infrastructure:**
   - Installation directory structure and file organization
   - Python Launcher dependency and validation
   - mkvmerge bundling vs. system installation
   - Registry file generation and maintenance

4. **Testing Strategy:**
   - Unit test requirements for pattern matching
   - Integration test scenarios with sample files
   - Manual testing procedures
   - Real-world validation datasets

Please ensure the architecture reflects SubFast as a complete dual-feature product with the correct v3.0.0 structure and paths (C:\subfast\, scripts/ folder, etc.)."

---

**End of PRD**
