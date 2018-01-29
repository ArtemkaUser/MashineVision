import PIL.Image
import PIL.ImageTk
import cv2
from tkinter.filedialog import *
import ParamOfCircuit as Pofc
import AverDeviat as ad


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
        self.button.bind(self.BIND_KEY, self.check)  # bind button by func
        self.circuits = []
        self.param_circuit = []

    def check(self, event):
        if all([c.state for c in self.containers]):
            path_to_first_circuit, path_to_second_circuit = [c.path for c in self.containers]
            self.circuits = [Handler(path_to_first_circuit), Handler(path_to_second_circuit)]
            first_circuit, second_circuit = [c.circuit for c in self.circuits]
            self.param_circuit = [Pofc.ParamCircuit(first_circuit), Pofc.ParamCircuit(second_circuit)]
            self.clear_win()
            self.result_win()

    def clear_win(self):
        self.button.destroy()
        for c in self.containers:
            c.button.destroy()
            c.label.destroy()

    def result_win(self):
        pass


class Handler:
    def __init__(self, path):
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (9, 9), 1)
        edged = cv2.Canny(gray_blur, 15, 30)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
        circuit = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[1]
        # circuit is array in arrays in list,
        # I cannot use max_id = circuit.index(max(circuit)
        # max_id = circuit.index(max(circuit))

        max_len_array = 0
        max_id = 0
        for i in range(len(circuit)):
            if max_len_array < len(circuit[i]):
                max_len_array = len(circuit[i])
                max_id = i
        self.circuit = circuit[max_id]


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