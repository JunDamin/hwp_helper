#!/usr/bin/env python3
"""
Alternative build script using flet pack instead of flet build.
"""

import subprocess
import sys
import os
from pathlib import Path

def build_with_flet_pack():
    """Build the application using flet pack."""
    
    # Ensure we're in the project directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Build command with comprehensive options for COM support
    cmd = [
        sys.executable, "-m", "flet", "pack",
        "main.py",
        "--name", "HwpHelper",
        "--icon", "src/ai.ico",
        "--add-data", "src;src",
        "--hidden-import", "pywintypes", 
        "--hidden-import", "win32com.client",
        "--hidden-import", "win32timezone",
        "--collect-all", "pywin32",
        "--collect-all", "pywintypes",
        "--onefile",
        "--windowed"
    ]
    
    print("Building with flet pack...")
    print("Command:", " ".join(cmd))
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build successful!")
        print("Output:", result.stdout)
        
        # Show the location of the built executable
        dist_dir = project_root / "dist"
        if dist_dir.exists():
            exe_files = list(dist_dir.glob("*.exe"))
            if exe_files:
                print(f"Executable created: {exe_files[0]}")
        
    except subprocess.CalledProcessError as e:
        print("Build failed!")
        print("Error:", e.stderr)
        print("Output:", e.stdout)
        return False
    
    return True

if __name__ == "__main__":
    success = build_with_flet_pack()
    sys.exit(0 if success else 1)
