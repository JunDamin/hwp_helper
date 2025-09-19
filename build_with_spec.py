#!/usr/bin/env python3
"""
Build script using the updated hwp_helper.spec file.
This ensures proper COM packaging with PyInstaller.
"""

import subprocess
import sys
import os
from pathlib import Path

def build_with_spec():
    """Build the application using the hwp_helper.spec file."""
    
    # Ensure we're in the project directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Check if spec file exists
    spec_file = project_root / "hwp_helper.spec"
    if not spec_file.exists():
        print(f"Error: {spec_file} not found!")
        return False
    
    # Build command using the spec file
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",  # Clean PyInstaller cache
        str(spec_file)
    ]
    
    print("Building with PyInstaller using hwp_helper.spec...")
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
                print(f"Size: {exe_files[0].stat().st_size / (1024*1024):.1f} MB")
        
    except subprocess.CalledProcessError as e:
        print("Build failed!")
        print("Error:", e.stderr)
        print("Output:", e.stdout)
        return False
    
    return True

def clean_build():
    """Clean build artifacts."""
    project_root = Path(__file__).parent
    
    # Directories to clean
    clean_dirs = ['build', 'dist', '__pycache__']
    
    for dir_name in clean_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"Cleaning {dir_path}")
            import shutil
            shutil.rmtree(dir_path, ignore_errors=True)
    
    # Clean .pyc files
    for pyc_file in project_root.rglob("*.pyc"):
        pyc_file.unlink(missing_ok=True)
    
    print("Clean completed.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Build HWP Helper with PyInstaller")
    parser.add_argument("--clean", action="store_true", help="Clean build artifacts before building")
    parser.add_argument("--clean-only", action="store_true", help="Only clean build artifacts")
    
    args = parser.parse_args()
    
    if args.clean_only:
        clean_build()
        sys.exit(0)
    
    if args.clean:
        clean_build()
    
    success = build_with_spec()
    sys.exit(0 if success else 1)
