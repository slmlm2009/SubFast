# Introduction

This document defines the complete architecture for SubFast v3.0.0, a Windows-based Python utility for automated subtitle management. SubFast provides two co-equal features:

1. **Subtitle Renaming**: Intelligent pattern-matching and automated renaming of subtitle files to match video filenames
2. **Subtitle Embedding**: Soft-subtitle embedding into MKV video files using mkvmerge integration

The architecture is designed for local execution on Windows 10/11 systems, prioritizing simplicity, performance, and reliability. SubFast operates as two standalone Python scripts integrated into Windows Explorer's context menu, requiring no server infrastructure, web interface, or complex deployment.

**Key Architectural Characteristics:**
- Standalone local execution (no client-server architecture)
- Windows-native integration via Registry
- Two independent but related command-line Python scripts
- Minimal dependencies (Python 3.7+, mkvmerge for embedding)
- File system-based operations with no database requirements
- Performance-optimized for batch processing (1000+ files in under 1 second for renaming)

**Starter Template:** N/A - Custom-built Windows utility

---
