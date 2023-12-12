import customtkinter as ctk
from components import ToolTip

class NaviBar(ctk.CTkFrame):
    """
    Navigation bar with buttons for various actions including showing the main app, 
    fullscreen, half-screen modes, and toggling 'always on top' state.
    """

    def __init__(self, parent, context, **kwargs):
        super().__init__(parent, **kwargs)
        self.context = context
        self.always_on_top = False

        self._create_hwp_button()
        self._create_fullscreen_button()
        self._create_halfscreen_button()
        self._create_always_on_top_button()

    def _create_hwp_button(self):
        """ Create a button to show the main application window. """
        hwp_btn = ctk.CTkButton(self, text="한글보이기", command=self.context["helper"].check_hwp, width=80)
        hwp_btn.grid(row=0, column=0, padx=2, pady=2)
        ToolTip(hwp_btn, text="연결되어 있는 한글을 보입니다. 연결된 한글이 없으면 새로 엽니다.")

    def _create_fullscreen_button(self):
        """ Create a button to set the application to fullscreen. """
        fullscreen_btn = ctk.CTkButton(self, text="전체화면", command=self.context["helper"].set_fullscreen, width=80)
        fullscreen_btn.grid(row=0, column=1, padx=2, pady=2)
        ToolTip(fullscreen_btn, text="현재 앱 폭에 맞춰 전체화면으로 설정합니다.")

    def _create_halfscreen_button(self):
        """ Create a button to set the application to half-screen. """
        halfscreen_btn = ctk.CTkButton(self, text="오른쪽화면", command=self.context["helper"].set_halfscreen, width=80)
        halfscreen_btn.grid(row=0, column=2, padx=2, pady=2)
        ToolTip(halfscreen_btn, text="현재 앱 폭에 맞춰 화면의 절반으로 설정합니다.")


    def _create_always_on_top_button(self):
        """ Create a button to toggle 'always on top' state. """
        self.always_on_top_btn = ctk.CTkButton(self, text="항상 위", command=self._toggle_always_on_top, width=80)
        self.always_on_top_btn.grid(row=0, column=3, padx=2, pady=2)
        ToolTip(self.always_on_top_btn, text="창을 항상 위에 놓습니다.")

    def _toggle_always_on_top(self):
        """ Toggle the 'always on top' state of the window. """
        self.always_on_top = not self.always_on_top
        self.context["helper"].attributes('-topmost', self.always_on_top)
        self._update_always_on_top_button_text()
        self.context["helper"]._setup_initial_windows()

    def _update_always_on_top_button_text(self):
        """ Update the text of the 'always on top' button based on its state. """
        if self.always_on_top:
            self.always_on_top_btn.configure(text="항상 위 취소")
        else:
            self.always_on_top_btn.configure(text="항상 위")




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
