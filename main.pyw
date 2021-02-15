import pynput
import multiprocessing
from time import perf_counter

from weather_node import weatherNode_method
from cameras import camerasFlip_method
from lights import autoLights_method, randomLights_method, manualLights_method
from wires import fixWires_method
from sabotage_O2 import fixO2_method

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
    def __init__(self, current):
        self.current = current

    def set_(self, solution):
        if self.current.state:
            self.current.stop()
        if self.current != solution:
            self.current = solution


class KeyHistory:
    def __init__(self):
        self.list = [None, None, None]
        self.just_matched = False

    def add(self, element):
        self.list[0] = self.list[1]
        self.list[1] = self.list[2]
        self.list[2] = element


def on_click(x, y, button, pressed):
    if pressed and button == pynput.mouse.Button.middle:
        initiatives.current.changeState()
    if pressed and button == pynput.mouse.Button.right and initiatives.current == auto and initiatives.current.state is True:
        initiatives.current.stop()
        if initiatives.current.args != [True]:
            initiatives.current.args = [True]
        else:
            initiatives.current.args = [False]
        initiatives.current.start()


def on_press(key):
    if perf_counter() - program_start > 36000:  # if has been running for 10h
        return False
        
    global key_history
    try:
        key_history.add(key.char)

        if key.char == '-':
            initiatives.set_(manual)
        if key.char == '=':
            initiatives.set_(auto)
        if key.char == ']':
            initiatives.set_(random)
        if key.char == 'x':
            initiatives.set_(cameras)
        
        if key.char == '\\':
            initiatives.current.stop()
            return False

    except AttributeError:  # special key
        key_history.add(key)

    finally:
        if key == pynput.keyboard.Key.space and key_history.just_matched is True:
            fixes.current.start()
        elif key_history.list == [pynput.keyboard.Key.space, pynput.keyboard.Key.alt_l, '1']:
            fixes.set_(wires)
            fixes.current.start()
            key_history.just_matched = True
        elif key_history.list == [pynput.keyboard.Key.space, pynput.keyboard.Key.alt_l, '2']:
            fixes.set_(node)
            fixes.current.start()
            key_history.just_matched = True
        elif key_history.list == [pynput.keyboard.Key.space, pynput.keyboard.Key.alt_l, '3']:
            fixes.set_(sabotageO2)
            fixes.current.start()
            key_history.just_matched = True
        else:
            key_history.just_matched = False


if __name__ == '__main__':
    auto = Power(autoLights_method)
    manual = Power(manualLights_method)
    random = Power(randomLights_method)
    cameras = Power(camerasFlip_method)
    initiatives = Solution(auto)

    wires = Power(fixWires_method)
    node = Power(weatherNode_method)
    sabotageO2 = Power(fixO2_method)
    fixes = Solution(node)  # any

    key_history = KeyHistory()

    mouse = pynput.mouse.Listener(on_click=on_click)
    mouse.start()

    program_start = perf_counter()

    with pynput.keyboard.Listener(on_press=on_press) as keyboard:
        keyboard.join()
