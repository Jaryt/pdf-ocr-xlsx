import pytesseract
import xlrd
# import pdfminer


def pdf_to_image(loc):
    fp = open(loc, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser, password)

    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    rsrcmgr = PDFResourceManager()
    device = PDFDevice(rsrcmgr)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)


def init():

    pass


if __name__ == "__main__":
    init()
