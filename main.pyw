import pyautogui as py
from time import sleep, perf_counter
import pynput
import multiprocessing
import sys, os
from random import randint


class Power():
    def __init__(self, function, args=[]):
        self.state = False

        self.process = None
        self.function = function
        self.args = args

    def start(self):
        self.process = multiprocessing.Process(target=self.function, args=self.args)
        self.process.start()

        self.state = True

    def stop(self):
        if self.state:
            self.process.terminate()

            self.state = False

    def changeState(self):
        if self.state:
            self.stop()
            if self.args == [True]:
                self.args = [False]
        else:
            self.start()


class Solution():
    def __init__(self):
        self.current = auto

    def _set(self, solution):
        if self.current.state:
            self.current.stop()
        if self.current != solution:
            self.current = solution


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

def fixWires():
    positions = {
        'x': [565, 1350],
        'y': [270, 460, 645, 830]
    }

    matches = []
    colors = {
        'left': [],
        'right': []
    }

    img = py.screenshot()
    for i in range(4):
        pixel = img.getpixel((positions['x'][0], positions['y'][i]))
        colors['left'].append(pixel)

        pixel = img.getpixel((positions['x'][1], positions['y'][i]))
        colors['right'].append(pixel)
    for l, left in enumerate(colors['left']):
        for r, right in enumerate(colors['right']):
            if left == right:
                matches.append((l, r))

    if len(matches) != 4:
        return
    for match in matches:
        py.moveTo(positions['x'][0], positions['y'][match[0]])
        py.dragTo(positions['x'][1], positions['y']
                  [match[1]], 0.2, py.easeInOutQuad)


def on_click(x, y, button, pressed):
    if pressed and button == pynput.mouse.Button.middle:
        solution.current.changeState()
    if pressed and button == pynput.mouse.Button.right and solution.current == auto and solution.current.state == True:
        solution.current.stop()
        if solution.current.args != [True]:
            solution.current.args = [True]
        else:
            solution.current.args = [False]
        solution.current.start()


def on_press(key):
    if perf_counter() - program_start > 36000:  # if has been running for 10h
        return False
        
    global prev_key
    try:
        if key.char == '-':
            solution._set(manual)
        if key.char == '=':
            solution._set(auto)
        if key.char == ']':
            solution._set(random)
        if key.char == 'x':
            solution._set(cameras)
        
        if key.char == '\\':
            solution.current.stop()
            return False
    except AttributeError:  # special key
        if prev_key == pynput.keyboard.Key.space and key == pynput.keyboard.Key.alt_l:
            extra1.current.start()
    finally:
        prev_key = key


if __name__ == '__main__':
    auto = Power(autoSolution)
    manual = Power(manualSolution)
    random = Power(randomSolution)
    cameras = Power(camerasFlip)
    solution = Solution()

    wires = Power(fixWires)
    extra1 = Solution()
    extra1._set(wires)
    prev_key = None

    mouse = pynput.mouse.Listener(on_click=on_click)
    mouse.start()

    program_start = perf_counter()

    with pynput.keyboard.Listener(on_press=on_press) as keyboard:
        keyboard.join()
