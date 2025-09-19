import flet as ft
from callback import (
    align_center,
    align_distributed,
    align_justified,
    align_left,
    align_right,
    break_page,
    break_section,
    decrease_fontsize,
    decrease_line_spacing,
    decrease_spacing,
    delete_column,
    delete_memo,
    delete_row,
    increase_fontsize,
    increase_line_spacing,
    increase_spacing,
    insert_endnote,
    insert_footnote,
    insert_memo,
    set_black,
    set_blue,
    set_cell_border,
    set_green,
    set_header_style,
    set_para_indent,
    set_red,
    set_white,
    setup_koica_page,
    setup_normal_page,
    super_script,
    color_doublespace,
    uncolor_doublespace,
    process_font,
)
from components import FontStyleManager


class HwpFeatureFrame(ft.Container):
    def __init__(self, context):
        super().__init__()
        self.app = context["app"]
        self.context = context
        
        content = ft.Column(scroll=ft.ScrollMode.AUTO)
        
        # Font Style Manager
        content.controls.append(FontStyleManager(self.context))
        
        # Feature sections
        content.controls.append(self._create_feature_section("글자 모양 기능", self._char_features(), 3))
        content.controls.append(self._create_feature_section("문단 정렬 기능", self._para_features(), 3))
        content.controls.append(self._create_feature_section("테이블 관련 기능", self._table_features(), 3))
        content.controls.append(self._create_feature_section("페이지 관련 기능", self._layout_features(), 3))
        content.controls.append(self._create_feature_section("메모 관련 기능", self._shape_features(), 3))
        content.controls.append(self._create_feature_section("검토 기능", self._review_features(), 3))
        
        self.content = content

    def _create_feature_section(self, title, features, n_columns):
        section = ft.Column()
        section.controls.append(ft.Text(title))
        grid = ft.GridView(expand=1, max_extent=150, child_aspect_ratio=1)
        section.controls.append(grid)
        
        for name, command, tooltip_text, image_path in features:
            grid.controls.append(
                ft.ElevatedButton(
                    text=name,
                    on_click=lambda e, cmd=command: cmd(self.app),
                    tooltip=tooltip_text,
                )
            )
        return section

    def _char_features(self):
        return [
            ("글자키우기\n(alt+shift+E)", increase_fontsize, "글자 크기를 키웁니다.", "src/increase_fontsize_btn.gif"),
            ("글자줄이기\n(alt+shift+R)", decrease_fontsize, "글자 크기를 줄입니다.", "src/decrease_fontsize_btn.gif"),
            ("자간늘리기\n(alt+shift+W)", increase_spacing, "글자 사이 간격을 늘립니다.", "src/increase_spacing_btn.gif"),
            ("자간줄이기\n(alt+shift+N)", decrease_spacing, "글자 사이 간격을 줄입니다.", "src/decrease_spacing_btn.gif"),
            ("빨간색\n(ctrl+M, R)", set_red, "글자 색을 붉은 색으로 설정합니다.", "src/set_red_btn.gif"),
            ("녹색\n(ctrl+M, G)", set_green, "글자 색을 녹색으로 설정합니다.", "src/set_green_btn.gif"),
            ("파란색\n(ctrl+M, B)", set_blue, "글자 색을 파란색으로 설정합니다.", "src/set_blue_btn.gif"),
            ("검은색\n(ctrl+M, K)", set_black, "글자 색을 검은 색으로 설정합니다.", "src/set_black_btn.gif"),
            ("흰색\n(ctrl+M, W)", set_white, "글자색을 흰색으로 설정합니다.", "src/set_white_btn.gif"),
        ]

    def _para_features(self):
        return [
            ("현재위치 들여쓰기\n(shift+tab)", set_para_indent, "현재 커서 위치에 맞춰 들여쓰기를 적용합니다. 표에서는 ctrl+shift+tab으로 가능합니다.", "src/align_btn.gif"),
            ("줄간격 줄이기\n(alt+shift+A)", decrease_line_spacing, "현재 커서 위치 문장 간격을 줄입니다.", "src/decrease_line_spacing_btn.gif"),
            ("줄간격 늘리기\n(alt+shift+Z)", increase_line_spacing, "현재 커서 위치 문장 간격을 늘립니다.", "src/increase_line_spacing_btn.gif"),
            ("왼쪽 정렬\n(ctrl+shift+L)", align_left, "현재 문장을 왼쪽 정렬 합니다.", "src/align_left_btn.gif"),
            ("가운데 정렬\n(ctrl+shift+C)", align_center, "현재 문장을 가운데 정렬 합니다.", "src/align_center_btn.gif"),
            ("오른쪽 정렬\n(ctrl+shift+R)", align_right, "현재 문장을 오른쪽 정렬 합니다.", "src/align_right_btn.gif"),
            ("양쪽 정렬\n(ctrl+shift+M)", align_justified, "현재 문장을 양쪽 정렬 합니다.", "src/align_justified_btn.gif"),
            ("배분 정렬\n(ctrl+shift+T)", align_distributed, "현재 문장을 배분 정렬 합니다.", "src/align_distributed_btn.gif"),
        ]

    def _table_features(self):
        return [
            ("표 테두리", set_cell_border, "선택한 셀영역의 가장 위와 가장 아래 테두리는 굵은 선으로 바꾸고 좌우 끝의 테두리를 없앱니다.", "src/table_border_btn.gif"),
            ("헤더 스타일 넣기", set_header_style, "선택한 셀영역가장 아래 테두리를 두줄로 바꾸고 셀에 연노란 바탕색을 넣습니다.", "src/table_header_btn.gif"),
            ("행 삭제하기\n(alt+Delete)", delete_row, "현재 위치의 행을 지웁니다.", "src/delete_row_btn.gif"),
            ("열 삭제하기\n(alt+Delete)", delete_column, "현재 위치의 열을 지웁니다.", "src/delete_column_btn.gif"),
        ]

    def _layout_features(self):
        return [
            ("구역 나누기\n(alt+shift+enter)", break_section, "구역 나누기를 합니다. 구역이 나누어지면 다른 페이지 여백을 설정하거나 이후부터 페이지 가로 세로를 바꾸는 적용이 가능해 집니다.", None),
            ("페이지 나누기\n(ctrl+enter)", break_page, "다음 페이지부터 시작하도록 합니다. 여러번 엔터를 칠 필요 없이 다음 페이지부터 시작합니다.", None),
            ("기안기 여백설정", setup_koica_page, "페이지여백을 KOICA 공문 기안기에 맞춰 설정합니다.", None),
            ("일반 여백설정", setup_normal_page, "페이지여백을 좌우를 20mm, 위는 20mm, 머리말 15mm 아래는 15mm, 꼬리말 5mm, 제본 0mm로 설정합니다.", None),
        ]

    def _shape_features(self):
        return [
            ("윗첨자\n(alt+shift+P)", super_script, "선택한 영역을 윗첨자, 혹은 원래 형태로 바꿉니다.", "src/super_script_btn.gif"),
            ("미주넣기\n(ctrl+N+E)", insert_endnote, "현재 위치에 번호를 표시하고 마지막 페이지에 설명을 적을 수 있는 미주를 추가합니다.", "src/endnote_btn.gif"),
            ("각주넣기\n(ctrl+N+N)", insert_footnote, "현재 위치에 번호를 표시하고 현재 페이지 아래쪽에 설명을 추가합니다.", "src/footnote_btn.gif"),
            ("메모넣기", insert_memo, "메모를 넣습니다.", "src/add_memo_btn.gif"),
            ("메모지우기", delete_memo, "메모를 지웁니다.", "src/remove_memo_btn.gif"),
        ]

    def _review_features(self):
        return [
            ("연속 공백 색칠하기", color_doublespace, "공백이 연속해서 들어가 있는 경우 주황색으로 음영색을 칠합니다.", None),
            ("공백 색 지우기", uncolor_doublespace, "공백의 음영색을 지웁니다.", None),
            ("Bold 처리 폰트로 변환하기", process_font, "Kopub 볼드 처리 글자를 볼드를 폰트를 바꿔 줍니다.", None),
        ]
