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
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """

    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info["duration"]
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)


# %%
class ToolTip:
    def __init__(self, widget, text, gif=None):
        self.widget = widget
        self.text = text
        self.gif = gif
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

        _, _, width, height = get_screen_size()
        self.screen_width = width
        self.screen_height = height

    def show_tooltip(self, event=None):
        self.widget.update_idletasks()

        x, y, width, height = self.widget.bbox("insert")
        x += self.widget.winfo_rootx()
        y += self.widget.winfo_rooty() + height

        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Remove window decorations
        # tw.wm_geometry(f"+{x}+{y}")  # Position tooltip

        label = tk.Label(
            tw, text=self.text, background="#dddddd", wraplength=350, font=15, pady=5
        )
        label.pack(pady=10)
        if self.gif:
            imagelabel = ImageLabel(tw)
            imagelabel.pack()
            imagelabel.load(self.gif)

        tw.update_idletasks()

        tw_width, tw_height = tw.winfo_width(), tw.winfo_height()
        
        if x + tw_width > self.screen_width:
            x -= (tw_width - width) 
        if y + tw_height > self.screen_height:
            y -= (tw_height + height)

        tw.wm_geometry(f"+{x}+{y}")  # Position tooltip

        
    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


# %%
class CollapsibleFrame(ctk.CTkFrame):
    """This Frame is for create collapsible frame for sub components"""

    def __init__(self, parent=None, text="toggle", n_columns=1, **kwargs):
        ctk.CTkFrame.__init__(self, parent, **kwargs)

        self._next_row = 0 
        self.n_columns=n_columns

        self.button_toggle = ctk.CTkButton(
            self, text=text, command=self.toggle, border_spacing=1
        )
        self.button_toggle.pack(fill=tk.X, anchor='w')

        self.frame_contents = ctk.CTkFrame(
            self, 
        )
        self.frame_contents.pack(fill=tk.X, anchor='w')

    def toggle(self):
        if self.frame_contents.winfo_viewable():
            self.frame_contents.pack_forget()
        else:
            self.frame_contents.pack(fill=tk.X, anchor='w')

    def collapse(self):
        self.frame_contents.pack_forget()

    def add_widget(self, widget, **grid_kwargs):
        i = self._next_row // self.n_columns
        j = self._next_row % self.n_columns

        widget.grid(row=i, column=j,  **grid_kwargs)
        self._next_row += 1


class GridFrame(ctk.CTkFrame):
    """This Frame is for auto grid frame"""

    def __init__(self, parent=None, n_columns=1, **kwargs):
        ctk.CTkFrame.__init__(self, parent, **kwargs)

        self.count = 0 
        self.n_columns=n_columns

    def add_widget(self, widget, **grid_kwargs):
        i = self.count // self.n_columns
        j = self.count % self.n_columns

        widget.grid(row=i, column=j, **grid_kwargs)
        self.count += 1




# %%

class AddTemplateForm(ctk.CTkToplevel):

    def __init__(self, parent, context):
        super().__init__(parent)
        self.context = context
        self.app = context["app"]


        self.intro = ctk.CTkLabel(self, text="아래 항목들을 채우고 버튼을 눌러주세요.")
        self.intro.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        ctk.CTkLabel(self, text="구분").grid(row=1, column=0)
        ctk.CTkLabel(self, text="제목").grid(row=2, column=0)
        self.category = category = ctk.CTkEntry(self, placeholder_text="구분명을 입력하세요.")
        self.name = name = ctk.CTkEntry(self, placeholder_text="제목을 입력하세요.")
        
        formal_category = context["setting"].get("last_category", None)
        if formal_category:
            category.insert(0, formal_category)
        
        category.grid(row=1, column=1, pady=5, padx=5)
        name.grid(row=2, column=1, pady=5, padx=5)
        
        self.add_btn = ctk.CTkButton(self, text="반영하기", command=self.add_template)
        self.add_btn.grid(row=3, column=0, columnspan=2, pady=5)

        make_topmost(self)

    def add_template(self):
        
        self.temp = Path("temp")
        self.temp.mkdir(exist_ok=True)
        self.temp_path = temp_path = Path("temp/temp.hwp")
        self.app.save_block(temp_path)

        category = self.category.get()
        name = self.name.get()
        fname = prettify_filename(f"{category}_{name}")
        
        destination = Path(f"templates/{fname}.hwp")
        if destination.exists():
            return self.intro.configure(text="같은 이름의 파일이 존재합니다. 다른 이름으로 수정해 주세요.")  # deletes the file
        Path(self.temp_path).rename(destination)

        
        self.add_btn.destroy()
        self.intro.configure(text="작업중입니다. 이는 다소 시간이 소요 될 수 있습니다.")
        
        temp_app = App(is_visible=False)
        update_template(temp_app, destination)
        temp_app.quit()

        self.context["template_frame"].refresh()
        sh.rmtree("temp")
        self.destroy()
        self.context["setting"]["last_category"] = category
        self.context["tabview"].set("templates")

# %% 

class FontStyleBtns(ctk.CTkFrame):
    def __init__(self, parent, context, **kwargs):
        self.app = context["app"]
        self.parent = parent
        self.context=context
        self.font_styles = context["setting"].get("font_styles", {})

        ctk.CTkFrame.__init__(self, parent, **kwargs)
        self.frame = CollapsibleFrame(self, text="글자서식")
        self.frame.pack(pady=5, fill="x")

        save_btn = ctk.CTkButton(self.frame.frame_contents, text="현재 서식 저장", command=self.add_style, fg_color="green")
        save_btn.pack(pady=5)
        ToolTip(save_btn, text="현재 커서가 위치의 글자 서식과 문단 서식을 저장합니다.")


        for idx, font_style in self.font_styles.items():
            charshape = CharShape()
            charshape.fromdict(font_style[0])
            parashape = ParaShape()
            parashape.fromdict(font_style[1])

            FontStyleBtn(self.frame.frame_contents, context, idx, charshape, parashape).pack(pady=5, anchor='w', fill=tk.X)

        
    def add_style(self):
        app = self.app
        charshape = app.get_charshape()
        parashape = app.get_parashape()
        idx = str(uuid1())
        self.font_styles[idx] = (charshape.todict(), parashape.todict())
        self.context["setting"]["font_styles"] = self.font_styles
        
        FontStyleBtn(self.frame.frame_contents, self.context, idx=idx, charshape=charshape, parashape=parashape).pack(pady=5, anchor='w', fill=tk.X)


# %%


class FontStyleBtn(ctk.CTkFrame):
    def __init__(self, parent, context, idx, charshape, parashape, **kwargs):
        self.context = context
        self.app = context["app"]
        self.idx = idx
        self.charshape = charshape
        self.parashape = parashape 

        charshape.super_script = 0
        charshape.sub_script = 0


        
        ctk.CTkFrame.__init__(self, parent, **kwargs)
        ctk.CTkButton(self, text="글자적용", command=self.apply_char, width=70).grid(
            row=0, column=1, pady=5
        )
        ctk.CTkButton(self, text="문단적용", command=self.apply_para, width=70).grid(
            row=1, column=1, pady=5
        )
        ctk.CTkButton(self, text="둘다적용", command=self.apply, width=70).grid(
            row=0, column=0, pady=5
        )
        ctk.CTkButton(
            self, text="삭제하기", command=self.delete, width=70, fg_color="red"
        ).grid(row=1, column=0, pady=5)
        FontDisplay(self, charshape, parashape).grid(
            row=0, rowspan=2, column=2, padx=5, pady=5
        )

    def apply(self):
        self.app.set_charshape(self.charshape)
        self.app.set_parashape(self.parashape)

    def apply_char(self):
        self.app.set_charshape(self.charshape)

    def apply_para(self):
        self.app.set_parashape(self.parashape)

    def delete(self):
        del self.context["setting"]["font_styles"][self.idx]
        self.destroy()




# %%
class FontDisplay(ctk.CTkFrame):
    def __init__(self, parent, charshape, parashape, **kwargs):
        ctk.CTkFrame.__init__(self, parent, **kwargs)
        self.charshape = charshape
        self.parashape = parashape

        hangul_font = CTkFont(
            family=charshape.hangul_font,
            size=int(charshape.fontsize) if charshape.fontsize > 10 else 10,
            weight="bold" if charshape.bold else "normal",
            slant="italic" if charshape.italic else "roman",
            underline=1 if charshape.underline_type else 0,
            overstrike=1 if charshape.strike_out_type else 0,
        )

        hangul = ctk.CTkLabel(self, text=f"{charshape.hangul_font}", font=hangul_font)
        hangul.grid(row=0, column=0, rowspan=2, padx=3)
        char_info = ctk.CTkLabel(
            self,
            text=f"{charshape.fontsize:.01f}pt, 장평 {charshape.ratio}%, 자간 {charshape.spacing}%",
            font=hangul_font,
        )
        char_info.grid(row=0, column=1, padx=5, pady=3)
        paragraph = ctk.CTkLabel(
            self,
            text=f"들여쓰기: {parashape.indentation}, 줄간격: {parashape.line_spacing}",
            font=hangul_font,
        )
        paragraph.grid(row=1, column=1, padx=5, pady=3)


class TemplateControl(ctk.CTkFrame):
    def __init__(self, parent, text, file_path, image_path, target_frame, **kwargs):
        super().__init__(parent, **kwargs)
        self.file_path = file_path
        self.image_path = image_path
        self.parent = parent
        self.target_frame = target_frame

        ctk.CTkButton(self, text="삭제", command=self.check).grid(row=0, column=0, pady=2, padx=2)
        ctk.CTkLabel(
            self,
            text=text,
            image=get_image(image_path),
            compound="bottom",
        ).grid(row=0, column=1, rowspan=2, pady=2, padx=2)
        ctk.CTkButton(self, text="이름 바꾸기", command=self.rename).grid(row=1, column=0, pady=2, padx=2)
        


    def check(self):
        ConfirmDialog(self, text="삭제하시겠습니까?", command=self.delete_template)

    def rename(self):
        RenameTemplateForm(self, file_path=self.file_path, image_path=self.image_path, target_frame=self.target_frame)

    def delete_template(self):
        Path(self.file_path).unlink()
        Path(self.image_path).unlink()
        self.target_frame.refresh()


class ConfirmDialog(ctk.CTkToplevel):
    def __init__(self, parent, text, command, **kwargs):
        super().__init__(parent, **kwargs)
        self.title("확인")
        ctk.CTkLabel(self, text=text).grid(row=0, column=0, columnspan=2, pady=2, padx=2)
        ctk.CTkButton(self, text="확인", command=command).grid(row=1, column=0, pady=2, padx=2)
        ctk.CTkButton(self, text="취소", command=self.destroy).grid(row=1, column=1, pady=2, padx=2)
        
        self.attributes('-topmost', 1)


class RenameTemplateForm(ctk.CTkToplevel):

    def __init__(self, parent, file_path, image_path, target_frame):
        super().__init__(parent)
        self.file_path = file_path
        self.image_path = image_path
        self.target_frame = target_frame

        names = Path(file_path).stem.split("_")
        current_category, current_name = (names[0], names[1]) if len(names) == 2 else (names[0], names[0]) 

        self.intro = ctk.CTkLabel(self, text="아래 항목들을 바꾸고 버튼을 눌러주세요.")
        self.intro.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        ctk.CTkLabel(self, text="구분").grid(row=1, column=0)
        ctk.CTkLabel(self, text="제목").grid(row=2, column=0)
        self.category = category = ctk.CTkEntry(self, placeholder_text="구분명을 입력하세요.")
        self.name = name = ctk.CTkEntry(self, placeholder_text="제목을 입력하세요.")
        category.insert(0, current_category)
        name.insert(0, current_name)
        category.grid(row=1, column=1, pady=5, padx=5)
        name.grid(row=2, column=1, pady=5, padx=5)
        ctk.CTkButton(self, text="반영하기", command=self.rename_template).grid(row=3, column=0, columnspan=2, pady=5)

        self.attributes('-topmost', 1)
        
    def rename_template(self):

        fname = prettify_filename(f"{self.category.get()}_{self.name.get()}")
        n = Path(self.image_path).stem.split("_")[-1]

        destination = Path(f"templates/{fname}.hwp")
        if destination.exists():
            return self.intro.configure(text="같은 이름의 파일이 존재합니다. 다른 이름으로 수정해 주세요.")  # deletes the file
        Path(self.file_path).rename(destination)
        image_destination = Path(f"images/{fname}_{n}.png")
        Path(self.image_path).rename(image_destination)
        
        self.destroy()
        self.target_frame.refresh()

# %%
if __name__ == "__main__":
    # demo :
    from hwpapi.core import App

    app = App()
    charshape = app.get_charshape()
    parashape = app.get_parashape()
    root = ctk.CTk()
    fonts = FontDisplay(root, charshape, parashape)
    fonts.pack()
    root.mainloop()

# %%
