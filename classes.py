import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class CollapsiblePane(ttk.Frame):
    """
    ---USAGE---
    collapsible_pane = CollapsiblePane(parent, expanded_text=[string], collapsed_text=[string])
    collapsible_pane.pack()
    button = Button(collapsible_pane.frame).pack()
    """

    def __init__(self, parent, expanded_text="Collapse <<", collapsed_text="Expand >>"):

        ttk.Frame.__init__(self, parent)

        # These a re the class variable
        # see a underscore in expanded_text and _collapsed_text
        # this means there are private to class
        self.parent = parent
        self._expanded_text = expanded_text
        self._collapsed_text = collapsed_text

        # Here weight implies that it can grow it's
        # size if extra space is available
        # default weight is 0
        self.columnconfigure(1, weight=1)

        # TK inter variable storing integer value
        self._variable = tk.IntVar()

        # CheckButton is created but will behave as Button
        # cause in style, Button is passed
        # main reason to do this is button do not support
        # variable piton but checkbutton do
        self._button = ttk.Checkbutton(self, variable=self._variable,
                                        command=self._activate, style="TButton")
        self._button.grid(row=0, column=0)

        # This will create a separator 
        # A separator is a line, we can also set thickness
        self._separator = ttk.Separator(self, orient="horizontal")
        self._separator.grid(row=0, column=1, sticky="we")

        self.frame = ttk.Frame(self)

        # This will call activate function of class
        self._activate()
    
    def _activate(self):
        if not self._variable.get():

            # As soon as button is pressed it remove this widget
            # but is not destroyed means can be displayed again

            self.frame.grid_forget()

            # This will change the text of the checkbutton
            self._button.configure(text=self._collapsed_text)

        elif self._variable.get():
            # increasing the frame area so new widgets 
            # could reside in this container
            self.frame.grid(row=1, column=0, columnspan=2)
            self._button.configure(text=self._expanded_text)
        
    def toggle(self):
        """switches the label frame to the opposite state."""
        self._variable.set(not self._variable.get())
        self._activate()