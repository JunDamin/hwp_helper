import customtkinter as ctk
import tkinter as tk
from functions import update_templates, get_categories, make_topmost
from components import CollapsibleFrame, TemplateControl, AddTemplateForm, ToolTip


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

        add_template_btn = ctk.CTkButton(
            self, text="선택영역 탬플릿 추가", command=self.add_template
        )
        add_template_btn.grid(
            row=1, column=0, columnspan=2, padx=2, pady=2, sticky="nesw"
        )
        ToolTip(add_template_btn, "한글에서 현재 선택중인 영역을 탬플릿으로 추가합니다.")

        update_btn = ctk.CTkButton(
            self, text="탬플릿 관리", command=self.update_templates, width=80
        )
        update_btn.grid(row=1, column=2, pady=2, padx=2)
        ToolTip(
            update_btn, text="탬플릿 이름을 수정하거나 삭제, 또는 templates 폴더에 있는 내용으로 전체를 업데이트 합니다."
        )

    def update_templates(self):
        toplevel = UpdateTemplateForm(
            self,
            self.context["template_frame"],
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
        self.progress_bar = ctk.CTkProgressBar(self)
        

        self.template_frame = ctk.CTkScrollableFrame(self)
        self.template_frame.pack(fill="both", expand=True)

        self.set_frame()
        make_topmost(self)

    def set_frame(self):
        # get categrory data from packages
        categories = get_categories()
        for key, value in categories.items():
            cframe = CollapsibleFrame(self.template_frame, key)
            cframe.pack(fill=tk.X, pady=5, padx=5, anchor="w")

            for text, image_path, filename, n in value:
                path = f"templates/{filename}.hwp"

                cframe.add_widget(
                    TemplateControl(
                        cframe.frame_contents,
                        text=text,
                        file_path=path,
                        image_path=image_path,
                        target_frame=self,
                    ), sticky='w'
                )

    def refresh(self):
        for child in self.template_frame.winfo_children():
            child.destroy()

        self.set_frame()
        self.template_form.refresh()

    def update_templates(self):
        self.update_btn.destroy()

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
