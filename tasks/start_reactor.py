import pyautogui as py
import ctypes
from time import perf_counter
from time import sleep


def startReactor_task():
    def getScreenCredentials(center: tuple, size: int, offset: int): 
        '''
        center: position of center button
        size: lenght/width of buttons' numpad - from left's center to rights's center 
        offset: lenght between a button to it's according position on a screen
        '''
        space = size / 2
        upper_left = (center[0] - space, center[1] - space)
        
        buttons = []
        for i in range(3):
            for j in range(3):
                buttons.append((upper_left[0] + space * i, upper_left[1] + space * j))
        
        display = []
        for i in range(9):
            display.append((buttons[i][0] - offset, buttons[i][1]))

        return tuple(buttons), tuple(display)
        
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    if screensize == (1920, 1080):
        buttons, display = getScreenCredentials((1260, 600), 250, 600)
    elif screensize == (2736, 1824):
        buttons, display = getScreenCredentials((1875, 1010), 430, 1000)
    else:
        raise IndexError("Your screen's size is not supported.")

    color_blue = (68, 168, 255)
    color_black = (0, 0, 0)

    for _ in range(5):
        button_history = []
        counter = perf_counter()
        finished = True
        while perf_counter() - counter < 1.5:
            img = py.screenshot()
            for index in range(9):
                pixel = img.getpixel(display[index])
                if pixel == color_blue:
                    while True:
                        img = py.screenshot()
                        pixel = img.getpixel(display[index])
                        if pixel == color_black:
                            break
                    finished = False
                    counter = perf_counter()
                    button_history.append(index)
        if finished:
            break
        for index in button_history:
            py.click(buttons[index])
            sleep(0.05)
