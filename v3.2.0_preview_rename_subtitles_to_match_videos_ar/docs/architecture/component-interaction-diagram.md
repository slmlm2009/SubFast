# Component Interaction Diagram

**Note:** This diagram shows logical components and their interactions. "Common Components" represent shared logic patterns that exist within both standalone scripts (`subfast_rename.py` and `subfast_embed.py`), not separate module files.

```mermaid
graph TD
    subgraph "Common Components (Shared Logic Patterns)"
        CONFIG[Configuration Loader]
        FILEMATCH[File Matcher Engine]
        PATTERN[Pattern Recognition Engine]
        ERROR[Error Handler]
        CONSOLE[Smart Console Manager]
        CSV[CSV Reporter]
    end
    
    subgraph "subfast_rename.py Specific"
        RENMAIN[Main Entry Point]
        RENPROC[Renaming Processor]
    end
    
    subgraph "subfast_embed.py Specific"
        EMBMAIN[Main Entry Point]
        EMBPROC[Embedding Processor]
        CMDBUILD[Command Builder]
        PROCRUN[Process Runner]
    end
    
    RENMAIN --> CONFIG
    RENMAIN --> FILEMATCH
    FILEMATCH --> PATTERN
    RENMAIN --> RENPROC
    RENPROC --> ERROR
    RENPROC --> CSV
    RENMAIN --> CONSOLE
    
    EMBMAIN --> CONFIG
    EMBMAIN --> FILEMATCH
    FILEMATCH --> PATTERN
    EMBMAIN --> EMBPROC
    EMBPROC --> CMDBUILD
    EMBPROC --> PROCRUN
    EMBPROC --> ERROR
    EMBPROC --> CSV
    EMBMAIN --> CONSOLE
```

---
