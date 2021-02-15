import pyautogui as py
import ctypes


class Node:
    def __init__(self):
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        if screensize == (1980, 1080):
            self.board = {
                'x1': 512,
                'y1': 387,
                'x2': 1404,
                'y2': 608
            }
        elif screensize == (2736, 1824):
            self.board = {
                'x1': 660,
                'y1': 670,
                'x2': 2075,
                'y2': 1023
            }
        else:
            raise IndexError("Your screen's size is not supported.")
        
        self.step = (self.board['x2'] - self.board['x1']) / 16
        self.position = (self.board['x1'], self.board['y1'])
        self.path = [(self.board['x1'], self.board['y1'] - self.step), self.position]
        self.direction = 'S'
        self.counter = 0
        self.image = py.screenshot()


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


def weatherNode_method():
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
