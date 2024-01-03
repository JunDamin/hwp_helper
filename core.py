import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import yaml
from functions import (
    get_screen_size, set_window_position, get_window_position,
    get_ratio, get_path, check_app, set_forewindow, show_window,
)
from features import HwpFeatureFrame
from templates import CategoryFrame
from navibar import NaviBar
import win32gui as wg
from pathlib import Path

VERSION = "0.3.2"
TEMPLATES_DIR = "templates"
IMAGES_DIR = "images"
ICON_PATH = "src/ai.ico"
AI_IMAGE_PATH = "src/ai.png"


class Helper(ctk.CTk):
    def __init__(self, context):
        super().__init__()
        self.context = context
        self._setup_basic_attributes()
        self._create_essential_folders()
        self._setup_ui()

        self.app = context["app"]


        
        # create essential folder
        Path("templates").mkdir(exist_ok=True)
        Path("images").mkdir(exist_ok=True)
        
        
        context["helper"] = self




    def _setup_basic_attributes(self):
        self.version = f"Hwp Helper v.{VERSION}"
        self.context["helper"] = self
        self.title(self.version)
        self.iconbitmap(get_path(ICON_PATH))
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _create_essential_folders(self):
        Path(TEMPLATES_DIR).mkdir(exist_ok=True)
        Path(IMAGES_DIR).mkdir(exist_ok=True)

    def _setup_ui(self):
        self._setup_menu()
        self._setup_tabview()
        self._setup_frames()
        self._setup_navigation_bar()
        self._setup_initial_windows()

    def _setup_menu(self):
        self.menu = ctk.CTkFrame(self)
        self.menu.pack(fill=tk.X)
        self._setup_menu_contents()

    def _setup_menu_contents(self):
        icon_image = ImageTk.PhotoImage(Image.open(get_path(AI_IMAGE_PATH)).resize((50, 50)))
        icon = ctk.CTkLabel(self.menu, image=icon_image, text="")
        icon.image = icon_image  # keep a reference
        icon.pack(side=tk.LEFT, padx=5, pady=5)

        header = ctk.CTkLabel(self.menu, text=self.version)
        header.pack(side=tk.LEFT, padx=5, pady=5)

    def _setup_tabview(self):
        self.tabview = ctk.CTkTabview(master=self)
        self.tabview.pack(padx=1, pady=1, fill="both", expand=True)
        self.context["tabview"] = self.tabview
        self.tabview.add("templates")
        self.tabview.add("features")
        self._set_initial_tab()

    def _set_initial_tab(self):
        initial_tab = self.context["setting"].get("tab", "features")
        self.tabview.set(initial_tab)

    def _setup_frames(self):
        self._setup_template_frame()
        self._setup_feature_frame()

    def _setup_template_frame(self):
        template_frame = CategoryFrame(self.tabview.tab("templates"), self.context)
        template_frame.pack(fill="both", expand=True)
        self.context["template_frame"] = template_frame

    def _setup_feature_frame(self):
        feature_frame = HwpFeatureFrame(self.tabview.tab("features"), self.context)
        feature_frame.pack(fill="both", expand=True)
        self.context["feature_frame"] = feature_frame

    def _setup_navigation_bar(self):
        navi_bar = NaviBar(self.menu, self.context)
        navi_bar.pack(side=tk.RIGHT)
        self.context["navi_bar"] = navi_bar

    def _setup_initial_windows(self):
        _, _, app_width, _ = self.get_window()
        x, y, width, height = get_screen_size()
        app_x, app_y = x + width - app_width, y
        self.set_window(app_x, app_y, width=app_width, height=height)


    def on_closing(self):
        current_tab = self.tabview.get()
        self.context["setting"]["tab"] = current_tab
        with open("setting.yaml", "w") as f:
            yaml.safe_dump(self.context["setting"], f)
        self.destroy()

    def set_windows(self, left, top, width, height):
        ratio = get_ratio(self)
        self.geometry(f"{int(width*ratio)}x{int(height*ratio)}+{int(left)}+{int(top)}")

    def set_fullscreen(self):
        self.check_hwp()

        setting = self.context["setting"]

        app_width = setting.get("app_width", 674)

        _, _, app_width, _ = self.get_window()
        setting["app_width"] = app_width
        x, y, width, height = get_screen_size()

        app_width = max(int(width / 4), app_width)
        hwp_width = width - app_width

        hwp_x, hwp_y = x, y
        app_x, app_y = x + hwp_width, y

        if self.app:
            set_window_position(self.app.get_hwnd(), hwp_x, hwp_y, hwp_width, height)
        self.set_window(app_x, app_y, width=(width - hwp_width), height=height)

    def set_halfscreen(self):
        self.check_hwp()

        setting = self.context["setting"]
        app_width = setting.get("app_width", 800)
        _, _, app_width, _ = self.get_window()
        setting["app_width"] = app_width

        x, y, width, height = get_screen_size()
        x = x + int(width / 2)
        hwp_ratio = (width / 2 - app_width) / (width / 2)
        hwp_width = int(max(width / 2 * hwp_ratio, width / 4))
        hwp_x, hwp_y = x, y
        app_x, app_y = x + hwp_width, y

        if self.app:
            set_window_position(self.app.get_hwnd(), hwp_x, hwp_y, hwp_width, height)
        self.set_window(app_x, app_y, width=int(width / 2 - hwp_width), height=height)

    def check_hwp(self):
        app = check_app(self.app)
        set_forewindow(self.app)
        show_window(self.app)

    def set_window(self, x, y, width, height):
        self.update_idletasks()
        hwnd = wg.GetParent(self.winfo_id())
        set_window_position(hwnd, x, y, width, height)

    def get_window(self):
        self.update_idletasks()
        hwnd = wg.GetParent(self.winfo_id())
        return get_window_position(hwnd)



if __name__ == "__main__":
    from hwpapi.core import App
    
    context = {"app": App()}
    with open("setting.yaml", encoding="utf-8") as f:
        context["setting"] = yaml.safe_load(f)
    app = Helper(context)
    app.set_fullscreen()
    app.mainloop()
