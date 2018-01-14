from tkinter import *
import math
import cv2
import numpy as np
from tkinter.filedialog import *


def open_first_file(event):
    global flag_1, circuit_1, maximX_1, maximY_1
    try:
        of = askopenfilename()

        if not of:
            label_1['fg'] = 'red'
            label_1['text'] = "-file doesn't choose-"
            flag_1 = 0
        else:
            file = open(of, 'r')

            if file.name.lower()[-3:].find("jpg") != -1:
                circuit_1, maximX_1, maximY_1 = handler(cv2.imread(file.name))
                file.close()
                temp = file.name.split('/')
                label_1['fg'] = 'green'
                label_1['text'] = temp[len(temp) - 1]
                flag_1 = 1

            else:
                label_1['fg'] = 'red'
                label_1['text'] = "-ErrTypeOfFile-"
                flag_1 = 0

    except TypeError or FileNotFoundError:
        label_1['fg'] = 'red'
        label_1['text'] = "-file doesn't choose-"
        flag_1 = 0
    check_btn_compare()

def open_second_file(event):
    global flag_2, circuit_2, maximX_2, maximY_2
    try:
        of = askopenfilename()

        if not of:
            label_2['fg'] = 'red'
            label_2['text'] = "-file doesn't choose-"
            flag_2 = 0

        else:
            file = open(of, 'r')
            if file.name.lower()[-3:].find("jpg") != -1:
                circuit_2, maximX_2, maximY_2 = handler(cv2.imread(file.name))
                file.close()
                temp = file.name.split('/')
                label_2['fg'] = 'green'
                label_2['text'] = temp[len(temp)-1]
                flag_2 = 1

            else:
                label_2['fg'] = 'red'
                label_2['text'] = "-ErrTypeOfFile-"
                flag_2 = 0

    except TypeError or FileNotFoundError:
        label_2['fg'] = 'red'
        label_2['text'] = "-file doesn't choose-"
        flag_2 = 0
    check_btn_compare()


def check_btn_compare():
    global flag_1, flag_2
    if flag_1 == 1 and flag_2 == 1:
        btn_3.configure(state=ACTIVE)
    else:
        btn_3.configure(state=DISABLED)


def compare(event):
    global circuit_1, circuit_2
    print (circuit_2)
    if btn_3['state'].find("active") != -1:
        result = cv2.imread('result.jpg')
        cv2.drawContours(result, circuit_2, 0, (0, 255, 0), 10)
        cv2.imshow('result', result)
        cv2.waitKey(0)
        photo = PhotoImage(file="result.jpg")
        photo.pack()


def handler(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.GaussianBlur(gray, (9, 9), 1)
    edged = cv2.Canny(gray_blur, 20, 30)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (250, 250))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    circuit = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[1]

    # поиск самого большого контура
    circuit_max = len(circuit[0])
    circuit_max_id = 0
    for i in range(len(circuit)):
        if circuit_max < len(circuit[i]):
            circuit_max = len(circuit[i])
            circuit_max_id = i

    # поиск минимальной координаты dx и dy для перемещения контура самого большого контура
    minimX = circuit[len(circuit) - 1][0][0][0]
    minimY = circuit[len(circuit) - 1][0][0][1]
    for i in range(len(circuit[circuit_max_id])):
        if minimX > circuit[circuit_max_id][i][0][0]:
            minimX = circuit[circuit_max_id][i][0][0]
        if minimY > circuit[circuit_max_id][i][0][1]:
            minimY = circuit[circuit_max_id][i][0][1]

    # перемещение контура к x=0 и y=0
    for i in range(len(circuit[circuit_max_id])):
        circuit[circuit_max_id][i][0][0] -= minimX
        circuit[circuit_max_id][i][0][1] -= minimY

    # поиск максимума X и Y для определения размера окна
    maximX = circuit[circuit_max_id][0][0][0]
    maximY = circuit[circuit_max_id][0][0][1]
    for i in range(len(circuit[len(circuit) - 1])):
        if maximX < circuit[circuit_max_id][i][0][0]:
            maximX = circuit[circuit_max_id][i][0][0]
        if maximY < circuit[circuit_max_id][i][0][1]:
            maximY = circuit[circuit_max_id][i][0][1]

    return circuit_max, maximX, maximY


flag_1 = 0
flag_2 = 0
circuit_1, circuit_2 = 0, 0
maximX_1, maximX_2, maximY_1, maximY_2 = 0, 0, 0, 0
root = Tk()
root.title("Compare details")

btn_1 = Button(root, text="First file", width=10, font=('Ubuntu', 15))
btn_1.grid(row=0, column=0, sticky="w")
btn_1.bind('<Button-1>', open_first_file)

label_1 = Label(root, width=20, text="-file doesn't choose-", font=('Ubuntu', 15))
label_1.grid(row=0, column=1)

btn_2 = Button(root, text="Second file", width=10, font=('Ubuntu', 15))
btn_2.grid(row=1, column=0, sticky="w")
btn_2.bind('<Button-1>', open_second_file)

label_2 = Label(root, width=20, text="-file doesn't choose-", font=('Ubuntu', 15))
label_2.grid(row=1, column=1)

btn_3 = Button(root, text="Compare", width=10, font=('Ubuntu', 15))
btn_3.grid(row=2, column=0, sticky="w")
btn_3.bind('<Button-1>', compare)

label_3 = Label(root, width=20, font=('Ubuntu', 15))
label_3.grid(row=2, column=1)

check_btn_compare()

root.mainloop()