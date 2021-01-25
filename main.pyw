import pyautogui as py
from time import sleep, perf_counter
import pynput
import multiprocessing
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
    def __init__(self, current):
        self.current = current

    def set_(self, solution):
        if self.current.state:
            self.current.stop()
        if self.current != solution:
            self.current = solution


class Node:
    def __init__(self):
        self.image = py.screenshot()
        self.board = {
            'x1': 512,
            'y1': 387,
            'x2': 1404,
            'y2': 608
        }
        self.step = (self.board['x2'] - self.board['x1']) / 16
        self.position = (self.board['x1'], self.board['y1'])
        self.path = [(self.board['x1'], self.board['y1'] - self.step), self.position]
        self.direction = 'S'
        self.counter = 0

    def solve(self):

        def getNextDirection(direction):
            if direction == 'S':
                return 'W'
            if direction == 'W':
                return 'N'
            if direction == 'N':
                return 'E'
            if direction == 'E':
                return 'S'
        
        def getPreviousDirection(direction):
            if direction == 'S':
                return 'E'
            if direction == 'E':
                return 'N'
            if direction == 'N':
                return 'W'
            if direction == 'W':
                return 'S'
        
        def getPosition(self, direction):
            if direction == 'S':
                position = (self.position[0], self.position[1] + self.step)
            elif direction == 'N':
                position = (self.position[0], self.position[1] - self.step)
            elif direction == 'E':
                position = (self.position[0] + self.step, self.position[1])
            elif direction == 'W':
                position = (self.position[0] - self.step, self.position[1])
            return position

        def ifPositionFree(self, position):
            pixel = self.image.getpixel(position)
            if pixel == (165, 162, 140):
                return True
            return False

        def ifInBoundaries(self, position):
            if (position[0] - self.board['x1'] > -self.step / 2 and
                position[0] - self.board['x2'] < self.step / 2 and
                position[1] - self.board['y1'] > -self.step / 2 and
                    position[1] - self.board['y2'] < self.step / 2):
                return True
            return False

        def ifDirectionFree(self, direction):
            position = getPosition(self, direction)
            return ifInBoundaries(self, position) and ifPositionFree(self, position)

        def moveToPosition(self, position):
            self.position = position
            self.path.append(self.position)

        def moveToDirection(self, direction):
            moveToPosition(self, getPosition(self, direction))
            self.direction = getPreviousDirection(getPreviousDirection(direction))


        def clean(self):
            loop = True
            while loop:
                loop = False
                for i, position in enumerate(self.path):
                    try:
                        second = self.path[i + 1:].index(position)
                        self.path = self.path[:i] + self.path[second + i + 1:]
                        loop = True
                        break
                    except ValueError:
                        pass

        def whenNextStep(self):
            next_direction = getNextDirection(self.direction)
            if ifDirectionFree(self, next_direction):
                moveToDirection(self, next_direction)
                self.counter = 0
            else:
                self.counter += 1
                if self.counter > 4:
                    return False

                self.direction = next_direction
                whenNextStep(self)
        
        def ifFinished(self):
            position = self.position
            if abs(self.board['x2'] - position[0]) < self.step / 2 and abs(self.board['y2'] - position[1]) < self.step / 2:
                return True
            return False

        
        while True:
            if whenNextStep(self) is False:
                return None
            if ifFinished(self) is True:
                clean(self)
                self.path.append((self.board['x2'], self.board['y2'] + self.step))
                return self.path


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
    for l_index, left in enumerate(colors['left']):
        for r_index, right in enumerate(colors['right']):
            if left == right:
                matches.append((l_index, r_index))

    if len(matches) != 4:
        return
    for match in matches:
        py.moveTo(positions['x'][0], positions['y'][match[0]])
        py.dragTo(positions['x'][1], positions['y']
                  [match[1]], 0.2, py.easeInOutQuad)


def weatherNode():
    node = Node()
    solution = node.solve()
    try:
        for i, step in enumerate(solution):
            if i == 0:
                py.mouseDown(step[0], step[1])
            else:
                py.moveTo(step[0], step[1])
        py.mouseUp()
    except TypeError:
        pass


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
        if key_history.list == [pynput.keyboard.Key.space, pynput.keyboard.Key.alt_l, '1']:
            wires.current.start()
        if key_history.list == [pynput.keyboard.Key.space, pynput.keyboard.Key.alt_l, '2']:
            node.current.start()



class KeyHistory:
    def __init__(self):
        self.list = [None, None, None]

    def add(self, element):
        self.list[0] = self.list[1]
        self.list[1] = self.list[2]
        self.list[2] = element



if __name__ == '__main__':
    auto = Power(autoSolution)
    manual = Power(manualSolution)
    random = Power(randomSolution)
    cameras = Power(camerasFlip)
    initiatives = Solution(auto)

    wiresPower = Power(fixWires)
    wires = Solution(wiresPower)

    nodePower = Power(weatherNode)
    node = Solution(nodePower)

    key_history = KeyHistory()

    mouse = pynput.mouse.Listener(on_click=on_click)
    mouse.start()

    program_start = perf_counter()

    with pynput.keyboard.Listener(on_press=on_press) as keyboard:
        keyboard.join()
