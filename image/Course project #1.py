import PIL.Image
import PIL.ImageTk
import cv2
import numpy as np
from tkinter.filedialog import *
from math import sqrt

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
    global dev_x, dev_y, max_dev_x, max_dev_y, pixels_1, pixels_2, maximX_1, maximY_1, maximX_2, maximY_2, label_1, label_2, label_3, circuit_1, circuit_2
    if btn_3['state'].find("active") != -1:
        max_x = max(maximX_1, maximX_2)
        max_y = max(maximY_1, maximY_2)
        result = create_np_white_image(max(maximY_1, maximY_2), max(maximX_1, maximX_2), 3)
        a_1, b_1, a_2, b_2, dev_x, dev_y, max_dev_x, max_dev_y = calculate(pixels_1, maximX_1, maximY_1, pixels_2, maximX_2, maximY_2)

        pixel_points_X1 = cv2.findNonZero(cv2.cvtColor(a_1, cv2.COLOR_BGR2GRAY))
        pixel_points_X2 = cv2.findNonZero(cv2.cvtColor(a_2, cv2.COLOR_BGR2GRAY))
        cv2.drawContours(a_1, pixel_points_X1, -1, (0, 255, 0), 5)
        cv2.drawContours(a_1, pixel_points_X2, -1, (255, 0, 0), 5)
        cv2.imwrite('result_X.jpg', a_1)

        pixel_points_Y1 = cv2.findNonZero(cv2.cvtColor(b_1, cv2.COLOR_BGR2GRAY))
        pixel_points_Y2 = cv2.findNonZero(cv2.cvtColor(b_2, cv2.COLOR_BGR2GRAY))
        cv2.drawContours(b_1, pixel_points_Y1, -1, (0, 255, 0), 5)
        cv2.drawContours(b_1, pixel_points_Y2, -1, (255, 0, 0), 5)
        cv2.imwrite('result_Y.jpg', b_1)

        cv2.drawContours(result, circuit_1, -1, (0, 255, 0), 5)
        cv2.drawContours(result, circuit_2, -1, (255, 0, 0), 5)
        cv2.imwrite("result_circuit.jpg", result)
        clear_win()

        image_result = PIL.Image.open("result_circuit.jpg")
        image_result = image_result.resize((int(max_x/5), int(max_y/5)), PIL.Image.ANTIALIAS)
        render_result = PIL.ImageTk.PhotoImage(image_result)

        image_result_x = PIL.Image.open("result_X.jpg")
        image_result_x = image_result_x.resize((int(max_x/5), int(max_y/5)), PIL.Image.ANTIALIAS)
        render_result_x = PIL.ImageTk.PhotoImage(image_result_x)

        image_result_y = PIL.Image.open("result_Y.jpg")
        image_result_y = image_result_y.resize((int(max_x/5), int(max_y/5)), PIL.Image.ANTIALIAS)
        render_result_y = PIL.ImageTk.PhotoImage(image_result_y)

        label_1 = Label(root, image=render_result)
        label_1.image = render_result
        label_1.grid(row=1, column=0)

        label_2 = Label(root, image=render_result_x)
        label_2.image = render_result_x
        label_2.grid(row=0, column=0)

        label_3 = Label(root, image=render_result_y)
        label_3.image = render_result_y
        label_3.grid(row=1, column=1)

        label_4 = Label(root, text="standard deviation X(px):", font=('Ubuntu', 15))
        label_4.grid(row=2, column=0)

        label_5 = Label(root, text=dev_x, font=('Ubuntu', 15))
        label_5.grid(row=2, column=1)

        label_6 = Label(root, text="standard deviation Y(px):", font=('Ubuntu', 15))
        label_6.grid(row=3, column=0)

        label_7 = Label(root, text=dev_y, font=('Ubuntu', 15))
        label_7.grid(row=3, column=1)

        label_8 = Label(root, text="max deviation X(px):", font=('Ubuntu', 15))
        label_8.grid(row=4, column=0)

        label_9 = Label(root, text=max_dev_x, font=('Ubuntu', 15))
        label_9.grid(row=4, column=1)

        label_10 = Label(root, text="max deviation Y(px):", font=('Ubuntu', 15))
        label_10.grid(row=5, column=0)

        label_11 = Label(root, text=max_dev_y, font=('Ubuntu', 15))
        label_11.grid(row=5, column=1)
        ###
        label_12.grid(row=2, column=2)

        label_13.grid(row=2, column=3)

        label_14.grid(row=3, column=2)

        label_15.grid(row=3, column=3)

        label_16.grid(row=4, column=2)

        label_17.grid(row=4, column=3)

        label_18.grid(row=5, column=2)

        label_19.grid(row=5, column=3)

        btn_1 = Button(root, text="Calculate into mm", font=('Ubuntu', 15), bg='green')
        btn_1.grid(row=6, column=0, sticky="w")
        btn_1.bind('<Button-1>', output)

        btn_2 = Button(root, text="Check deviation x", font=('Ubuntu', 15), bg='green')
        btn_2.grid(row=6, column=2, sticky="w")
        btn_2.bind('<Button-1>', check)

        entry_1.grid(row=6, column=1, sticky="w")
        entry_2.grid(row=6, column=3, sticky="w")


