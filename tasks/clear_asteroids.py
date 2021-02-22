import pyautogui as py
import pynput.keyboard
import ctypes
import os


def clearAsteroids_task():
    def getScreenCredentials(left: int, top: int, right: int, bottom: int): 
        '''
        left: top-left x of the boundary
        top: top-left y of the boundary
        right: bottom-right x of the boundary
        bottom: bottom-right x of the boundary
        '''
        size = (right - left, (bottom - top) / 10)
        
        y_ticks = [(top + i * size[1]) for i in range(10)]

        index = len(y_ticks) - 1
        for i, y_tick in enumerate(y_ticks):
            if y_tick + size[0] > bottom:
                index = i
                break
        for _ in range(len(y_ticks) - 1 - index):
            y_ticks.pop(-1)

        return left, tuple(y_ticks), size
        
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    if screensize == (1920, 1080):
        x_tick, y_ticks, size = getScreenCredentials(1290, 140, 1360, 945)
    elif screensize == (2736, 1824):
        x_tick, y_ticks, size = getScreenCredentials(1920, 230, 2050, 1600)
    else:
        raise IndexError("Your screen's size is not supported.")

    def on_press(key):
        os._exit(0)

    keyboard = pynput.keyboard.Listener(on_press=on_press)
    keyboard.start()

    py.PAUSE = 0.03


    while True:
        for y_tick in y_ticks:
            py.click((x_tick + size[0] / 2, y_tick + size[0] / 2))
