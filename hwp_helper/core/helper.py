"""Core helper functionality."""

import flet as ft
from pathlib import Path
from typing import Dict, Any

from .config import ConfigManager
from .app_manager import HwpAppManager
from ..utils.window_utils import get_screen_size, set_window_position


class HwpHelper:
    """Main helper class that coordinates all application functionality."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.config = ConfigManager()
        self.app_manager = HwpAppManager()
        
        self._setup_page()
        self._create_essential_folders()
    
    def _setup_page(self) -> None:
        """Setup the main page properties."""
        from .. import __version__
        self.page.title = f"Hwp Helper v.{__version__}"
    
    def _create_essential_folders(self) -> None:
        """Create essential directories if they don't exist."""
        Path("templates").mkdir(exist_ok=True)
        Path("images").mkdir(exist_ok=True)
    
    def get_context(self) -> Dict[str, Any]:
        """Get application context for components."""
        return {
            "helper": self,
            "page": self.page,
            "app": self.app_manager.app,
            "config": self.config,
            "app_manager": self.app_manager,
        }
    
    def on_closing(self) -> None:
        """Handle application closing."""
        # Save current tab state
        if hasattr(self.page, 'tabs') and self.page.tabs:
            self.config.set("tab", self.page.tabs.selected_index)
        
        # Save window always on top state
        self.config.set("window_always_on_top", self.page.window_always_on_top)
        
        # Save configuration
        self.config.save_config()
        
        # Clean up COM resources
        self.app_manager.cleanup()
    
    def set_fullscreen(self) -> None:
        """Set application to fullscreen mode."""
        self._ensure_hwp_ready()
        
        app_width = self.config.get("app_width", 674)
        x, y, width, height = get_screen_size()
        
        app_width = max(int(width / 4), app_width)
        hwp_width = width - app_width
        
        # Position HWP window
        if self.app_manager.app:
            set_window_position(
                self.app_manager.app.get_hwnd(),
                x, y, hwp_width, height
            )
        
        # Position helper window
        self.page.window_left = x + hwp_width
        self.page.window_top = y
        self.page.window_width = app_width
        self.page.window_height = height
        self.page.update()
    
    def set_halfscreen(self) -> None:
        """Set application to half-screen mode."""
        self._ensure_hwp_ready()
        
        app_width = self.config.get("app_width", 800)
        x, y, width, height = get_screen_size()
        
        x = x + int(width / 2)
        hwp_ratio = (width / 2 - app_width) / (width / 2)
        hwp_width = int(max(width / 2 * hwp_ratio, width / 4))
        
        # Position HWP window
        if self.app_manager.app:
            set_window_position(
                self.app_manager.app.get_hwnd(),
                x, y, hwp_width, height
            )
        
        # Position helper window
        self.page.window_left = x + hwp_width
        self.page.window_top = y
        self.page.window_width = int(width / 2 - hwp_width)
        self.page.window_height = height
        self.page.update()
    
    def _ensure_hwp_ready(self) -> None:
        """Ensure HWP is ready and visible."""
        self.app_manager.ensure_app_ready()
