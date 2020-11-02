from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk

class GUI:
    page = 1
    rectangle = None

    def update_page(self, inc):
        self.page = max(1, min(self.page + inc, self.max_page))
        self.str_page.set(self.page)
        self.image = ImageTk.PhotoImage(self.images[self.page - 1].resize(self.size), Image.ANTIALIAS)
        self.canvas.itemconfig(self.canvas_image, image=self.image)
        self.canvas.pack(side = BOTTOM)

    def resize(self, event):
        self.size = (event.width, event.height)
        scaled_image = self.images[self.page - 1].resize(self.size, Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(scaled_image)
        self.canvas.itemconfig(self.canvas_image, image=self.image)

    def on_click(self, event):
        self.selection = {'lower': (event.x, event.y)}

    def on_drag(self, event):
        self.selection['upper'] = (event.x, event.y)

        if (not self.rectangle):
            self.rectangle = self.canvas.create_rectangle(*self.selection['lower'], *self.selection['upper'], outline='red', width = 3)
        else:
            self.canvas.coords(self.rectangle, *self.selection['lower'], *self.selection['upper'])

    def __init__(self, root, images):
        self.max_page = len(images)
        root.geometry('%dx%d' % (700, 900))

        self.top = Frame(root)
        self.top.pack(side = TOP, fill = BOTH, expand = True)

        self.bottom = Frame(root)
        self.bottom.pack(side = BOTTOM)

        self.str_page = StringVar()
        self.str_page.set("1")
        self.lbl_page = Label(root, textvariable = self.str_page)
        self.images = images
        self.canvas = Canvas(root)

        self.image = ImageTk.PhotoImage(self.images[0])
        self.canvas_image = self.canvas.create_image(0, 0, image=self.image,anchor="nw")
        self.canvas.pack(in_=self.top, side = BOTTOM, fill = BOTH, expand = True)

        self.canvas.bind('<Button-1>', self.on_click)    
        self.canvas.bind('<B1-Motion>', self.on_drag)   
        self.canvas.bind("<Configure>", self.resize)

        self.cell = Text(self.bottom, height = 1, width = 5)
        self.cell.pack(in_=self.bottom, side = RIGHT)
        self.lbl_cell = Label(root, text="       Cell:")
        self.lbl_cell.pack(in_=self.bottom, side = RIGHT)

        self.btn_prev  = Button(root, text = 'Prev', command = lambda: self.update_page(-1)) 
        self.btn_prev.pack(in_=self.bottom, side = LEFT)
        self.lbl_page.pack(in_=self.bottom, side = LEFT)
        self.btn_next = Button(root, text = 'Next', command = lambda: self.update_page(1)) 
        self.btn_next.pack(in_=self.bottom, side = LEFT)
