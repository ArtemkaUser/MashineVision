import cv2
import numpy as np


class ParamCircuit:
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
        for row in range(len(self.fill_circuit)):
            for column in range(len(self.fill_circuit[row])):
                if self.fill_circuit[row][column][0] == 255:
                    array[row] += 1
        self.lens_of_circuit = array

    def create_array_skeleton(self, length):
        array = []
        for i in range(length + 1):
            array.append(0)
        return array

    def calculate_histogram(self):
        self.histogram = self.create_np_white_image(self.width_of_image, self.height_of_image)
        self.lens_of_circuit = np.array(self.lens_of_circuit)
        for row in range(len(self.lens_of_circuit) - 1):
            for channel in range(3):
                self.histogram[row, self.lens_of_circuit[row], channel] = 255

    def create_np_white_image(self, width, height):
        array = np.zeros((width, height, 3), dtype=np.uint8)
        array[::] = (0, 0, 0)
        return array
