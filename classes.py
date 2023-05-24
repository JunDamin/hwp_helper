import customtkinter as ctk
import tkinter as tk
from PIL import Image
import yaml
from functions import (
    set_button,
    get_categories,
    update_templates,
    set_forewindows,
    set_hwp_size,
    get_screen_size,
    check_app,
    get_ratio,
    back_to_app,
    get_path,
)


class Helper(ctk.CTk):
    def __init__(self, context):
        super().__init__()

        self.context = context

        context["helper"] = self

        # Override the default close behavior
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title("Hwp Helper v.0.2.0")
        self.iconbitmap(get_path("src/ai.ico"))

        # set app
        self.app = context["app"]
        self.set_fullscreen()

        # set navi bar

        self.menu = ctk.CTkFrame(self)
        self.menu.pack()

        tabview = ctk.CTkTabview(master=self)
        tabview.pack(padx=20, pady=20, fill="both", expand=True)

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
        icon.grid(row=0, column=0, padx=10)
        header = ctk.CTkLabel(
            self.menu,
            text="Hwp Helper v.0.2.0",
        )
        header.grid(row=0, column=1, padx=10)

        navi_bar = NaviBar(self.menu, context)
        navi_bar.grid(row=0, column=2)
        context["navi_bar"] = navi_bar

    def set_windows(self, left, top, width, height):
        ratio = get_ratio(self)
        self.geometry(f"{int(width*ratio)}x{int(height*ratio)}+{int(left)}+{int(top)}")

    def set_fullscreen(self):
        setting = self.context["setting"]
        app_width = setting.get("app_width", 800)
        side = setting.get("side", "left")

        x1, y1, x2, y2 = get_screen_size()
        width = x2 - x1
        height = y2 - y1
        hwp_ratio = (width - app_width) / width
        hwp_width = int(width * hwp_ratio)

        hwp_x, hwp_y = x1 + int(width * (1 - hwp_ratio)), y1
        app_x, app_y = x1, y1

        if side == "left":
            hwp_x, hwp_y = x1, y1
            app_x, app_y = x1 + hwp_width, y1

        set_hwp_size(self.app, hwp_x, hwp_y, hwp_width, height)
        self.set_windows(app_x, app_y, width=width - hwp_width, height=height)

    def on_closing(self):
        with open("setting.yaml", "w") as f:
            yaml.safe_dump(self.context["setting"], f)
        self.destroy()


class CategoryFrame(ctk.CTkScrollableFrame):
    """
    from categories from images file
    """

    def __init__(self, parent, context):
        super().__init__(parent)
        self.parent = parent
        self.app = context["app"]
        self.set_frames()

    def refresh(self):
        for child in self.winfo_children():
            child.destroy()

        self.set_frames()

    def set_frames(self):
        # make command
        def make_func(path, n):
            def func():
                check_app(self.app)
                set_forewindows(self.app)
                self.app.insert_file(path)
                for _ in range(n):
                    self.app.move("NextPara")
                return None

            return func

        # get categrory data from packages
        categories = get_categories()
        for key, value in categories.items():
            cframe = CollapsibleFrame(self, key)
            cframe.pack(fill="x", pady=5, padx=5)

            for text, image_path, filename, n in value:
                path = f"templates/{filename}.hwp"

                # create button
                btn = set_button(
                    cframe.frame_contents,
                    text=text,
                    image_path=image_path,
                    command=make_func(path, n),
                )
            cframe.collapse()


class CollapsibleFrame(ctk.CTkFrame):
    """This Frame is for create collapsible frame for sub components"""

    def __init__(self, master=None, text="toggle", **kwargs):
        ctk.CTkFrame.__init__(self, master, **kwargs)

        self.button_toggle = ctk.CTkButton(
            self, text=text, command=self.toggle, border_spacing=10
        )
        self.button_toggle.pack(fill="x")

        self.frame_contents = ctk.CTkFrame(
            self,
        )
        self.frame_contents.pack()

    def toggle(self):
        if self.frame_contents.winfo_viewable():
            self.frame_contents.pack_forget()
        else:
            self.frame_contents.pack()

    def collapse(self):
        self.frame_contents.pack_forget()


