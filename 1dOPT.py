import numpy as np
import sympy as sp
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt 

xValueForDupe = []
yValueForDupe = []

def drawFuncGraph():
    try:
        if not var_func.get() or not var_interval.get() or not var_step.get():
            raise ValueError("Поля функции, интервала и шага должны быть заполнены!")

        ax.clear()
        xValueForDupe.clear()
        yValueForDupe.clear()
        function = var_func.get()
        f = sp.sympify(function)
        intervals = var_interval.get().split(", ")

        intervals[0] = float(intervals[0].strip())
        intervals[1] = float(intervals[1].strip())
        step = float(var_step.get())

        progressBar.configure(maximum=intervals[1] - step, value=0)
        for _ in np.arange(intervals[0], intervals[1], step):
            progressBar.step(step)
            root.update()
            xValueForDupe.append(_)
            yValueForDupe.append(f.subs(x, _))
            print(f"{_} - X:{_}, Y:{f.subs(x, _)}")

        xValueForGraph = xValueForDupe
        yValueForGraph = yValueForDupe

        ax.plot(xValueForGraph, yValueForGraph)
        canvas.draw()
    except ValueError as e:
        messagebox.showerror("Некоторые поля заполнены некорректно!", str(e))
    except SyntaxError:
        messagebox.showerror("Синтаксическая ошибка!")
    except Exception as e:
        messagebox.showerror("Ошибка!", str(e))


def calcFunc():
    try:
        if not var_func.get() or not var_interval.get() or not var_step.get() or not var_X0.get() or not var_iter.get():
            raise ValueError("Поля функции и интервала должны быть заполнены!")
        
        x0 = float(X0Entry.get())
        iterAmount = int(iterEntry.get())
        intervals = var_interval.get().split(", ")
        intervals[0] = float(intervals[0].strip())
        intervals[1] = float(intervals[1].strip())
        if ((x0 < intervals[0]) or (x0 > intervals[1])):
            messagebox.showwarning("Неверное начальное приближение!", "Измените значение X0!")
            return

        ax.cla()
        ax.plot(xValueForDupe, yValueForDupe)
        canvas.draw()

        function = var_func.get()
        f = sp.sympify(function)

        f_firstDeriv = sp.diff(f, x)
        f_fD_at_x0_value = f_firstDeriv.subs(x, x0)

        f_secondDeriv = sp.diff(f_firstDeriv, x)
        f_sD_at_x0_value = f_secondDeriv.subs(x, x0)

        xNewArray = []
        yValAtXNew = []
        xNewArray.append(x0)
        yValAtXNew.append(f.subs(x, x0))
        print(f"\t\t|    X0      |     f(x)    |    f`(x)    |    f``(x)  ")
        print(f"\tITER 1 | {x0:.9f} | {f.subs(x,x0):.9f} | {f_fD_at_x0_value:.9f} | {f_sD_at_x0_value:.9f}")

        for _ in range(iterAmount):
            f_fD_at_x0_value = f_firstDeriv.subs(x, x0)
            f_sD_at_x0_value = f_secondDeriv.subs(x, x0)
            x0 = float(x0 - (f_fD_at_x0_value / f_sD_at_x0_value))
            if abs(f_fD_at_x0_value) < 1e-10:
                break
            if x0 < intervals[0]:
                print(f"\t\tITER {_ + 2} - [ ! ] X is lower than {intervals[0]} - {x0}")
                x0 = intervals[0]
                print(f"\t\tX0 = {x0}")
            elif x0 > intervals[1]:
                print(f"\t\tITER {_ + 2} - [ ! ] X is higher than {intervals[1]} - {x0}")
                x0 = intervals[1]
                print(f"\t\tX0 = {x0}")

            xNewArray.append(x0)
            yValAtXNew.append(f.subs(x, x0))
            print(f"\tITER {_ + 2} | {x0:.9f} | {f.subs(x,x0):.9f} | {f_fD_at_x0_value:.9f} | {f_sD_at_x0_value:.9f}")

        print(f"\nxNewArray - {len(xNewArray)} - {xNewArray}")
        print(f"\nyValAtXNew - {len(yValAtXNew)} - {yValAtXNew}")
        for i in range(len(xNewArray)):
            ax.scatter(xNewArray[i], yValAtXNew[i])
            ax.annotate(f'Point {i+1}', (xNewArray[i], yValAtXNew[i]))
        canvas.draw()

        
        var_result.set(x0)

        print("  ______      ____  ___  ______")
        print(" <  / _ \____/ __ \/ _ \/_  __/")
        print(" / / // /___/ /_/ / ___/ / /   ")
        print("/_/____/    \____/_/    /_/    ")
        print("                               ")

    except ValueError as e:
        messagebox.showerror("Некоторые поля заполнены некорректно!", str(e))
    except SyntaxError:
        messagebox.showerror("Синтаксическая ошибка!")
    except Exception as e:
        messagebox.showerror("Ошибка!", str(e))

