import pynput
import pyautogui as py
import ctypes
import os


def cameraFlip_other():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    if screensize == (1920, 1080):
        buttons = ((500, 650), (1450, 650))
    elif screensize == (2736, 1824):
        buttons = ((560, 1120), (2170, 1120))
    else:
        raise IndexError("Your screen's size is not supported.")

    keys = ['a', 'd']
    

    def on_click(x, y, button, pressed):
        if button == pynput.mouse.Button.left and (x, y) not in buttons:
            os._exit(0)

    def on_press(key):
        if key == pynput.keyboard.Key.esc:
            return False

        try:
            if key.char in keys:
                index = keys.index(key.char)
                py.click(buttons[index])
        except AttributeError:  # special key
            pass

        
    mouse = pynput.mouse.Listener(on_click=on_click)
    mouse.start()

    with pynput.keyboard.Listener(on_press=on_press) as keyboard:
        keyboard.join()
