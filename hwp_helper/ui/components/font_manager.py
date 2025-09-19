"""Font style management component."""

import flet as ft
from uuid import uuid1
from typing import Dict, Any

from hwpapi.classes import CharShape, ParaShape


class FontStyleManager(ft.Container):
    """A Flet component for managing font styles."""

    def __init__(self, context: Dict[str, Any], **kwargs):
        super().__init__(**kwargs)
        self.context = context
        self.app_manager = context["app_manager"]
        self.config = context["config"]
        
        self.font_styles = self.config.get("font_styles", {})
        self.font_style_controls = ft.Column()
        
        self._refresh_font_styles()
        
        self.content = ft.ExpansionPanelList([
            ft.ExpansionPanel(
                header=ft.ListTile(title=ft.Text("글자서식")),
                content=ft.Column([
                    ft.ElevatedButton(content=ft.Text("현재 서식 저장"), on_click=self._add_style),
                    self.font_style_controls
                ])
            )
        ])

    def _refresh_font_styles(self) -> None:
        """Refresh the font styles display."""
        self.font_style_controls.controls.clear()
        
        for idx, font_style in self.font_styles.items():
            charshape = CharShape().fromdict(font_style[0])
            parashape = ParaShape().fromdict(font_style[1])
            self.font_style_controls.controls.append(
                self._create_font_style_button(idx, charshape, parashape)
            )

    def _add_style(self, e) -> None:
        """Add current font style to saved styles."""
        app = self.app_manager.get_or_create_app()
        charshape, parashape = app.get_charshape(), app.get_parashape()
        
        idx = str(uuid1())
        self.font_styles[idx] = (charshape.todict(), parashape.todict())
        self.config.set("font_styles", self.font_styles)
        
        self._refresh_font_styles()
        self.update()

    def _create_font_style_button(self, idx: str, charshape: CharShape, 
                                 parashape: ParaShape) -> ft.Row:
        """Create a button row for a font style."""
        def apply_char(e):
            app = self.app_manager.ensure_app_ready()
            app.set_charshape(charshape)

        def apply_para(e):
            app = self.app_manager.ensure_app_ready()
            app.set_parashape(parashape)

        def apply_both(e):
            app = self.app_manager.ensure_app_ready()
            app.set_charshape(charshape)
            app.set_parashape(parashape)

        def delete_style(e):
            del self.font_styles[idx]
            self.config.set("font_styles", self.font_styles)
            self._refresh_font_styles()
            self.update()

        return ft.Row([
            ft.ElevatedButton(content=ft.Text("둘다적용"), on_click=apply_both),
            ft.ElevatedButton(content=ft.Text("글자적용"), on_click=apply_char),
            ft.ElevatedButton(content=ft.Text("문단적용"), on_click=apply_para),
            ft.ElevatedButton(content=ft.Text("삭제하기"), on_click=delete_style),
            ft.Text(f"{charshape.hangul_font} {charshape.fontsize}pt")
        ])
