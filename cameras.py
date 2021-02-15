import pynput
import pyautogui as py
import ctypes


def camerasFlip_method():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    if screensize == (1980, 1080):
        positions = ((500, 650), (1450, 650))
    elif screensize == (2736, 1824):
        positions = ((620, 1100), (2150, 1100))
    else:
        raise IndexError("Your screen's size is not supported.")

    keys = ['z', 'c']


    def on_press_local(key):
        try:
            if key.char in keys:
                index = keys.index(key.char)
                py.click(positions[index])
        except AttributeError:  # special key
            pass

    with pynput.keyboard.Listener(on_press=on_press_local) as keyboard:
        keyboard.join()