class HwpFeatureFrame(ctk.CTkScrollableFrame):
    """"""

    def __init__(self, parent, context):
        super().__init__(parent)
        self.app = context["app"]

        # set a function for btn
        def set_feature_btn(parent, name, command, text):
            btn = ctk.CTkButton(parent, text=name, command=command)
            ToolTip(btn, text)
            return btn

        # table related feature
        ctk.CTkLabel(self, text="테이블 관련 기능").pack()

        table_frame = ctk.CTkFrame(self)
        table_frame.pack()

        cell_border_btn = set_feature_btn(
            table_frame,
            "표 테두리",
            command=self.set_cell_border,
            text="선택한 셀영역의 가장 위와 가장 아래 테두리는 굵은 선으로 바꾸고 좌우 끝의 테두리를 없앱니다.",
        )
        cell_border_btn.grid(row=1, column=0, pady=3, padx=3, sticky="nsew")

        cell_color_btn = set_feature_btn(
            table_frame,
            "헤더 스타일 넣기",
            command=self.set_header_style,
            text="선택한 셀영역가장 아래 테두리를 두줄로 바꾸고 셀에 연노란 바탕색을 넣습니다.",
        )
        cell_color_btn.grid(row=1, column=1, pady=3, padx=3, sticky="nsew")

        # alignment related feature
        ctk.CTkLabel(self, text="정렬 기능").pack()
        alignment_frame = ctk.CTkFrame(self)
        alignment_frame.pack()

        para_indent_btn = set_feature_btn(
            alignment_frame,
            "현재 커서 위치에 맞춰 들여쓰기",
            command=self.set_para_indent,
            text="현재 커서 위치에 맞춰 들여쓰기를 적용합니다. 표에서도 사용이 가능합니다.",
        )
        para_indent_btn.grid(row=1, column=0, pady=3, padx=3, sticky="nsew")

        # page break related feature
        ctk.CTkLabel(self, text="페이지 관련 기능").pack()
        layout_frame = ctk.CTkFrame(self)
        layout_frame.pack()

        break_section_btn = set_feature_btn(
            layout_frame,
            "구역 나누기",
            command=self.break_section,
            text="구역 나누기를 합니다. 구역이 나누어지면 다른 페이지 여백을 설정하거나 이후부터 페이지 가로 세로를 바꾸는 적용이 가능해 집니다.",
        )
        break_section_btn.grid(row=1, column=0, pady=3, padx=3, sticky="nsew")

        break_page_btn = set_feature_btn(
            layout_frame,
            "페이지 나누기",
            command=self.break_page,
            text="다음 페이지부터 시작하도록 합니다. 여러번 엔터를 칠 필요 없이 다음 페이지부터 시작합니다.",
        )
        break_page_btn.grid(row=1, column=1, pady=3, padx=3, sticky="nsew")

        # shape related feature
        ctk.CTkLabel(self, text="형태 설정 기능").pack()
        shape_frame = ctk.CTkFrame(self)
        shape_frame.pack()

        super_script_btn = set_feature_btn(
            shape_frame,
            "윗첨자",
            command=self.super_script,
            text="선택한 영역을 윗첨자, 혹은 원래 형태로 바꿉니다.",
        )
        super_script_btn.grid(row=1, column=0, pady=3, padx=3, sticky="nsew")

        insert_endnote_btn = set_feature_btn(
            shape_frame,
            "미주넣기",
            command=self.insert_endnote,
            text="현재 위치에 번호를 표시하고 마지막 페이지에 설명을 적을 수 있는 미주를 추가합니다.",
        )
        insert_endnote_btn.grid(row=1, column=1, pady=3, padx=3, sticky="nsew")

        insert_footnote_btn = set_feature_btn(
            shape_frame,
            "각주넣기",
            command=self.insert_footnote,
            text="현재 위치에 번호를 표시하고 현재 페이지 아래쪽에 설명을 추가합니다.",
        )
        insert_footnote_btn.grid(row=1, column=2, pady=3, padx=3, sticky="nsew")

        insert_memo_btn = set_feature_btn(
            shape_frame, "메모넣기", command=self.insert_memo, text="메모를 넣습니다."
        )
        insert_memo_btn.grid(row=2, column=0, padx=3, pady=3, sticky="nsew")

        delete_memo_btn = set_feature_btn(
            shape_frame, "메모지우기", command=self.delete_memo, text="메모를 지웁니다."
        )
        delete_memo_btn.grid(row=2, column=1, padx=3, pady=3, sticky="nsew")

    @back_to_app
    def set_cell_border(self):
        return self.app.set_cell_border(
            top=1, bottom=1, right=0, left=0, top_width=0.4, bottom_width=0.4
        )

    @back_to_app
    def set_header_style(self):
        self.app.set_cell_color(bg_color=(250, 243, 219))
        self.app.set_cell_border(bottom=8, bottom_width=0.5)
        return None

    @back_to_app
    def set_para_indent(self):
        return self.app.actions.ParagraphShapeIndentAtCaret().run()

    @back_to_app
    def break_section(self):
        return self.app.actions.BreakSection().run()

    @back_to_app
    def super_script(self):
        return self.app.actions.CharShapeSuperscript().run()

    @back_to_app
    def break_page(self):
        return self.app.actions.BreakPage().run()

    @back_to_app
    def insert_endnote(self):
        return self.app.actions.InsertEndnote().run()

    @back_to_app
    def insert_footnote(self):
        return self.app.actions.InsertFootnote().run()

    @back_to_app
    def insert_memo(self):
        return self.app.actions.InsertFieldMemo().run()

    @back_to_app
    def delete_memo(self):
        return self.app.actions.DeleteFieldMemo().run()


class NaviBar(ctk.CTkFrame):
    def __init__(self, parent, context):
        super().__init__(parent)
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


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 50

        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Remove window decorations
        tw.wm_geometry(f"+{x}+{y}")  # Position tooltip

        label = tk.Label(tw, text=self.text, background="#dddddd", wraplength=500, font=15)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x800")
    context = {"app": None}
    app = HwpFeatureFrame(root, context)
    app.pack(fill="both", expand=True)
    root.mainloop()
