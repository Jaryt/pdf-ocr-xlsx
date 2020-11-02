from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import json


class GUI:
    page = 1
    selection_rect = None
    selections = {}

    def update_page(self, inc):
        if self.page in self.selections:
            for selection in self.selections[self.page]:
                self.canvas.delete(selection['text'])
                self.canvas.delete(selection['rect'])

        self.page = max(1, min(self.page + inc, self.max_page))
        self.str_page.set(self.page)
        self.image = ImageTk.PhotoImage(
            self.images[self.page - 1].resize(self.size), Image.ANTIALIAS)
        self.canvas.itemconfig(self.canvas_image, image=self.image)
        self.canvas.pack(side=BOTTOM)

        if self.page in self.selections:
            for selection in self.selections[self.page]:
                new_rect, lbl_text = self.draw_rect(selection['bounds'], selection['cell'])

                selection['rect'] = new_rect
                selection['text'] = lbl_text

    def resize(self, event):
        self.size = (event.width, event.height)
        scaled_image = self.images[self.page -
                                   1].resize(self.size, Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(scaled_image)
        self.canvas.itemconfig(self.canvas_image, image=self.image)

    def on_right_click(self, event):
        for selection in self.selections:
            bounds = selection['bounds']

            if (event.x >= bounds['min'][0] and event.y >= bounds['min'][1] and event.x <= bounds['max'][0] and event.y <= bounds['max'][1]):
                self.selections.remove(selection)
                self.canvas.delete(selection['text'])
                self.canvas.delete(selection['rect'])
                break

    def on_click(self, event):
        self.selection = {'min': (event.x, event.y)}

    def on_drag(self, event):
        self.selection['max'] = (event.x, event.y)

        if (not self.selection_rect):
            self.selection_rect = self.canvas.create_rectangle(
                *self.selection['min'], *self.selection['max'], outline='red', width=3)
        else:
            self.canvas.coords(self.selection_rect, *
                               self.selection['min'], *self.selection['max'])

    def draw_rect(self,  rect, cell):
        new_rect = self.canvas.create_rectangle(
            *rect['min'], *rect['max'], outline='blue', width=2)
        x = rect['min'][0] + \
            (rect['max'][0] - rect['min'][0]) / 2
        y = rect['min'][1] + \
            (rect['max'][1] - rect['min'][1]) / 2

        lbl_text = self.canvas.create_text(
            x, y, text=cell, fill='red', width=3)

        return new_rect, lbl_text

    def add_rect(self):
        if (not self.page in self.selections):
            self.selections[self.page] = []
        cell = self.cell.get("1.0", END+"-1c")

        new_rect, lbl_text = self.draw_rect(self.selection, cell)

        self.selections[self.page].append(
            {'rect': new_rect, 'bounds': self.selection, 'cell': cell, 'text': lbl_text})

        self.canvas.delete(self.selection_rect)
        self.selection_rect = None
        self.selection = None

    def __init__(self, root, images):
        self.max_page = len(images)
        root.geometry('%dx%d' % (700, 900))

        self.top = Frame(root)
        self.top.pack(side=TOP, fill=BOTH, expand=True)

        self.bottom = Frame(root)
        self.bottom.pack(side=BOTTOM)

        self.str_page = StringVar()
        self.str_page.set("1")
        self.lbl_page = Label(root, textvariable=self.str_page)
        self.images = images
        self.canvas = Canvas(root)

        self.image = ImageTk.PhotoImage(self.images[0])
        self.canvas_image = self.canvas.create_image(
            0, 0, image=self.image, anchor="nw")
        self.canvas.pack(in_=self.top, side=BOTTOM, fill=BOTH, expand=True)

        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<Button-2>', self.on_right_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind("<Configure>", self.resize)

        self.btn_prev = Button(
            root, text='Prev', command=lambda: self.update_page(-1))
        self.btn_prev.pack(in_=self.bottom, side=LEFT)
        self.lbl_page.pack(in_=self.bottom, side=LEFT)
        self.btn_next = Button(
            root, text='Next', command=lambda: self.update_page(1))
        self.btn_next.pack(in_=self.bottom, side=LEFT)

        self.lbl_cell = Label(root, text="       Cell:")
        self.lbl_cell.pack(in_=self.bottom, side=LEFT)
        self.cell = Text(self.bottom, height=1, width=5)
        self.cell.pack(in_=self.bottom, side=LEFT)
        self.btn_add = Button(root, text='Add', command=self.add_rect)
        self.btn_add.pack(in_=self.bottom, side=LEFT)
