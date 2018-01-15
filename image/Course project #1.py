import PIL.Image
import PIL.ImageTk
from tkinter import *
import math
import cv2
import numpy as np
from tkinter.filedialog import *
from matplotlib import pyplot as plt

def open_first_file(event):
    global flag_1, circuit_1, maximX_1, maximY_1, pixels_1
    try:
        of = askopenfilename()

        if not of:
            label_1['fg'] = 'red'
            label_1['text'] = "-file doesn't choose-"
            flag_1 = 0
        else:
            file = open(of, 'r')

            if file.name.lower()[-3:].find("jpg") != -1:
                circuit_1, maximX_1, maximY_1,pixels_1 = handler(cv2.imread(file.name))
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
    global flag_2, circuit_2, maximX_2, maximY_2, pixels_2
    try:
        of = askopenfilename()

        if not of:
            label_2['fg'] = 'red'
            label_2['text'] = "-file doesn't choose-"
            flag_2 = 0

        else:
            file = open(of, 'r')
            if file.name.lower()[-3:].find("jpg") != -1:
                circuit_2, maximX_2, maximY_2, pixels_2 = handler(cv2.imread(file.name))
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
    global pixels_1, pixels_2, maximY_1, maximY_2, label_1, label_2, label_3, circuit_1, circuit_2
    if btn_3['state'].find("active") != -1:
        max_X, max_Y = compare_size(maximX_1, maximX_2, maximY_1, maximY_2)
        result = np.zeros((max_Y, max_X, 3), np.uint8)
        result[::] = (255, 255, 255)

        a_1, b_1 = calculate(pixels_1, max_X, max_Y)
        a_2, b_2 = calculate(pixels_2, max_X, max_Y)

        cv2.imwrite('result_a1.jpg', a_1)
        cv2.imwrite('result_b1.jpg', b_1)
        cv2.imwrite('result_a2.jpg', a_2)
        cv2.imwrite('result_b2.jpg', b_2)
        cv2.drawContours(result, circuit_1, -1, (0, 255, 0), 10)
        cv2.drawContours(result, circuit_2, -1, (255, 0, 0), 10)
        cv2.imwrite("result_1.jpg", result)
        clear_win()

        image = PIL.Image.open("result_1.jpg")
        image = image.resize((int(max_X/4), int(max_Y/4)), PIL.Image.ANTIALIAS)
        render = PIL.ImageTk.PhotoImage(image)
        root.geometry("1020x620")
        label_2 = Label(root, image=render)
        label_2.image = render
        label_2.grid(row=1, column=1)





def handler(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.GaussianBlur(gray, (9, 9), 1)
    edged = cv2.Canny(gray_blur, 15, 30)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    circuit = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[1]

    # поиск самого большого контура
    circuit_max = len(circuit[0])
    circuit_max_id = 0
    for i in range(len(circuit)):
        if circuit_max < len(circuit[i]):
            circuit_max = len(circuit[i])
            circuit_max_id = i
    # поиск минимальной координаты dx и dy для перемещения контура
    minimX = circuit[circuit_max_id][0][0][0]
    minimY = circuit[circuit_max_id][0][0][1]
    for i in range(len(circuit[circuit_max_id])):
        if minimX > circuit[circuit_max_id][i][0][0]:
            minimX = circuit[circuit_max_id][i][0][0]
        if minimY > circuit[circuit_max_id][i][0][1]:
            minimY = circuit[circuit_max_id][i][0][1]
    # перемещение контура к x=0 и y=0
    for i in range(len(circuit[circuit_max_id])):
        circuit[circuit_max_id][i][0][0] -= minimX
        circuit[circuit_max_id][i][0][1] -= minimY
    maximX = circuit[circuit_max_id][0][0][0]
    maximY = circuit[circuit_max_id][0][0][1]
    # поиск максимума X и Y для определения размера окна
    for i in range(len(circuit[circuit_max_id])):
        if maximX < circuit[circuit_max_id][i][0][0]:
            maximX = circuit[circuit_max_id][i][0][0]
        if maximY < circuit[circuit_max_id][i][0][1]:
            maximY = circuit[circuit_max_id][i][0][1]

    mask = np.zeros(gray.shape, np.uint8)
    cv2.drawContours(mask, circuit, circuit_max_id, 255, -1)
    pixelpoints = cv2.findNonZero(mask)

    return circuit[circuit_max_id], maximX, maximY, pixelpoints


def clear_win():
    #root.forget()
    btn_1.grid_forget()
    btn_2.grid_forget()
    btn_3.grid_forget()
    label_1.grid_forget()
    label_2.grid_forget()
    label_3.grid_forget()


def compare_size(max_X1, max_X2, max_Y1, max_Y2):
    max_X = max(max_X1, max_X2)
    max_Y = max(max_Y1, max_Y2)

    return max_X, max_Y


def calculate(pixels, maxX, maxY):
    x = []
    y = []
    for i in range(maxX+1):
        x.append(0)
    for j in range(maxY+1):
        y.append(0)
    for k in range(len(pixels)-1):
        x[pixels[k][0][0]] += 1
        y[pixels[k][0][1]] += 1
    m = x[0]
    n = y[0]
    for i in range(len(x)-1):
        if m < x[i]:
            m = x[i]
    for j in range(len(y)-1):
        if n < y[j]:
            n = y[j]
    a = np.zeros((m+2, len(x)+2, 3), dtype=np.uint8)
    a[::] = (255, 255, 255)
    for i in range(len(x)):
        a[m-x[i], i, 0] = 0
        a[m-x[i], i, 1] = 0
        a[m-x[i], i, 2] = 0
    b = np.zeros((len(y)+2, n+2,  3), dtype=np.uint8)
    b[::] = (255, 255, 255)
    for j in range(len(y)-1):
        b[j, y[j], 0] = 0
        b[j, y[j], 1] = 0
        b[j, y[j], 2] = 0
    return a, b


flag_1 = 0
flag_2 = 0
circuit_1, circuit_2 = 0, 0
maximX_1, maximX_2, maximY_1, maximY_2 = 0, 0, 0, 0
pixels_1, pixels_2 = 0, 0
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