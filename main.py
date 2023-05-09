# -*- coding: utf-8 -*-
"""
Created on Tue May  9 09:31:12 2023

@author: 2015026
"""

import tkinter as tk
from tkinter import ttk, PhotoImage
import customtkinter as ctk
from classes import CollapsiblePane as cp


win = tk.Tk()

win.title("test")

ttk.Label(win, text="test label").grid(column=0, row=0)

cpane = cp(win, "테이블", "테이블")
cpane.grid(row=0, column=0)

def button_text():
    btn.configure(text="clicked")
btn = ctk.CTkButton(win, text="test botton", command=button_text)
btn.grid(column=0, row=1)

img = PhotoImage(file="images/grid01.png")
b1 = ttk.Button(cpane.frame, text="test", image=img).grid(row=1, column=2, pady=10)
cb1 = ttk.Checkbutton(cpane.frame, text="test cb").grid(row=2, column=2, pady=10)

win.attributes('-topmost', 1)
win.mainloop()
