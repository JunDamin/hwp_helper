"""Features page with HWP operation buttons."""

import flet as ft
from typing import Dict, Any, List, Tuple, Callable

from ..components.font_manager import FontStyleManager
from ...services.hwp_operations import HwpOperationService
from ...callbacks.hwp_callbacks import color_double_space, uncolor_double_space, process_font


class FeaturesPage(ft.Container):
    """Page containing HWP feature buttons organized by category."""

    def __init__(self, context: Dict[str, Any]):
        super().__init__()
        self.context = context
        self.hwp_ops = HwpOperationService(context["app_manager"])
        
        content = ft.Column(scroll=ft.ScrollMode.AUTO)
        
        # Font Style Manager
        content.controls.append(FontStyleManager(context))
        
        # Feature sections
        content.controls.append(
            self._create_feature_section("글자 모양 기능", self._get_char_features(), 3)
        )
        content.controls.append(
            self._create_feature_section("문단 정렬 기능", self._get_para_features(), 3)
        )
        content.controls.append(
            self._create_feature_section("테이블 관련 기능", self._get_table_features(), 3)
        )
        content.controls.append(
            self._create_feature_section("페이지 관련 기능", self._get_layout_features(), 3)
        )
        content.controls.append(
            self._create_feature_section("메모 관련 기능", self._get_shape_features(), 3)
        )
        content.controls.append(
            self._create_feature_section("검토 기능", self._get_review_features(), 3)
        )
        
        self.content = content

    def _create_feature_section(self, title: str, 
                               features: List[Tuple[str, Callable, str, str]], 
                               n_columns: int) -> ft.Column:
        """Create a feature section with buttons."""
        section = ft.Column()
        section.controls.append(ft.Text(title, size=16, weight=ft.FontWeight.BOLD))
        
        grid = ft.GridView(expand=1, max_extent=150, child_aspect_ratio=1)
        section.controls.append(grid)
        
        for name, command, tooltip_text, image_path in features:
            grid.controls.append(
                ft.ElevatedButton(
                    text=name,
                    on_click=lambda e, cmd=command: cmd(),
                    tooltip=tooltip_text,
                )
            )
        return section

    def _get_char_features(self) -> List[Tuple[str, Callable, str, str]]:
        """Get character formatting features."""
        return [
            ("글자키우기\n(alt+shift+E)", self.hwp_ops.increase_font_size, 
             "글자 크기를 키웁니다.", "src/increase_fontsize_btn.gif"),
            ("글자줄이기\n(alt+shift+R)", self.hwp_ops.decrease_font_size, 
             "글자 크기를 줄입니다.", "src/decrease_fontsize_btn.gif"),
            ("자간늘리기\n(alt+shift+W)", self.hwp_ops.increase_spacing, 
             "글자 사이 간격을 늘립니다.", "src/increase_spacing_btn.gif"),
            ("자간줄이기\n(alt+shift+N)", self.hwp_ops.decrease_spacing, 
             "글자 사이 간격을 줄입니다.", "src/decrease_spacing_btn.gif"),
            ("빨간색\n(ctrl+M, R)", self.hwp_ops.set_text_color_red, 
             "글자 색을 붉은 색으로 설정합니다.", "src/set_red_btn.gif"),
            ("녹색\n(ctrl+M, G)", self.hwp_ops.set_text_color_green, 
             "글자 색을 녹색으로 설정합니다.", "src/set_green_btn.gif"),
            ("파란색\n(ctrl+M, B)", self.hwp_ops.set_text_color_blue, 
             "글자 색을 파란색으로 설정합니다.", "src/set_blue_btn.gif"),
            ("검은색\n(ctrl+M, K)", self.hwp_ops.set_text_color_black, 
             "글자 색을 검은 색으로 설정합니다.", "src/set_black_btn.gif"),
            ("흰색\n(ctrl+M, W)", self.hwp_ops.set_text_color_white, 
             "글자색을 흰색으로 설정합니다.", "src/set_white_btn.gif"),
        ]

    def _get_para_features(self) -> List[Tuple[str, Callable, str, str]]:
        """Get paragraph formatting features."""
        return [
            ("현재위치 들여쓰기\n(shift+tab)", self.hwp_ops.set_paragraph_indent, 
             "현재 커서 위치에 맞춰 들여쓰기를 적용합니다.", "src/align_btn.gif"),
            ("줄간격 줄이기\n(alt+shift+A)", self.hwp_ops.decrease_line_spacing, 
             "현재 커서 위치 문장 간격을 줄입니다.", "src/decrease_line_spacing_btn.gif"),
            ("줄간격 늘리기\n(alt+shift+Z)", self.hwp_ops.increase_line_spacing, 
             "현재 커서 위치 문장 간격을 늘립니다.", "src/increase_line_spacing_btn.gif"),
            ("왼쪽 정렬\n(ctrl+shift+L)", self.hwp_ops.align_left, 
             "현재 문장을 왼쪽 정렬 합니다.", "src/align_left_btn.gif"),
            ("가운데 정렬\n(ctrl+shift+C)", self.hwp_ops.align_center, 
             "현재 문장을 가운데 정렬 합니다.", "src/align_center_btn.gif"),
            ("오른쪽 정렬\n(ctrl+shift+R)", self.hwp_ops.align_right, 
             "현재 문장을 오른쪽 정렬 합니다.", "src/align_right_btn.gif"),
            ("양쪽 정렬\n(ctrl+shift+M)", self.hwp_ops.align_justified, 
             "현재 문장을 양쪽 정렬 합니다.", "src/align_justified_btn.gif"),
            ("배분 정렬\n(ctrl+shift+T)", self.hwp_ops.align_distributed, 
             "현재 문장을 배분 정렬 합니다.", "src/align_distributed_btn.gif"),
        ]

    def _get_table_features(self) -> List[Tuple[str, Callable, str, str]]:
        """Get table-related features."""
        return [
            ("표 테두리", self.hwp_ops.set_cell_border, 
             "선택한 셀영역의 테두리를 설정합니다.", "src/table_border_btn.gif"),
            ("헤더 스타일 넣기", self.hwp_ops.set_header_style, 
             "선택한 셀영역에 헤더 스타일을 적용합니다.", "src/table_header_btn.gif"),
            ("행 삭제하기\n(alt+Delete)", self.hwp_ops.delete_row, 
             "현재 위치의 행을 지웁니다.", "src/delete_row_btn.gif"),
            ("열 삭제하기\n(alt+Delete)", self.hwp_ops.delete_column, 
             "현재 위치의 열을 지웁니다.", "src/delete_column_btn.gif"),
        ]

    def _get_layout_features(self) -> List[Tuple[str, Callable, str, str]]:
        """Get page layout features."""
        return [
            ("구역 나누기\n(alt+shift+enter)", self.hwp_ops.break_section, 
             "구역 나누기를 합니다.", None),
            ("페이지 나누기\n(ctrl+enter)", self.hwp_ops.break_page, 
             "다음 페이지부터 시작하도록 합니다.", None),
            ("기안기 여백설정", self.hwp_ops.setup_koica_page, 
             "페이지여백을 KOICA 공문 기안기에 맞춰 설정합니다.", None),
            ("일반 여백설정", 
             lambda: self.hwp_ops.setup_page_margins(), 
             "페이지여백을 일반 설정으로 변경합니다.", None),
        ]

    def _get_shape_features(self) -> List[Tuple[str, Callable, str, str]]:
        """Get shape and special text features."""
        return [
            ("윗첨자\n(alt+shift+P)", self.hwp_ops.toggle_superscript, 
             "선택한 영역을 윗첨자로 바꿉니다.", "src/super_script_btn.gif"),
            ("미주넣기\n(ctrl+N+E)", self.hwp_ops.insert_endnote, 
             "현재 위치에 미주를 추가합니다.", "src/endnote_btn.gif"),
            ("각주넣기\n(ctrl+N+N)", self.hwp_ops.insert_footnote, 
             "현재 위치에 각주를 추가합니다.", "src/footnote_btn.gif"),
            ("메모넣기", self.hwp_ops.insert_memo, 
             "메모를 넣습니다.", "src/add_memo_btn.gif"),
            ("메모지우기", self.hwp_ops.delete_memo, 
             "메모를 지웁니다.", "src/remove_memo_btn.gif"),
        ]

    def _get_review_features(self) -> List[Tuple[str, Callable, str, str]]:
        """Get review and editing features."""
        return [
            ("연속 공백 색칠하기", self._color_double_space, 
             "공백이 연속해서 들어가 있는 경우 주황색으로 음영색을 칠합니다.", None),
            ("공백 색 지우기", self._uncolor_double_space, 
             "공백의 음영색을 지웁니다.", None),
            ("Bold 처리 폰트로 변환하기", self._process_font, 
             "Kopub 볼드 처리 글자를 볼드를 폰트를 바꿔 줍니다.", None),
        ]

    def _color_double_space(self) -> None:
        """Color double spaces in the document."""
        color_double_space(self.context["app_manager"])

    def _uncolor_double_space(self) -> None:
        """Remove color from double spaces."""
        uncolor_double_space(self.context["app_manager"])

    def _process_font(self) -> None:
        """Process font formatting."""
        process_font(self.context["app_manager"])
