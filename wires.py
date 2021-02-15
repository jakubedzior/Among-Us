import pyautogui as py
import ctypes


def fixWires():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    if screensize == (1980, 1080):
        positions = {
            'x': (565, 1350),
            'y': (270, 460, 645, 830)
        }
    elif screensize == (2736, 1824):
        positions = {
            'x': (750, 1990),
            'y': (490, 790, 1080, 1375)
        }
    else:
        raise IndexError("Your screen's size is not supported.")


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
