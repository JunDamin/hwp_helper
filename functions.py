# -*- coding: utf-8 -*-
"""
Created on Tue May  9 09:31:12 2023

@author: 2015026
"""
# %% 
import customtkinter as ctk
from PIL import Image, ImageChops
from pathlib import Path
from hwpapi import App

def set_button(ctkframe, image_path, command=None):
    """set image button"""
    image_path = Path(image_path)
    img = Image.open(image_path)

    image = ctk.CTkImage(   
        light_image=img,
        dark_image=img,
        size=img.size
        )

    text = image_path.stem

    btn = ctk.CTkButton(ctkframe, text=text, image=image, fg_color="transparent", compound='bottom', command=command)
    btn.pack()
    return btn

def crop_background(image):
    """crop background of image"""
    img = Image.open(image)
    bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    return img.crop(bbox)

# %%
images = list(Path("images").glob("*"))
# %%
