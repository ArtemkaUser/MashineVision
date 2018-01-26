from tkinter.filedialog import *
import os


class WindowOnTheScreen:
    def __init__(self, master):
        self.master = master
        self.first_container = Container(master, 0, 0, "First file")
        self.second_container = Container(master, 1, 0, "Second file")
        self.window()

    def window(self):
        """Output window on the screen"""
        self.master.title("Compare details")  # title window
        self.master.configure(bg="white")  # back ground color of window
        self.button("Compare", 2, 0, lambda event: self.check(event))

    def button(self, text, row_place, column_place, func_bind):
        """Place button in the window"""
        button = Button(self.master, text=text, width=10, font=('Ubuntu', 15), bg='white')
        button.grid(row=row_place, column=column_place, sticky="w")
        button.bind('<Button-1>', func_bind)  # bind button by func

    def check(self, event):
        if self.first_container.state is True and self.second_container.state is True:
            print("good")
        else:
            print("bad")


class Handler:
    def compare(self):
        pass


class Container:
    def __init__(self, master, row, column, text_button):
        self.master = master
        self.row_button = row
        self.column_button = column
        self.column_label = column + 1
        self.text_button = text_button
        self.text_label = "-file doesn't choose-"
        self.bind_key = "<Button-1>"  # Button-1 is left click of mouse
        self.bg = 'white'  # back ground colour
        self.font = ('Ubuntu', 15)  # font properties
        self.fg_err = 'red'  # colour of error text
        self.state = False  # state of func
        self.button()
        self.label(self.text_label)

    def button(self):
        """Place button in the window"""
        button = Button(self.master, text=self.text_button, width=10, font=self.font, bg=self.bg)
        button.grid(row=self.row_button, column=self.column_button, sticky="w")
        button.bind(self.bind_key, lambda event: self.open_file_event(event))  # bind button by func

    def label(self, text, fg='black'):
        """Place label in the window"""
        label = Label(self.master, width=20, text=text, font=self.font, bg=self.bg, fg=fg)
        label.grid(row=self.row_button, column=self.column_label)

    def open_file_event(self, event):
        """Open window for get path on the file, filter .jpg and .JPG files, filter all errors"""
        path = askopenfilename()
        try:
            if not path:
                self.label(self.text_label, self.fg_err)
                self.state = False
            else:
                if path.split('.')[-1] == 'jpg' or path.split('.')[-1] == 'JPG':
                    self.label(os.path.split(path)[-1], 'green')
                    # it'll return name of file into label
                    self.state = True
                else:
                    self.label("-ErrTypeOfFile-", self.fg_err)
                    # if choose file which has different enhancing type, it'll return error into label
                    self.state = False
        except TypeError or FileNotFoundError:
            self.label(self.text_label, self.fg_err)
            self.state = False
            # if return some errors, it'll be painted label in red colour


root = Tk()
gui = WindowOnTheScreen(root)
root.mainloop()