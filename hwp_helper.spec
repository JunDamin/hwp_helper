# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

block_cipher = None

# Add project root to path for imports
project_root = Path(os.getcwd())
sys.path.insert(0, str(project_root))

# Collect pywin32 system32 files
pywin32_system32_datas = []
try:
    import pywin32_system32
    if hasattr(pywin32_system32, '__file__') and pywin32_system32.__file__:
        pywin32_path = os.path.dirname(pywin32_system32.__file__)
        pywin32_system32_datas = [(pywin32_path, 'pywin32_system32')]
except (ImportError, AttributeError, TypeError):
    pass

a = Analysis(
    ['main.py'],  # Updated to use main.py instead of hwp_helper.py
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        ('src', 'src'),
        # Add hwp_helper package data
        ('hwp_helper', 'hwp_helper'),
    ] + pywin32_system32_datas,
    hiddenimports=[
        # COM and Windows API imports
        'pythoncom',
        'pywintypes', 
        'win32com.client',
        'win32com.server',
        'win32timezone',
        'win32api',
        'win32gui',
        'win32con',
        'win32com.shell',
        'win32com.propsys',
        'win32com.taskscheduler',
        # Flet and application imports
        'flet',
        'hwpapi',
        'hwpapi.core',
        # Our application modules
        'hwp_helper.core.helper',
        'hwp_helper.core.app_manager',
        'hwp_helper.ui.main_window',
        'hwp_helper.utils.com_utils',
        'hwp_helper.utils.window_utils',
        'hwp_helper.services.template_service',
    ],
    hookspath=['hooks'],  # Use our custom hooks directory
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='HwpHelper',  # Updated name to match project
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[
        # Exclude COM-related DLLs from UPX compression to avoid issues
        'pythoncom*.dll',
        'pywintypes*.dll',
    ],
    runtime_tmpdir=None,
    console=False,  # Windowed application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['src\\ai.ico'],
    version='version_info.txt' if os.path.exists('version_info.txt') else None,
)
