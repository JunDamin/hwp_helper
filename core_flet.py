import flet as ft
import yaml
from functions import (
    get_screen_size, set_window_position, get_window_position,
    get_path, check_app, set_forewindow, show_window,
)
from pathlib import Path

VERSION = "0.3.3"
TEMPLATES_DIR = "templates"
IMAGES_DIR = "images"
ICON_PATH = "src/ai.ico"
AI_IMAGE_PATH = "src/ai.png"


class Helper:
    def __init__(self, page: ft.Page, context):
        self.page = page
        self.context = context
        self.app = context["app"]
        self._setup_basic_attributes()
        self._create_essential_folders()
        
        context["helper"] = self

    def _setup_basic_attributes(self):
        self.version = f"Hwp Helper v.{VERSION}"
        self.page.title = self.version

    def _create_essential_folders(self):
        Path(TEMPLATES_DIR).mkdir(exist_ok=True)
        Path(IMAGES_DIR).mkdir(exist_ok=True)

    def on_closing(self):
        current_tab = self.page.tabs.selected_index if hasattr(self.page, 'tabs') else 0
        self.context["setting"]["tab"] = current_tab
        with open("setting.yaml", "w") as f:
            yaml.safe_dump(self.context["setting"], f)

    def set_fullscreen(self):
        self.check_hwp()

        setting = self.context["setting"]
        app_width = setting.get("app_width", 674)

        x, y, width, height = get_screen_size()
        app_width = max(int(width / 4), app_width)
        hwp_width = width - app_width

        hwp_x, hwp_y = x, y
        app_x, app_y = x + hwp_width, y

        if self.app:
            set_window_position(self.app.get_hwnd(), hwp_x, hwp_y, hwp_width, height)
        
        # Update Flet window position
        self.page.window_left = app_x
        self.page.window_top = app_y
        self.page.window_width = width - hwp_width
        self.page.window_height = height
        self.page.update()

    def set_halfscreen(self):
        self.check_hwp()

        setting = self.context["setting"]
        app_width = setting.get("app_width", 800)

        x, y, width, height = get_screen_size()
        x = x + int(width / 2)
        hwp_ratio = (width / 2 - app_width) / (width / 2)
        hwp_width = int(max(width / 2 * hwp_ratio, width / 4))
        hwp_x, hwp_y = x, y
        app_x, app_y = x + hwp_width, y

        if self.app:
            set_window_position(self.app.get_hwnd(), hwp_x, hwp_y, hwp_width, height)
        
        # Update Flet window position
        self.page.window_left = app_x
        self.page.window_top = app_y
        self.page.window_width = int(width / 2 - hwp_width)
        self.page.window_height = height
        self.page.update()

    def check_hwp(self):
        app = check_app(self.app)
        set_forewindow(self.app)
        show_window(self.app)
