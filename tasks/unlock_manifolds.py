import pyautogui as py
import ctypes
from time import perf_counter, sleep
import pytesseract
from PIL import Image, ImageFilter
from random import choice


def unlockManifolds_task():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    if screensize == (1920, 1080):
        region = (570, 380, 1345, 700)
    elif screensize == (2736, 1824):
        region = (715, 650, 2020, 1180)
    else:
        raise IndexError("Your screen's size is not supported.")

    indexes = list(range(10))

    size = (region[2] - region[0]) / 5
    buttons = []
    for i in range(2):
        for j in range(5):
            buttons.append((region[0] + (0.5 + j) * size, region[1] + (0.5 + i) * size))

    def get_concat_h(im1, im2):
        dst = Image.new('RGB', (im1.width + im2.width, im1.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (im1.width, 0))
        return dst


    img = py.screenshot()
    # img = Image.open('./Screenshots/nums_small.png')
    img = img.crop(region)

    img = img.convert('L')
    img = img.point(lambda p: p > 100 and 255)
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    img = img.point(lambda p: p > 200 and 255)
    # img.show()
    squares = []
    for i in range(2):
        for j in range(5):
            square = img.crop((j * size, i * size, (j + 1) * size, (i + 1) * size))
            square = square.crop((0.2 * size, 0.2 * size, 0.8 * size, 0.8 * size))
            squares.append(square)

    counter = perf_counter()
    while perf_counter() - counter < 10:
        finals = []

        order = []
        indexes_copy = indexes.copy()
        for _ in range(10):
            random = choice(indexes_copy)
            indexes_copy.remove(random)
            order.append(random)

        photo = squares[order[0]]
        for index in order[1:]:
            photo = get_concat_h(photo, squares[index])
        
        string = pytesseract.pytesseract.image_to_string(photo, lang='eng', config='--psm 8 -c tessedit_char_whitelist=0123456789')
        string_clean = ''
        for i, sign in enumerate(string):
            if sign.isnumeric():
                string_clean = string_clean + sign
        if len(string_clean) != 10:
            continue

        all_different = True
        results = [int(each) for each in string_clean]
        for each in results:
            if results.count(each) != 1:
                all_different = False
                break
        if not all_different:
            continue

        for i, each in enumerate(results):
            results[i] = each - 1
        results[results.index(-1)] = 9

        for i in range(10):
            finals.append(results[order.index(i)])
        break
    if len(finals) == 10:
        for index in range(10):
            py.click(buttons[finals.index(index)])
            sleep(0.05)