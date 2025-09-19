"""Main entry point for HWP Helper application."""

import flet as ft
import pythoncom

from hwp_helper.core.helper import HwpHelper
from hwp_helper.ui.main_window import MainWindow


def main(page: ft.Page) -> None:
    """Main application entry point."""
    # Initialize COM for HWP API
    pythoncom.CoInitialize()
    
    helper = None
    try:
        # Create helper and main window
        helper = HwpHelper(page)
        main_window = MainWindow(helper)
        
        # Set up page close handler
        def on_page_close(e):
            if helper:
                helper.on_closing()
            pythoncom.CoUninitialize()
        
        page.on_window_event = on_page_close
        
    except Exception as e:
        print(f"Error initializing application: {e}")
        page.add(ft.Text(f"Error: {e}"))
        # Clean up COM if initialization failed
        if helper:
            helper.on_closing()
        pythoncom.CoUninitialize()


if __name__ == "__main__":
    # Use absolute path for assets directory when running as script
    import os
    assets_dir = os.path.dirname(os.path.abspath(__file__))
    ft.run(main=main, assets_dir=assets_dir)