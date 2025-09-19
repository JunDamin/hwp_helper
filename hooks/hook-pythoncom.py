"""
PyInstaller hook for pythoncom module.
This ensures proper packaging of COM-related modules.
"""

from PyInstaller.utils.hooks import collect_all, collect_data_files
import os

# Collect all pythoncom related modules
datas, binaries, hiddenimports = collect_all('pythoncom')

# Add additional COM-related hidden imports
hiddenimports += [
    'pythoncom',
    'pywintypes',
    'win32com.client',
    'win32com.server',
    'win32timezone',
]

# Collect pywin32 system32 files
try:
    import pywin32_system32
    if hasattr(pywin32_system32, '__file__') and pywin32_system32.__file__:
        pywin32_path = os.path.dirname(pywin32_system32.__file__)
        datas += [(pywin32_path, 'pywin32_system32')]
except (ImportError, AttributeError, TypeError):
    pass

# Collect additional data files for COM support
try:
    datas += collect_data_files('win32com')
except:
    pass
