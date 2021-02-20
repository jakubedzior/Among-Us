import pyautogui as py
import ctypes


def chartCourse_task():
    def getScreenCredentials(left: int, top: int, right: int, bottom: int): 
        '''
        left: top-left x of the boundary
        top: top-left y of the boundary
        right: bottom-right x of the boundary
        bottom: bottom-right x of the boundary
        '''
        size = ((right - left) / 5, (bottom - top) / 100)
        
        x_ticks = []
        x_ticks.append(left + 0.5 * size[0])
        for i in range(4):
            x_ticks.append(x_ticks[i] + size[0])

        y_ticks = [(top + i * size[1]) for i in range(100)]

        return (left, top, right, bottom), tuple(x_ticks), tuple(y_ticks), size
        
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    if screensize == (1920, 1080):
        region, x_ticks, y_ticks, size = getScreenCredentials(460, 260, 1450, 820)
    elif screensize == (2736, 1824):
        region, x_ticks, y_ticks, size = getScreenCredentials(660, 513, 2076, 1311)
    else:
        raise IndexError("Your screen's size is not supported.")

    color_white = (255, 255, 255)


    img = py.screenshot()
    rgb_image = img.convert('RGB')

    elements = []
    for x_tick in x_ticks:
        white_in_step = []
        for y_tick in y_ticks:      
            square = rgb_image.crop((x_tick - size[0] / 2, y_tick, x_tick - size[0] / 2 + size[0], y_tick + size[1]))

            color_count = {}
            for x in range(square.size[0]):
                for y in range(square.size[1]):
                    rgb = square.getpixel((x, y))

                    if rgb in color_count:
                        color_count[rgb] += 1
                    else:
                        color_count[rgb] = 1
            if color_white in color_count.keys():
                white_in_step.append(color_count[color_white])
            else:
                white_in_step.append(0)
        elements.append((x_tick, y_ticks[white_in_step.index(max(white_in_step))] + size[1] / 2))
    
    elements_long = []
    elements_long.append(elements[0])
    for i in range(1, 5):
        elements_long.append((elements[i][0] + (elements[i][0] - elements[i-1][0]) * 0.5, elements[i][1] + (elements[i][1] - elements[i-1][1]) * 0.5))

    
    for i in range(1, 5):
        py.moveTo(elements[i - 1])
        py.dragTo(elements_long[i][0], elements_long[i][1], 0.2, py.easeInOutQuad)
