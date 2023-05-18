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
import win32gui as wg
from win32api import GetMonitorInfo, MonitorFromPoint
import pywintypes
import sys
import os



def set_button(ctkframe, text, image_path, command=None):
    """set image button"""
    image_path = Path(image_path)
    img = Image.open(image_path)

    image = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)

    btn = ctk.CTkButton(
        ctkframe,
        text=text,
        image=image,
        fg_color="transparent",
        compound="bottom",
        command=command,
    )
    btn.pack()
    return btn


def crop_background(image):
    """crop background of image"""
    img = Image.open(image)
    bg = Image.new(img.mode, img.size, img.getpixel((0, 0)))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if not bbox:
        return None
    if bbox[2] - bbox[0] < 300:
        bbox = (bbox[0], bbox[1], bbox[0] + 300, bbox[3])
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
    
    if not cropped:
        return None
    cropped.save(f"images/{re.sub('001$', '', temp.stem)}.png")
    return hwp


def update_templates():
    # clear old image and create temp folder for images
    if Path("images").is_dir():
        sh.rmtree("images")
    if Path("temp").is_dir():
        sh.rmtree("temp")
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


def set_forewindows(app):
    hwnd = app.api.XHwpWindows.Active_XHwpWindow.WindowHandle
    return wg.SetForegroundWindow(hwnd)


def get_screen_size():
    x1, y1, x2, y2 = GetMonitorInfo(MonitorFromPoint((0, 0))).get("Work")
    return x1, y1, x2 - x1, y2 - y1


def set_hwp_size(app, left, top, width, height):
    app.api.XHwpWindows.Active_XHwpWindow.Left = left
    app.api.XHwpWindows.Active_XHwpWindow.Top = top
    app.api.XHwpWindows.Active_XHwpWindow.Width = width
    app.api.XHwpWindows.Active_XHwpWindow.Height = height


def check_app(app):
    try:
        return app.api.PageCount
    except pywintypes.com_error as e:
        return app.reload()


def get_ratio(ctk_app):
    app_width = ctk_app.winfo_screenwidth()
    app_height = ctk_app.winfo_screenheight()
    _, _, screen_width, screen_height = get_screen_size()
    return min(app_width / screen_width, app_height / screen_height)


def back_to_app(method):
    def func_wrapper(self, *args, **kwargs):
        check_app(self.app)
        set_forewindows(self.app)
        result = method(self, *args, **kwargs)
        return result

    return func_wrapper


def get_path(path):
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, path)


# %%
if __name__ == "__main__":
    update_templates()

# %%