# Инициализация Tkinter
root = tk.Tk()
root.title("1D-Optimization")
root.geometry("1020x550")
root.minsize(1020, 550)
root.maxsize(1020, 550)
#photo = tk.PhotoImage(file = 'icon.ico')
#root.wm_iconphoto(False, photo)

# Заголовок
mainLabel = tk.Label(root, text = "1D-Optimization. Newton's method")
mainLabel.config(font=("Arial", 16))
mainLabel.pack()

####################################

entryFrame = tk.Frame(borderwidth=1,  relief="solid", padx=6, pady=8)
entryFrame.place(x=20,y=35)

# Переменные для хранения введённых данных
var_func = tk.StringVar()
var_interval = tk.StringVar()
var_X0 = tk.StringVar()
var_iter = tk.StringVar()
var_step = tk.StringVar()
var_result = tk.StringVar()

# Надписи для текстовых полей и сами текстовые поля
label1 = tk.Label(entryFrame, text="f = ")
funcEntry = tk.Entry(entryFrame, textvariable=var_func)
label2 = tk.Label(entryFrame, text="Интервал = ")
intervalEntry = tk.Entry(entryFrame, textvariable=var_interval)
label3 = tk.Label(entryFrame, text="Шаг = ")
stepEntry = tk.Entry(entryFrame, textvariable=var_step)
label4 = tk.Label(entryFrame, text="X0 =")
X0Entry = tk.Entry(entryFrame, textvariable=var_X0)
label5 = tk.Label(entryFrame, text="Итерации =")
iterEntry = tk.Entry(entryFrame, textvariable=var_iter)
label6 = tk.Label(entryFrame, text="Result: ")
label7 = tk.Label(entryFrame, textvariable=var_result)

label1.grid(row=0, column=0, padx=2, pady=2)
funcEntry.grid(row=0, column=1, padx=2, pady=2)
label2.grid(row=1, column=0, padx=2, pady=2)
intervalEntry.grid(row=1, column=1, padx=2, pady=2)

label3.grid(row=2, column=0, padx=2, pady=2)
stepEntry.grid(row=2, column=1, padx=2, pady=2)

label4.grid(row=3, column=0, padx=2, pady=2)
X0Entry.grid(row=3, column=1, padx=2, pady=2)
label5.grid(row=4, column=0, padx=2, pady=2)
iterEntry.grid(row=4, column=1, padx=2, pady=2)

label6.grid(row=5, column=0, padx=2, pady=2)
label7.grid(row=5, column=1, padx=2, pady=2)

progressBar = ttk.Progressbar(root, mode="determinate")
progressBar.place(x=20, y=210, width=220)

####################################

buttonFrame = tk.Frame(borderwidth=1, relief="solid", padx=6, pady=8)
buttonFrame.place(x=255, y=35)

btn_Draw = tk.Button(buttonFrame, text="DRAW", command=drawFuncGraph, pady=2)
btn_Calc = tk.Button(buttonFrame, text="CALC", command=calcFunc, pady=2)

btn_Draw.grid(row=0, column=0, pady=8)
btn_Calc.grid(row=1, column=0, pady=8)

####################################

exitFrame = tk.Frame(borderwidth=1, relief="solid", padx=6, pady=8)
exitFrame.place(x=10, y=476)

btn_Exit = tk.Button(exitFrame, text="Exit", command=root.quit, width=41, height=2)
btn_Exit.pack()

####################################
x = sp.symbols('x')
graphFrame = tk.Frame(borderwidth=1, relief="solid", padx=6, pady=8)
graphFrame.place(x=330, y=35)

figure, ax = plt.subplots()

canvas = FigureCanvasTkAgg(figure, graphFrame)
toolbar = NavigationToolbar2Tk(canvas, graphFrame)
toolbar.update()

canvas.get_tk_widget().config(width=665, height=440)
canvas.get_tk_widget().pack()

root.mainloop()
