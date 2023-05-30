import customtkinter as ctk
from functions import (
    update_templates,
)

class NaviBar(ctk.CTkFrame):
    def __init__(self, parent, context, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = context["app"]
        self.context = context

        update_btn = ctk.CTkButton(
            self, text="update template", command=self.update_templates
        )
        update_btn.pack(side="left", padx=10, pady=10)

        fullscreen_btn = ctk.CTkButton(
            self, text="full screen", command=context["helper"].set_fullscreen
        )
        fullscreen_btn.pack(side="left", padx=10, pady=10)

    def update_templates(self):
        toplevel = UpdateTemplateForm(
            self, self.context["template_frame"]
        )  # master argument is optional
        toplevel.focus()


class UpdateTemplateForm(ctk.CTkToplevel):
    def __init__(self, parent, template_form):
        super().__init__(parent)
        self.guide = ctk.CTkLabel(
            self,
            text="""update 버튼을 누르면 templates 폴더에 있는 한글 파일을 template화 하여 넣어 놓습니다. 
            분류하는 방법은 언더바를 기준으로 진행되며 언더바 이전의 단어는 카테고리로, 그 이후 단어는 이름으로 사용하게 됩니다.""",
            wraplength=300,
            justify="left",
        )
        self.guide.pack(pady=5, padx=5)
        self.template_form = template_form

        self.update_btn = ctk.CTkButton(
            self, text="update", command=self.update_templates
        )
        self.update_btn.pack(pady=5)

    def update_templates(self):
        self.update_btn.destroy()

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(padx=10, pady=10)
        self.progress_bar.set(0)
        self.update()

        # new window and progress bar
        for i, n in update_templates():
            progress = i / (n - 1)
            self.progress_bar.set(progress)
            self.update()

        self.progress_bar.pack_forget()

        self.template_form.refresh()

        self.destroy()


if __name__=="__main__":
    
    from types import SimpleNamespace
    # create mockup
    d = {'set_fullscreen': 1, 'b': 2}
    ns = SimpleNamespace(**d)

    root = ctk.CTk()
    root.geometry("800x800")
    context = {"app": None, "helper": ns}
    app = NaviBar(root, context)
    app.pack(fill="both", expand=True)
    root.mainloop()