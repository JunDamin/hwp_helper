# -*- coding: utf-8 -*-
"""
Created on Tue May  9 09:31:12 2023

@author: 2015026
"""

import tkinter as tk
from tkinter import ttk, PhotoImage
import customtkinter as ctk
from classes import CollapsiblePane, CollapsibleFrame
from PIL import Image

win = ctk.CTk()

win.title("test")

ctk.CTkLabel(win, text="test label").grid(column=0, row=0)

cpane = CollapsiblePane(win, "테이블", "테이블")
cpane.grid(row=0, column=0)

img = PhotoImage(file="images/grid01.png")
b1 = ctk.CTkButton(cpane.frame, text="test", image=img).grid(row=1, column=2, pady=10)
cb1 = ctk.CTkCheckBox(cpane.frame, text="test cb").grid(row=2, column=2, pady=10)

dimg = ctk.CTkImage(dark_image=Image.open("images/grid01.png"))
cframe = CollapsibleFrame(win)
cframe.grid(row=1, column=0)
b2 = ctk.CTkButton(cframe.frame_contents, text="test", image=dimg).pack()
l2 = ctk.CTkLabel(cframe.frame_contents, text="test label").pack()

def button_text():
    btn.configure(text="clicked")
btn = ctk.CTkButton(win, text="test botton", command=button_text)
btn.grid(column=0, row=2)

win.attributes('-topmost', 1)
win.mainloop()
