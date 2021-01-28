import pynput
import pyautogui as py

def camerasFlip():
    def on_press_local(key):
        try:
            if key.char in keys:
                button = keys.index(key.char)
                py.click(positions[button])
        except AttributeError:  # special key
            pass

    keys = ['z', 'c']
    positions = [(500, 650), (1450, 650)]

    with pynput.keyboard.Listener(on_press=on_press_local) as keyboard:
        keyboard.join()
