import pytesseract
import xlrd
import fitz
import io
from tkinter import Tk
from gui import GUI
from PIL import Image

scale = 1

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


def init():
    images = get_pdf_images('input.pdf')

    root = Tk()
    app = GUI(root, images)
    root.mainloop()

    pass


if __name__ == "__main__":
    init()