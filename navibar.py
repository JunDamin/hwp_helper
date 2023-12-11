import customtkinter as ctk
from components import ToolTip

class NaviBar(ctk.CTkFrame):
    def __init__(self, parent, context, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = context["app"]
        self.context = context

        hwp_btn = ctk.CTkButton(
            self,
            text="한글보이기",
            command=context["helper"].check_hwp,
            width=80,
        )
        hwp_btn.grid(row=0, column=0, padx=2, pady=2)
        ToolTip(hwp_btn, text="연결되어 있는 한글을 보입니다. 연결된 한글이 없으면 새로 엽니다.")

        fullscreen_btn = ctk.CTkButton(
            self,
            text="전체화면",
            command=context["helper"].set_fullscreen,
            width=80,
        )
        fullscreen_btn.grid(row=0, column=1, padx=2, pady=2)
        ToolTip(fullscreen_btn, text="현재 앱 폭에 맞춰 전체화면으로 설정합니다.")

        halfscreen_btn = ctk.CTkButton(
            self,
            text="오른쪽화면",
            command=context["helper"].set_halfscreen,
            width=80,
        )
        halfscreen_btn.grid(row=0, column=2, padx=2, pady=2)
        ToolTip(halfscreen_btn, text="현재 앱 폭에 맞춰 화면의 절반으로 설정합니다.")




if __name__ == "__main__":
    from types import SimpleNamespace

    # create mockup
    d = {"set_fullscreen": 1, "set_halfscreen": 1, "check_hwp": 2}
    ns = SimpleNamespace(**d)

    root = ctk.CTk()
    root.geometry("800x800")
    context = {"app": None, "helper": ns, "template_frame": None}
    app = NaviBar(root, context)
    app.pack(fill="both", expand=True)
    root.mainloop()
