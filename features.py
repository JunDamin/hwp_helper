import customtkinter as ctk
import tkinter as tk
from functions import (
    back_to_app,
    get_path,
)
from components import ToolTip, FontStyleBtns


class HwpFeatureFrame(ctk.CTkScrollableFrame):
    """"""

    def __init__(self, parent, context):
        super().__init__(parent)
        self.app = context["app"]

        font_style_btns = FontStyleBtns(self, context)
        font_style_btns.pack(fill=tk.X, expand=True)

        # set a function for btn
        def set_feature_btn(parent, name, command, text, gif=None):
            btn = ctk.CTkButton(parent, text=name, command=command)
            ToolTip(btn, text, gif)
            return btn

        # table related feature
        ctk.CTkLabel(self, text="테이블 관련 기능").pack()

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill=tk.X)

        table_border_btn = set_feature_btn(
            table_frame,
            "표 테두리",
            command=self.set_cell_border,
            text="선택한 셀영역의 가장 위와 가장 아래 테두리는 굵은 선으로 바꾸고 좌우 끝의 테두리를 없앱니다.",
            gif=get_path("src/table_border_btn.gif"),
        )
        table_border_btn.grid(row=1, column=0, pady=3, padx=3, sticky="nsew")

        cell_header_btn = set_feature_btn(
            table_frame,
            "헤더 스타일 넣기",
            command=self.set_header_style,
            text="선택한 셀영역가장 아래 테두리를 두줄로 바꾸고 셀에 연노란 바탕색을 넣습니다.",
            gif=get_path("src/table_header_btn.gif"),
        )
        cell_header_btn.grid(row=1, column=1, pady=3, padx=3, sticky="nsew")

        # alignment related feature
        ctk.CTkLabel(self, text="정렬 기능").pack()
        alignment_frame = ctk.CTkFrame(self)
        alignment_frame.pack(fill=tk.X)

        para_indent_btn = set_feature_btn(
            alignment_frame,
            "현재 커서 위치에 맞춰 들여쓰기(shift+tab)",
            command=self.set_para_indent,
            text="현재 커서 위치에 맞춰 들여쓰기를 적용합니다. 표에서는 ctrl+shift+tab으로 가능합니다.",
            gif=get_path("src/align_btn.gif"),
        )
        para_indent_btn.grid(row=1, column=0, pady=3, padx=3, sticky="nsew")

        decrease_line_spacing_btn = set_feature_btn(
            alignment_frame,
            "줄간격 줄이기(alt+shift+A)",
            command=self.decrease_line_spacing,
            text="현재 커서 위치 문장 간격을 줄입니다.",
            gif=get_path("src/decrease_line_spacing_btn.gif"),
        )
        decrease_line_spacing_btn.grid(row=0, column=0, pady=3, padx=3, sticky="nsew")

        increase_line_spacing_btn = set_feature_btn(
            alignment_frame,
            "줄간격 늘리기(alt+shift+Z)",
            command=self.increase_line_spacing,
            text="현재 커서 위치 문장 간격을 늘립니다.",
            gif=get_path("src/increase_line_spacing_btn.gif"),
        )
        increase_line_spacing_btn.grid(row=0, column=1, pady=3, padx=3, sticky="nsew")

        # page break related feature
        ctk.CTkLabel(self, text="페이지 관련 기능").pack()
        layout_frame = ctk.CTkFrame(self)
        layout_frame.pack(fill=tk.X)

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


        koica_page_setup_btn = set_feature_btn(
            layout_frame,
            "기안기 여백설정",
            command=self.setup_koica_page,
            text="페이지여백을 KOICA 공문 기안기에 맞춰 설정합니다.",
        )
        koica_page_setup_btn.grid(row=2, column=0, pady=3, padx=3, sticky="nsew")

        normal_page_setup_btn = set_feature_btn(
            layout_frame,
            "일반 여백설정",
            command=self.setup_normal_page,
            text="페이지여백을 좌우를 20mm, 위는 20mm, 머리말 15mm 아래는 15mm, 꼬리말 5mm, 제본 0mm로 설정합니다.",
        )
        normal_page_setup_btn.grid(row=2, column=1, pady=3, padx=3, sticky="nsew")


        # shape related feature
        ctk.CTkLabel(self, text="형태 설정 기능").pack()
        shape_frame = ctk.CTkFrame(self)
        shape_frame.pack(fill=tk.X)

        super_script_btn = set_feature_btn(
            shape_frame,
            "윗첨자(alt+shift+P)",
            command=self.super_script,
            text="선택한 영역을 윗첨자, 혹은 원래 형태로 바꿉니다.",
            gif=get_path("src/super_script_btn.gif"),
        )
        super_script_btn.grid(row=1, column=0, pady=3, padx=3, sticky="nsew")

        insert_endnote_btn = set_feature_btn(
            shape_frame,
            "미주넣기",
            command=self.insert_endnote,
            text="현재 위치에 번호를 표시하고 마지막 페이지에 설명을 적을 수 있는 미주를 추가합니다.",
            gif=get_path("src/endnote_btn.gif"),
        )
        insert_endnote_btn.grid(row=1, column=1, pady=3, padx=3, sticky="nsew")

        insert_footnote_btn = set_feature_btn(
            shape_frame,
            "각주넣기",
            command=self.insert_footnote,
            text="현재 위치에 번호를 표시하고 현재 페이지 아래쪽에 설명을 추가합니다.",
            gif=get_path("src/footnote_btn.gif"),
        )
        insert_footnote_btn.grid(row=1, column=2, pady=3, padx=3, sticky="nsew")

        insert_memo_btn = set_feature_btn(
            shape_frame,
            "메모넣기",
            command=self.insert_memo,
            text="메모를 넣습니다.",
            gif=get_path("src/add_memo_btn.gif"),
        )
        insert_memo_btn.grid(row=2, column=0, padx=3, pady=3, sticky="nsew")

        delete_memo_btn = set_feature_btn(
            shape_frame,
            "메모지우기",
            command=self.delete_memo,
            text="메모를 지웁니다.",
            gif=get_path("src/remove_memo_btn.gif"),
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

    @back_to_app
    def increase_line_spacing(self):
        return self.app.actions.ParagraphShapeIncreaseLineSpacing().run()

    @back_to_app
    def decrease_line_spacing(self):
        return self.app.actions.ParagraphShapeDecreaseLineSpacing().run()

    @back_to_app
    def setup_koica_page(self):
        return self.app.setup_page(top=30, bottom=15, left=20, right=15, header=0, footer=15, gutter=0)
        

    @back_to_app
    def setup_normal_page(self):
        return self.app.setup_page()
        

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x800")
    context = {"app": None}
    app = HwpFeatureFrame(root, context)
    app.pack(fill="both", expand=True)
    root.mainloop()
