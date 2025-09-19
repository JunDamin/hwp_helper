"""Templates page for managing and using HWP templates."""

import flet as ft
from typing import Dict, Any

from ..components.dialogs import AddTemplateDialog, TemplateManagementDialog
from ...services.template_service import TemplateService
from ...services.hwp_operations import HwpOperationService


class TemplatesPage(ft.Container):
    """Page for template management and usage."""

    def __init__(self, context: Dict[str, Any]):
        super().__init__()
        self.context = context
        self._page = context["page"]
        self.template_service = TemplateService()
        self.hwp_ops = HwpOperationService(context["app_manager"])
        
        self.template_content = ft.Column(scroll=ft.ScrollMode.AUTO)
        self._populate_templates()
        
        self.content = ft.Column([
            ft.Row([
                ft.ElevatedButton(
                    content=ft.Text("선택영역 탬플릿 추가"),
                    on_click=self._add_template
                ),
                ft.ElevatedButton(
                    content=ft.Text("탬플릿 관리"),
                    on_click=self._manage_templates
                ),
            ]),
            self.template_content
        ])

    def _populate_templates(self) -> None:
        """Populate the templates display."""
        self.template_content.controls.clear()
        categories = self.template_service.get_categories()
        panels = []
        
        for key, value in categories.items():
            buttons = []
            for text, image_path, filename, n in value:
                template_path = f"templates/{filename}.hwp"
                buttons.append(
                    ft.ElevatedButton(
                        content=ft.Text(text),
                        on_click=self._create_template_handler(template_path, n),
                    )
                )
            
            panels.append(
                ft.ExpansionPanel(
                    header=ft.ListTile(title=ft.Text(key)),
                    content=ft.Column(buttons)
                )
            )
        
        if panels:
            self.template_content.controls.append(ft.ExpansionPanelList(panels))
        else:
            self.template_content.controls.append(
                ft.Text("템플릿이 없습니다. 템플릿을 추가해주세요.")
            )

    def _create_template_handler(self, template_path: str, move_count: int):
        """Create a handler function for template insertion."""
        def handler(e):
            self.hwp_ops.insert_template(template_path, move_count)
        return handler

    def _add_template(self, e) -> None:
        """Show add template dialog."""
        dialog = AddTemplateDialog(
            self._page, 
            self.context,
            on_complete=self.refresh
        )
        dialog.show()

    def _manage_templates(self, e) -> None:
        """Show template management dialog."""
        categories = self.template_service.get_categories()
        dialog = TemplateManagementDialog(
            self._page,
            categories,
            on_refresh=self.refresh
        )
        dialog.show()

    def refresh(self) -> None:
        """Refresh the templates display."""
        self._populate_templates()
        self.update()
