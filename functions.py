# -*- coding: utf-8 -*-
"""
Created on Tue May  9 09:31:12 2023

@author: 2015026
"""
# %% 
import customtkinter as ctk
from PIL import Image, ImageChops
from pathlib import Path
import re
import shutil as sh
from hwpapi.core import App
from time import sleep

def set_button(ctkframe, text, image_path, command=None):
    """set image button"""
    image_path = Path(image_path)
    img = Image.open(image_path)

    image = ctk.CTkImage(   
        light_image=img,
        dark_image=img,
        size=img.size
        )

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
    if bbox[2] - bbox[0] < 300:
        bbox = (bbox[0], bbox[1], bbox[0]+300, bbox[3])
    return img.crop(bbox)


# %%

def update_template(app, hwp):
    hwp = Path(hwp)
    app.open(hwp)
    app.actions.MoveDocEnd().run()
    # if it is not end with blank line
    if app.get_text() != "\r\n":
        app.actions.BreakPara().run()
        app.save()    

    _, n, _ = app.api.GetPos()
    temp = Path(f"temp/{hwp.stem}_{n}.png")
    app.save(temp)
    cropped = crop_background("temp/" + temp.stem + "001.png")
    cropped.save(f"images/{re.sub('001$', '', temp.stem)}.png")
    return hwp

def update_templates():
    
    #clear old image and create temp folder for images
    if Path("images").is_dir(): sh.rmtree("images")
    if Path("temp").is_dir(): sh.rmtree("temp")
    Path("temp").mkdir()
    Path("images").mkdir()
    # convert hwp into png
    hwps = list(Path("templates").glob("*"))
    n = len(hwps)

    app = App(is_visible=False)
    for i, hwp in enumerate(hwps):
        update_template(app, hwp)
        yield i, n
    app.quit()
    sh.rmtree("temp")
# %%

def get_categories():
    """get iamges names"""
    images = list(Path("images").glob("*"))
    categories = {}
    for image in images:
        splited = image.stem.split("_")
        if len(splited) == 1:
            splited = [splited[0], "None", "0"]
        key, value, n = splited[0], splited[1], splited[2]
        filename = f"{key}_{value}" if value != "None" else key
        components = categories.get(key, [])
        components.append((value, image, filename, int(n)))
        categories[key] = components
    return categories

# %%
if __name__ == "__main__":
    update_templates()