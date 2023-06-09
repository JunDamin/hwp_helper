import customtkinter as ctk
import tkinter as tk
from components import CollapsibleFrame
from functions import (
    set_button,
    get_categories,
    set_forewindow,
    check_app,
    get_image
)


class CategoryFrame(ctk.CTkScrollableFrame):
    """
    from categories from images file
    """

    def __init__(self, parent, context):
        super().__init__(parent)
        self.parent = parent
        self.app = context["app"]
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
                set_forewindow(self.app)
                self.app.insert_file(path)
                for _ in range(n):
                    self.app.move("NextPara")
                return None

            return func

        # get categrory data from packages
        categories = get_categories()
        for key, value in categories.items():
            cframe = CollapsibleFrame(self, key)
            cframe.pack(fill=tk.X, padx=2, pady=2, anchor='nw')

            for text, image_path, filename, n in value:
                path = f"templates/{filename}.hwp"
                
                image = get_image(image_path)
                btn = ctk.CTkButton(cframe.frame_contents,
                    text=text,
                    command=make_func(path, n),
                    fg_color="transparent",
                    image=image,
                    compound="bottom",
                )
                cframe.add_widget(btn, sticky='w')
            cframe.collapse()


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x800")
    context = {"app": None}
    app = CategoryFrame(root, context)
    app.pack(fill="both", expand=True)
    root.mainloop()