import flet as ft
import yaml
from functions import (
    check_app, 
    get_path, 
    get_screen_size, 
)
from pathlib import Path
import pythoncom
from core import Helper
from features import HwpFeatureFrame
from templates import CategoryFrame
from navibar import NaviBar

VERSION = "0.3.3"
TEMPLATES_DIR = "templates"
IMAGES_DIR = "images"
ICON_PATH = "src/ai.ico"
AI_IMAGE_PATH = "src/ai.png"

def main(page: ft.Page):
    pythoncom.CoInitialize()
    page.title = f"Hwp Helper v.{VERSION}"

    with open("setting.yaml", encoding='utf-8') as f:
        settings = yaml.safe_load(f)

    app = check_app(None)
    
    # Create context
    context = {
        "app": app,
        "setting": settings
    }

    # Initialize helper
    helper = Helper(page, context)
    
    def on_closing(e):
        helper.on_closing()
        page.window_destroy()

    page.on_window_event = on_closing

    # Create main components
    features_frame = HwpFeatureFrame(context)
    templates_frame = CategoryFrame(context)
    navi_bar = NaviBar(context)

    # Create tabs
    tabs = ft.Tabs(
        selected_index=settings.get("tab", 0),
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Features",
                content=features_frame,
            ),
            ft.Tab(
                text="Templates",
                content=templates_frame,
            ),
        ],
        expand=1,
    )

    # Main layout
    page.add(
        ft.Row([
            ft.Image(src=get_path(AI_IMAGE_PATH), width=50, height=50),
            ft.Text(page.title),
            ft.Container(expand=True),
            navi_bar
        ]),
        tabs,
    )

    # Initial window size and position
    x, y, width, height = get_screen_size()
    app_width = settings.get("app_width", 674)
    app_x, app_y = x + width - app_width, y
    page.window_left = app_x
    page.window_top = app_y
    page.window_width = app_width
    page.window_height = height

    page.update()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="C:\\Users\\freed\\Documents\\python_projects\\008_hwp_helper")
