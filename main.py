import flet as ft
import yaml
from functions import (
    check_app, 
    get_path, 
    get_screen_size, 
    set_window_position,
    get_categories,
    set_forewindow,
    get_image,
    update_templates,
    prettify_filename,
)
from pathlib import Path
import shutil as sh
from hwpapi.core import App
from hwpapi.classes import CharShape, ParaShape
from uuid import uuid1
import pythoncom
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

VERSION = "0.3.3"
TEMPLATES_DIR = "templates"
IMAGES_DIR = "images"
ICON_PATH = "src/ai.ico"
AI_IMAGE_PATH = "src/ai.png"

def main(page: ft.Page):
    pythoncom.CoInitialize()
    page.title = f"Hwp Helper v.{VERSION}"
    # page.window_always_on_top = True

    with open("setting.yaml", encoding='utf-8') as f:
        settings = yaml.safe_load(f)

    app = check_app(None)

    def on_closing(e):
        settings["tab"] = page.tabs.selected_index
        with open("setting.yaml", "w") as f:
            yaml.safe_dump(settings, f)
        page.window_destroy()

    page.on_window_event = on_closing

    def set_fullscreen(e):
        pass

    def set_halfscreen(e):
        pass

    def check_hwp(e):
        pass

    def toggle_always_on_top(e):
        page.window_always_on_top = not page.window_always_on_top
        page.update()

    # Navigation Bar
    navi_bar = ft.Row(
        [
            ft.IconButton(icon=ft.Icons.VISIBILITY, on_click=check_hwp, tooltip="한글보이기"),
            ft.IconButton(icon=ft.Icons.FULLSCREEN, on_click=set_fullscreen, tooltip="전체화면"),
            ft.IconButton(icon=ft.Icons.FULLSCREEN_EXIT, on_click=set_halfscreen, tooltip="오른쪽화면"),
            ft.IconButton(icon=ft.Icons.PUSH_PIN, on_click=toggle_always_on_top, tooltip="항상 위"),
        ]
    )

    def _create_feature_button(name, command, tooltip_text, image_path):
        return ft.ElevatedButton(
            text=name,
            on_click=lambda e: command(app),
            tooltip=tooltip_text,
            # image_src=get_path(image_path) if image_path else None
        )

    def _create_feature_section(title, features, n_columns):
        section = ft.Column()
        section.controls.append(ft.Text(title))
        grid = ft.GridView(expand=1, max_extent=150, child_aspect_ratio=1)
        section.controls.append(grid)
        for name, command, tooltip_text, image_path in features:
            grid.controls.append(_create_feature_button(name, command, tooltip_text, image_path))
        return section

    def _char_features():
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

    def _para_features():
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

    def _table_features():
        return [
            ("표 테두리", set_cell_border, "선택한 셀영역의 가장 위와 가장 아래 테두리는 굵은 선으로 바꾸고 좌우 끝의 테두리를 없앱니다.", "src/table_border_btn.gif"),
            ("헤더 스타일 넣기", set_header_style, "선택한 셀영역가장 아래 테두리를 두줄로 바꾸고 셀에 연노란 바탕색을 넣습니다.", "src/table_header_btn.gif"),
            ("행 삭제하기\n(alt+Delete)", delete_row, "현재 위치의 행을 지웁니다.", "src/delete_row_btn.gif"),
            ("열 삭제하기\n(alt+Delete)", delete_column, "현재 위치의 열을 지웁니다.", "src/delete_column_btn.gif"),
        ]

    def _layout_features():
        return [
            ("구역 나누기\n(alt+shift+enter)", break_section, "구역 나누기를 합니다. 구역이 나누어지면 다른 페이지 여백을 설정하거나 이후부터 페이지 가로 세로를 바꾸는 적용이 가능해 집니다.", None),
            ("페이지 나누기\n(ctrl+enter)", break_page, "다음 페이지부터 시작하도록 합니다. 여러번 엔터를 칠 필요 없이 다음 페이지부터 시작합니다.", None),
            ("기안기 여백설정", setup_koica_page, "페이지여백을 KOICA 공문 기안기에 맞춰 설정합니다.", None),
            ("일반 여백설정", setup_normal_page, "페이지여백을 좌우를 20mm, 위는 20mm, 머리말 15mm 아래는 15mm, 꼬리말 5mm, 제본 0mm로 설정합니다.", None),
        ]

    def _shape_features():
        return [
            ("윗첨자\n(alt+shift+P)", super_script, "선택한 영역을 윗첨자, 혹은 원래 형태로 바꿉니다.", "src/super_script_btn.gif"),
            ("미주넣기\n(ctrl+N+E)", insert_endnote, "현재 위치에 번호를 표시하고 마지막 페이지에 설명을 적을 수 있는 미주를 추가합니다.", "src/endnote_btn.gif"),
            ("각주넣기\n(ctrl+N+N)", insert_footnote, "현재 위치에 번호를 표시하고 현재 페이지 아래쪽에 설명을 추가합니다.", "src/footnote_btn.gif"),
            ("메모넣기", insert_memo, "메모를 넣습니다.", "src/add_memo_btn.gif"),
            ("메모지우기", delete_memo, "메모를 지웁니다.", "src/remove_memo_btn.gif"),
        ]

    def _review_features():
        return [
            ("연속 공백 색칠하기", color_doublespace, "공백이 연속해서 들어가 있는 경우 주황색으로 음영색을 칠합니다.", None),
            ("공백 색 지우기", uncolor_doublespace, "공백의 음영색을 지웁니다.", None),
            ("Bold 처리 폰트로 변환하기", process_font, "Kopub 볼드 처리 글자를 볼드를 폰트를 바꿔 줍니다.", None),
        ]

    # Features Tab
    features_tab_content = ft.Column(scroll=ft.ScrollMode.AUTO)
    
    # Font Styles
    font_styles = settings.get("font_styles", {})
    font_style_controls = ft.Column()

    def refresh_font_styles():
        font_style_controls.controls.clear()
        for idx, font_style in font_styles.items():
            charshape = CharShape().fromdict(font_style[0])
            parashape = ParaShape().fromdict(font_style[1])
            font_style_controls.controls.append(create_font_style_button(idx, charshape, parashape))
        page.update()

    def add_style(e):
        charshape, parashape = app.get_charshape(), app.get_parashape()
        idx = str(uuid1())
        font_styles[idx] = (charshape.todict(), parashape.todict())
        settings["font_styles"] = font_styles
        refresh_font_styles()

    def create_font_style_button(idx, charshape, parashape):
        def apply_char(e):
            app.set_charshape(charshape)

        def apply_para(e):
            app.set_parashape(parashape)

        def apply_both(e):
            app.set_charshape(charshape)
            app.set_parashape(parashape)

        def delete_style(e):
            del font_styles[idx]
            settings["font_styles"] = font_styles
            refresh_font_styles()

        return ft.Row([
            ft.ElevatedButton("둘다적용", on_click=apply_both),
            ft.ElevatedButton("글자적용", on_click=apply_char),
            ft.ElevatedButton("문단적용", on_click=apply_para),
            ft.ElevatedButton("삭제하기", on_click=delete_style),
            ft.Text(f"{charshape.hangul_font} {charshape.fontsize}pt")
        ])

    refresh_font_styles() # Initial population

    font_style_panel = ft.ExpansionPanelList(
        [
            ft.ExpansionPanel(
                header=ft.ListTile(title=ft.Text("글자서식")),
                content=ft.Column([
                    ft.ElevatedButton("현재 서식 저장", on_click=add_style),
                    font_style_controls
                ])
            )
        ]
    )
    features_tab_content.controls.append(font_style_panel)

    features_tab_content.controls.append(_create_feature_section("글자 모양 기능", _char_features(), 3))
    features_tab_content.controls.append(_create_feature_section("문단 정렬 기능", _para_features(), 3))
    features_tab_content.controls.append(_create_feature_section("테이블 관련 기능", _table_features(), 3))
    features_tab_content.controls.append(_create_feature_section("페이지 관련 기능", _layout_features(), 3))
    features_tab_content.controls.append(_create_feature_section("메모 관련 기능", _shape_features(), 3))
    features_tab_content.controls.append(_create_feature_section("검토 기능", _review_features(), 3))

    # Templates Tab
    def refresh_templates():
        # Clear existing templates
        for control in templates_tab_content.controls:
            if isinstance(control, ft.ExpansionPanelList):
                templates_tab_content.controls.remove(control)

        # Repopulate templates
        categories = get_categories()
        panels = []
        for key, value in categories.items():
            buttons = []
            for text, image_path, filename, n in value:
                path = f"templates/{filename}.hwp"
                buttons.append(
                    ft.ElevatedButton(
                        text=text,
                        # image_src=get_path(image_path),
                        on_click=_make_func(path, n),
                    )
                )
            panels.append(
                ft.ExpansionPanel(
                    header=ft.ListTile(title=ft.Text(key)),
                    content=ft.Column(buttons)
                )
            )
        
        templates_tab_content.controls.append(ft.ExpansionPanelList(panels))
        page.update()

    def add_template(category, name):
        temp = Path("temp")
        temp.mkdir(exist_ok=True)
        temp_path = Path("temp/temp.hwp")
        app.save_block(temp_path)

        destination = Path(f"templates/{prettify_filename(f'{category}_{name}')}.hwp")

        if destination.exists():
            return False
        
        Path(temp_path).rename(destination)

        temp_app = App(is_visible=False, new_app=True)
        # update_template(temp_app, destination)
        temp_app.quit()
        sh.rmtree("temp")
        refresh_templates()
        return True

    def add_template_dialog(e):
        category_field = ft.TextField(label="구분")
        name_field = ft.TextField(label="제목")

        def on_add(e):
            if add_template(category_field.value, name_field.value):
                dialog.open = False
                page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("선택영역 탬플릿 추가"),
            content=ft.Column([category_field, name_field]),
            actions=[ft.TextButton("추가", on_click=on_add), ft.TextButton("취소", on_click=lambda e: setattr(dialog, 'open', False) or page.update())]
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def update_templates_dialog(e):
        def delete_template(template_path, image_path):
            Path(template_path).unlink()
            Path(image_path).unlink()
            refresh_templates()

        def rename_template(template_path, image_path, new_category, new_name):
            new_fname = prettify_filename(f"{new_category}_{new_name}")
            n = Path(image_path).stem.split("_")[-1]
            destination = Path(f"templates/{new_fname}.hwp")
            if destination.exists():
                return

            Path(template_path).rename(destination)
            image_destination = Path(f"images/{new_fname}_{n}.png")
            Path(image_path).rename(image_destination)
            refresh_templates()

        def rename_dialog(template_path, image_path):
            category, name = Path(template_path).stem.split("_")
            category_field = ft.TextField(label="구분", value=category)
            name_field = ft.TextField(label="제목", value=name)

            def on_rename(e):
                rename_template(template_path, image_path, category_field.value, name_field.value)
                dialog.open = False
                page.update()

            dialog = ft.AlertDialog(
                title=ft.Text("이름 바꾸기"),
                content=ft.Column([category_field, name_field]),
                actions=[ft.TextButton("바꾸기", on_click=on_rename), ft.TextButton("취소", on_click=lambda e: setattr(dialog, 'open', False) or page.update())]
            )
            page.dialog = dialog
            dialog.open = True
            page.update()

        controls = []
        categories = get_categories()
        for key, value in categories.items():
            for text, image_path, filename, n in value:
                template_path = f"templates/{filename}.hwp"
                controls.append(
                    ft.Row([
                        ft.Text(text),
                        ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, path=template_path, img_path=image_path: rename_dialog(path, img_path)),
                        ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, path=template_path, img_path=image_path: delete_template(path, img_path))
                    ])
                )

        dialog = ft.AlertDialog(
            title=ft.Text("탬플릿 관리"),
            content=ft.Column(controls, scroll=ft.ScrollMode.AUTO),
            actions=[ft.TextButton("닫기", on_click=lambda e: setattr(dialog, 'open', False) or page.update())]
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def _make_func(path, n):
        def func(e):
            check_app(app)
            set_forewindow(app)
            app.insert_file(path)
            for _ in range(n):
                app.move("NextPara")
            return None
        return func

    templates_tab_content = ft.Column(scroll=ft.ScrollMode.AUTO)
    template_buttons = ft.Row(
        [
            ft.ElevatedButton(text="선택영역 탬플릿 추가", on_click=add_template_dialog),
            ft.ElevatedButton(text="탬플릿 관리", on_click=update_templates_dialog),
        ]
    )
    templates_tab_content.controls.append(template_buttons)

    categories = get_categories()
    panels = []
    for key, value in categories.items():
        buttons = []
        for text, image_path, filename, n in value:
            path = f"templates/{filename}.hwp"
            buttons.append(
                ft.ElevatedButton(
                    text=text,
                    # image_src=get_path(image_path),
                    on_click=_make_func(path, n),
                )
            )
        panels.append(
            ft.ExpansionPanel(
                header=ft.ListTile(title=ft.Text(key)),
                content=ft.Column(buttons)
            )
        )
    
    templates_tab_content.controls.append(ft.ExpansionPanelList(panels))

    tabs = ft.Tabs(
        selected_index=settings.get("tab", 0),
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Features",
                content=features_tab_content,
            ),
            ft.Tab(
                text="Templates",
                content=templates_tab_content,
            ),
        ],
        expand=1,
    )

    page.add(
        ft.Row([ft.Image(src=get_path(AI_IMAGE_PATH), width=50, height=50), ft.Text(page.title)]),
        navi_bar,
        tabs,
    )

    # Initial window size and position
    x, y, width, height = get_screen_size()
    app_width = settings.get("app_width", 674)
    app_x, app_y = x + width - app_width, y
    page.window_left = app_x
    page.window_top = app_y
    page.window_width = app_width
    page.window_height = height

    page.update()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="C:\\Users\\freed\\Documents\\python_projects\\008_hwp_helper")