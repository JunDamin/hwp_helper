import customtkinter as ctk
from functions import set_button, get_categories, update_templates
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
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app
 
        # make command
        def make_func(path, n):
            def func():
                self.app.insert_file(path)
                for _ in range(n):
                    self.app.move("NextPara")
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


class NaviBar(ctk.CTkFrame):

    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app
 
        update_btn = ctk.CTkButton(self, text="update template", command=self.update_templates)
        update_btn.pack()

    def update_templates(self):
 
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(padx=10, pady=10)
        self.progress_bar.set(0)
        self.update() 

        # new window and progress bar
        for i, n in update_templates():
            progress = i/(n-1)
            self.progress_bar.set(progress)
            self.update()

        self.progress_bar.pack_forget()
        self.parent.refresh()

class Helper(ctk.CTk):

    def __init__(self):

        super().__init__()
        self.geometry("850x800")
        self.title("test")
        # self.attributes('-topmost', 1)

        # set app
        self.app = App()

        # set navi bar
        self.navi_bar = NaviBar(self, self.app)
        self.navi_bar.pack()

        # set category frame
        self.category_frame = CategoryFrame(self, self.app)
        self.category_frame.pack(fill='both', expand=True)

    def refresh(self):

        self.category_frame.pack_forget()
        self.category_frame.destroy()
        self.category_frame = CategoryFrame(self, self.app)
        self.category_frame.pack(fill="both", expand=True)
