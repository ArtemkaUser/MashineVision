from tkinter.filedialog import *


class ContBtnLbl:
    TEXT_LABEL = "-file doesn't choose-"
    BIND_KEY = "<Button-1>"  # Button-1 is left click of mouse
    BG = 'white'  # back ground colour
    FONT = ('Ubuntu', 15)  # font properties

    def __init__(self, master, row, column, text_button):
        self.state = False  # state of func
        self.button = Button(master, text=text_button, width=10, font=self.FONT, bg=self.BG)
        self.button.grid(row=row, column=column, sticky="w")
        self.button.bind(self.BIND_KEY, self.open_file_event)  # bind button by func
        self.label = Label(master, width=20, text=self.TEXT_LABEL, font=self.FONT, bg=self.BG, fg='black')
        self.label.grid(row=row, column=column + 1)
        self.path = ""

    def open_file_event(self, event):
        """Open window for get path on the file, filter .jpg and .JPG files, filter all errors"""
        self.path = askopenfilename()
        try:
            if not self.path:
                self.label['text'] = self.TEXT_LABEL
                self.label['fg'] = 'red'
                self.state = False
            else:
                if self.path.split('.')[-1].lower() in ['jpg', 'jpeg']:
                    self.label['text'] = os.path.split(self.path)[-1]
                    self.label['fg'] = 'green'
                    # it'll return name of file into label
                    self.state = True
                else:
                    self.label['text'] = "-ErrTypeOfFile-"
                    self.label['fg'] = 'red'
                    # if choose file which has different enhancing type, it'll return error into label
                    self.state = False
        except TypeError or FileNotFoundError:
            self.label['text'] = self.TEXT_LABEL
            self.label['fg'] = 'red'
            self.state = False
            # if return some errors, it'll be painted label in red colour
