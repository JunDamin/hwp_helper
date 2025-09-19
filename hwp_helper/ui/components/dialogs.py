"""Dialog components for various operations."""

import flet as ft
from pathlib import Path
from typing import Dict, Any, Optional, Callable

from ...services.template_service import TemplateService
from ...utils.file_utils import prettify_filename


class AddTemplateDialog:
    """Dialog for adding a new template."""

    def __init__(self, page: ft.Page, context: Dict[str, Any], 
                 on_complete: Optional[Callable] = None):
        self.page = page
        self.context = context
        self.app_manager = context["app_manager"]
        self.config = context["config"]
        self.template_service = TemplateService()
        self.on_complete = on_complete
        
        self.category_field = ft.TextField(label="구분")
        self.name_field = ft.TextField(label="제목")
        
        # Prefill category if available
        last_category = self.config.get("last_category")
        if last_category:
            self.category_field.value = last_category

    def show(self) -> None:
        """Show the add template dialog."""
        def on_add(e):
            if self._add_template():
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

    def _add_template(self) -> bool:
        """Add the template."""
        try:
            app = self.app_manager.get_or_create_app()
            category = self.category_field.value
            name = self.name_field.value
            
            if not category or not name:
                return False
            
            success = self.template_service.add_template(app, category, name)
            if success:
                # Save last category
                self.config.set("last_category", category)
                self.config.save_config()
            
            return success
            
        except Exception as e:
            print(f"Error adding template: {e}")
            return False


class TemplateManagementDialog:
    """Dialog for managing templates (rename/delete)."""

    def __init__(self, page: ft.Page, categories: Dict, 
                 on_refresh: Optional[Callable] = None):
        self.page = page
        self.categories = categories
        self.template_service = TemplateService()
        self.on_refresh = on_refresh

    def show(self) -> None:
        """Show the template management dialog."""
        def delete_template(template_path: str, image_path: str):
            def confirm_delete(e):
                self.template_service.delete_template(template_path, image_path)
                if self.on_refresh:
                    self.on_refresh()
                self.dialog.open = False
                self.page.update()
            return confirm_delete

        def rename_template(template_path: str, image_path: str):
            def show_rename_dialog(e):
                self._show_rename_dialog(template_path, image_path)
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
                            on_click=rename_template(template_path, str(image_path))
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            on_click=delete_template(template_path, str(image_path))
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

    def _show_rename_dialog(self, template_path: str, image_path: str) -> None:
        """Show rename dialog for a template."""
        try:
            category, name = Path(template_path).stem.split("_", 1)
        except ValueError:
            category, name = Path(template_path).stem, ""
            
        category_field = ft.TextField(label="구분", value=category)
        name_field = ft.TextField(label="제목", value=name)

        def on_rename(e):
            success = self.template_service.rename_template(
                template_path, image_path,
                category_field.value, name_field.value
            )
            if success:
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


class UpdateTemplatesDialog:
    """Dialog for updating all templates."""

    def __init__(self, page: ft.Page, on_complete: Optional[Callable] = None):
        self.page = page
        self.template_service = TemplateService()
        self.on_complete = on_complete

    def show(self) -> None:
        """Show the update templates dialog."""
        self.progress_bar = ft.ProgressBar(width=400)
        
        def start_update(e):
            self.dialog.content = ft.Column([
                ft.Text("탬플릿을 업데이트 중입니다..."),
                self.progress_bar
            ])
            self.page.update()
            
            # Run the update process
            try:
                for i, n in self.template_service.update_templates():
                    progress = i / (n - 1) if n > 1 else 1.0
                    self.progress_bar.value = progress
                    self.page.update()
            except Exception as e:
                print(f"Error updating templates: {e}")
            
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
