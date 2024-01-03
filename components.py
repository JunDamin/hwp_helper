# %%

import customtkinter as ctk
from customtkinter import CTkFont
import tkinter as tk
from pathlib import Path
import shutil as sh
from PIL import Image, ImageTk
from itertools import count, cycle
from functions import get_image, make_topmost, prettify_filename, update_template, get_screen_size
from hwpapi.dataclasses import CharShape, ParaShape
from hwpapi.core import App
from uuid import uuid1


# %%
class ImageLabel(tk.Label):
    """
    A custom tkinter label for displaying images and animations (GIFs).
    """

    def load(self, image_source):
        """ Load an image or GIF from the given source. """
        frames, self.delay = self._extract_frames(image_source)
        self.frames = cycle(frames) if frames else None
        self._display_initial_frame(frames)

    def _extract_frames(self, image_source):
        """ Extract frames from the given image source. """
        if isinstance(image_source, str):
            image_source = Image.open(image_source)

        frames = []
        delay = 100  # default delay for non-animated images

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(image_source.copy()))
                image_source.seek(i)
                delay = image_source.info.get("duration", delay)
        except EOFError:
            pass

        return frames, delay

    def _display_initial_frame(self, frames):
        """ Display the initial frame of the image or GIF. """
        if frames:
            self.config(image=next(self.frames))
            if len(frames) > 1:
                self.next_frame()

    def unload(self):
        """ Unload the current image or GIF. """
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        """ Display the next frame in the GIF. """
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)



# %%
class ToolTip:
    """
    A class to create a tooltip for a given widget.
    """

    def __init__(self, widget, text, gif=None):
        """ Initialize the tooltip with the widget, text, and optional GIF. """
        self.widget = widget
        self.text = text
        self.gif = gif
        self.tooltip_window = None
        self._bind_widget_events()
        self._set_screen_dimensions()

    def _bind_widget_events(self):
        """ Bind mouse enter and leave events to the widget. """
        self.widget.bind("<Enter>", self._show_tooltip)
        self.widget.bind("<Leave>", self._hide_tooltip)

    def _set_screen_dimensions(self):
        """ Set screen dimensions for positioning the tooltip. """
        _, _, self.screen_width, self.screen_height = get_screen_size()

    def _show_tooltip(self, event=None):
        """ Show the tooltip. """
        x, y, width, height = self._calculate_tooltip_position()
        self._create_tooltip_window(x, y, width, height)

    def _calculate_tooltip_position(self):
        """ Calculate the position of the tooltip based on the widget's position. """
        self.widget.update_idletasks()
        x, y, width, height = self.widget.bbox("insert")
        x += self.widget.winfo_rootx()
        y += self.widget.winfo_rooty() + height
        return x, y, width, height

    def _create_tooltip_window(self, x, y, width, height):
        """ Create the tooltip window at the calculated position. """
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)

        self._add_tooltip_content(tw)
        self._adjust_tooltip_position(tw, x, y, width, height)

    def _add_tooltip_content(self, tooltip_window):
        """ Add text and optional GIF to the tooltip window. """
        label = tk.Label(
            tooltip_window, text=self.text, background="#dddddd", wraplength=350, font=15, pady=5
        )
        label.pack(pady=10)
        if self.gif:
            imagelabel = ImageLabel(tooltip_window)
            imagelabel.pack()
            imagelabel.load(self.gif)

    def _adjust_tooltip_position(self, tooltip_window, x, y, width, height):
        """ Adjust the tooltip position to fit within the screen. """
        tooltip_window.update_idletasks()
        tw_width, tw_height = tooltip_window.winfo_width(), tooltip_window.winfo_height()
        
        if x + tw_width > self.screen_width:
            x -= (tw_width - width)
        if y + tw_height > self.screen_height:
            y -= (tw_height + height)

        tooltip_window.wm_geometry(f"+{x}+{y}")

    def _hide_tooltip(self, event=None):
        """ Hide the tooltip. """
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None



# %%

