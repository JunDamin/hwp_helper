import customtkinter as ctk
from functions import (
    update_templates,
    update_template,
    prettify_filename
)
from pathlib import Path
import shutil as sh 

class NaviBar(ctk.CTkFrame):
    def __init__(self, parent, context, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = context["app"]
        self.context = context

        update_btn = ctk.CTkButton(
            self, text="탬플릿 업데이트", command=self.update_templates
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
            self, self.context["template_frame"]
        )  # master argument is optional
        toplevel.focus()

    def add_template(self):
        toplevel = AddTemplateForm(self, self.context)
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

class AddTemplateForm(ctk.CTkToplevel):

    def __init__(self, parent, context):
        super().__init__(parent)
        self.context = context
        self.app = context["app"]


        self.intro = ctk.CTkLabel(self, text="아래 항목들을 채우고 버튼을 눌러주세요.")
        self.intro.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        ctk.CTkLabel(self, text="구분").grid(row=1, column=0)
        ctk.CTkLabel(self, text="이름").grid(row=2, column=0)
        self.category = category = ctk.CTkEntry(self, placeholder_text="구분명을 입력하세요.")
        self.name = name = ctk.CTkEntry(self, placeholder_text="구분명을 입력하세요.")
        category.grid(row=1, column=1, pady=5, padx=5)
        name.grid(row=2, column=1, pady=5, padx=5)
        ctk.CTkButton(self, text="반영하기", command=self.add_template).grid(row=3, column=0, columnspan=2, pady=5)


    def add_template(self):
        
        self.temp = Path("temp")
        self.temp.mkdir(exist_ok=True)
        self.temp_path = temp_path = Path("temp/temp.hwp")
        self.app.save_block(temp_path)

        fname = prettify_filename(f"{self.category.get()}_{self.name.get()}")
        
        destination = Path(f"templates/{fname}.hwp")
        if destination.exists():
            return self.intro.configure(text="같은 이름의 파일이 존재합니다. 다른 이름으로 수정해 주세요.")  # deletes the file
        Path(self.temp_path).rename(destination)

        update_template(self.app, destination)
        self.context["template_frame"].refresh()
        sh.rmtree("temp")
        self.destroy()
        self.context["tabview"].set("templates")



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