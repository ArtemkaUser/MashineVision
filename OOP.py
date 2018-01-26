from tkinter.filedialog import *
import os


class WindowOnTheScreen:
    def __init__(self, master):
        """Initialization window"""
        self.master = master
        self.window()

    def window(self):
        """Output window on the screen"""
        self.master.title("Compare details")  # title window
        self.master.configure(bg="white")  # back ground color of window

        # input <lambda> func for initialization event trigger
        self.button("First file", 0, 0,  # first number is row, second is column where will be placed button
                    lambda event: self.open_file_event(event, 0, 1))
        # first number is row, second is column where'll be placed information label about result of pushing button

        self.button("Second file", 1, 0,
                    lambda event: self.open_file_event(event, 1, 1))
        self.button("Compare", 2, 0, lambda event: self.compare(event, 2, 1))
        self.label("-file doesn't choose-", 0, 1)  # first number is row, second is column where will be placed label
        self.label("-file doesn't choose-", 1, 1)

    def button(self, text, row_place, column_place, func_bind):
        """Place button in the window"""
        button = Button(self.master, text=text, width=10, font=('Ubuntu', 15), bg='white')
        button.grid(row=row_place, column=column_place, sticky="w")
        button.bind('<Button-1>', func_bind)  # bind button by func

    def label(self, text, row_place, column_place, fg="black"):
        """Place label in the window"""
        label = Label(self.master, width=20, text=text, font=('Ubuntu', 15), bg='white', fg=fg)
        label.grid(row=row_place, column=column_place)

    def open_file_event(self, event, row, column):
        """Open window for get path on the file, filter .jpg and .JPG, filter all errors"""
        path = askopenfilename()
        try:
            if not path:
                self.label("-file doesn't choose-", row, column, 'red')
            else:
                if path.split('.')[-1] == 'jpg' or path.split('.')[-1] == 'JPG':
                    self.label(os.path.split(path)[-1], row, column, 'green')
                    # it'll return name of file into label
                    print(path)  # temporary response, then func will take the path into next class
                else:
                    self.label("-ErrTypeOfFile-", row, column, 'red')
                    # if choose file which has different enhancing type, it'll return error into label
        except TypeError or FileNotFoundError:
            self.label("-file doesn't choose-", row, column, 'red')
            # if return some errors, it'll be painted label in red colour

    def compare(self, event, row, column):
        pass  # coming soon


root = Tk()
gui = WindowOnTheScreen(root)
root.mainloop()