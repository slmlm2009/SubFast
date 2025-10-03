#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Subtitle Embedding Tool [AR] - Embed Subtitles into MKV Files

Automatically embeds subtitle files into corresponding MKV video files using mkvmerge.
Leverages intelligent pattern matching from the rename_subtitles_to_match_videos_ar.py
script to find matching pairs of videos and subtitles.

Features:
- Automatic video-subtitle file matching based on episode patterns
- Configurable mkvmerge.exe path
- Backup of original files (.original.mkv suffix)
- Batch processing of multiple files
- Language tag detection from subtitle filenames
- Windows context menu integration

Configuration:
Settings are read from config.ini in the script directory.
Key settings:
  - mkvmerge_path: Path to mkvmerge.exe (optional, defaults to script directory)
  - Default subtitle track properties (language, default flag)

Usage:
    python embed_subtitles_to_match_videos_ar.py [directory]
    python embed_subtitles_to_match_videos_ar.py --test-mkvmerge
    python embed_subtitles_to_match_videos_ar.py --version
"""

import os
import sys
import argparse
import configparser
import subprocess
from pathlib import Path

__version__ = "1.0.0"


def load_config():
    """
    Load configuration from config.ini file.
    
    Reads mkvmerge path and other settings from the [Embedding] section
    of config.ini. If the file doesn't exist or the setting is missing,
    uses sensible defaults.
    
    Returns:
        dict: Configuration dictionary with keys:
            - mkvmerge_path: Path to mkvmerge.exe (or None for default)
            - default_track: Whether subtitle track should be marked as default
            - language: Default language code for subtitle tracks
    """
    script_dir = Path(__file__).parent
    config_path = script_dir / 'config.ini'
    
    # Default configuration
    config_dict = {
        'mkvmerge_path': None,
        'default_track': True,
        'language': None
    }
    
    if not config_path.exists():
        print(f"[INFO] config.ini not found at {config_path}")
        print("[INFO] Using default configuration: mkvmerge.exe in script directory")
        return config_dict
    
    try:
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        
        # Read [Embedding] section
        if config.has_section('Embedding'):
            if config.has_option('Embedding', 'mkvmerge_path'):
                path = config.get('Embedding', 'mkvmerge_path').strip()
                if path:
                    config_dict['mkvmerge_path'] = path
            
            if config.has_option('Embedding', 'default_track'):
                config_dict['default_track'] = config.getboolean('Embedding', 'default_track')
            
            if config.has_option('Embedding', 'language'):
                lang = config.get('Embedding', 'language').strip()
                if lang:
                    config_dict['language'] = lang
        
        print(f"[INFO] Configuration loaded from: {config_path}")
        if config_dict['mkvmerge_path']:
            print(f"  mkvmerge path: {config_dict['mkvmerge_path']}")
        else:
            print(f"  mkvmerge path: (default - script directory)")
        
        return config_dict
        
    except Exception as e:
        print(f"[WARNING] Failed to parse config.ini: {e}")
        print("[INFO] Using default configuration")
        return config_dict


def validate_mkvmerge(mkvmerge_path=None):
    """
    Validate that mkvmerge.exe exists and is executable.
    
    Checks for mkvmerge at the specified path, or in the script directory
    if no path is provided. Runs 'mkvmerge --version' to verify it works.
    
    Args:
        mkvmerge_path: Optional path to mkvmerge.exe. If None, checks script directory.
    
    Returns:
        tuple: (success: bool, resolved_path: str or None, version_info: str or None)
    
    Examples:
        >>> validate_mkvmerge()
        (True, 'C:/path/to/mkvmerge.exe', 'mkvmerge v82.0')
        
        >>> validate_mkvmerge('/invalid/path')
        (False, None, None)
    """
    script_dir = Path(__file__).parent
    
    # Determine path to check
    if mkvmerge_path:
        mkvmerge_exe = Path(mkvmerge_path)
    else:
        mkvmerge_exe = script_dir / 'mkvmerge.exe'
    
    # Check if file exists
    if not mkvmerge_exe.exists():
        return False, None, None
    
    # Check if file is accessible (try to read it)
    if not os.access(mkvmerge_exe, os.R_OK):
        return False, str(mkvmerge_exe), None
    
    # Try to run mkvmerge --version
    try:
        result = subprocess.run(
            [str(mkvmerge_exe), '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            # Parse version from output (first line usually contains version)
            version_info = result.stdout.split('\n')[0] if result.stdout else "mkvmerge (version unknown)"
            return True, str(mkvmerge_exe), version_info
        else:
            return False, str(mkvmerge_exe), None
            
    except subprocess.TimeoutExpired:
        return False, str(mkvmerge_exe), None
    except FileNotFoundError:
        return False, str(mkvmerge_exe), None
    except Exception as e:
        print(f"[WARNING] Error running mkvmerge: {e}")
        return False, str(mkvmerge_exe), None


def find_matching_files(directory):
    """
    Find and match MKV video files with corresponding subtitle files.
    
    This function will be fully implemented in Story 2.1.
    Stub implementation returns empty list.
    
    Args:
        directory: Path to directory to scan for files
    
    Returns:
        list: List of tuples (video_file, subtitle_file)
    """
    # TODO: Implement in Story 2.1
    print("[INFO] find_matching_files() - stub implementation")
    return []


def build_mkvmerge_command(video_file, subtitle_file, output_file, config):
    """
    Build mkvmerge command line for embedding subtitle into video.
    
    This function will be fully implemented in Story 1.2.
    Stub implementation returns placeholder command.
    
    Args:
        video_file: Path to source video file
        subtitle_file: Path to subtitle file to embed
        output_file: Path for output merged file
        config: Configuration dictionary
    
    Returns:
        list: Command line arguments for subprocess
    """
    # TODO: Implement in Story 1.2
    print("[INFO] build_mkvmerge_command() - stub implementation")
    return []


def run_command(command):
    """
    Execute a command using subprocess and return the result.
    
    Args:
        command: List of command arguments to execute
    
    Returns:
        tuple: (success: bool, stdout: str, stderr: str)
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout for mkvmerge operations
        )
        
        success = (result.returncode == 0)
        return success, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out after 5 minutes"
    except Exception as e:
        return False, "", str(e)


