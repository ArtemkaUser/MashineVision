import PIL.Image
import PIL.ImageTk
import cv2
import numpy as np
from tkinter.filedialog import *
from math import sqrt


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
        self.param_circuit = []

    def check(self, event):
        if all([c.state for c in self.containers]):
            path_to_first_circuit, path_to_second_circuit = [c.path for c in self.containers]
            self.circuits = [Handler(path_to_first_circuit), Handler(path_to_second_circuit)]
            first_circuit, second_circuit = [c.circuit for c in self.circuits]
            self.param_circuit = [ParamOfCircuit(first_circuit), ParamOfCircuit(second_circuit)]


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


class ParamOfCircuit:
    def __init__(self, circuit):
        self.circuit = circuit
        self.circuit_for_histogram = 0
        self.lens_of_circuit = 0
        self.width_of_image = 0
        self.height_of_image = 0
        self.fill_circuit = 0
        self.histogram = 0
        self.moving_circuit_in_a_thin()
        self.get_fill_circuit()
        self.calculate_lens()
        self.calculate_histogram()
        self.draw_circuit()

    def moving_circuit_in_a_thin(self):
        # calculate min X and min Y for moving into (0, 0)
        minim_x = self.circuit[0][0][0]
        minim_y = self.circuit[0][0][1]
        for i in range(len(self.circuit)):
            if minim_x > self.circuit[i][0][0]:
                minim_x = self.circuit[i][0][0]
            if minim_y > self.circuit[i][0][1]:
                minim_y = self.circuit[i][0][1]

        # moving circuit in (0, 0)
        for i in range(len(self.circuit)):
            self.circuit[i][0][0] -= minim_x
            self.circuit[i][0][1] -= minim_y

        maxim_x = self.circuit[0][0][0]
        maxim_y = self.circuit[0][0][1]
        # seek max X and max Y for calculate width and height of image
        for i in range(len(self.circuit)):
            if maxim_x < self.circuit[i][0][0]:
                maxim_x = self.circuit[i][0][0]
            if maxim_y < self.circuit[i][0][1]:
                maxim_y = self.circuit[i][0][1]
        self.width_of_image = maxim_y
        self.height_of_image = maxim_x

    def get_fill_circuit(self):
        # create black list for draw circuit in it
        self.fill_circuit = self.create_np_white_image(self.width_of_image, self.height_of_image)
        # dra filling circuit in fill_circuit
        cv2.fillPoly(self.fill_circuit, pts=[self.circuit], color=(255, 255, 255))

    def calculate_lens(self):
        array = self.create_array_skeleton(self.width_of_image)
        self.fill_circuit = np.array(self.fill_circuit)
        for i in range(len(self.fill_circuit)):
            for j in range(len(self.fill_circuit[i])):
                if self.fill_circuit[i][j][0] == 255:
                    array[i] += 1
        self.lens_of_circuit = array

    def create_array_skeleton(self, length):
        array = []
        for i in range(length + 1):
            array.append(0)
        return array

    def calculate_histogram(self):
        self.histogram = self.create_np_white_image(self.width_of_image, self.height_of_image)
        self.lens_of_circuit = np.array(self.lens_of_circuit)
        for j in range(len(self.lens_of_circuit) - 1):
            self.histogram[j, self.lens_of_circuit[j], 0] = 255
            self.histogram[j, self.lens_of_circuit[j], 1] = 255
            self.histogram[j, self.lens_of_circuit[j], 2] = 255

    def create_np_white_image(self, width, height):
        array = np.zeros((width, height, 3), dtype=np.uint8)
        array[::] = (0, 0, 0)
        return array


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