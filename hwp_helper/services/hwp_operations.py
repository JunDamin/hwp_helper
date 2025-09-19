"""HWP operation service for business logic."""

from typing import Any
from functools import wraps

from ..core.app_manager import HwpAppManager


def ensure_app_ready(func):
    """Decorator to ensure HWP app is ready before operation."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        app = self.app_manager.ensure_app_ready()
        return func(self, app, *args, **kwargs)
    return wrapper


class HwpOperationService:
    """Service for HWP-specific operations."""
    
    def __init__(self, app_manager: HwpAppManager):
        self.app_manager = app_manager
    
    @ensure_app_ready
    def insert_template(self, app, template_path: str, move_count: int = 0) -> None:
        """Insert a template file and move cursor."""
        app.insert_file(template_path)
        for _ in range(move_count):
            app.move("NextPara")
    
    @ensure_app_ready
    def set_cell_border(self, app, top: int = 1, bottom: int = 1, 
                       right: int = 0, left: int = 0, 
                       top_width: float = 0.4, bottom_width: float = 0.4) -> Any:
        """Set cell border style."""
        return app.set_cell_border(
            top=top, bottom=bottom, right=right, left=left,
            top_width=top_width, bottom_width=bottom_width
        )
    
    @ensure_app_ready
    def set_header_style(self, app) -> None:
        """Apply header style to selected cells."""
        app.set_cell_color(bg_color=(250, 243, 219))
        app.set_cell_border(bottom=8, bottom_width=0.5)
    
    @ensure_app_ready
    def setup_page_margins(self, app, top: int = 20, bottom: int = 15, 
                          left: int = 20, right: int = 20, header: int = 15, 
                          footer: int = 5, gutter: int = 0) -> Any:
        """Setup page margins."""
        return app.setup_page(
            top=top, bottom=bottom, left=left, right=right,
            header=header, footer=footer, gutter=gutter
        )
    
    @ensure_app_ready
    def setup_koica_page(self, app) -> Any:
        """Setup KOICA document page margins."""
        return app.setup_page(
            top=30, bottom=15, left=20, right=15, 
            header=0, footer=15, gutter=0
        )
    
    # Font and character operations
    @ensure_app_ready
    def increase_font_size(self, app) -> Any:
        """Increase font size."""
        return app.actions.CharShapeHeightIncrease().run()
    
    @ensure_app_ready
    def decrease_font_size(self, app) -> Any:
        """Decrease font size."""
        return app.actions.CharShapeHeightDecrease().run()
    
    @ensure_app_ready
    def increase_spacing(self, app) -> Any:
        """Increase character spacing."""
        return app.actions.CharShapeSpacingIncrease().run()
    
    @ensure_app_ready
    def decrease_spacing(self, app) -> Any:
        """Decrease character spacing."""
        return app.actions.CharShapeSpacingDecrease().run()
    
    # Paragraph alignment operations
    @ensure_app_ready
    def align_left(self, app) -> Any:
        """Align paragraph to left."""
        return app.actions.ParagraphShapeAlignLeft().run()
    
    @ensure_app_ready
    def align_center(self, app) -> Any:
        """Align paragraph to center."""
        return app.actions.ParagraphShapeAlignCenter().run()
    
    @ensure_app_ready
    def align_right(self, app) -> Any:
        """Align paragraph to right."""
        return app.actions.ParagraphShapeAlignRight().run()
    
    @ensure_app_ready
    def align_justified(self, app) -> Any:
        """Justify paragraph alignment."""
        return app.actions.ParagraphShapeAlignJustify().run()
    
    @ensure_app_ready
    def align_distributed(self, app) -> Any:
        """Distribute paragraph alignment."""
        return app.actions.ParagraphShapeAlignDistribute().run()
    
    # Color operations
    @ensure_app_ready
    def set_text_color_red(self, app) -> Any:
        """Set text color to red."""
        return app.actions.CharShapeTextColorRed().run()
    
    @ensure_app_ready
    def set_text_color_green(self, app) -> Any:
        """Set text color to green."""
        return app.actions.CharShapeTextColorGreen().run()
    
    @ensure_app_ready
    def set_text_color_blue(self, app) -> Any:
        """Set text color to blue."""
        return app.actions.CharShapeTextColorBlue().run()
    
    @ensure_app_ready
    def set_text_color_black(self, app) -> Any:
        """Set text color to black."""
        return app.actions.CharShapeTextColorBlack().run()
    
    @ensure_app_ready
    def set_text_color_white(self, app) -> Any:
        """Set text color to white."""
        return app.actions.CharShapeTextColorWhite().run()
    
    # Line spacing operations
    @ensure_app_ready
    def increase_line_spacing(self, app) -> Any:
        """Increase line spacing."""
        return app.actions.ParagraphShapeIncreaseLineSpacing().run()
    
    @ensure_app_ready
    def decrease_line_spacing(self, app) -> Any:
        """Decrease line spacing."""
        return app.actions.ParagraphShapeDecreaseLineSpacing().run()
    
    # Table operations
    @ensure_app_ready
    def delete_row(self, app) -> Any:
        """Delete current row."""
        action = app.actions.TableDeleteRowColumn()
        action.pset.type = 1
        return action.run()
    
    @ensure_app_ready
    def delete_column(self, app) -> Any:
        """Delete current column."""
        action = app.actions.TableDeleteRowColumn()
        action.pset.type = 0
        return action.run()
    
    # Document structure operations
    @ensure_app_ready
    def break_page(self, app) -> Any:
        """Insert page break."""
        return app.actions.BreakPage().run()
    
    @ensure_app_ready
    def break_section(self, app) -> Any:
        """Insert section break."""
        return app.actions.BreakSection().run()
    
    @ensure_app_ready
    def set_paragraph_indent(self, app) -> Any:
        """Set paragraph indent at caret position."""
        return app.actions.ParagraphShapeIndentAtCaret().run()
    
    # Special text operations
    @ensure_app_ready
    def toggle_superscript(self, app) -> Any:
        """Toggle superscript formatting."""
        return app.actions.CharShapeSuperscript().run()
    
    # Notes operations
    @ensure_app_ready
    def insert_footnote(self, app) -> Any:
        """Insert footnote."""
        return app.actions.InsertFootnote().run()
    
    @ensure_app_ready
    def insert_endnote(self, app) -> Any:
        """Insert endnote."""
        return app.actions.InsertEndnote().run()
    
    # Memo operations
    @ensure_app_ready
    def insert_memo(self, app) -> Any:
        """Insert memo."""
        return app.actions.InsertFieldMemo().run()
    
    @ensure_app_ready
    def delete_memo(self, app) -> Any:
        """Delete memo."""
        return app.actions.DeleteFieldMemo().run()
