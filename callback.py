# %%
from functions import back_to_app
from hwpapi.dataclasses import CharShape


@back_to_app
def set_cell_border(app):
    return app.set_cell_border(
        top=1, bottom=1, right=0, left=0, top_width=0.4, bottom_width=0.4
    )


@back_to_app
def set_header_style(app):
    app.set_cell_color(bg_color=(250, 243, 219))
    app.set_cell_border(bottom=8, bottom_width=0.5)
    return None


@back_to_app
def set_para_indent(app):
    return app.actions.ParagraphShapeIndentAtCaret().run()


@back_to_app
def break_section(app):
    return app.actions.BreakSection().run()


@back_to_app
def super_script(app):
    return app.actions.CharShapeSuperscript().run()


@back_to_app
def break_page(app):
    return app.actions.BreakPage().run()


@back_to_app
def insert_endnote(app):
    return app.actions.InsertEndnote().run()


@back_to_app
def insert_footnote(app):
    return app.actions.InsertFootnote().run()


@back_to_app
def insert_memo(app):
    return app.actions.InsertFieldMemo().run()


@back_to_app
def delete_memo(app):
    return app.actions.DeleteFieldMemo().run()


@back_to_app
def increase_line_spacing(app):
    return app.actions.ParagraphShapeIncreaseLineSpacing().run()


@back_to_app
def decrease_line_spacing(app):
    return app.actions.ParagraphShapeDecreaseLineSpacing().run()


@back_to_app
def setup_koica_page(app):
    return app.setup_page(
        top=30, bottom=15, left=20, right=15, header=0, footer=15, gutter=0
    )


@back_to_app
def setup_normal_page(app):
    return app.setup_page()


@back_to_app
def delete_row(app):
    action = app.actions.TableDeleteRowColumn()
    p = action.pset
    p.type = 1
    return action.run()


@back_to_app
def delete_column(app):
    action = app.actions.TableDeleteRowColumn()
    p = action.pset
    p.type = 0
    return action.run()


@back_to_app
def increase_fontsize(app):
    return app.actions.CharShapeHeightIncrease().run()


@back_to_app
def decrease_fontsize(app):
    return app.actions.CharShapeHeightDecrease().run()


@back_to_app
def increase_spacing(app):
    return app.actions.CharShapeSpacingIncrease().run()


@back_to_app
def decrease_spacing(app):
    return app.actions.CharShapeSpacingDecrease().run()


@back_to_app
def align_left(app):
    return app.actions.ParagraphShapeAlignLeft().run()


@back_to_app
def align_center(app):
    return app.actions.ParagraphShapeAlignCenter().run()


@back_to_app
def align_right(app):
    return app.actions.ParagraphShapeAlignRight().run()


@back_to_app
def align_justified(app):
    return app.actions.ParagraphShapeAlignJustify().run()


@back_to_app
def align_distributed(app):
    return app.actions.ParagraphShapeAlignDistribute().run()


@back_to_app
def set_red(app):
    return app.actions.CharShapeTextColorRed().run()


@back_to_app
def set_green(app):
    return app.actions.CharShapeTextColorGreen().run()


@back_to_app
def set_blue(app):
    return app.actions.CharShapeTextColorBlue().run()


@back_to_app
def set_black(app):
    return app.actions.CharShapeTextColorBlack().run()


@back_to_app
def set_white(app):
    return app.actions.CharShapeTextColorWhite().run()


### get color for double space

color = "#ffaa11"


@back_to_app
def color_doublespace(app):
    app.replace_all(
        "  ",
        "  ",
        old_charshape=CharShape(),
        new_charshape=CharShape(shade_color=color),
        find_reg_exp=True,
    )


@back_to_app
def uncolor_doublespace(app):
    app.replace_all(
        " ",
        " ",
        old_charshape=CharShape(shade_color=color),
        new_charshape=CharShape(shade_color=4294967295),
        find_reg_exp=True,
    )

@back_to_app
def process_font(app):
    font_families = [
        ["KoPubWorld돋움체 Bold", ("KoPubWorld돋움체 Medium", "KoPubWorld돋움체 Light")],
        ["KoPubWorld바탕체 Bold", ("KoPubWorld바탕체 Medium", "KoPubWorld바탕체 Light")],
        [
            "KoPub돋움체 Bold",
            ("KoPub돋움체 Medium", "KoPub돋움체 Light"),
        ],
        [
            "KoPub바탕체 Bold",
            (
                "KoPub바탕체 Medium",
                "KoPub바탕체 Light",
            ),
        ],
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

# %%
