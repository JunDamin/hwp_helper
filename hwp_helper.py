# -*- coding: utf-8 -*-
"""
Created on Tue May  9 09:31:12 2023

@author: 2015026
"""
import customtkinter as ctk
from classes import Helper
from hwpapi.core import App
import yaml



ctk.set_appearance_mode("dark")

context = {}
with open("setting.yaml", encoding='utf-8') as f:
    context["setting"] = yaml.safe_load(f)

context["app"] = App()
helper = Helper(context)
helper.set_fullscreen()
helper.mainloop()