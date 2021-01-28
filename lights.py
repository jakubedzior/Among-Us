import pyautogui as py
from time import sleep, perf_counter
from random import randint
import pynput

def autoSolution(reverse=False):
    region = (550, 850, 800, 100)
    button = 'on.png' if reverse else 'off.png'
    start = perf_counter()

    while True:
        clicked = []

        img = py.screenshot(region=region)
        for pos in py.locateAll(button, img, confidence=0.99):
            x, y = py.center(pos)
            x += region[0]
            y += region[1] - 100

            exists = False
            for each in clicked:
                if each - 5 < x < each + 5:
                    exists = True
                    break
            if not exists:
                py.click(x, y)
                clicked.append(x)
        now = perf_counter()
        if now - start > 300:
            return
        sleep(0.5)


def randomSolution():
    positions = {
        0: [(610, 780), (790, 780), (960, 780), (1140, 780), (1310, 780)],
        1: [(1110, -310), (1240, -310), (1380, -310), (1555, -310), (1720, -310)]
    }
    while True:
        start = perf_counter()

        for position in positions[0]:
            if randint(0, 1) == 1:
                py.click(position)

        now = perf_counter()
        if now - start > 300:
            return
        sleep(0.1)


def manualSolution():
    def on_press_local(key):
        try:
            if key.char in keys:
                button = keys.index(key.char)
                py.click(positions[method][button])
        except AttributeError:  # special key
            pass

    method = 0
    keys = ['a', 's', 'd', 'q', 'e']
    positions = {
        0: [(610, 780), (790, 780), (960, 780), (1140, 780), (1310, 780)],
        1: [(1110, -310), (1240, -310), (1380, -310), (1555, -310), (1720, -310)]
    }


    with pynput.keyboard.Listener(on_press=on_press_local) as keyboard:
        keyboard.join()
