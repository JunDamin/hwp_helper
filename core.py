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
    check_app,
    set_forewindow,
    show_window,
)
from features import HwpFeatureFrame
from templates import CategoryFrame
from navibar import NaviBar
import win32gui as wg
from pathlib import Path


class Helper(ctk.CTk):
    def __init__(self, context):
        """
        이 코드는 "Hwp Helper v.0.2.1"라는 제목의 GUI 어플리케이션을 생성하는데 사용됩니다. 주로 tkinter, customtkinter, PIL, yaml, win32gui와 같은 여러 파이썬 라이브러리를 활용합니다. 이 코드는 주로 창을 만들고 설정하는데 중점을 두고 있습니다.

        class Helper(ctk.CTk): Helper라는 이름의 클래스는 ctk.CTk 클래스를 상속하며, 이 클래스는 tkinter의 Tk 클래스를 상속받아서 제작된 것입니다. 따라서 이 클래스는 창을 만들고 제어하는 메서드들을 가지고 있습니다.
        __init__(self, context): 이 메서드는 Helper 인스턴스를 초기화합니다. 여기서는 여러 가지 변수를 설정하고, 필요한 요소들을 화면에 배치합니다.
        set_windows(self, left, top, width, height): 이 메서드는 창의 위치와 크기를 설정합니다.
        set_fullscreen(self), set_halfscreen(self): 이 두 메서드는 창을 전체 화면으로 설정하거나, 화면의 절반 크기로 설정합니다.
        check_hwp(self): 이 메서드는 한/글 애플리케이션이 실행 중인지 확인하고, 실행 중이라면 그 애플리케이션을 최상위 창으로 만드는 역할을 합니다.
        set_window(self, x, y, width, height), get_window(self): 이 두 메서드는 창의 위치와 크기를 설정하거나 가져옵니다.
        on_closing(self): 이 메서드는 창이 닫힐 때 실행되는 메서드로, 설정을 저장하고 창을 파괴하는 역할을 합니다.
        """
        super().__init__()

        self.version = "Hwp Helper v.0.2.1"
        self.context = context

        # create essential folder
        Path("templates").mkdir(exist_ok=True)
        Path("images").mkdir(exist_ok=True)

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

        self.tabview = tabview = ctk.CTkTabview(master=self)
        tabview.pack(padx=1, pady=1, fill="both", expand=True)
        context["tabview"] = tabview

        tabview.add("templates")  # add tab at the end
        tabview.add("features")  # add tab at the end

        tabname = context["setting"].get("tab", "features")
        tabview.set(tabname)  # set currently visible tab

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
        check_app(self.app)
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

    def on_closing(self):
        current_tab = self.tabview.get()
        self.context["setting"]["tab"] = current_tab
        with open("setting.yaml", "w") as f:
            yaml.safe_dump(self.context["setting"], f)
        self.destroy()


if __name__ == "__main__":
    context = {"app": None}
    with open("setting.yaml", encoding="utf-8") as f:
        context["setting"] = yaml.safe_load(f)
    app = Helper(context)
    app.set_fullscreen()
    app.mainloop()
