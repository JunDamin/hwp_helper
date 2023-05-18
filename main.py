# -*- coding: utf-8 -*-
"""
Created on Tue May  9 09:31:12 2023

@author: 2015026
"""
import customtkinter as ctk
from classes import Helper
from hwpapi.core import App

ctk.set_appearance_mode("dark")
context = {}
context["app"] = App()
helper = Helper(context)
helper.mainloop()
