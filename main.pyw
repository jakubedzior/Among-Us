import pynput
import multiprocessing
from time import perf_counter

from initiatives.lights import autoLights_method, manualLights_method, randomLights_method
from others.camera_flip import cameraFlip_other
from others.door_open import doorOpen_other
from sabotages.o2_fix import o2Fix_sabotage
from tasks.calibrate_distribution import calibrateDistribution_task
from tasks.chart_course import chartCourse_task
from tasks.start_reactor import startReactor_task
from tasks.unlock_manifolds import unlockManifolds_task
from tasks.weather_node import weatherNode_task
from tasks.wires import wires_task


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

def whenCombination(key: str, power: Power, just_matched: bool = True):
    if key_history.list == [pynput.keyboard.Key.space, pynput.keyboard.Key.alt_l, key]:
        combinations.set_(power)
        combinations.current.start()
        if just_matched:
            key_history.just_matched = True
        return True
    return False


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
        if key.char == '`':
            controller = pynput.keyboard.Controller()
            controller.press(pynput.keyboard.Key.esc)
        
        if key.char == '\\':
            initiatives.current.stop()
            return False

    except AttributeError:  # special key
        key_history.add(key)

    finally:
        if key == pynput.keyboard.Key.space and key_history.just_matched is True:
            combinations.current.start()
        elif whenCombination('q', wires_task):
            pass
        elif whenCombination('w', weatherNode_task):
            pass
        elif whenCombination('e', startReactor_task):
            pass
        elif whenCombination('r', doorOpen_other):
            pass
        elif whenCombination('a', calibrateDistribution_task):
            pass
        elif whenCombination('s', chartCourse_task):
            pass
        elif whenCombination('d', unlockManifolds_task):
            pass
        elif whenCombination('x', o2Fix_sabotage):
            pass
        elif whenCombination('c', cameraFlip_other, just_matched=False):
            pass
        else:
            key_history.just_matched = False


if __name__ == '__main__':
    auto = Power(autoLights_method)
    manual = Power(manualLights_method)
    random = Power(randomLights_method)
    initiatives = Solution(auto)

    wires_task = Power(wires_task)
    weatherNode_task = Power(weatherNode_task)
    o2Fix_sabotage = Power(o2Fix_sabotage)
    startReactor_task = Power(startReactor_task)
    cameraFlip_other = Power(cameraFlip_other)
    doorOpen_other = Power(doorOpen_other)
    calibrateDistribution_task = Power(calibrateDistribution_task)
    chartCourse_task = Power(chartCourse_task)
    unlockManifolds_task = Power(unlockManifolds_task)
    combinations = Solution(weatherNode_task)  # any

    key_history = KeyHistory()

    mouse = pynput.mouse.Listener(on_click=on_click)
    mouse.start()

    program_start = perf_counter()

    with pynput.keyboard.Listener(on_press=on_press) as keyboard:
        keyboard.join()