class CollapsibleFrame(ctk.CTkFrame):
    """
    A custom tkinter frame that can be collapsed or expanded.

    This frame contains a toggle button to show/hide its contents and allows 
    dynamic addition of widgets in a grid layout.
    """

    def __init__(self, parent=None, text="Toggle", n_columns=1, **kwargs):
        super().__init__(parent, **kwargs)
        self._next_row = 0
        self.n_columns = n_columns

        self._create_toggle_button(text)
        self._create_content_frame()

    def _create_toggle_button(self, text):
        """ Create the toggle button. """
        self.button_toggle = ctk.CTkButton(self, text=text, command=self._toggle, border_spacing=1)
        self.button_toggle.pack(fill=tk.X, anchor='w')

    def _create_content_frame(self):
        """ Create the frame that holds the collapsible content. """
        self.frame_contents = ctk.CTkFrame(self)
        self.frame_contents.pack(fill=tk.X, anchor='w')

    def _toggle(self):
        """ Toggle the visibility of the content frame. """
        if self.frame_contents.winfo_viewable():
            self.frame_contents.pack_forget()
        else:
            self.frame_contents.pack(fill=tk.X, anchor='w')

    def collapse(self):
        """ Collapse the frame contents. """
        self.frame_contents.pack_forget()

    def add_widget(self, widget, **grid_kwargs):
        """ Add a widget to the content frame in a grid layout. """
        row, col = self._calculate_grid_position()
        widget.grid(row=row, column=col, **grid_kwargs)

    def _calculate_grid_position(self):
        """ Calculate the next grid position for a widget. """
        row = self._next_row // self.n_columns
        col = self._next_row % self.n_columns
        self._next_row += 1
        return row, col

# %% 
class GridFrame(ctk.CTkFrame):
    """
    A custom tkinter frame that automatically arranges added widgets in a grid layout.

    Widgets are placed in the grid based on the specified number of columns.
    """

    def __init__(self, parent=None, n_columns=1, **kwargs):
        """ Initialize the GridFrame with a specified number of columns. """
        super().__init__(parent, **kwargs)
        self._widget_count = 0
        self._n_columns = n_columns

    def add_widget(self, widget, **grid_kwargs):
        """ Add a widget to the frame in the next available grid position. """
        row, column = self._calculate_next_grid_position()
        widget.grid(row=row, column=column, **grid_kwargs)
        self._widget_count += 1

    def _calculate_next_grid_position(self):
        """ Calculate the grid position for the next widget. """
        row = self._widget_count // self._n_columns
        column = self._widget_count % self._n_columns
        return row, column




# %%
class AddTemplateForm(ctk.CTkToplevel):
    """
    Form for adding a new template. It allows users to input a category and name for the template.
    """

    def __init__(self, parent, context):
        super().__init__(parent)
        self.context = context
        self.app = context["app"]
        self._setup_ui()
        make_topmost(self)

    def _setup_ui(self):
        """ Set up the user interface for the form. """
        self._create_intro_label()
        self._create_form_fields()
        self._create_add_button()

    def _create_intro_label(self):
        """ Create the introductory label. """
        self.intro = ctk.CTkLabel(self, text="아래 항목들을 채우고 버튼을 눌러주세요.")
        self.intro.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

    def _create_form_fields(self):
        """ Create the input fields for category and name. """
        ctk.CTkLabel(self, text="구분").grid(row=1, column=0)
        ctk.CTkLabel(self, text="제목").grid(row=2, column=0)

        self.category = ctk.CTkEntry(self, placeholder_text="구분명을 입력하세요.")
        self.name = ctk.CTkEntry(self, placeholder_text="제목을 입력하세요.")
        self._prefill_category()

        self.category.grid(row=1, column=1, pady=5, padx=5)
        self.name.grid(row=2, column=1, pady=5, padx=5)

    def _prefill_category(self):
        """ Prefill the category field if a last category is available. """
        last_category = self.context["setting"].get("last_category")
        if last_category:
            self.category.insert(0, last_category)

    def _create_add_button(self):
        """ Create the 'add' button. """
        self.add_btn = ctk.CTkButton(self, text="반영하기", command=self.add_template)
        self.add_btn.grid(row=3, column=0, columnspan=2, pady=5)

    def add_template(self):
        """ Handle the addition of a new template. """
        if self._prepare_template():
            self._save_new_template()
            self._update_context_and_close()

    def _prepare_template(self):
        """ Prepare the template for saving. """
        self.temp = Path("temp")
        self.temp.mkdir(exist_ok=True)
        self.temp_path = Path("temp/temp.hwp")
        self.app.save_block(self.temp_path)

        category = self.category.get()
        name = self.name.get()
        self.destination = Path(f"templates/{prettify_filename(f'{category}_{name}')}.hwp")

        if self.destination.exists():
            self.intro.configure(text="같은 이름의 파일이 존재합니다. 다른 이름으로 수정해 주세요.")
            return False
        return True

    def _save_new_template(self):
        """ Save the new template. """
        Path(self.temp_path).rename(self.destination)

        self.intro.configure(text="작업중입니다. 이는 다소 시간이 소요 될 수 있습니다.")
        temp_app = App(is_visible=False, new_app=True)
        update_template(temp_app, self.destination)
        temp_app.quit()

    def _update_context_and_close(self):
        """ Update the context and close the form. """
        sh.rmtree("temp")
        self.destroy()
        self.context["parent"].refresh()


