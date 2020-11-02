import pytesseract
import fitz
import io
import sys
import getopt
import json
import xlwings as xw
import pandas as pd
from tkinter import Tk
from PIL import Image
from gui import GUI

scale = 1
file_name = 'data.json'


def get_pdf_images(loc):
    pdf = fitz.open(loc)

    images = []

    for page_index in range(len(pdf)):
        page = pdf[page_index]

        for img in page.getImageList():
            xref = img[0]
            base_image = pdf.extractImage(xref)
            image_bytes = base_image["image"]

            images.append(Image.open(io.BytesIO(image_bytes)))

    return images


def load():
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except:
        return {}


def save(config):
    with open(file_name, 'w') as file:
        json.dump(config, file, indent=4)


def usage():
    print()


def init():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:e:h:s', [
            'pdf=', 'excel=', 'help', 'setup'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    pdf = 'input.pdf'
    excel = 'output.xlsx'
    setup = False

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-s', '--setup'):
            setup = True
        elif opt in ('-p', '--pdf'):
            pdf = arg
        elif opt in ('-e', '--excel'):
            excel = arg
        else:
            usage()
            sys.exit(2)

    images = get_pdf_images(pdf)
    config = load()

    if setup:
        root = Tk()
        GUI(root, images, config, save)
        root.mainloop()
    else:
        wb = xw.Book(excel)
        last_rows = {}

        for n, page in enumerate(images, start=1):
            if str(n) in config:
                selections = config[str(n)]

                for selection in selections:
                  sheet = wb.sheets[selection['sheet'] or 0]

                  if not selection['sheet'] in last_rows:
                    last_rows[selection['sheet']] = sheet.range(selection['cell'] + str(sheet.cells.last_cell.row)).end('up').row + 1
                  last_row = last_rows[selection['sheet']]

                  bounds = selection['bounds']
                  crop = page.crop((*bounds['min'], *bounds['max']))
                  sheet.range(selection['cell'] + str(last_row)).value = pytesseract.image_to_string(crop).strip()

if __name__ == "__main__":
    init()
