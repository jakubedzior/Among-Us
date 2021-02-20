import pyautogui as py
import ctypes
from time import perf_counter


def calibrateDistribution_task():
    def getScreenCredentials(left: int, top: int, right: int, bottom: int): 
        '''
        left: top-left x
        top: top-left y
        right: bottom-right x
        bottom: bottom-right x
        '''
        space = (right - left, (bottom - top) / 2)
        
        buttons = []
        for i in range(3):
            buttons.append((right, top + i * space[1]))
        
        pixels = []
        for i in range(3):
            pixels.append((left, top + i * space[1]))

        return tuple(buttons), tuple(pixels)      
        
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    if screensize == (1920, 1080):
        buttons, pixels = getScreenCredentials(820, 290, 1240, 820)
    elif screensize == (2736, 1824):
        buttons, pixels = getScreenCredentials(1166, 558, 1750, 1309)
    else:
        raise IndexError("Your screen's size is not supported.")

    color_grey = (71, 73, 71)


    for step in range(3):
        counter = perf_counter()
        while perf_counter() - counter < 2:
            img = py.screenshot()
            if img.getpixel(pixels[step]) == color_grey:
                py.click(buttons[step])
                break

