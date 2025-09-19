"""File utility functions."""

import os
import sys
import re
from pathlib import Path
from typing import Optional


def prettify_filename(name: str) -> str:
    """Clean and prettify a filename by removing invalid characters."""
    result = re.sub(r"[!\"\$\&\'\*\+\,/:;<=>\?@\\^_`{|}~\n]", "_", name)
    return re.sub(r" +", r" ", result)


def get_path(path: str) -> Optional[str]:
    """Get absolute path for a resource file."""
    if not path:
        return None
    
    if getattr(sys, "frozen", False):
        # Running as compiled executable
        base_dir = sys._MEIPASS
    else:
        # Running as script
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_dir, path)