# %% 

class FontStyleBtns(ctk.CTkFrame):
    """
    A custom tkinter frame for managing font styles. 
    It includes buttons for saving current font styles and displaying saved styles.
    """

    def __init__(self, parent, context, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = context["app"]
        self.context = context
        self.font_styles = context["setting"].get("font_styles", {})

        self._setup_ui()

    def _setup_ui(self):
        """ Set up the user interface components. """
        self._create_collapsible_frame()
        self._create_save_button()
        self._populate_font_styles()

    def _create_collapsible_frame(self):
        """ Create a collapsible frame for font styles. """
        self.frame = CollapsibleFrame(self, text="글자서식")
        self.frame.pack(pady=5, fill="x")

    def _create_save_button(self):
        """ Create a button to save the current font style. """
        save_btn = ctk.CTkButton(
            self.frame.frame_contents, text="현재 서식 저장", 
            command=self.add_style, fg_color="green"
        )
        save_btn.pack(pady=5)
        ToolTip(save_btn, text="현재 커서가 위치의 글자 서식과 문단 서식을 저장합니다.")

    def _populate_font_styles(self):
        """ Populate the frame with buttons for each saved font style. """
        for idx, font_style in self.font_styles.items():
            charshape, parashape = self._create_shapes_from_dict(font_style)
            self._create_font_style_button(idx, charshape, parashape)

    def _create_shapes_from_dict(self, font_style):
        """ Create CharShape and ParaShape objects from saved font style. """
        charshape = CharShape().fromdict(font_style[0])
        parashape = ParaShape().fromdict(font_style[1])
        return charshape, parashape

    def _create_font_style_button(self, idx, charshape, parashape):
        """ Create a button for a specific font style. """
        FontStyleBtn(
            self.frame.frame_contents, self.context, idx, charshape, parashape
        ).pack(pady=5, anchor='w', fill=tk.X)

    def add_style(self):
        """ Save the current font style and add a button for it. """
        charshape, parashape = self.app.get_charshape(), self.app.get_parashape()
        idx = str(uuid1())
        self.font_styles[idx] = (charshape.todict(), parashape.todict())
        self.context["setting"]["font_styles"] = self.font_styles

        self._create_font_style_button(idx, charshape, parashape)


# %%

class FontStyleBtn(ctk.CTkFrame):
    """
    A custom tkinter frame for applying, deleting, and displaying font styles.

    This frame provides buttons to apply character and paragraph styles,
    as well as a button to delete a saved style.
    """

    def __init__(self, parent, context, idx, charshape, parashape, **kwargs):
        super().__init__(parent, **kwargs)
        self.context = context
        self.app = context["app"]
        self.idx = idx
        self.charshape = self._prepare_charshape(charshape)
        self.parashape = parashape

        self._setup_ui()

    def _prepare_charshape(self, charshape):
        """ Prepare the CharShape object by resetting certain attributes. """
        charshape.super_script = 0
        charshape.sub_script = 0
        return charshape

    def _setup_ui(self):
        """ Set up the user interface components of the frame. """
        self._create_apply_buttons()
        self._create_delete_button()
        self._create_font_display()

    def _create_apply_buttons(self):
        """ Create buttons for applying character and paragraph styles. """
        ctk.CTkButton(self, text="글자적용", command=self._apply_char, width=70).grid(row=0, column=1, pady=5)
        ctk.CTkButton(self, text="문단적용", command=self._apply_para, width=70).grid(row=1, column=1, pady=5)
        ctk.CTkButton(self, text="둘다적용", command=self._apply_both, width=70).grid(row=0, column=0, pady=5)

    def _create_delete_button(self):
        """ Create a button for deleting the font style. """
        ctk.CTkButton(
            self, text="삭제하기", command=self._delete_style, width=70, fg_color="red"
        ).grid(row=1, column=0, pady=5)

    def _create_font_display(self):
        """ Create a display area for the font style. """
        FontDisplay(self, self.charshape, self.parashape).grid(row=0, rowspan=2, column=2, padx=5, pady=5)

    def _apply_both(self):
        """ Apply both character and paragraph styles. """
        self.app.set_charshape(self.charshape)
        self.app.set_parashape(self.parashape)

    def _apply_char(self):
        """ Apply only the character style. """
        self.app.set_charshape(self.charshape)

    def _apply_para(self):
        """ Apply only the paragraph style. """
        self.app.set_parashape(self.parashape)

    def _delete_style(self):
        """ Delete the font style from settings and destroy the button frame. """
        del self.context["setting"]["font_styles"][self.idx]
        self.destroy()


# %%

class FontDisplay(ctk.CTkFrame):
    """
    A custom tkinter frame for displaying font and paragraph styles.
    """

    def __init__(self, parent, charshape, parashape, **kwargs):
        super().__init__(parent, **kwargs)
        self.charshape = charshape
        self.parashape = parashape

        self._create_font_display()

    def _create_font_display(self):
        """ Create and display the font and paragraph style information. """
        hangul_font = self._create_hangul_font(self.charshape)
        self._create_hangul_label(hangul_font)
        self._create_char_info_label(hangul_font)
        self._create_paragraph_label(hangul_font)

    def _create_hangul_font(self, charshape):
        """ Create a font object based on the character shape properties. """
        return CTkFont(
            family=charshape.hangul_font,
            size=max(int(charshape.fontsize), 10),
            weight="bold" if charshape.bold else "normal",
            slant="italic" if charshape.italic else "roman",
            underline=1 if charshape.underline_type else 0,
            overstrike=1 if charshape.strike_out_type else 0,
        )

    def _create_hangul_label(self, hangul_font):
        """ Create and display the label for Hangul font. """
        hangul = ctk.CTkLabel(self, text=self.charshape.hangul_font, font=hangul_font)
        hangul.grid(row=0, column=0, rowspan=2, padx=3)

    def _create_char_info_label(self, hangul_font):
        """ Create and display the label for character style information. """
        char_info_text = f"{self.charshape.fontsize:.01f}pt, 장평 {self.charshape.ratio}%, 자간 {self.charshape.spacing}%"
        char_info = ctk.CTkLabel(self, text=char_info_text, font=hangul_font)
        char_info.grid(row=0, column=1, padx=5, pady=3)

    def _create_paragraph_label(self, hangul_font):
        """ Create and display the label for paragraph style information. """
        paragraph_text = f"들여쓰기: {self.parashape.indentation}, 줄간격: {self.parashape.line_spacing}"
        paragraph = ctk.CTkLabel(self, text=paragraph_text, font=hangul_font)
        paragraph.grid(row=1, column=1, padx=5, pady=3)


# %%
class TemplateControl(ctk.CTkFrame):
    """
    A custom tkinter frame for controlling template actions such as delete and rename.
    """

    def __init__(self, parent, text, file_path, image_path, target_frame, **kwargs):
        super().__init__(parent, **kwargs)
        self.file_path = file_path
        self.image_path = image_path
        self.target_frame = target_frame

        self._create_delete_button()
        self._create_template_label(text, image_path)
        self._create_rename_button()

    def _create_delete_button(self):
        """ Create a button for deleting the template. """
        delete_button = ctk.CTkButton(self, text="삭제", command=self._confirm_delete)
        delete_button.grid(row=0, column=0, pady=2, padx=2)

    def _create_template_label(self, text, image_path):
        """ Create a label displaying the template's name and image. """
        template_label = ctk.CTkLabel(
            self, text=text, image=get_image(image_path), compound="bottom"
        )
        template_label.grid(row=0, column=1, rowspan=2, pady=2, padx=2)

    def _create_rename_button(self):
        """ Create a button for renaming the template. """
        rename_button = ctk.CTkButton(self, text="이름 바꾸기", command=self._open_rename_form)
        rename_button.grid(row=1, column=0, pady=2, padx=2)

    def _confirm_delete(self):
        """ Display a confirmation dialog before deleting the template. """
        ConfirmDialog(self, text="삭제하시겠습니까?", command=self._delete_template)

    def _open_rename_form(self):
        """ Open a form to rename the template. """
        RenameTemplateForm(self, file_path=self.file_path, image_path=self.image_path, target_frame=self.target_frame)

    def _delete_template(self):
        """ Delete the template files and refresh the target frame. """
        Path(self.file_path).unlink()
        Path(self.image_path).unlink()
        self.target_frame.refresh()


# %%

class ConfirmDialog(ctk.CTkToplevel):
    """
    A confirmation dialog window.
    """

    def __init__(self, parent, text, command, **kwargs):
        super().__init__(parent, **kwargs)
        self.title("확인")
        self._setup_ui(text, command)
        self.attributes('-topmost', 1)

    def _setup_ui(self, text, command):
        """ Set up the user interface components of the dialog. """
        self._create_label(text)
        self._create_confirm_button(command)
        self._create_cancel_button()

    def _create_label(self, text):
        """ Create a label displaying the confirmation text. """
        ctk.CTkLabel(self, text=text).grid(row=0, column=0, columnspan=2, pady=2, padx=2)

    def _create_confirm_button(self, command):
        """ Create a confirm button. """
        ctk.CTkButton(self, text="확인", command=command).grid(row=1, column=0, pady=2, padx=2)

    def _create_cancel_button(self):
        """ Create a cancel button. """
        ctk.CTkButton(self, text="취소", command=self.destroy).grid(row=1, column=1, pady=2, padx=2)

# %%
class RenameTemplateForm(ctk.CTkToplevel):
    """
    A form for renaming a template.
    """

    def __init__(self, parent, file_path, image_path, target_frame):
        super().__init__(parent)
        self.file_path = file_path
        self.image_path = image_path
        self.target_frame = target_frame

        self._setup_ui()
        self.attributes('-topmost', 1)

    def _setup_ui(self):
        """ Set up the user interface components of the form. """
        self.intro = ctk.CTkLabel(self, text="아래 항목들을 바꾸고 버튼을 눌러주세요.")
        self.intro.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self._create_labels_and_entries()
        self._create_rename_button()

    def _create_labels_and_entries(self):
        """ Create labels and entries for renaming the template. """
        ctk.CTkLabel(self, text="구분").grid(row=1, column=0)
        ctk.CTkLabel(self, text="제목").grid(row=2, column=0)

        self.category, self.name = self._get_current_names()
        self.category.grid(row=1, column=1, pady=5, padx=5)
        self.name.grid(row=2, column=1, pady=5, padx=5)

    def _get_current_names(self):
        """ Get the current names from the file path and populate the entries. """
        names = Path(self.file_path).stem.split("_")
        category, name = (names[0], names[1]) if len(names) == 2 else (names[0], names[0])
        category_entry = ctk.CTkEntry(self, placeholder_text="구분명을 입력하세요.")
        name_entry = ctk.CTkEntry(self, placeholder_text="제목을 입력하세요.")
        category_entry.insert(0, category)
        name_entry.insert(0, name)
        return category_entry, name_entry

    def _create_rename_button(self):
        """ Create a button for renaming the template. """
        ctk.CTkButton(self, text="반영하기", command=self.rename_template).grid(row=3, column=0, columnspan=2, pady=5)

    def rename_template(self):
        """ Rename the template based on user input. """
        new_fname = prettify_filename(f"{self.category.get()}_{self.name.get()}")
        n = Path(self.image_path).stem.split("_")[-1]
        self._rename_files(new_fname, n)
        self._refresh_and_close()

    def _rename_files(self, new_fname, n):
        """ Rename the template and image files. """
        destination = Path(f"templates/{new_fname}.hwp")
        if destination.exists():
            self.intro.configure(text="같은 이름의 파일이 존재합니다. 다른 이름으로 수정해 주세요.")
            return

        Path(self.file_path).rename(destination)
        image_destination = Path(f"images/{new_fname}_{n}.png")
        Path(self.image_path).rename(image_destination)

    def _refresh_and_close(self):
        """ Refresh the target frame and close the form. """
        self.target_frame.refresh()
        self.destroy()

# %%
if __name__ == "__main__":
    # demo :
    from hwpapi.core import App

    app = App()
    charshape = app.get_charshape()
    parashape = app.get_parashape()
    root = ctk.CTk()
    fonts = FontStyleBtns(root, {"app": app, "setting": {}})
    fonts.pack()
    root.mainloop()

# %%
