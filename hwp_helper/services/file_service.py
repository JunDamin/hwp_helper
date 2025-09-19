"""File service for file operations."""

from pathlib import Path
from typing import Optional

from ..utils.file_utils import get_path


class FileService:
    """Service for file operations."""
    
    @staticmethod
    def get_asset_path(relative_path: str) -> Optional[str]:
        """Get absolute path for an asset file."""
        return get_path(relative_path)
    
    @staticmethod
    def ensure_directory_exists(directory: str) -> Path:
        """Ensure a directory exists and return Path object."""
        path = Path(directory)
        path.mkdir(exist_ok=True)
        return path
    
    @staticmethod
    def get_template_path(filename: str) -> Path:
        """Get path for a template file."""
        return Path("templates") / f"{filename}.hwp"
    
    @staticmethod
    def get_image_path(filename: str) -> Path:
        """Get path for an image file."""
        return Path("images") / f"{filename}.png"
