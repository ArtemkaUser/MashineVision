from tkinter.filedialog import *


class OutputLabel:
    BG = 'white'  # back ground colour
    FONT = ('Ubuntu', 15)  # font properties

    def __init__(self, master, row, column, text_label, number):
        first_label = Label(master, width=20, text=text_label, font=self.FONT, bg=self.BG)
        first_label.grid(row=row, column=column)
        second_label = Label(master, width=20, text=number, font=self.FONT, bg=self.BG)
        second_label.grid(row=row, column=column+1)
