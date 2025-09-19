"""HWP callback functions for complex operations."""

from hwpapi.classes import CharShape

from ..core.app_manager import HwpAppManager
from ..utils.window_utils import set_forewindow


def ensure_app_ready(func):
    """Decorator to ensure HWP app is ready before operation."""
    def wrapper(app_manager: HwpAppManager, *args, **kwargs):
        app = app_manager.ensure_app_ready()
        return func(app, *args, **kwargs)
    return wrapper


@ensure_app_ready
def color_double_space(app) -> None:
    """Color double spaces in the document."""
    color = "#ffaa11"
    app.replace_all(
        "  ",
        "  ",
        old_charshape=CharShape(),
        new_charshape=CharShape(shade_color=color),
        find_reg_exp=True,
    )


@ensure_app_ready
def uncolor_double_space(app) -> None:
    """Remove color from double spaces."""
    color = "#ffaa11"
    app.replace_all(
        " ",
        " ",
        old_charshape=CharShape(shade_color=color),
        new_charshape=CharShape(shade_color=4294967295),
        find_reg_exp=True,
    )


@ensure_app_ready
def process_font(app) -> None:
    """Process KoPub font formatting."""
    font_families = [
        ["KoPubWorld돋움체 Bold", ("KoPubWorld돋움체 Medium", "KoPubWorld돋움체 Light")],
        ["KoPubWorld바탕체 Bold", ("KoPubWorld바탕체 Medium", "KoPubWorld바탕체 Light")],
        ["KoPub돋움체 Bold", ("KoPub돋움체 Medium", "KoPub돋움체 Light")],
        ["KoPub바탕체 Bold", ("KoPub바탕체 Medium", "KoPub바탕체 Light")],
    ]

    for bold_font, fonts in font_families:
        for font in fonts:
            app.replace_all(
                old_charshape=CharShape(font=font, bold=True),
                new_charshape=CharShape(font=bold_font, bold=False),
            )
            app.replace_all(
                old_charshape=CharShape(font=bold_font, bold=True),
                new_charshape=CharShape(font=bold_font, bold=False),
            )
