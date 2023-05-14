import customtkinter as ctk
from functions import set_button, get_categories, update_templates, set_forewindows, set_hwp_size, get_screen_size, check_app
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
        self.set_frames()

    def refresh(self):

        for child in self.winfo_children():
            child.destroy()
        
        self.set_frames()


    def set_frames(self):
        # make command
        def make_func(path, n):
            def func():
                check_app(self.app)
                set_forewindows(self.app)
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



class UpdateTemplateForm(ctk.CTkToplevel):

    def __init__(self, parent, template_form):

        super().__init__(parent)
        self.title = ctk.CTkLabel(self, text="update template")
        self.title.pack()
        self.template_form = template_form
        
        self.update_btn = ctk.CTkButton(self, text="update", command=self.update_templates)
        self.update_btn.pack()
        

    def update_templates(self):
        
        self.update_btn.destroy()

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

        self.template_form.refresh()

        self.destroy()

class NaviBar(ctk.CTkFrame):

    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app

        update_btn = ctk.CTkButton(self, text="update template", command=self.update_templates)
        update_btn.pack(side="left", padx=10, pady=10)

        fullscreen_btn = ctk.CTkButton(self, text="full screen", command=self.set_fullscreen)
        fullscreen_btn.pack(side="left", padx=10, pady=10)

    def update_templates(self):
        
        toplevel = UpdateTemplateForm(self, self.parent.category_frame)  # master argument is optional  
        toplevel.focus()

    def set_fullscreen(self):
        x1, y1, x2, y2 = get_screen_size()
        width = x2-x1
        height = y2-y1
        hwp_width = int(width/2)
        set_hwp_size(self.parent.app, x1, y1, hwp_width, height)
        self.parent.set_windows(x1+hwp_width, y1, 0.5)

class Helper(ctk.CTk):

    def __init__(self):

        super().__init__()
        
        x1, y1, x2, y2 = get_screen_size()
        width = x2-x1
        height = y2-y1
        hwp_width = int(width/2)
        
        self.title("test")
        self.set_windows(x1+hwp_width, y1, 0.5)

        # set app
        self.app = App()
        set_hwp_size(self.app, x1, y1, hwp_width, height)


        # set navi bar
        self.navi_bar = NaviBar(self, self.app)
        self.navi_bar.pack()

        # set category frame
        self.category_frame = CategoryFrame(self, self.app)
        self.category_frame.pack(fill='both', expand=True)

    def set_windows(self, left, top, width_ratio=0.5, height_ratio=1):
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry(f'{int(width*width_ratio)}x{int(height*height_ratio)}+{int(left)}+{int(top)}')