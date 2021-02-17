import pyautogui as py
import ctypes
from time import sleep


def openDoor_method():
    def getScreenCredentials(upper_left: tuple, bottom_right: tuple): 
        '''
        upper_left: position of upper-left button
        bottom_right: lenght, position of bottom_right button
        '''
        space = (bottom_right[0] - upper_left[0], (bottom_right[1] - upper_left[1]) / 3)

        buttons = []
        for i in range(2):
            for j in range(4):
                buttons.append((upper_left[0] + space[0] * i, upper_left[1] + space[1] * j))
        return tuple(buttons)

        
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    if screensize == (1920, 1080):
        buttons = getScreenCredentials((875, 215), (1210, 800))
    elif screensize == (2736, 1824):
        buttons = getScreenCredentials()
    else:
        raise IndexError("Your screen's size is not supported.")

    color_red = (187, 34, 34)


    img = py.screenshot()
    for button in buttons:
        if img.getpixel(button) == color_red:
            py.click(button)
            # sleep(0.05)
