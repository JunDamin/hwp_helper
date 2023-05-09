import customtkinter as ctk
from functions import set_button, get_categories
from hwpapi.core import App

class CollapsibleFrame(ctk.CTkFrame):
    """This Frame is for create collapsible frame for sub components"""

    def __init__(self, master=None, text="toggle", **kwargs):
        ctk.CTkFrame.__init__(self, master, **kwargs)

        self.button_toggle = ctk.CTkButton(self, text=text, command=self.toggle, border_spacing=10)
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


class CategoryFrame(ctk.CTkScrollableFrame):
    """
    from categories from images file
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
 
        # make command
        def make_func(path, n):
            def func():
                self.parent.app.insert_file(path)
                for _ in range(n):
                    self.parent.app.move("NextPara")
                return None
            return func
        
        # get categrory data from packages
        categories = get_categories()
        for key, value in categories.items():
            cframe = CollapsibleFrame(self, key)
            cframe.pack(fill='x', pady=5, padx=5)

            for text, image_path, filename, n in value:
                
                path = f"templates/{filename}.hwp"

                
                # create button
                btn = set_button(
                    cframe.frame_contents, 
                    text=text, 
                    image_path=image_path, 
                    command=make_func(path, n)
                    )
            cframe.collapse()


class Helper(ctk.CTk):

    def __init__(self):

        super().__init__()
        self.geometry("850x800")
        self.title("test")
        self.attributes('-topmost', 1)

        # set app
        self.app = App()

        # set category frame
        category_frame = CategoryFrame(self)
        category_frame.pack(fill='both', expand=True)
