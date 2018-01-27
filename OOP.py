from tkinter.filedialog import *
import os
import cv2


class Window:
    BIND_KEY = "<Button-1>"  # Button-1 is left click of mouse
    TEXT_LABEL = "-file doesn't choose-"
    BG = 'white'  # back ground colour
    FONT = ('Ubuntu', 15)  # font properties

    def __init__(self, master):
        master.title("Compare details")  # title window
        master.configure(bg="white")  # back ground color of window
        self.containers = [Container(master, 0, 0, "First file"), Container(master, 1, 0, "Second file")]
        button = Button(master, text='Compare', width=10, font=self.FONT, bg=self.BG)
        button.grid(row=2, column=0, sticky="w")
        button.bind(self.BIND_KEY, self.check)  # bind button by func
        self.circuits = []

    def check(self, event):
        if all([c.state for c in self.containers]):
            first_circuit, second_circuit = [c.path for c in self.containers]
            self.circuits = [Handler(first_circuit), Handler(second_circuit)]
            a, b = [c.circuit for c in self.circuits]


class Handler:
    def __init__(self, path):
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (9, 9), 1)
        edged = cv2.Canny(gray_blur, 15, 30)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
        circuit = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[1]
        # circuit is array in arrays in arrays,
        # I cannot use max_id = max(list(map(len, circuit))) or max_id = circuit.index(max(circuit)
        max_len_array = 0
        max_id = 0
        for i in range(len(circuit)):
            if max_len_array < len(circuit[i]):
                max_len_array = len(circuit[i])
                max_id = i
        self.circuit = circuit[max_id]


class Container:
    def __init__(self, master, row, column, text_button):
        self.state = False  # state of func
        button = Button(master, text=text_button, width=10, font=Window.FONT, bg=Window.BG)
        button.grid(row=row, column=column, sticky="w")
        button.bind(Window.BIND_KEY, self.open_file_event)  # bind button by func
        self.label = Label(master, width=20, text=Window.TEXT_LABEL, font=Window.FONT, bg=Window.BG, fg='black')
        self.label.grid(row=row, column=column+1)
        self.path = ""

    def open_file_event(self, event):
        """Open window for get path on the file, filter .jpg and .JPG files, filter all errors"""
        self.path = askopenfilename()
        try:
            if not self.path:
                self.label['text'] = Window.TEXT_LABEL
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
            self.label['text'] = Window.TEXT_LABEL
            self.label['fg'] = 'red'
            self.state = False
            # if return some errors, it'll be painted label in red colour


root = Tk()
gui = Window(root)
root.mainloop()