def check(event):
    global compare_size
    txt = entry_2.get()
    label_20.grid_forget()
    label_21.grid_forget()

    if float(txt) >= compare_size:
        label_20.grid(row=1, column=3)
    else:
        label_21.grid(row=1, column=3)

def output(event):
    global dev_x, dev_y, max_dev_x, max_dev_y, compare_size
    txt = entry_1.get()
    scale = max(maximX_1, maximX_2)/float(txt)
    a = dev_x/scale
    b = dev_y/scale
    c = max_dev_x/scale
    d = max_dev_y/scale
    compare_size = d
    label_13 = Label(root, text=a, font=('Ubuntu', 15))
    label_13.grid(row=2, column=3)
    label_15 = Label(root, text=b, font=('Ubuntu', 15))
    label_15.grid(row=3, column=3)
    label_17 = Label(root, text=c, font=('Ubuntu', 15))
    label_17.grid(row=4, column=3)
    label_19 = Label(root, text=d, font=('Ubuntu', 15))
    label_19.grid(row=5, column=3)


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
    minim_x = circuit[circuit_max_id][0][0][0]
    minim_y = circuit[circuit_max_id][0][0][1]
    for i in range(len(circuit[circuit_max_id])):
        if minim_x > circuit[circuit_max_id][i][0][0]:
            minim_x = circuit[circuit_max_id][i][0][0]
        if minim_y > circuit[circuit_max_id][i][0][1]:
            minim_y = circuit[circuit_max_id][i][0][1]
    # перемещение контура к x=0 и y=0
    for i in range(len(circuit[circuit_max_id])):
        circuit[circuit_max_id][i][0][0] -= minim_x
        circuit[circuit_max_id][i][0][1] -= minim_y
    maxim_x = circuit[circuit_max_id][0][0][0]
    maxim_y = circuit[circuit_max_id][0][0][1]
    # поиск максимума X и Y для определения размера окна
    for i in range(len(circuit[circuit_max_id])):
        if maxim_x < circuit[circuit_max_id][i][0][0]:
            maxim_x = circuit[circuit_max_id][i][0][0]
        if maxim_y < circuit[circuit_max_id][i][0][1]:
            maxim_y = circuit[circuit_max_id][i][0][1]

    mask = np.zeros(gray.shape, np.uint8)
    cv2.drawContours(mask, circuit, circuit_max_id, 255, -1)
    pixel_points = cv2.findNonZero(mask)

    return circuit[circuit_max_id], maxim_x, maxim_y, pixel_points


def clear_win():
    btn_1.grid_forget()
    btn_2.grid_forget()
    btn_3.grid_forget()
    label_1.grid_forget()
    label_2.grid_forget()
    label_3.grid_forget()


def maximum_number_in_array(array):
    maxim = array[0]
    for i in range(len(array)-1):
        if maxim < array[i]:
            maxim = array[i]
    return maxim


def create_array_skeleton(array, length):
    for i in range(length + 1):
        array.append(0)
    return array


def create_histogram_for_graphics(array_x, array_y, pixels):
    for k in range(len(pixels)-1):
        array_x[pixels[k][0][0]] += 1
        array_y[pixels[k][0][1]] += 1
    return array_x, array_y


def maximum_number_in_two_arrays(array_1, array_2):
    maximum_in_first_array = maximum_number_in_array(array_1)
    maximum_in_second_array = maximum_number_in_array(array_2)
    return max(maximum_in_first_array, maximum_in_second_array)


def create_np_white_image(width, height, number_of_channels):
    a = np.zeros((width + 2, height + 2, number_of_channels), dtype=np.uint8)
    a[::] = (0, 0, 0)
    return a


