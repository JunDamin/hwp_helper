import customtkinter as ctk
import tkinter as tk
from functions import (
    update_templates,
    update_template,
    prettify_filename,
    get_categories,
    make_topmost
)
from components import CollapsibleFrame, TemplateControl, AddTemplateForm

class NaviBar(ctk.CTkFrame):
    def __init__(self, parent, context, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = context["app"]
        self.context = context

        update_btn = ctk.CTkButton(
            self, text="탬플릿 관리", command=self.update_templates
        )
        update_btn.pack(side="left", padx=10, pady=10)

        add_template_btn = ctk.CTkButton(
            self, text="선택영역 탬플릿으로 추가하기", command=self.add_template
        )
        add_template_btn.pack(side="left", padx=10, pady=10)

        fullscreen_btn = ctk.CTkButton(
            self, text="전체화면", command=context["helper"].set_fullscreen
        )
        fullscreen_btn.pack(side="left", padx=10, pady=10)

    def update_templates(self):
        toplevel = UpdateTemplateForm(
            self, self.context["template_frame"], 
        )  # master argument is optional
        toplevel.focus()

    def add_template(self):
        toplevel = AddTemplateForm(self, self.context)
        toplevel.focus()

class UpdateTemplateForm(ctk.CTkToplevel):
    def __init__(self, parent, template_form, **kwargs):
        super().__init__(parent, **kwargs)

        self.geometry("800x1000")

        self.guide = ctk.CTkLabel(
            self,
            text="""update 버튼을 누르면 templates 폴더에 있는 한글 파일을 template화 하여 넣어 놓습니다. 
            분류하는 방법은 언더바를 기준으로 진행되며 언더바 이전의 단어는 카테고리로, 그 이후 단어는 이름으로 사용하게 됩니다.""",
            wraplength=600,
            justify="left",
        )
        self.guide.pack(pady=5, padx=5)
        self.template_form = template_form

        self.update_btn = ctk.CTkButton(
            self, text="update", command=self.update_templates
        )
        self.update_btn.pack(pady=5)

        self.template_frame = ctk.CTkScrollableFrame(self)
        self.template_frame.pack(fill="both", expand=True)

        self.set_frame()
        make_topmost(self)

    def set_frame(self):
        # get categrory data from packages
        categories = get_categories()
        for key, value in categories.items():
            cframe = CollapsibleFrame(self.template_frame, key)
            cframe.pack(fill=tk.X, pady=5, padx=5, anchor='w')

            for text, image_path, filename, n in value:
                path = f"templates/{filename}.hwp"

                # create button
                TemplateControl(
                    cframe.frame_contents,
                    text=text,
                    file_path=path,
                    image_path=image_path,
                    target_frame=self,
                ).pack(fill=tk.X, pady=5, padx=5, anchor='w')
    
    def refresh(self):
        for child in self.template_frame.winfo_children():
            child.destroy()

        self.set_frame()
        self.template_form.refresh()

    

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
    context = {"app": None, "helper": ns, "template_frame": None}
    app = NaviBar(root, context)
    app.pack(fill="both", expand=True)
    root.mainloop()