import customtkinter as ctk
import tkinter as tk
from PIL import Image
import yaml
from functions import (
    get_screen_size,
    set_window_position,
    get_window_position,
    get_ratio,
    get_path,
)
from features import HwpFeatureFrame
from templates import CategoryFrame
from navibar import NaviBar
import win32gui as wg


class Helper(ctk.CTk):
    def __init__(self, context):
        super().__init__()

        self.version = "Hwp Helper v.0.2.1"
        self.context = context

        context["helper"] = self

        # Override the default close behavior
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title(self.version)
        self.iconbitmap(get_path("src/ai.ico"))

        # set app
        self.app = context["app"]

        # set navi bar

        self.menu = ctk.CTkFrame(self)
        self.menu.pack(fill=tk.X)

        tabview = ctk.CTkTabview(master=self)
        tabview.pack(padx=20, pady=20, fill="both", expand=True)
        context["tabview"] = tabview
        
        tabview.add("templates")  # add tab at the end
        tabview.add("features")  # add tab at the end
        tabview.set("features")  # set currently visible tab

        # set category frame
        template_frame = CategoryFrame(tabview.tab("templates"), context)
        template_frame.pack(fill="both", expand=True)
        context["template_frame"] = template_frame

        # set feature frame
        feature_frame = HwpFeatureFrame(tabview.tab("features"), context)
        feature_frame.pack(fill="both", expand=True)
        context["feature_frame"] = feature_frame

        icon = ctk.CTkLabel(
            self.menu,
            text="",
            image=ctk.CTkImage(Image.open(get_path("src/ai.png")), size=(50, 50)),
            compound="left",
        )
        icon.pack(anchor="w", side=tk.LEFT, padx=5, pady=5)
        header = ctk.CTkLabel(
            self.menu,
            text=self.version,
        )
        header.pack(anchor="w", side=tk.LEFT, padx=5, pady=5)

        navi_bar = NaviBar(self.menu, context)
        navi_bar.pack(anchor="e", side=tk.RIGHT)
        context["navi_bar"] = navi_bar

    def set_windows(self, left, top, width, height):
        ratio = get_ratio(self)
        self.geometry(f"{int(width*ratio)}x{int(height*ratio)}+{int(left)}+{int(top)}")

    def set_fullscreen(self, ratio=None):
        setting = self.context["setting"]
        app_width = setting.get("app_width", 800)
        side = setting.get("side", "left")
        _, _, app_width, _ = self.get_window()
        setting["app_width"] = app_width

        x, y, width, height = get_screen_size()
        hwp_ratio = (width - app_width) / width
        hwp_width = int(width * hwp_ratio)

        hwp_x, hwp_y = x + int(width * (1 - hwp_ratio)), y
        app_x, app_y = x, y

        if side == "left":
            hwp_x, hwp_y = x, y
            app_x, app_y = x + hwp_width, y

        if self.app:
            set_window_position(self.app.get_hwnd(), hwp_x, hwp_y, hwp_width, height)
        self.set_window(app_x, app_y, width=(width - hwp_width), height=height)


    def set_window(self, x, y, width, height):
        self.update_idletasks()
        hwnd = wg.GetParent(self.winfo_id())
        set_window_position(hwnd, x, y, width, height)
        

    def get_window(self):
        self.update_idletasks()
        hwnd = wg.GetParent(self.winfo_id())
        return get_window_position(hwnd)
        
         
    def on_closing(self):
        with open("setting.yaml", "w") as f:
            yaml.safe_dump(self.context["setting"], f)
        self.destroy()


if __name__ == "__main__":
    context = {"app": None}
    with open("setting.yaml", encoding='utf-8') as f:
        context["setting"] = yaml.safe_load(f)
    app = Helper(context)
    app.set_fullscreen()
    app.mainloop()
