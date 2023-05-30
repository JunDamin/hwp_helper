# %%

import customtkinter as ctk
from customtkinter import CTkFont
import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle


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

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 50

        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Remove window decorations
        tw.wm_geometry(f"+{x}+{y}")  # Position tooltip

        label = tk.Label(
            tw, text=self.text, background="#dddddd", wraplength=350, font=15, ipady=15
        )
        label.pack()
        if self.gif:
            imagelabel = ImageLabel(tw)
            imagelabel.pack()
            imagelabel.load(self.gif)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


# %%
class CollapsibleFrame(ctk.CTkFrame):
    """This Frame is for create collapsible frame for sub components"""

    def __init__(self, master=None, text="toggle", **kwargs):
        ctk.CTkFrame.__init__(self, master, **kwargs)

        self.button_toggle = ctk.CTkButton(
            self, text=text, command=self.toggle, border_spacing=10
        )
        self.button_toggle.pack(fill="x")

        self.frame_contents = ctk.CTkFrame(
            self,
        )
        self.frame_contents.pack()

    def toggle(self):
        if self.frame_contents.winfo_viewable():
            self.frame_contents.pack_forget()
        else:
            self.frame_contents.pack()

    def collapse(self):
        self.frame_contents.pack_forget()


# %%
class FontDisplay(ctk.CTkFrame):
    def __init__(self, master, charshape, parashape, **kwargs):
        ctk.CTkFrame.__init__(self, master, **kwargs)
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

        hangul = ctk.CTkLabel(
            self, text=f"폰트 {charshape.hangul_font}", font=hangul_font
        )
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


# %%
if __name__ == "__main__":
    # demo :
    from hwpapi.core import App

    app = App()
    charshape = app.get_charshape()
    parashape= app.get_parashape()
    root = ctk.CTk()
    fonts = FontDisplay(root, charshape, parashape)
    fonts.pack()
    root.mainloop()

# %%
