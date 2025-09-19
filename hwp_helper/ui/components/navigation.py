"""Navigation bar component."""

import flet as ft
from typing import Dict, Any


class NavigationBar(ft.Container):
    """Navigation bar with buttons for various actions."""

    def __init__(self, context: Dict[str, Any], **kwargs):
        super().__init__(**kwargs)
        self.context = context
        self.helper = context["helper"]
        self.page = context["page"]
        
        self.content = ft.Row([
            ft.IconButton(
                icon=ft.Icons.VISIBILITY,
                on_click=self._show_hwp,
                tooltip="한글보이기"
            ),
            ft.IconButton(
                icon=ft.Icons.FULLSCREEN,
                on_click=self._set_fullscreen,
                tooltip="전체화면"
            ),
            ft.IconButton(
                icon=ft.Icons.FULLSCREEN_EXIT,
                on_click=self._set_halfscreen,
                tooltip="오른쪽화면"
            ),
            ft.IconButton(
                icon=ft.Icons.PUSH_PIN,
                on_click=self._toggle_always_on_top,
                tooltip="항상 위"
            ),
        ])

    def _show_hwp(self, e) -> None:
        """Show the HWP application window."""
        self.helper.app_manager.bring_to_foreground()

    def _set_fullscreen(self, e) -> None:
        """Set the application to fullscreen."""
        self.helper.set_fullscreen()

    def _set_halfscreen(self, e) -> None:
        """Set the application to half-screen."""
        self.helper.set_halfscreen()

    def _toggle_always_on_top(self, e) -> None:
        """Toggle the 'always on top' state of the window."""
        self.page.window_always_on_top = not self.page.window_always_on_top
        self.page.update()
