import flet as ft
from pathlib import Path
import shutil as sh
from functions import prettify_filename, update_template, get_path
from hwpapi.classes import CharShape, ParaShape
from hwpapi.core import App
from uuid import uuid1


class FontStyleManager(ft.UserControl):
    """
    A Flet component for managing font styles. 
    It includes buttons for saving current font styles and displaying saved styles.
    """

    def __init__(self, context, **kwargs):
        super().__init__(**kwargs)
        self.app = context["app"]
        self.context = context
        self.font_styles = context["setting"].get("font_styles", {})
        self.font_style_controls = ft.Column()

    def build(self):
        self.refresh_font_styles()
        
        return ft.ExpansionPanelList(
            [
                ft.ExpansionPanel(
                    header=ft.ListTile(title=ft.Text("글자서식")),
                    content=ft.Column([
                        ft.ElevatedButton("현재 서식 저장", on_click=self.add_style),
                        self.font_style_controls
                    ])
                )
            ]
        )

    def refresh_font_styles(self):
        self.font_style_controls.controls.clear()
        for idx, font_style in self.font_styles.items():
            charshape = CharShape().fromdict(font_style[0])
            parashape = ParaShape().fromdict(font_style[1])
            self.font_style_controls.controls.append(
                self.create_font_style_button(idx, charshape, parashape)
            )

    def add_style(self, e):
        charshape, parashape = self.app.get_charshape(), self.app.get_parashape()
        idx = str(uuid1())
        self.font_styles[idx] = (charshape.todict(), parashape.todict())
        self.context["setting"]["font_styles"] = self.font_styles
        self.refresh_font_styles()
        self.update()

    def create_font_style_button(self, idx, charshape, parashape):
        def apply_char(e):
            self.app.set_charshape(charshape)

        def apply_para(e):
            self.app.set_parashape(parashape)

        def apply_both(e):
            self.app.set_charshape(charshape)
            self.app.set_parashape(parashape)

        def delete_style(e):
            del self.font_styles[idx]
            self.context["setting"]["font_styles"] = self.font_styles
            self.refresh_font_styles()
            self.update()

        return ft.Row([
            ft.ElevatedButton("둘다적용", on_click=apply_both),
            ft.ElevatedButton("글자적용", on_click=apply_char),
            ft.ElevatedButton("문단적용", on_click=apply_para),
            ft.ElevatedButton("삭제하기", on_click=delete_style),
            ft.Text(f"{charshape.hangul_font} {charshape.fontsize}pt")
        ])


class AddTemplateDialog:
    """
    Dialog for adding a new template.
    """

    def __init__(self, page: ft.Page, context, on_complete=None):
        self.page = page
        self.context = context
        self.app = context["app"]
        self.on_complete = on_complete
        self.category_field = ft.TextField(label="구분")
        self.name_field = ft.TextField(label="제목")
        
        # Prefill category if available
        last_category = self.context["setting"].get("last_category")
        if last_category:
            self.category_field.value = last_category

    def show(self):
        def on_add(e):
            if self.add_template():
                self.dialog.open = False
                self.page.update()
                if self.on_complete:
                    self.on_complete()

        def on_cancel(e):
            self.dialog.open = False
            self.page.update()

        self.dialog = ft.AlertDialog(
            title=ft.Text("선택영역 탬플릿 추가"),
            content=ft.Column([
                self.category_field,
                self.name_field
            ]),
            actions=[
                ft.TextButton("추가", on_click=on_add),
                ft.TextButton("취소", on_click=on_cancel)
            ]
        )
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def add_template(self):
        temp = Path("temp")
        temp.mkdir(exist_ok=True)
        temp_path = Path("temp/temp.hwp")
        self.app.save_block(temp_path)

        category = self.category_field.value
        name = self.name_field.value
        destination = Path(f"templates/{prettify_filename(f'{category}_{name}')}.hwp")

        if destination.exists():
            # Show error message
            return False
        
        Path(temp_path).rename(destination)

        temp_app = App(is_visible=False, new_app=True)
        # update_template(temp_app, destination)
        temp_app.quit()
        sh.rmtree("temp")
        return True


class TemplateManagementDialog:
    """
    Dialog for managing templates (rename/delete).
    """

    def __init__(self, page: ft.Page, categories, on_refresh=None):
        self.page = page
        self.categories = categories
        self.on_refresh = on_refresh

    def show(self):
        def delete_template(template_path, image_path):
            def confirm_delete(e):
                Path(template_path).unlink()
                Path(image_path).unlink()
                if self.on_refresh:
                    self.on_refresh()
                self.dialog.open = False
                self.page.update()
            return confirm_delete

        def rename_template(template_path, image_path):
            def show_rename_dialog(e):
                self.show_rename_dialog(template_path, image_path)
            return show_rename_dialog

        controls = []
        for key, value in self.categories.items():
            for text, image_path, filename, n in value:
                template_path = f"templates/{filename}.hwp"
                controls.append(
                    ft.Row([
                        ft.Text(text),
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            on_click=rename_template(template_path, image_path)
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            on_click=delete_template(template_path, image_path)
                        )
                    ])
                )

        def on_close(e):
            self.dialog.open = False
            self.page.update()

        self.dialog = ft.AlertDialog(
            title=ft.Text("탬플릿 관리"),
            content=ft.Column(controls, scroll=ft.ScrollMode.AUTO),
            actions=[ft.TextButton("닫기", on_click=on_close)]
        )
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def show_rename_dialog(self, template_path, image_path):
        category, name = Path(template_path).stem.split("_")
        category_field = ft.TextField(label="구분", value=category)
        name_field = ft.TextField(label="제목", value=name)

        def on_rename(e):
            self.rename_template_files(template_path, image_path, 
                                     category_field.value, name_field.value)
            rename_dialog.open = False
            self.dialog.open = False
            self.page.update()
            if self.on_refresh:
                self.on_refresh()

        def on_cancel(e):
            rename_dialog.open = False
            self.page.update()

        rename_dialog = ft.AlertDialog(
            title=ft.Text("이름 바꾸기"),
            content=ft.Column([category_field, name_field]),
            actions=[
                ft.TextButton("바꾸기", on_click=on_rename),
                ft.TextButton("취소", on_click=on_cancel)
            ]
        )
        self.page.dialog = rename_dialog
        rename_dialog.open = True
        self.page.update()

    def rename_template_files(self, template_path, image_path, new_category, new_name):
        new_fname = prettify_filename(f"{new_category}_{new_name}")
        n = Path(image_path).stem.split("_")[-1]
        destination = Path(f"templates/{new_fname}.hwp")
        if destination.exists():
            return

        Path(template_path).rename(destination)
        image_destination = Path(f"images/{new_fname}_{n}.png")
        Path(image_path).rename(image_destination)
