import serial
import os
import datetime
import random
import threading
import time
from tkinter import PhotoImage
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

ser = serial.Serial('COM5', 9600)
t = open('temp.data', 'a+')
f = open('freq.data', 'a+')
login_db = {"1": "1"}

def graph():
    global dfl
    dfl = False
    temperature_data = []
    sound_data = []
    time_data = []
    fig, (ax1, ax2) = plt.subplots(2, 1)
    line1, = ax1.plot(time_data, temperature_data, label='Temperature')
    line2, = ax2.plot(time_data, sound_data, label='Sound Level')

    ax1.set_xlabel('Time')
    ax1.set_ylabel('Temperature')
    ax1.set_title('Temperature vs. Time')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Sound Level')
    ax2.set_title('Sound Level vs. Time')

    def update_plots(frame):
        now = datetime.datetime.now()
        time_data.append(now)
        line = ser.readline().decode().strip()
        print(line)
        data = line.split(',')

        if len(data) == 2:
            temperature, sound_level = data
            try:
                temperature = float(temperature)
                sound_level = float(sound_level)
                temperature_data.append(temperature)
                sound_data.append(sound_level)
                line1.set_data(time_data, temperature_data)
                line2.set_data(time_data, sound_data)
            except ValueError:
                print("Invalid data format:", data)


    ax1.relim()
    ax1.autoscale_view()
    ax2.relim()
    ax2.autoscale_view()

    ani = FuncAnimation(fig, update_plots, interval=1000, cache_frame_data=False)

    # Start the animation
    plt.show()
    ser.close()

def ot(output_window):
    stop_flag = threading.Event()
    sno = 1
    def stop():
        global dfl
        stop_flag.set()
        dfl = True
        t = open('temp.data', 'a+')
        f = open('freq.data', 'a+')
        print("Stopped")
        t.write("Stopped")
        f.write("Stopped")

    stop_button = Button(output_window, text="Stop", font=("Arial 23 bold"), command=stop, bg="purple")
    stop_button.pack()

    output_text = Text(output_window, wrap="none")
    output_text.pack(fill="both", expand=True)

    scrollbar = Scrollbar(output_window, command=output_text.yview)
    scrollbar.pack(side="right", fill="y")
    output_text.config(yscrollcommand=scrollbar.set)

    try:
        while not stop_flag.is_set():
            t = open('temp.data', 'a+')
            f = open('freq.data', 'a+')
            now = datetime.datetime.now()
            s = (str(now.year) + '/' + str(now.month) + '/' + str(now.day) + '    ')
            t.write(s)
            f.write(s)
            line = ser.readline().decode().strip()

            print(line)
            data = line.split(',')
            if len(data) == 2:
                temperature, sound_level = data
                freq = float(round(10 ** (float(sound_level) / 10)))
                t.write(str(now.hour) + 'hrs' + ' ' + str(now.minute) + 'min' + ' ' + str(now.second) + 'sec' + "  " + temperature + '\n')
                f.write(str(now.hour) + 'hrs' + ' ' + str(now.minute) + 'min' + ' ' + str(now.second) + 'sec' + "  " + sound_level + "  " + "frequency(Hz)" + str(freq) + '\n')
                message = str(sno) + '. ' + str(now.hour) + 'hrs' + ' ' + str(now.minute) + 'min' + ' ' + str(now.second) + 'sec' + "  temp c" +temperature + "       sound.lvl dB" +sound_level + "      frequency:" + str(freq)
                sno += 1 
                update_output(output_text, message)
                output_window.update()
                time.sleep(1)
            
    except Exception:
        print("Stopped")
        t.write("Stopped")
        f.write("Stopped")
    finally:
        t.close()
        f.close()
        ser.close()

def update_output(text_widget, message):
    text_widget.insert("end", message + "\n")
    text_widget.see("end")

def notice():
    output_window = Toplevel()
    output_window.title("Output Window")

    threading.Thread(target=ot, args=(output_window,)).start()

