# Tech Stack

## Core Technology Stack

| Category | Technology | Version | Purpose | Rationale |
|----------|-----------|---------|---------|-----------|
| **Primary Language** | Python | 3.7+ | Core scripting language | Strong file system libraries, subprocess management, regex support, and cross-platform potential |
| **Runtime** | Python Launcher | py.exe | Python script execution | Standard Windows Python launcher at `C:\Windows\py.exe` for .py file associations |
| **External Tool** | MKVToolNix (mkvmerge) | Latest Stable (bundled) | Matroska video muxing | Industry-standard tool for MKV manipulation; reliable soft-subtitle embedding |
| **Configuration Format** | INI File | config.ini | User configuration | Simple, human-readable format parsable by Python's `configparser` module |
| **OS Integration** | Windows Registry | .reg files | Context menu integration | Native Windows mechanism for shell extension without requiring COM DLL development |
| **File System Library** | Python pathlib | 3.7+ stdlib | Path operations | Modern, object-oriented path handling with Windows compatibility |
| **Subprocess Management** | Python subprocess | 3.7+ stdlib | mkvmerge execution | Standard library for safe external process invocation with list-based arguments |
| **Regex Engine** | Python re module | 3.7+ stdlib | Episode pattern matching | Built-in regex with compilation support for performance optimization |
| **CSV Export** | Python csv module | 3.7+ stdlib | Optional reporting | Standard library for Excel-compatible CSV generation |

## Development & Testing Tools

| Category | Technology | Version | Purpose | Rationale |
|----------|-----------|---------|---------|-----------|
| **Version Control** | Git | Any | Source control | Industry standard version control |
| **Testing Approach** | Manual + Unit Tests | Python unittest | Quality assurance | Manual testing for real-world validation; unit tests for critical pattern matching |
| **Code Editor** | Any Python IDE | - | Development | No specific IDE requirement |
| **Performance Profiling** | Python time module | stdlib | Execution timing | Built-in timing for performance metrics |

## Deployment & Distribution

| Category | Technology | Version | Purpose | Rationale |
|----------|-----------|---------|---------|-----------|
| **Package Format** | ZIP Archive | - | Distribution | Simple extraction to `C:\subfast\` |
| **Bundled Dependencies** | mkvmerge.exe | Latest | Embedded tool | Pre-bundled to eliminate user configuration complexity |
| **Installation** | Windows Registry | .reg files | Context menu setup | One-click installation via registry merge |

## Windows-Specific Considerations

**Python Launcher Requirement:**
- **Constraint:** Must be installed at `C:\Windows\py.exe`
- **Validation:** Scripts verify launcher existence at startup
- **Troubleshooting:** Clear error message if not found

**Registry Integration:**
- **Scope:** User-level or system-level (depending on admin rights)
- **Keys Modified:** `HKEY_CLASSES_ROOT\Directory\shell\SubFast`
- **Icon Support:** Uses `.ico` file for menu branding

**Subprocess Pattern:**
- **Critical:** Always use list-based arguments without `shell=True`
- **Reason:** Ensures compatibility with all Windows COMSPEC configurations
- **Example:** `subprocess.run([str(mkvmerge_path), '-o', str(output), ...])`

---
