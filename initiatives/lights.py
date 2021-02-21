import pyautogui as py
from time import sleep, perf_counter
from random import randint
import pynput
import ctypes


def autoLights_method(reverse=False):
    def getScreenCredentials(left: tuple, right: tuple): 
        '''
        left: position of most left switch
        right: position of most right switch
        '''
        size = (right[0] - left[0]) / 4
        
        buttons = []
        for i in range(5):
            buttons.append((left[0] + size * i, left[1]))

        return tuple(buttons)

    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    if screensize == (1920, 1080):
        buttons = getScreenCredentials((612, 900), (1310, 900))
        offset = -100
    elif screensize == (2736, 1824):
        buttons = getScreenCredentials((780, 1520), (1960, 1520))
        offset = -200
    else:
        raise IndexError("Your screen's size is not supported.")
        
    start = perf_counter()
    if reverse:
        color_green = (0, 255, 0)
    else:
        color_green = (26, 77, 26)


    while True:
        img = py.screenshot()
        for pos in buttons:
            pixel = img.getpixel(pos)
            if pixel == color_green:
                py.click((pos[0], pos[1] + offset))

        now = perf_counter()
        if now - start > 300:
            return
        sleep(0.5)


def randomLights_method():
    def getScreenCredentials(left: tuple, right: tuple): 
        '''
        left: position of most left switch
        right: position of most right switch
        '''
        size = (right[0] - left[0]) / 4
        
        buttons = []
        for i in range(5):
            buttons.append((left[0] + size * i, left[1]))

        return tuple(buttons)

    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    if screensize == (1920, 1080):
        buttons = getScreenCredentials((612, 900), (1310, 900))
    elif screensize == (2736, 1824):
        buttons = getScreenCredentials((780, 1320), (1960, 1320))
    else:
        raise IndexError("Your screen's size is not supported.")


    while True:
        start = perf_counter()

        for pos in buttons:
            if randint(0, 1) == 1:
                py.click(pos)

        now = perf_counter()
        if now - start > 300:
            return
        sleep(0.1)


def manualLights_method():
    def getScreenCredentials(left: tuple, right: tuple): 
        '''
        left: position of most left switch
        right: position of most right switch
        '''
        size = (right[0] - left[0]) / 4
        
        buttons = []
        for i in range(5):
            buttons.append((left[0] + size * i, left[1]))

        return tuple(buttons)

    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    if screensize == (1920, 1080):
        buttons = getScreenCredentials((612, 900), (1310, 900))
    elif screensize == (2736, 1824):
        buttons = getScreenCredentials((780, 1320), (1960, 1320))
    else:
        raise IndexError("Your screen's size is not supported.")

    keys = ['a', 's', 'd', 'q', 'e']


    def on_press_local(key):
        try:
            if key.char in keys:
                index = keys.index(key.char)
                py.click(buttons[index])
        except AttributeError:  # special key
            pass

    with pynput.keyboard.Listener(on_press=on_press_local) as keyboard:
        keyboard.join()