def clear():
    userentry.delete(0, END)
    passentry.delete(0, END)

def a():
    notice()
    #graph()

def b():
    os.startfile("temp.data")

def c():
    os.startfile("freq.data")

def check1():
    u_name = user_name.get()
    pass_word = password.get()
    print(login_db)
    data = login_db.get(u_name)
    if data == pass_word:
        messagebox.showinfo(title='Hello', message="Welcome your login....success")

        win = Tk()
        filemenu = Frame(win)
        win.geometry('1000x1000')
        win.title('MENU')
        scrollbar = Scrollbar(filemenu, orient=VERTICAL, width=15)
        scrollbar.place()
        scrollbar.pack(side=RIGHT, fill=Y)
        win.configure(bg='purple')
        scrollbar.configure()
        scrollbar.set(100, 500)

        b1 = Button(filemenu, text='Run', width=20, height=1, padx=5, pady=5, bg='black', command=a, activebackground='white',font=('Helvetica', 25, 'bold'), fg='purple', bd=0)
        b2 = Button(filemenu, text='Rs from\n Temperature sensor', width=20, height=2, padx=5, pady=5, bg='black',command=b, activebackground='white', font=('Helvetica', 25, 'bold'), fg='purple', bd=0)
        b3 = Button(filemenu, text='Rs from\n Sound sensor', width=20, height=2, padx=5, pady=5, bg='black', command=c,activebackground='white', font=('Helvetica', 25, 'bold'), fg='purple', bd=0)

        b1.pack(padx=2, pady=2)
        b2.pack(pady=2)
        b3.pack(pady=2)
        filemenu.pack()
        win.mainloop()

    else:
        messagebox.showinfo(title='hello', message="sorry, username and \npassword is incorrect")

def check():
    def step():
        for i in range(1):
            win.update_idletasks()
            pb['value'] += 100
            time.sleep(1)
            txt['text'] = pb['value'], '%'

    pb = Progressbar(win, orient=HORIZONTAL, length=200, mode='determinate')

    pb.place(x=200, y=340)

    txt = Label(
        win,
        text='0%',
        bg='#000',
        fg='#fff'
    )

    txt.place(x=400, y=340)
    step()
    check1()

win = Tk()
win.title("Stress Monitor")
win.maxsize(width=3000, height=1000)
win.minsize(width=1000, height=1000)

bg_image = PhotoImage(file="pic3.png")
x = Label(win, image=bg_image)
x.place(x=0, y=0)
heading1 = Label(win, text=' STRESS MONITOR', font=('TimesNewRoman', 20), fg="purple", bg="black")
heading1.place(x=300, y=10)
heading = Label(win, text="Login", font='Verdana 25 bold')
heading.place(x=80, y=150)
username = Label(win, text="User Name:", font='Verdana 10 bold')
username.place(x=80, y=220)
userpass = Label(win, text="Password:", font='Verdana 10 bold')
userpass.place(x=80, y=260)
heading = Label(win, text="Show password", font='Verdana 10 bold')
heading.place(x=480, y=260)

user_name = StringVar()
password = StringVar()
userentry = Entry(win, width=40, textvariable=user_name)
userentry.focus()
userentry.place(x=200, y=223)
passentry = Entry(win, width=40, show="*", textvariable=password)
passentry.place(x=200, y=260)

def mark():
    if var.get() == 1:
        passentry.configure(show="")
    elif var.get() == 0:
        passentry.configure(show="*")

var = IntVar()
bt = Checkbutton(win, command=mark, offvalue=0, onvalue=1)
bt.place(x=450, y=260)
btn_login = Button(win, text="login", font='Verdana 10 bold', command=check)
btn_login.place(x=210, y=290)
btn_login = Button(win, text="Clear", font='Verdana 10 bold', command=clear)
btn_login.place(x=260, y=290)

win.mainloop()
