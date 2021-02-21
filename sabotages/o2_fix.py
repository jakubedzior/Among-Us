import pyautogui as py
import ctypes
import pytesseract
from PIL import ImageFilter


def o2Fix_sabotage():
    def getScreenCredentials(upper_left: tuple, bottom_right: tuple): 
        '''
        upper_left: position of upper-left button (1)
        bottom_right: lenght, position of bottom_right button (confirm)
        '''
        space = ((bottom_right[0] - upper_left[0]) / 2, (bottom_right[1] - upper_left[1]) / 3)

        buttons = []
        for i in range(4):
            for j in range(3):
                buttons.append((upper_left[0] + space[0] * j, upper_left[1] + space[1] * i))
        buttons.insert(0, buttons[-2])
        del buttons[-3:-1]
        
        return tuple(buttons)


    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    if screensize == (1920, 1080):
        region = (1300, 485, 1425, 525)
        buttons = getScreenCredentials((800, 380), (1125, 870))
    elif screensize == (2736, 1824):
        region = (1950, 830, 2150, 885)
        buttons = getScreenCredentials((1090, 650), (1640, 1470))
    else:
        raise IndexError("Your screen's size is not supported.")


    img = py.screenshot()
    img = img.rotate(-25)
    img = img.crop(region)
    # img = img.resize((125, 40))
    img = img.convert('LA')
    img = img.point(lambda p: p > 100 and 255)
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    img = img.point(lambda p: p > 200 and 255)


    string = pytesseract.pytesseract.image_to_string(img, config='--psm 8 -c tessedit_char_whitelist=0123456789')
    string = string[:5]

    if string.isnumeric():
        number = [int(sign) for sign in string]
    else:
        py.click(buttons[-1])
        return

    for digit in number:
        py.click(buttons[digit])
    py.click(buttons[-1])

    img.save(f'Screenshots/o2/{string}.png')