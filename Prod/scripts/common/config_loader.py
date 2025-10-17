"""
Configuration Loader Module

Handles loading, validation, and generation of config.ini for SubFast.
Provides unified configuration management for both renaming and embedding modules.

Version: 3.1.0
"""

import configparser
from pathlib import Path
from typing import Dict, List, Any


DEFAULT_CONFIG = {
    'renaming_report': False,
    'language_suffix': '',
    'video_extensions': ['mkv', 'mp4'],
    'subtitle_extensions': ['srt', 'ass'],
    'keep_console_open': False,
    'mkvmerge_path': 'bin\\mkvmerge.exe',
    'embedding_language_code': '',
    'default_flag': True,
    'embedding_report': False
}


def get_script_directory() -> Path:
    """Get the installation root directory (parent of scripts folder)"""
    return Path(__file__).parent.parent.parent


def create_default_config_file(config_path: Path) -> None:
    """
    Create unified config.ini with all sections.
    
    Args:
        config_path: Path where config file should be created
    """
    config_content = """# ============================================================================
# SubFast - Unified Configuration
# ============================================================================

[General]
# Video and subtitle file formats to process (comma-separated, no dots)
detected_video_extensions = mkv, mp4
detected_subtitle_extensions = srt, ass

# Console window behavior
# false = auto-close on success, stay open on errors (recommended)
# true = always wait for keypress before closing
keep_console_open = false

[Renaming]
# Enable CSV export of renaming operations (true/false)
renaming_report = true

# Language tag added to renamed files (e.g., 'ar', 'en', 'es')
# Leave empty for no language suffix
renaming_language_suffix = 

[Embedding]
# Path to mkvmerge.exe (relative to this config file or absolute path)
# Default uses bundled mkvmerge in bin/ directory
mkvmerge_path = bin\\mkvmerge.exe

# Language code for embedded subtitles (ISO 639-2 three-letter code)
# Leave empty to auto-detect from subtitle filename
# Examples: ara (Arabic), eng (English), fra (French), spa (Spanish)
embedding_language_code = 

# Mark embedded subtitle as default track (true/false)
default_flag = true

# Enable CSV export of embedding operations (true/false)
embedding_report = true
"""
    
    config_path.write_text(config_content, encoding='utf-8')


def parse_extensions(value: str) -> List[str]:
    """
    Parse comma-separated file extensions.
    
    Args:
        value: Comma-separated extension string (e.g., 'mkv, mp4, avi')
        
    Returns:
        List of lowercase extensions without dots
    """
    if not value:
        return []
    
    extensions = []
    for ext in value.split(','):
        ext = ext.strip().lower()
        ext = ext.lstrip('.')
        if ext and ext.replace('_', '').isalnum():
            extensions.append(ext)
    
    return extensions


def parse_boolean(value: str, default: bool = False) -> bool:
    """
    Parse boolean configuration value.
    
    Args:
        value: String value from config
        default: Default value if parsing fails
        
    Returns:
        Boolean value
    """
    if not value:
        return default
    
    value_lower = value.lower().strip()
    if value_lower in ('true', 'yes', '1', 'on'):
        return True
    elif value_lower in ('false', 'no', '0', 'off'):
        return False
    else:
        return default


def load_config(config_path: Path = None) -> Dict[str, Any]:
    """
    Load and validate configuration from config.ini.
    
    Creates default config if file doesn't exist.
    Uses safe defaults for any invalid values.
    
    Args:
        config_path: Path to config.ini (defaults to script directory)
        
    Returns:
        Dictionary with validated configuration values
    """
    if config_path is None:
        config_path = get_script_directory() / 'config.ini'
    
    if not config_path.exists():
        print(f"[INFO] config.ini not found. Creating default configuration at: {config_path}")
        create_default_config_file(config_path)
    
    config = configparser.ConfigParser()
    
    try:
        config.read(config_path, encoding='utf-8')
    except Exception as e:
        print(f"[WARNING] Failed to read config.ini: {e}")
        print("[INFO] Using default configuration")
        return DEFAULT_CONFIG.copy()
    
    config_dict = {}
    
    # [General] section
    try:
        video_exts = config.get('General', 'detected_video_extensions', fallback='mkv, mp4')
        config_dict['video_extensions'] = parse_extensions(video_exts) or DEFAULT_CONFIG['video_extensions']
        
        subtitle_exts = config.get('General', 'detected_subtitle_extensions', fallback='srt, ass')
        config_dict['subtitle_extensions'] = parse_extensions(subtitle_exts) or DEFAULT_CONFIG['subtitle_extensions']
        
        keep_open = config.get('General', 'keep_console_open', fallback='false')
        config_dict['keep_console_open'] = parse_boolean(keep_open, False)
    except Exception as e:
        print(f"[WARNING] Error parsing [General] section: {e}")
        config_dict['video_extensions'] = DEFAULT_CONFIG['video_extensions']
        config_dict['subtitle_extensions'] = DEFAULT_CONFIG['subtitle_extensions']
        config_dict['keep_console_open'] = DEFAULT_CONFIG['keep_console_open']
    
    # [Renaming] section
    try:
        renaming_report = config.get('Renaming', 'renaming_report', fallback='true')
        config_dict['renaming_report'] = parse_boolean(renaming_report, True)
        
        config_dict['language_suffix'] = config.get('Renaming', 'renaming_language_suffix', fallback='').strip()
    except Exception as e:
        print(f"[WARNING] Error parsing [Renaming] section: {e}")
        config_dict['renaming_report'] = DEFAULT_CONFIG['renaming_report']
        config_dict['language_suffix'] = DEFAULT_CONFIG['language_suffix']
    
    # [Embedding] section
    try:
        mkvmerge_path = config.get('Embedding', 'mkvmerge_path', fallback='bin\\mkvmerge.exe').strip()
        config_dict['mkvmerge_path'] = mkvmerge_path or DEFAULT_CONFIG['mkvmerge_path']
        
        config_dict['embedding_language_code'] = config.get('Embedding', 'embedding_language_code', fallback='').strip()
        
        default_flag = config.get('Embedding', 'default_flag', fallback='true')
        config_dict['default_flag'] = parse_boolean(default_flag, True)
        
        embedding_report = config.get('Embedding', 'embedding_report', fallback='true')
        config_dict['embedding_report'] = parse_boolean(embedding_report, True)
    except Exception as e:
        print(f"[WARNING] Error parsing [Embedding] section: {e}")
        config_dict['mkvmerge_path'] = DEFAULT_CONFIG['mkvmerge_path']
        config_dict['embedding_language_code'] = DEFAULT_CONFIG['embedding_language_code']
        config_dict['default_flag'] = DEFAULT_CONFIG['default_flag']
        config_dict['embedding_report'] = DEFAULT_CONFIG['embedding_report']
    
    return config_dict


def validate_and_load_config() -> Dict[str, Any]:
    """
    Load configuration with validation and user-friendly messages.
    
    Returns:
        Validated configuration dictionary
    """
    try:
        config = load_config()
        print(f"[INFO] Configuration loaded successfully")
        return config
    except Exception as e:
        print(f"[ERROR] Failed to load configuration: {e}")
        print("[INFO] Using default configuration")
        return DEFAULT_CONFIG.copy()
