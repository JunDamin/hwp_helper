import customtkinter as ctk
from functions import set_button, get_categories

class CollapsibleFrame(ctk.CTkFrame):
    
    def __init__(self, master=None, text="toggle", **kwargs):
        ctk.CTkFrame.__init__(self, master, **kwargs)

        self.button_toggle = ctk.CTkButton(self, text=text, command=self.toggle, border_spacing=5)
        self.button_toggle.pack(fill='x')

        self.frame_contents = ctk.CTkFrame(self, )
        self.frame_contents.pack()

    def toggle(self):
        if self.frame_contents.winfo_viewable():
            self.frame_contents.pack_forget()
        else:
            self.frame_contents.pack()

    def collapse(self):
        self.frame_contents.pack_forget()


class CategoryFrame(ctk.CTkFrame):
    """
    from categories from images file
    """
    def __init__(self, parent):
        super().__init__(parent)
        categories = get_categories()
        for key, value in categories.items():
            cframe = CollapsibleFrame(self, key)
            cframe.pack(fill='x', pady=5, padx=5)
            for text, image_path in value:
                btn = set_button(cframe.frame_contents, text=text, image_path=image_path)
            cframe.collapse()


class Helper(ctk.CTk):

    def __init__(self):

        super().__init__()
        category_frame = CategoryFrame(self)
        category_frame.pack(fill='x')

        self.geometry("850x800")
        self.title("test")
        self.attributes('-topmost', 1)
