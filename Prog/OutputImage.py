import PIL.Image
import PIL.ImageTk
from tkinter.filedialog import *


class OutputImage:
    def __init__(self, master, row, column, width, height, file_name):
        image_result = PIL.Image.open(file_name)
        image_result = image_result.resize((int(width/5), int(height/5)), PIL.Image.ANTIALIAS)
        render_result = PIL.ImageTk.PhotoImage(image_result)
        label = Label(master, image=render_result)
        label.image = render_result
        label.grid(row=row, column=column)