def deviation(array_1, array_2):
    temp = 0
    average = 0
    deviation = []
    for i in range(len(array_1) - 1):
        deviation.append(array_1[i] - array_2[i])
        average += deviation[i]
    average = average/len(deviation)
    for i in range(len(array_1) - 1):
        temp += pow(deviation[i]-average, 2)
    average_deviation = sqrt(temp / len(deviation))
    return average_deviation


def max_deviation(array_1, array_2):
    deviation = []
    for i in range (len(array_1)-1):
        deviation.append(abs(array_1[i]-array_2[i]))
    return max(deviation)


def calculate(pixels_array_1, max_x_1, max_y_1, pixels_array_2, max_x_2, max_y_2):
    x_1, y_1, x_2, y_2 = [], [], [], []

    # создание каркаса нулевого массива для изображения
    x_1 = create_array_skeleton(x_1, max(max_x_1, max_x_2))
    y_1 = create_array_skeleton(y_1, max(max_y_1, max_y_2))
    x_2 = create_array_skeleton(x_2, max(max_x_1, max_x_2))
    y_2 = create_array_skeleton(y_2, max(max_y_1, max_y_2))

    # создание гистограммы
    x_1, y_1 = create_histogram_for_graphics(x_1, y_1, pixels_array_1)
    x_2, y_2 = create_histogram_for_graphics(x_2, y_2, pixels_array_2)

    # расчет отклонений
    deviation_x = deviation(x_1, x_2)
    deviation_y = deviation(y_1, y_2)
    max_deviation_x = max_deviation(x_1, x_2)
    max_deviation_y = max_deviation(y_1, y_2)

    # поиск максимумов
    m_1 = maximum_number_in_array(x_1)
    m_2 = maximum_number_in_array(x_2)
    m = maximum_number_in_two_arrays(x_1, x_2)
    n = maximum_number_in_two_arrays(y_1, y_2)

    # создание белой картинки
    a_1 = create_np_white_image(m, max(len(x_1), len(x_2)), 3)
    a_2 = create_np_white_image(m, max(len(x_1), len(x_2)), 3)

    b_1 = create_np_white_image(max(len(y_1), len(y_2)), n, 3)
    b_2 = create_np_white_image(max(len(y_1), len(y_2)), n, 3)


    # запись гистограмы в картунку
    for i in range(len(x_1)):
        a_1[m_1-x_1[i], i, 0] = 255
        a_1[m_1-x_1[i], i, 1] = 255
        a_1[m_1-x_1[i], i, 2] = 255
    for i in range(len(x_2)):
        a_2[m_2-x_2[i], i, 0] = 255
        a_2[m_2-x_2[i], i, 1] = 255
        a_2[m_2-x_2[i], i, 2] = 255
    for j in range(len(y_1)-1):
        b_1[j, y_1[j], 0] = 255
        b_1[j, y_1[j], 1] = 255
        b_1[j, y_1[j], 2] = 255
    for j in range(len(y_2)-1):
        b_2[j, y_2[j], 0] = 255
        b_2[j, y_2[j], 1] = 255
        b_2[j, y_2[j], 2] = 255
    return a_1, b_1, a_2, b_2, deviation_x, deviation_y, max_deviation_x, max_deviation_y

dev_x, dev_y, max_dev_x, max_dev_y = 0, 0, 0, 0
flag_1 = 0
flag_2 = 0
circuit_1, circuit_2 = 0, 0
maximX_1, maximX_2, maximY_1, maximY_2 = 0, 0, 0, 0
pixels_1, pixels_2 = 0, 0
compare_size = 0
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

entry_1 = Entry(root, font=15)
entry_2 = Entry(root, font=15)

label_12 = Label(root, text="standard deviation X(mm):", font=('Ubuntu', 15))
label_13 = Label(root, text="           -//-          ", font=('Ubuntu', 15))
label_14 = Label(root, text="standard deviation Y(mm):", font=('Ubuntu', 15))
label_15 = Label(root, text="           -//-          ", font=('Ubuntu', 15))
label_16 = Label(root, text="max deviation X(mm):", font=('Ubuntu', 15))
label_17 = Label(root, text="           -//-          ", font=('Ubuntu', 15))
label_18 = Label(root, text="max deviation Y(mm):", font=('Ubuntu', 15))
label_19 = Label(root, text="           -//-          ", font=('Ubuntu', 15))
label_20 = Label(root, text="GOOD!", font=('Ubuntu', 20), bg='green')
label_21 = Label(root, text="NOPE!", font=('Ubuntu', 20), bg='red')

check_btn_compare()

root.mainloop()
