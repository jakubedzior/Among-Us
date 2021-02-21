import pyautogui as py
import ctypes


class Node:
    def __init__(self, sides=['left', 'right']):
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        if screensize == (1920, 1080):
            self.board = {
                'x1': 512,
                'y1': 387,
                'x2': 1404,
                'y2': 608
            }
        elif screensize == (2736, 1824):
            self.board = {
                'x1': 610,
                'y1': 650,
                'x2': 2120,
                'y2': 1030
            }
        else:
            raise IndexError("Your screen's size is not supported.")
        
        self.step = (self.board['x2'] - self.board['x1']) / 16
        self.position = (self.board['x1'], self.board['y1'])
        self.path = [(self.board['x1'], self.board['y1'] - self.step), self.position]
        self.direction = 'S'
        self.counter = 0
        self.image = py.screenshot()
        self.sides = sides


    def solve(self):

        def getNearDirection(direction: str, order: str):
            if order == 'right':
                if direction == 'S':
                    return 'W'
                if direction == 'W':
                    return 'N'
                if direction == 'N':
                    return 'E'
                if direction == 'E':
                    return 'S'
            if order == 'left':
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
            self.direction = getNearDirection(getNearDirection(direction, self.sides[0]), self.sides[0])


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
            next_direction = getNearDirection(self.direction, self.sides[1])
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

def get_concat_solutions(sol1: list, sol2: list):
    solution = sol1.copy()
    for step1 in sol1[::-1]:
        found = False
        for step2 in sol1:
            if found:
                continue
            if step1 not in sol2 or step2 not in sol2:
                continue
            if sol1.index(step2) - sol1.index(step1) <= 1:
                continue
            if (solution.index(step2) - solution.index(step1)) - (sol2.index(step2) - sol2.index(step1)) <= 0:
                continue
            found = True
            solution[solution.index(step1):solution.index(step2)] = sol2[sol2.index(step1):sol2.index(step2)]
    return solution



def weatherNode_task():
    node = Node(['left', 'right'])
    solution_left = node.solve()

    node = Node(['right', 'left'])
    solution_right = node.solve()

    solution = get_concat_solutions(solution_left, solution_right)

    try:
        for i, step in enumerate(solution):
            if i == 0:
                py.mouseDown(step[0], step[1])
            else:
                py.moveTo(step[0], step[1])
        py.mouseUp()
    except TypeError:
        pass
