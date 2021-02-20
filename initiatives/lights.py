import pyautogui as py
from time import sleep, perf_counter
from random import randint
import pynput
import ctypes


def autoLights_method(reverse=False):
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    if screensize == (1920, 1080):
        positions = ((612, 900), (788, 900), (960, 900), (1140, 900), (1310, 900))
        offset = -100
    elif screensize == (2736, 1824):
        positions = ((820, 1480), (1100, 1480), (1370, 1480), (1650, 1480), (1920, 1480))
        offset = -200
    else:
        raise IndexError("Your screen's size is not supported.")
        
    start = perf_counter()
    if reverse:
        button = (0, 255, 0)
    else:
        button = (26, 77, 26)


    while True:
        img = py.screenshot()
        for pos in positions:
            pixel = img.getpixel(pos)
            if pixel == button:
                py.click((pos[0], pos[1] + offset))

        now = perf_counter()
        if now - start > 300:
            return
        sleep(0.5)


def randomLights_method():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    if screensize == (1920, 1080):
        positions = ((612, 800), (788, 800), (960, 800), (1140, 800), (1310, 800))
    elif screensize == (2736, 1824):
        positions = ((820, 1280), (1100, 1280), (1370, 1280), (1650, 1280), (1920, 1280))
    else:
        raise IndexError("Your screen's size is not supported.")


    while True:
        start = perf_counter()

        for pos in positions:
            if randint(0, 1) == 1:
                py.click(pos)

        now = perf_counter()
        if now - start > 300:
            return
        sleep(0.1)


def manualLights_method():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    if screensize == (1920, 1080):
        positions = ((612, 800), (788, 800), (960, 800), (1140, 800), (1310, 800))
    elif screensize == (2736, 1824):
        positions = ((820, 1280), (1100, 1280), (1370, 1280), (1650, 1280), (1920, 1280))
    else:
        raise IndexError("Your screen's size is not supported.")

    keys = ['a', 's', 'd', 'q', 'e']


    def on_press_local(key):
        try:
            if key.char in keys:
                index = keys.index(key.char)
                py.click(positions[index])
        except AttributeError:  # special key
            pass

    with pynput.keyboard.Listener(on_press=on_press_local) as keyboard:
        keyboard.join()
