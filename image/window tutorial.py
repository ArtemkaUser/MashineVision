from tkinter import *
from datetime import datetime
from tkinter.filedialog import *


root =Tk()

c1 = Canvas(root, width=500, height=580, cursor='tcross', bg='white')
c1.pack()

c1.create_line(250, 0, 250, 500, width=1, fill='red', arrow=LAST)
'''
def open_file():
    of = askopenfilename()
    file=open(of,'r')
    txt.insert(END, file.read())
    file.close()
def save_file():
    sf = asksaveasfilename()
    final_text = txt.get(1.0, END)
    file = open(sf, 'w')
    file.write(final_text)
    file.close()

def exit_up():
    root.quit()

main_menu = Menu(root)
root.configure(menu=main_menu)

first_item = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='File', menu=first_item)

first_item.add_command(label='Open', command=open_file)
first_item.add_command(label='Save', command=save_file)
first_item.add_command(label='Exit', command=exit_up)

txt = Text(root, width=40, height=15, font=12)
txt.pack(expand=YES, fill=BOTH)


def new_win():
    win = Toplevel(root)
    label1 = Label(win, text='Текст в окне верхнего уровня', font=20)
    label1.pack()

def exit_app():
    root.destroy()

main_menu = Menu(root)
root.configure(menu=main_menu)

first_item = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='File', menu=first_item)
first_item.add_command(label='New', command=new_win)
first_item.add_command(label='Exit', command=exit_app)

second_item = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='Edit', menu=second_item)
second_item.add_command(label='Item1')
second_item.add_command(label='Item2')
second_item.add_command(label='Item3')
second_item.add_separator()
second_item.add_command(label='Item4')

tool_bar = Frame(root, bg='#A1A1A1')
tool_bar.pack(side=TOP, fill=X)

btn1 = Button(tool_bar, text="Cut")
btn1.grid(row=0, column=0, padx=2, pady=2)

btn2 = Button(tool_bar, text="Copy")
btn2.grid(row=0, column=1, padx=2, pady=2)

btn3 = Button(tool_bar, text="Past")
btn3.grid(row=0, column=2, padx=2, pady=2)

status_bar = Label(root, relief=SUNKEN, anchor=W, text='mission complete.')
status_bar.pack(side=BOTTOM, fill=X)

class Question:

    def __init__(self, main):

        self.entry1 = Entry(main, width=3, font=15)
        self.button1 = Button(main, text="Проверить")
        self.label1 = Label(main, width=27, font=15)

        self.entry1.grid(row=0,column=0)
        self.button1.grid(row=0, column=1)
        self.label1.grid(row=0, column=2)

        self.button1.bind('<Button-1>', self.answer)

    def answer(self, event):

        txt = self.entry1.get()

        try:
            if int(txt) < 18:
                self.label1["text"] = "Вам сюда рано."
            else:
                self.label1["text"] = 'Добро пожаловать!'
        except ValueError:
            self.label1["text"] = "Введите корректный возраст!"



root.title('Сколько вам лет?')

q = Question(root)


temp = 0
after_id = ''

def tick():
    global temp, after_id
    after_id = root.after(1000, tick)
    f_temp = datetime.fromtimestamp(temp).strftime("%M:%S")
    label_1.configure(text=str(f_temp))
    temp += 1


def start_sw():
    btn_1.grid_forget()
    btn_2.grid(row=1, columnspan=2, sticky='ew')
    tick()

def stop_sw():
    btn_2.grid_forget()
    btn_3.grid(row=1, column=0, sticky='ew')
    btn_4.grid(row=1, column=1, sticky='ew')
    root.after_cancel(after_id)

def continue_sw():
    btn_3.grid_forget()
    btn_4.grid_forget()
    btn_2.grid(row=1, columnspan=2, sticky='ew')
    tick()
def reset_sw():
    btn_3.grid_forget()
    btn_4.grid_forget()
    global temp
    temp = 0
    label_1.configure(text='00:00')
    btn_1.grid(row=1, columnspan=2, sticky='ew')

root.title("Stopwatch")

label_1 = Label(root, width=5, font=("Ubuntu", 100), text="00:00")
label_1.grid(row=0, columnspan=2)

btn_1 = Button(root, text="Start", font=('Ubuntu', 30), command=start_sw)
btn_2 = Button(root, text="Stop", font=('Ubuntu', 30), command=stop_sw)
btn_3 = Button(root, text="Continue", font=('Ubuntu', 30), command=continue_sw)
btn_4 = Button(root, text="Reset", font=('Ubuntu', 30), command=reset_sw)

btn_1.grid(row=1, columnspan=2, sticky='ew')

def print_su(event):
    label_1.configure(text='Shift up')

def print_cd(event):
    label_1.configure(text='Control down')

def print_char(event):
    label_1.configure(text=event.char)


#Описание виджета текста
label_1 = Label(root, width=12, font=('Ubuntu', 100))
label_1.pack()

for i in range(65,123):
    root.bind(chr(i), print_char)

#Команда для связки клавиш
    #Shift+Up
root.bind('<Shift-Up>', print_su)
    #Control+Down
root.bind('<Control-Down>', print_cd)


#Функция для события для левой кнопки мыши
def left_click(event):
    frame_1.configure(bg='red')
    frame_2.configure(bg='white')
    frame_3.configure(bg='white')

#Функция для события для средней кнопки мыши
def middle_click(event):
    frame_1.configure(bg='white')
    frame_2.configure(bg='red')
    frame_3.configure(bg='white')

#Функция для события для правой кнопки мыши
def right_click(event):
    frame_1.configure(bg='white')
    frame_2.configure(bg='white')
    frame_3.configure(bg='red')

#изменить окрас фона
root.configure(bg='black')

#разметка фреймов для текста
frame_1 = Frame(root, width=250, heigh=250, bg='white')
frame_2 = Frame(root, width=250, heigh=250, bg='white')
frame_3 = Frame(root, width=250, heigh=250, bg='white')

#разметка таблицы для фреймов
frame_1.grid(row=0, column=0)
frame_2.grid(row=0, column=1, padx=1)
frame_3.grid(row=0, column=2)

#события для клавишей мыши
root.bind('<Button-1>', left_click)
root.bind('<Button-2>', middle_click)
root.bind('<Button-3>', right_click)

#Функция проверки возраста
def output(event):
    txt = entry_1.get()
    try:
        if int(txt) < 18:
            label_1['text'] = 'Вам еще рано сюда!'
        else:
            label_1['text'] = 'Добро пожаловать!'
    except ValueError:
        label_1['text'] = 'Введите корректный возраст!'

#Название окна
root.title('Сколько вам лет?')

#Разметка под начинку
#поле ввода
entry_1 = Entry(root, width=3, font=15)
#кнопка
button1 = Button(root, text='Проверить')
#текстовый виджет
label_1 = Label(root, width=27, font=15)

#Разметка таблицы для начинки
entry_1.grid(row=0, column=0)
button1.grid(row=0, column=1)
label_1.grid(row=0, column=2)

#Событие при нажатии правой клавишей мыши на кнопку
button1.bind('<Button-1>', output)

label_1 = Label(root, text='Имя')
label_2 = Label(root, text='Пароль')

entry_1 = Entry(root)
entry_2 = Entry(root)

label_1.grid(row=0, column=0, sticky=E)
label_2.grid(row=1, column=0)

entry_1.grid(row=0, column=1)
entry_2.grid(row=1, column=1)

#галочка с подписью
c = Checkbutton(root, text='Остаться в системе')
c.grid(columnspan=2)
'''
'''
#текстовый виджет
the_lable = Label(root, text='ВИДЖЕТ! АХУЕТЬ!')
the_lable.pack()

#Тексотовое поле
one = Label(root, text="Е", bg='red', fg='black')
one.pack()

two = Label(root, text="Б", bg='blue', fg='white')
two.pack(fill=X)

three = Label(root, text="A", bg='white', fg='red')
three.pack(side=LEFT, fill=Y)

#Контейнер разбиения окна: верхняя область по умолчанию
top_frame = Frame(root)
top_frame.pack()

#Контейнер разбиение окна: нижняя область
buttom_frame = Frame(root)
buttom_frame.pack(side=BOTTOM)

#Кнопка
button1 = Button(top_frame, text='ЕБАТЬ! КНОПКА', fg='red')
button1.pack(side=LEFT)
button2 = Button(top_frame, text='ЕБАТЬ! КНОПКА_1', fg='pink')
button2.pack(side=LEFT)
button3 = Button(top_frame, text='ЕБАТЬ! КНОПКА_2', fg='blue')
button3.pack(side=LEFT)
button4 = Button(buttom_frame, text='ЕБАТЬ! КНОПКА_3', fg='yellow')
button4.pack(side=BOTTOM)
'''
#Зацикливаем приложение
root.mainloop()