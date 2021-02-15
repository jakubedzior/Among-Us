import pyautogui as py
import ctypes
from time import sleep
import pytesseract
from PIL import Image
from random import randint


def fixO2():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    if screensize == (1980, 1080):
        region = ()
        buttons = ()
    elif screensize == (2736, 1824):
        region = (1900, 830, 2120, 900)
        buttons = ((1370, 1440), (1100, 660), (1370, 660), (1620, 670), (1100, 910), (1370, 910), (1620, 910), (1100, 1180), (1370, 1180), (1620, 1180), (1620, 1440))
    else:
        raise IndexError("Your screen's size is not supported.")


    img = py.screenshot()
    img = img.rotate(-25)
    img = img.crop(region)
    img = img.convert('LA')
    img = img.point(lambda p: p > 90 and 255)
    # img = img.resize((img.size[0]*2, img.size[1]*2), Image.ANTIALIAS)

    # pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    string = pytesseract.pytesseract.image_to_string(img, config='-c tessedit_char_whitelist=0123456789')
    string = string[:5]

    if string.isnumeric():
        number = [int(sign) for sign in string]
    else:
        return

    for digit in number:
        py.click(buttons[digit])
        sleep(0.05)
    py.click(buttons[-1])

    img.save(f'Screenshots/o2/{string}.png')
