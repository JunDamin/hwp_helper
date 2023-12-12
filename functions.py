# -*- coding: utf-8 -*-
"""
Created on Tue May  9 09:31:12 2023

@author: 2015026
"""
# %%
import customtkinter as ctk
from PIL import Image, ImageChops
from pathlib import Path
import subprocess
import re
import shutil as sh
from time import sleep
from hwpapi.core import App, Engines
import win32gui as wg
from win32api import GetMonitorInfo, MonitorFromPoint
import pywintypes
import sys
import os
import win32con
import re
from time import sleep

def prettify_filename(name):
    result = re.sub(r"[!\"\$\&\'\*\+\,/:;<=>\?@\\^_`{|}~\n]", "_", name)
    return re.sub(r" +", r" ", result)

def get_image(image_path):
    """set image button"""
    image_path = Path(image_path)
    img = Image.open(image_path)

    return ctk.CTkImage(light_image=img, dark_image=img, size=img.size)

def get_image(image_path):
    image_path = Path(image_path)
    img = Image.open(image_path)

    return ctk.CTkImage(light_image=img, dark_image=img, size=img.size)

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
    btn.pack(anchor='w')
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
    
    bbox = (bbox[0]-2, bbox[1]-2, bbox[2]+2, bbox[3]+2)
    return img.crop(bbox)


# %%


def update_template(app, hwp_path):
    hwp = Path(hwp_path)
    app.open(hwp)
    app.actions.MoveDocEnd().run()
    # if it is not end with blank line
    if app.get_text() != "\r\n":
        app.actions.BreakPara().run()
        app.save()

    _, n, _ = app.api.GetPos()
    temp = Path(f"temp/{hwp.stem}_{n}.png")

    #delete master page info
    app.api.SetMessageBoxMode(0x00010001)
    master_page_delete = app.actions.MasterPageDelete()
    master_page_delete.pset.Duplicate = 0
    master_page_delete.pset.Front = 0
    master_page_delete.pset.type = 0
    master_page_delete.run()

    sleep(0.1)
    app.save()
    app.api.SetMessageBoxMode(0xf0000)

    # save as image file
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

    app = App(new_app=True, is_visible=False)
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


def set_forewindow(app):
    hwnd = app.api.XHwpWindows.Active_XHwpWindow.WindowHandle
    return wg.SetForegroundWindow(hwnd)

def show_window(app):
    hwnd = app.api.XHwpWindows.Active_XHwpWindow.WindowHandle
    return wg.ShowWindow(hwnd, 1)

def get_screen_size():
    x1, y1, x2, y2 = GetMonitorInfo(MonitorFromPoint((0, 0))).get("Work")
    return x1, y1, x2 - x1, y2 - y1


def get_window_position(hwnd):
    rect = wg.GetWindowRect(hwnd)
    # Window position
    x = rect[0]
    y = rect[1]

    # Window size
    width = rect[2] - x
    height = rect[3] - y
    return x, y, width, height


def set_window_position(hwnd, x, y, width, height):
    wg.SetWindowPos(hwnd, win32con.HWND_TOP, x, y, width, height, 0)


def run_hwp(i=0):
    path = list(Path(r"C:\Program Files (x86)\HNC").rglob("hwp.exe"))[i]
    if len(Engines()) < 1:
        subprocess.Popen(path)
    return 

def check_app(app):
    try:
        app.api.PageCount
        return app
    except (pywintypes.com_error, AttributeError) as e:
        run_hwp()
        while True:
            engines = Engines()
            if len(engines) < 1:
                sleep(1)
                continue
            if isinstance(app, App):
                app.engine = engines[0]
                break
            app = App(engines[0], dll_path=r"bin/FilePathCheckerModuleExample.dll")
            break
    return app
    

def get_ratio(ctk_app):
    app_width = ctk_app.winfo_screenwidth()
    app_height = ctk_app.winfo_screenheight()
    _, _, screen_width, screen_height = get_screen_size()
    return min(app_width / screen_width, app_height / screen_height)


def back_to_app(func):
    def func_wrapper(app, *args, **kwargs):
        check_app(app)
        set_forewindow(app)
        result = func(app, *args, **kwargs)
        return result

    return func_wrapper


def get_path(path):
    """get path"""
    if not path:
        return None
    if getattr(sys, "frozen", False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, path)

def make_topmost(window):
    # Makes the window topmost
    window.attributes('-topmost', 1)
    # After 1 millisecond, turn off topmost
    window.after(1, lambda: window.attributes('-topmost', 0))
    
# %%
if __name__ == "__main__":
    update_templates()

# %%