def generate_report(processed_files, output_path):
    """
    Generate CSV report of embedding operations.
    
    This function will be fully implemented in Story 3.3.
    Stub implementation does nothing.
    
    Args:
        processed_files: List of processed file information
        output_path: Path where CSV report should be saved
    """
    # TODO: Implement in Story 3.3
    print("[INFO] generate_report() - stub implementation")
    pass


def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Embed subtitle files into MKV video files using mkvmerge',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    Process files in current directory
  %(prog)s /path/to/videos    Process files in specified directory
  %(prog)s --test-mkvmerge    Test mkvmerge connectivity
  %(prog)s --version          Show script version
        """
    )
    
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory containing video and subtitle files (default: current directory)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    parser.add_argument(
        '--test-mkvmerge',
        action='store_true',
        help='Test mkvmerge connectivity and exit'
    )
    
    return parser.parse_args()


def main():
    """
    Main entry point for the subtitle embedding script.
    
    Workflow:
    1. Parse command-line arguments
    2. Load configuration
    3. Validate mkvmerge
    4. Find matching files (if not in test mode)
    5. Process each file pair
    6. Generate report
    """
    print("=" * 60)
    print("Subtitle Embedding Tool [AR]")
    print(f"Version {__version__}")
    print("=" * 60)
    print()
    
    # Parse arguments
    args = parse_arguments()
    
    # Load configuration
    config = load_config()
    print()
    
    # Validate mkvmerge
    print("Validating mkvmerge...")
    success, mkvmerge_path, version_info = validate_mkvmerge(config['mkvmerge_path'])
    
    if not success:
        print("[ERROR] mkvmerge.exe not found or not executable")
        if mkvmerge_path:
            print(f"  Checked path: {mkvmerge_path}")
        else:
            script_dir = Path(__file__).parent
            print(f"  Checked path: {script_dir / 'mkvmerge.exe'}")
        print("\nPlease ensure:")
        print("  1. MKVToolNix is installed")
        print("  2. mkvmerge.exe is in the script directory, OR")
        print("  3. mkvmerge_path is correctly set in config.ini [Embedding] section")
        return 1
    
    print(f"[OK] {version_info}")
    print(f"  Path: {mkvmerge_path}")
    print()
    
    # If test mode, exit here
    if args.test_mkvmerge:
        print("[SUCCESS] mkvmerge connectivity test passed")
        return 0
    
    # Validate target directory
    target_dir = Path(args.directory).resolve()
    if not target_dir.exists():
        print(f"[ERROR] Directory does not exist: {target_dir}")
        return 1
    
    if not target_dir.is_dir():
        print(f"[ERROR] Path is not a directory: {target_dir}")
        return 1
    
    print(f"Target directory: {target_dir}")
    print()
    
    # TODO: Implement file processing in future stories
    print("[INFO] File processing will be implemented in Story 2.1 and beyond")
    print("[INFO] This is the base script structure - embedding functionality coming soon")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
