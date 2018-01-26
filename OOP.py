from tkinter.filedialog import *


class WindowOnTheScreen:
    def __init__(self, master):
        """Initialization window"""
        self.master = master
        self.window()

    def window(self):
        """Output window on the screen"""
        self.master.title("Compare details")
        self.master.configure(bg="white")
        self.button("First file", 0, 0,
                    lambda event: self.open_file_event(event, 0, 1))
        self.button("Second file", 1, 0,
                    lambda event: self.open_file_event(event, 1, 1))
        self.button("Compare", 2, 0, lambda event: self.compare(event, 2, 1))
        self.label("-file doesn't choose-", 0, 1)
        self.label("-file doesn't choose-", 1, 1)

    def button(self, text, row_place, column_place, func_bind):
        """Place button in the window"""
        button = Button(self.master, text=text, width=10, font=('Ubuntu', 15), bg='white')
        button.grid(row=row_place, column=column_place, sticky="w")
        button.bind('<Button-1>', func_bind)

    def label(self, text, row_place, column_place, fg="black"):
        """Place label in the window"""
        label = Label(self.master, width=20, text=text, font=('Ubuntu', 15), bg='white', fg=fg)
        label.grid(row=row_place, column=column_place)

    def open_file_event(self, event, row, column):
        of = askopenfilename()
        try:
            if not of:
                self.label("-file doesn't choose-", row, column, 'red')
            else:
                if of.split('.')[-1] == 'jpg' or of.split('.')[-1] == 'JPG':
                    self.label(of.split("/")[-1], row, column, 'green')
                    print(of)  # temporary response, then func will take the path into next class
                else:
                    self.label("-ErrTypeOfFile-", row, column, 'red')
        except TypeError or FileNotFoundError:
            self.label("-file doesn't choose-", row, column, 'red')

    def compare(self, event, row, column):
        pass


root = Tk()
gui = WindowOnTheScreen(root)
root.mainloop()