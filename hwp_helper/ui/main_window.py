"""Main application window."""

import flet as ft
from typing import Dict, Any

from .components.navigation import NavigationBar
from .pages.features import FeaturesPage
from .pages.templates import TemplatesPage
from ..utils.window_utils import get_screen_size
from ..utils.file_utils import get_path


class MainWindow:
    """Main application window manager."""

    def __init__(self, helper):
        self.helper = helper
        self.page = helper.page
        self.context = helper.get_context()
        self._setup_window()
        self._create_ui()

    def _setup_window(self) -> None:
        """Setup window properties."""
        # Set window icon if available
        icon_path = get_path("src/ai.ico")
        if icon_path:
            self.page.window_icon = icon_path
        
        # Set initial window position and size
        x, y, width, height = get_screen_size()
        app_width = self.helper.config.get("app_width", 674)
        app_x, app_y = x + width - app_width, y
        
        self.page.window_left = app_x
        self.page.window_top = app_y
        self.page.window_width = app_width
        self.page.window_height = height
        
        # Set window event handlers
        self.page.on_window_event = self._on_window_event
        
        # Restore always on top setting
        always_on_top = self.helper.config.get("window_always_on_top", False)
        self.page.window_always_on_top = always_on_top

    def _create_ui(self) -> None:
        """Create the main UI components."""
        # Create navigation bar
        nav_bar = NavigationBar(self.context)
        
        # Create pages
        features_page = FeaturesPage(self.context)
        templates_page = TemplatesPage(self.context)
        
        # For now, just show features page (simplified navigation)
        self.current_page = features_page
        self.features_page = features_page
        self.templates_page = templates_page
        
        # Create navigation buttons
        nav_buttons = ft.Row([
            ft.ElevatedButton(content=ft.Text("Features"), on_click=self._show_features),
            ft.ElevatedButton(content=ft.Text("Templates"), on_click=self._show_templates),
        ])
        
        # Create header with logo and navigation
        ai_image_path = get_path("src/ai.png")
        header = ft.Row([
            ft.Image(src=ai_image_path, width=50, height=50) if ai_image_path else ft.Container(),
            ft.Text(self.page.title, size=16, weight=ft.FontWeight.BOLD),
            ft.Container(expand=True),
            nav_bar
        ])
        
        # Create main content area
        self.main_content = ft.Container(content=self.current_page, expand=True)
        
        # Add components to page
        self.page.add(header, nav_buttons, self.main_content)
        self.page.update()

    def _show_features(self, e) -> None:
        """Show features page."""
        self.current_page = self.features_page
        self.main_content.content = self.current_page
        self.page.update()
    
    def _show_templates(self, e) -> None:
        """Show templates page."""
        self.current_page = self.templates_page
        self.main_content.content = self.current_page
        self.page.update()

    def _on_window_event(self, e) -> None:
        """Handle window events."""
        if e.data == "close":
            # Handle closing
            self.helper.on_closing()
            self.page.window_destroy()
