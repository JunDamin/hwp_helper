import flet as ft
from components_flet import AddTemplateDialog, TemplateManagementDialog
from functions import (
    update_templates,
    get_categories,
    set_forewindow,
    check_app,
    get_path,
)


class CategoryFrame(ft.UserControl):
    """
    A frame that displays categories from images file.
    """

    def __init__(self, context):
        super().__init__()
        self.app = context["app"]
        self.context = context
        self.page = context["helper"].page

    def build(self):
        self.template_content = ft.Column(scroll=ft.ScrollMode.AUTO)
        self._populate_templates()
        
        return ft.Column([
            ft.Row([
                ft.ElevatedButton(
                    text="선택영역 탬플릿 추가",
                    on_click=self.add_template
                ),
                ft.ElevatedButton(
                    text="탬플릿 관리",
                    on_click=self.manage_templates
                ),
            ]),
            self.template_content
        ])

    def _populate_templates(self):
        self.template_content.controls.clear()
        categories = get_categories()
        panels = []
        
        for key, value in categories.items():
            buttons = []
            for text, image_path, filename, n in value:
                path = f"templates/{filename}.hwp"
                buttons.append(
                    ft.ElevatedButton(
                        text=text,
                        on_click=self._make_func(path, n),
                    )
                )
            
            panels.append(
                ft.ExpansionPanel(
                    header=ft.ListTile(title=ft.Text(key)),
                    content=ft.Column(buttons)
                )
            )
        
        self.template_content.controls.append(ft.ExpansionPanelList(panels))

    def _make_func(self, path, n):
        def func(e):
            check_app(self.app)
            set_forewindow(self.app)
            self.app.insert_file(path)
            for _ in range(n):
                self.app.move("NextPara")
            return None
        return func

    def add_template(self, e):
        dialog = AddTemplateDialog(
            self.page, 
            self.context,
            on_complete=self.refresh
        )
        dialog.show()

    def manage_templates(self, e):
        categories = get_categories()
        dialog = TemplateManagementDialog(
            self.page,
            categories,
            on_refresh=self.refresh
        )
        dialog.show()

    def refresh(self):
        self._populate_templates()
        self.update()


class UpdateTemplatesDialog:
    """
    Dialog for updating all templates from the templates folder.
    """

    def __init__(self, page: ft.Page, on_complete=None):
        self.page = page
        self.on_complete = on_complete

    def show(self):
        self.progress_bar = ft.ProgressBar(width=400)
        
        def start_update(e):
            self.dialog.content = ft.Column([
                ft.Text("탬플릿을 업데이트 중입니다..."),
                self.progress_bar
            ])
            self.page.update()
            
            # Run the update process
            for i, n in update_templates():
                progress = i / (n - 1) if n > 1 else 1.0
                self.progress_bar.value = progress
                self.page.update()
            
            self.dialog.open = False
            self.page.update()
            if self.on_complete:
                self.on_complete()

        def on_cancel(e):
            self.dialog.open = False
            self.page.update()

        self.dialog = ft.AlertDialog(
            title=ft.Text("탬플릿 업데이트"),
            content=ft.Text("templates 폴더의 한글 파일들을 탬플릿으로 변환하시겠습니까?"),
            actions=[
                ft.TextButton("시작", on_click=start_update),
                ft.TextButton("취소", on_click=on_cancel)
            ]
        )
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()
