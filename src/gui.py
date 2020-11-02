from tkinter import *
from tkinter.ttk import *
from operator import mul
from operator import truediv as div
from PIL import Image, ImageTk


class GUI:
    page = 1
    scale = (1, 1)
    selection_rect = None

    def load_selections(self):
        if str(self.page) in self.selections:
            for selection in self.selections[str(self.page)]:
                bounds = selection['bounds']
                scaled_bounds = {'min': tuple(map(mul, bounds['min'], self.scale)),
                                 'max': tuple(map(mul, bounds['max'], self.scale))}
                new_rect, lbl_text = self.draw_rect(
                    scaled_bounds, selection['cell'])

                selection['rect'] = new_rect
                selection['text'] = lbl_text

    def update_page(self, inc):
        if str(self.page) in self.selections:
            for selection in self.selections[str(self.page)]:
                self.canvas.delete(selection['text'])
                self.canvas.delete(selection['rect'])

        self.page = max(1, min(self.page + inc, self.max_page))
        self.str_page.set(self.page)
        self.image = ImageTk.PhotoImage(
            self.images[self.page - 1].resize(self.size), Image.ANTIALIAS)
        self.canvas.itemconfig(self.canvas_image, image=self.image)
        self.canvas.pack(side=BOTTOM)

        self.load_selections()

    def resize(self, event):
        image = self.images[self.page - 1]
        self.size = (event.width, event.height)
        self.scale = (event.width / image.width, event.height / image.height)
        scaled_image = image.resize(self.size, Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(scaled_image)
        self.canvas.itemconfig(self.canvas_image, image=self.image)

        if str(self.page) in self.selections:
            for selection in self.selections[str(self.page)]:
                bounds = selection['bounds']
                scaled_min = tuple(map(mul, bounds['min'], self.scale))
                scaled_max = tuple(map(mul, bounds['max'], self.scale))
                self.canvas.coords(selection['rect'], *scaled_max, *scaled_min)

                x = scaled_min[0] + \
                    (scaled_max[0] - scaled_min[0]) / 2
                y = scaled_min[1] + \
                    (scaled_max[1] - scaled_min[1]) / 2

                self.canvas.coords(selection['text'], x, y)

    def on_right_click(self, event):
        if str(self.page) in self.selections:
            for selection in self.selections[str(self.page)]:
                bounds = selection['bounds']
                scaled_min = tuple(map(mul, bounds['min'], self.scale))
                scaled_max = tuple(map(mul, bounds['max'], self.scale))

                if (event.x >= scaled_min[0] and event.y >= scaled_min[1] and event.x <= scaled_max[0] and event.y <= scaled_max[1]):
                    self.selections[str(self.page)].remove(selection)
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
        if (not str(self.page) in self.selections):
            self.selections[str(self.page)] = []
        cell = self.cell.get("1.0", END+"-1c")
        sheet = self.sheet.get("1.0", END+"-1c")

        new_rect, lbl_text = self.draw_rect(self.selection, cell)
        scaled_min = tuple(map(div, self.selection['min'], self.scale))
        scaled_max = tuple(map(div, self.selection['max'], self.scale))
        bounds = {'min': (min(scaled_min[0], scaled_max[0]),
                          min(scaled_min[1], scaled_max[1])),
                  'max': (max(scaled_min[0], scaled_max[0]),
                          max(scaled_min[1], scaled_max[1]))}

        self.selections[str(self.page)].append(
            {'rect': new_rect, 'bounds': bounds, 'sheet': sheet, 'cell': cell, 'text': lbl_text})

        self.canvas.delete(self.selection_rect)
        self.selection_rect = None
        self.selection = None

    def __init__(self, root, images, config, save):
        self.selections = config
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
        self.lbl_sheet = Label(root, text="Sheet:")
        self.lbl_sheet.pack(in_=self.bottom, side=LEFT)
        self.sheet = Text(self.bottom, height=1, width=15)
        self.sheet.pack(in_=self.bottom, side=LEFT)
        self.btn_add = Button(root, text='Add', command=self.add_rect)
        self.btn_add.pack(in_=self.bottom, side=LEFT)
        self.btn_save = Button(
            root, text='Save', command=lambda: save(self.selections))
        self.btn_save.pack(in_=self.bottom, side=LEFT)
        self.load_selections()
