import pytesseract
import xlrd
import pdfextract

def init():
    pdfextract.pdf_to_image('input.pdf')

    pass


if __name__ == "__main__":
    init()
