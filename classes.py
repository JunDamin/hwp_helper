import customtkinter as ctk
from functions import set_button, get_categories, update_templates, set_forewindows, set_hwp_size, get_screen_size, check_app, get_ratio, back_to_app
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

class HwpFeatureFrame(ctk.CTkScrollableFrame):
    """"""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        cell_border_btn = ctk.CTkButton(self, text="표 테두리", command=self.set_cell_border)
        cell_border_btn.grid(row=0, column=0, pady=3, padx=3)

        cell_color_btn = ctk.CTkButton(self, text="셀 색", command=self.set_cell_color)
        cell_color_btn.grid(row=0, column=1, pady=3, padx=3)       

    @back_to_app
    def set_cell_border(self):
        return self.app.set_cell_border(right=0, left=0, top_width=0.4, bottom_width=0.4)
        
    @back_to_app
    def set_cell_color(self):
        return self.app.set_cell_color(bg_color=(250, 243, 219))


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

        fullscreen_btn = ctk.CTkButton(self, text="full screen", command=self.parent.set_fullscreen)
        fullscreen_btn.pack(side="left", padx=10, pady=10)

    def update_templates(self):
        
        toplevel = UpdateTemplateForm(self, self.parent.category_frame)  # master argument is optional  
        toplevel.focus()

class Helper(ctk.CTk):

    def __init__(self):

        super().__init__()
        
        x1, y1, x2, y2 = get_screen_size()
        width = x2-x1
        height = y2-y1
        hwp_width = int(width/2)
        
        self.title("test")

        # set app
        self.app = App()
        self.set_fullscreen()

        # set navi bar
        self.navi_bar = NaviBar(self, self.app)
        self.navi_bar.pack()


        tabview = ctk.CTkTabview(master=self)
        tabview.pack(padx=20, pady=20, fill="both", expand=True)

        tabview.add("template")  # add tab at the end
        tabview.add("features")  # add tab at the end
        tabview.set("features")  # set currently visible tab

        # set category frame
        self.category_frame = CategoryFrame(tabview.tab("template"), self.app)
        self.category_frame.pack(fill='both', expand=True)

        # set feature frame
        self.feature_frame = HwpFeatureFrame(tabview.tab("features"), self.app)
        self.feature_frame.pack(fill='both', expand=True)

    def set_windows(self, left, top, width, height):
        ratio = get_ratio(self)
        self.geometry(f'{int(width*ratio)}x{int(height*ratio)}+{int(left)}+{int(top)}')

    def set_fullscreen(self, hwp_ratio=0.5, side='left'):
        x1, y1, x2, y2 = get_screen_size()
        width = x2-x1
        height = y2-y1
        hwp_width = int(width*hwp_ratio)

        hwp_x, hwp_y = x1+int(width * (1-hwp_ratio)), y1
        app_x, app_y = x1, y1

        if side == "left":
            hwp_x, hwp_y = x1, y1
            app_x, app_y = x1+hwp_width, y1
    

        set_hwp_size(self.app, hwp_x, hwp_y, hwp_width, height)
        self.set_windows(app_x, app_y, width= width - hwp_width, height=height)

