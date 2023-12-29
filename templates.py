import customtkinter as ctk
import tkinter as tk
from components import CollapsibleFrame, ToolTip, AddTemplateForm, TemplateControl
from functions import (
    update_templates,
    get_categories,
    set_forewindow,
    check_app,
    get_image,
    make_topmost,
)


class CategoryFrame(ctk.CTkFrame):
    """
    A frame that displays categories from images file.
    """

    def __init__(self, parent, context):
        super().__init__(parent)
        self.app = context["app"]
        self.template_frame = ctk.CTkScrollableFrame(self)
        self.template_frame.pack(fill="both", expand=True)
        self.frame_header = ctk.CTkFrame(self.template_frame)
        self.frame_header.pack()

        self._initialize_frames()

    def _initialize_frames(self):
        self._create_add_template_button()
        self._create_update_template_button()
        self._populate_category_frames()

    def _create_add_template_button(self):
        add_template_btn = ctk.CTkButton(
            self.frame_header,
            text="선택영역 탬플릿 추가",
            command=self.add_template,
            fg_color="green",
        )
        add_template_btn.grid(
            row=1, column=0, columnspan=2, padx=2, pady=2, sticky="nesw"
        )
        ToolTip(add_template_btn, "한글에서 현재 선택중인 영역을 탬플릿으로 추가합니다.")

    def _create_update_template_button(self):
        update_btn = ctk.CTkButton(
            self.frame_header,
            text="탬플릿 관리",
            command=self.update_templates,
            fg_color="green",
        )
        update_btn.grid(row=1, column=2, pady=2, padx=2)
        ToolTip(
            update_btn, text="탬플릿 이름을 수정하거나 삭제, 또는 templates 폴더에 있는 내용으로 전체를 업데이트 합니다."
        )

    def _populate_category_frames(self):
        categories = get_categories()
        for key, value in categories.items():
            cframe = CollapsibleFrame(self.template_frame, key)
            cframe.pack(fill=tk.X, padx=2, pady=2, anchor="nw")
            for text, image_path, filename, n in value:
                btn = self._create_category_button(
                    cframe, text, image_path, filename, n
                )
                cframe.add_widget(btn, sticky="w")
            cframe.collapse()

    def _create_category_button(self, parent_frame, text, image_path, filename, n):
        path = f"templates/{filename}.hwp"
        image = get_image(image_path)
        return ctk.CTkButton(
            parent_frame.frame_contents,
            text=text,
            command=self._make_func(path, n),
            fg_color="transparent",
            image=image,
            compound="bottom",
        )

    def _make_func(self, path, n):
        def func():
            check_app(self.app)
            set_forewindow(self.app)
            self.app.insert_file(path)
            for _ in range(n):
                self.app.move("NextPara")
            return None

        return func

    def add_template(self):
        toplevel = AddTemplateForm(
            self, {"app": self.app, "template_frame": self.template_frame}
        )
        toplevel.focus()

    def update_templates(self):
        toplevel = UpdateTemplateForm(self, self.template_frame)
        toplevel.focus()

    def refresh(self):
        for child in self.template_frame.winfo_children():
            child.destroy()
        self._initialize_frames()


class UpdateTemplateForm(ctk.CTkToplevel):
    def __init__(self, parent, template_frame, **kwargs):
        super().__init__(parent, **kwargs)
        self.geometry("800x1000")
        self.template_frame = template_frame

        self._initialize_ui()
        make_topmost(self)

    def _initialize_ui(self):
        self._create_guide_label()
        self._create_update_button()
        self._create_progress_bar()
        self._create_scrollable_frame()
        self._populate_categories()

    def _create_guide_label(self):
        guide_text = """update 버튼을 누르면 templates 폴더에 있는 한글 파일을 template화 하여 넣어 놓습니다. 
        분류하는 방법은 언더바를 기준으로 진행되며 언더바 이전의 단어는 카테고리로, 그 이후 단어는 이름으로 사용하게 됩니다."""
        self.guide = ctk.CTkLabel(self, text=guide_text, wraplength=600, justify="left")
        self.guide.pack(pady=5, padx=5)

    def _create_update_button(self):
        self.update_btn = ctk.CTkButton(
            self, text="update", command=self.update_templates
        )
        self.update_btn.pack(pady=5)

    def _create_progress_bar(self):
        self.progress_bar = ctk.CTkProgressBar(self)

    def _create_scrollable_frame(self):
        self.template_frame = ctk.CTkScrollableFrame(self)
        self.template_frame.pack(fill="both", expand=True)

    def _populate_categories(self):
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
                    ),
                    sticky="w",
                )

    def refresh(self):
        for child in self.template_frame.winfo_children():
            child.destroy()
        self._populate_categories()

    def update_templates(self):
        self.update_btn.destroy()
        self.progress_bar.pack(padx=10, pady=10)
        self.progress_bar.set(0)
        self.update()
        for i, n in update_templates():
            progress = i / (n - 1)
            self.progress_bar.set(progress)
            self.update()
        self.progress_bar.pack_forget()
        self.refresh()
        self.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x800")
    app = CategoryFrame(root, {"app": None})
    app.pack(fill="both", expand=True)
    root.mainloop()
