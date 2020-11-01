import fitz
import io
import tkinter
from PIL import Image, ImageTk


def pdf_to_image(loc):
    pdf = fitz.open(loc)

    root = tkinter.Tk()
    root.bind("<Button>", lambda event: event.widget.quit())
    root.geometry('+%d+%d' % (100, 100))
    old_label_image = None

    for page_index in range(len(pdf)):
        # get the page itself
        page = pdf[page_index]

        for img in page.getImageList():
            xref = img[0]
            base_image = pdf.extractImage(xref)
            image_bytes = base_image["image"]

            image = Image.open(io.BytesIO(image_bytes))

            try:
                root.geometry('%dx%d' % (image.size[0], image.size[1]))
                tkpi = ImageTk.PhotoImage(image)
                label_image = tkinter.Label(root, image=tkpi)
                label_image.place(
                    x=0, y=0, width=image.size[0], height=image.size[1])
                root.title(f)
                if old_label_image is not None:
                    old_label_image.destroy()
                old_label_image = label_image
                root.mainloop()  # wait until user clicks the window
            except e:
                # This is used to skip anything not an image.
                # Image.open will generate an exception if it cannot open a file.
                # Warning, this will hide other errors as well.
                pass
