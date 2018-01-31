from tkinter.filedialog import *
import ParamOfCircuit as Pofc
import AverDeviat as Ad
import Draw2Circuits as D2c
import Handler
import OutputImage as Oi
import ContainLabel as CLabel
import ContBtnLbl as Cbl


class Window:
    BIND_KEY = "<Button-1>"  # Button-1 is left click of mouse
    BG = 'white'  # back ground colour
    FONT = ('Ubuntu', 15)  # font properties
    FIRST_FILE_NAME = "first image.jpg"
    SECOND_FILE_NAME = "second image.jpg"

    def __init__(self, master):
        self.master = master
        master.title("Compare details")  # title window
        master.configure(bg="white")  # back ground color of window
        self.containers = [Cbl.ContBtnLbl(master, 0, 0, "First file"), Cbl.ContBtnLbl(master, 1, 0, "Second file")]
        self.button = Button(master, text='Compare', width=10, font=self.FONT, bg=self.BG)
        self.button.grid(row=2, column=0, sticky="w")
        self.button.bind(self.BIND_KEY, self.calculate)  # bind button by func
        self.circuits = []
        self.param_circuit = []

    def calculate(self, event):
        if all([c.state for c in self.containers]):
            path_to_first_circuit, path_to_second_circuit = [c.path for c in self.containers]
            self.circuits = [Handler.Handler(path_to_first_circuit), Handler.Handler(path_to_second_circuit)]
            first_circuit, second_circuit = [c.circuit for c in self.circuits]
            self.param_circuit = [Pofc.ParamCircuit(first_circuit), Pofc.ParamCircuit(second_circuit)]
            self.draw()

    def draw(self):
        a, b = [c.fill_circuit for c in self.param_circuit]
        D2c.Draw2Circuits(a, b, self.FIRST_FILE_NAME)
        a, b = [c.histogram for c in self.param_circuit]
        D2c.Draw2Circuits(a, b, self.SECOND_FILE_NAME)
        self.clear_win()
        self.result_win()

    def clear_win(self):
        self.button.destroy()
        for c in self.containers:
            c.button.destroy()
            c.label.destroy()

    def result_win(self):
        a, b = [c.lens_of_circuit for c in self.param_circuit]
        nums_px = Ad.AverDev(a, b)
        first_height, second_height = [c.width_of_image for c in self.param_circuit]
        first_width, second_width = [c.height_of_image for c in self.param_circuit]
        nums_mm = Ad.AverDev(a, b, max(first_height, second_height), 24.4)
        Oi.OutputImage(self.master, 0, 0, max(first_width, second_width), max(first_height, second_height), self.FIRST_FILE_NAME)
        Oi.OutputImage(self.master, 0, 1, max(first_width, second_width), max(first_height, second_height), self.SECOND_FILE_NAME)
        CLabel.OutputLabel(self.master, 1, 0, 'Ср. отклонение(px):', nums_px.deviation())
        CLabel.OutputLabel(self.master, 2, 0, 'Ср.кв.отклонение(px):', nums_px.average_dev())
        CLabel.OutputLabel(self.master, 3, 0, 'Макс. отклонение(px):', nums_px.max_deviation())
        CLabel.OutputLabel(self.master, 1, 2, 'Ср. отклонение(mm):', nums_mm.deviation())
        CLabel.OutputLabel(self.master, 2, 2, 'Ср.кв.отклонение(mm):', nums_mm.average_dev())
        CLabel.OutputLabel(self.master, 3, 2, 'Макс. отклонение(px):', nums_mm.max_deviation())


root = Tk()
gui = Window(root)
root.mainloop()
