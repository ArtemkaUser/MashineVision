import PIL.Image
import PIL.ImageTk
from tkinter.filedialog import *
import ParamOfCircuit as Pofc
import AverDeviat as Ad
import Draw2Circuits as D2c
import Handler


class Window:
    BIND_KEY = "<Button-1>"  # Button-1 is left click of mouse
    BG = 'white'  # back ground colour
    FONT = ('Ubuntu', 15)  # font properties

    def __init__(self, master):
        self.master = master
        master.title("Compare details")  # title window
        master.configure(bg="white")  # back ground color of window
        self.containers = [ContBtnLbl(master, 0, 0, "First file"), ContBtnLbl(master, 1, 0, "Second file")]
        self.button = Button(master, text='Compare', width=10, font=self.FONT, bg=self.BG)
        self.button.grid(row=2, column=0, sticky="w")
        self.button.bind(self.BIND_KEY, self.calculate)  # bind button by func
        self.circuits = []
        self.param_circuit = []
        self.nums_px = 0
        self.nums_mm = 0
        self.d_circuit = 0
    def calculate(self, event):
        if all([c.state for c in self.containers]):
            path_to_first_circuit, path_to_second_circuit = [c.path for c in self.containers]
            self.circuits = [Handler.Handler(path_to_first_circuit), Handler.Handler(path_to_second_circuit)]
            first_circuit, second_circuit = [c.circuit for c in self.circuits]
            self.param_circuit = [Pofc.ParamCircuit(first_circuit), Pofc.ParamCircuit(second_circuit)]
            self.draw()

    def draw(self):
        a, b = [c.fill_circuit for c in self.param_circuit]
        first_file_name = "first image.jpg"
        second_file_name = "second image.jpg"
        D2c.Draw2Circuits(a, b, first_file_name)
        a, b = [c.histogram for c in self.param_circuit]
        D2c.Draw2Circuits(a, b, second_file_name)
        self.calc_param()
        self.clear_win()
        self.result_win(first_file_name, second_file_name)

    def calc_param(self):
        a, b = [c.lens_of_circuit for c in self.param_circuit]
        self.nums_px = Ad.AverDev(a, b)
        c, d = [c.width_of_image for c in self.param_circuit]
        self.nums_mm = Ad.AverDev(a, b, max(c, d), 24.4)

    def clear_win(self):
        self.button.destroy()
        for c in self.containers:
            c.button.destroy()
            c.label.destroy()

    def result_win(self, first_file, second_file):
        pass


class ContBtnLbl:
    TEXT_LABEL = "-file doesn't choose-"

    def __init__(self, master, row, column, text_button):
        self.state = False  # state of func
        self.button = Button(master, text=text_button, width=10, font=Window.FONT, bg=Window.BG)
        self.button.grid(row=row, column=column, sticky="w")
        self.button.bind(Window.BIND_KEY, self.open_file_event)  # bind button by func
        self.label = Label(master, width=20, text=self.TEXT_LABEL, font=Window.FONT, bg=Window.BG, fg='black')
        self.label.grid(row=row, column=column+1)
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


root = Tk()
gui = Window(root)
root.mainloop()