"""Main entry point for HWP Helper application."""

import flet as ft

from hwp_helper.core.helper import HwpHelper
from hwp_helper.ui.main_window import MainWindow


def main(page: ft.Page) -> None:
    """Main application entry point."""

    helper = None
    try:
        # Create helper and main window
        helper = HwpHelper(page)
        main_window = MainWindow(helper)
        
        # Set up page close handler
        def on_page_close(e):
            if helper:
                helper.on_closing()
        
        page.on_window_event = on_page_close
        
    except Exception as e:
        print(f"Error initializing application: {e}")
        page.add(ft.Text(f"Error: {e}"))
        # Clean up COM if initialization failed
        if helper:
            helper.on_closing()



if __name__ == "__main__":
    # Use absolute path for assets directory when running as script
    import os
    assets_dir = os.path.dirname(os.path.abspath(__file__))
    ft.run(main=main, assets_dir=assets_dir)