# -*- coding: utf-8 -*-
"""
Created on Tue May  9 09:31:12 2023

@author: 2015026
"""
from tkinter import Menubutton, Menu
import customtkinter as ctk
from classes import CollapsibleFrame
from functions import set_button, get_categories

win = ctk.CTk()
win.geometry("850x800")
win.title("test")

category_frame = ctk.CTkFrame(win)
category_frame.pack()

categories = get_categories()

for key, value in categories.items():
    cframe = CollapsibleFrame(category_frame, key)
    cframe.pack()
    for text, image_path in value:
        btn = set_button(cframe.frame_contents, text=text, image_path=image_path)
    cframe.collapse()

def button_text():
    btn.configure(text="clicked")
btn = ctk.CTkButton(win, text="test botton", command=button_text)
btn.pack()

win.attributes('-topmost', 1)
win.mainloop()
