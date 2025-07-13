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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

td = []
sd = []
fd = []
tid = []
hid=[]

ser = serial.Serial('COM5', 9600)
t = open('temp.data', 'a+')
f = open('freq.data', 'a+')
login_db = {"1": "1","22BCE9319":"Sw7bNSyJ","22BCE9102":"gzM5b4FS","22BCE8341":"LLa9epZm","22BCE9351":"82ZvdaX6","22BCE8525":"uK5d6AzP","22BCE7517":"f4x2YVfv"}
def Amessage(title,msg):
    messagebox.showinfo(title,msg)
def close_message_box():
    messagebox._show(title='', message='')
def minwin(root):
    root.iconify()
def graph():
    global dfl
    global td,sd,tid,fd
    dfl = False
    fig, (ax1, ax2,ax3) = plt.subplots(1,3)
    current_datetime = datetime.datetime.now()
    filename = "temp_sound"+current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    custom_figure_name = filename
    ax1.plot(tid, td,marker='o')
    ax1.set_xlabel("Time (sec) →")
    ax1.set_ylabel("Temperature C° →")
    ax1.set_title("Temperature vs. Time")
    ax2.plot(tid, sd,marker='o')
    ax2.set_xlabel("Time (sec) →")
    ax2.set_ylabel("Sound Level db →")
    ax2.set_title("Sound Level vs. Time")
    ax3.plot(fd,tid,marker='*')
    ax3.set_xlabel("Time (sec) →")
    ax3.set_ylabel("Frequency Hz →")
    ax3.set_title("Frequency vs. Time")
    plt.suptitle("Sensor Data V/S Time")
    plt.show()
    td=[]
    sd=[]
    tid=[]
    fd=[]
    hid=[]
    
output_window = None
def ot(output_window,output_text):
    stop_flag = threading.Event()
    sno = 1
    def stop():
        global dfl
        stop_flag.set()
        dfl = True
        t = open('temp.data', 'a+')
        f = open('freq.data', 'a+')
        print("Stopped")
        t.write("Stopped\n")
        f.write("Stopped\n")
        try:
            lt=tid[-1]
            hdf=hid[0]
            hdl=hid[-1] 
            mesg="DATA:  \n Start: "+hdf+" Stopped: "+hdl+" \n Total time noted: "+str(lt)+ "seconds"
            Amessage("Note", mesg)
            output_window.after(15000, close_message_box)
        except Exception:
            messagebox.showerror("Exception found",str(Exception))
            pass
        graph()
    
    stop_button = Button(output_window, text="Stop and\n Show Graphs", font=("Arial 23 bold"), command=stop, bg="purple")
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
            s = (str(now.day) + '/' + str(now.month) + '/' + str(now.year) + '    ')
            t.write(s)
            f.write(s)
            line = ser.readline().decode().strip()
            print(line)
            data = line.split(',')
            if len(data) == 2:
                temperature, sound_level = data
                #if float(temperature)== -127.00:
                 #   Amessage("Alert!","Please check your temp. sensor connection.")
                  #  output_window.close()
                if float(temperature)<=10 or float(temperature)>=35:
                    t.write("Next value is found above range!!!")
                td.append(float(temperature))
                sd.append(float(sound_level))
                freq = float(round(10 ** (round(float(sound_level)) / 10)))
                fd.append(float(freq))
                hd=str(now.hour) + 'hrs' + ' ' + str(now.minute) + 'min' + ' ' + str(now.second) + 'sec' + "  "
                hid.append(hd)
                t.write(hd + temperature + '\n')
                f.write(str(now.hour) + 'hrs' + ' ' + str(now.minute) + 'min' + ' ' + str(now.second) + 'sec' + "  " + sound_level + "  " + "frequency(Hz)" + str(freq) + '\n')
                message = str(sno) + '. ' + str(now.hour) + 'hrs' + ' ' + str(now.minute) + 'min' + ' ' + str(now.second) + 'sec' + "  temp (C°) " + temperature + "       sound.lvl dB" + sound_level + "      frequency:" + str(freq)
                tid.append(sno-1) 
                sno += 1
                update_output(output_text, message)
                output_window.update()
                time.sleep(1)

    except Exception:
        print("Stopped")
        t.write("\nStopped\n")
        f.write("\nStopped\n")
    finally:
        t.close()
        f.close()

def update_output(text_widget, message):
    text_widget.insert("end", message + "\n")
    text_widget.see("end")

def notice():
    output_window = Toplevel()
    output_window.title("Output Window")

    output_text = Text(output_window, wrap="none")
    output_text.pack(fill="both", expand=True)

    scrollbar = Scrollbar(output_window, command=output_text.yview)
    scrollbar.pack(side="right", fill="y")
    output_text.config(yscrollcommand=scrollbar.set)

    threading.Thread(target=ot, args=(output_window, output_text)).start()

def clear():
    userentry.delete(0, END)
    passentry.delete(0, END)

def b():
    os.startfile("temp.data")

def c():
    os.startfile("freq.data")
def d():
    os.startfile("login_details.data")
def check1():
    u_name = user_name.get()
    pass_word = password.get()
    u_name=u_name.upper()
    data = login_db.get(u_name)
    if data == pass_word :
        Amessage('Hello',"Welcome your login....success")
        l = open('login_details.data', 'a+')
        now = datetime.datetime.now()
        s = ("\n"+str(now.day) + '/' + str(now.month) + '/' + str(now.year) +"-"+str(now.hour)+':'+ str(now.minute) + ':' + str(now.second) +'         ')
        l.write(s+u_name)
        l.close()
        win.update_idletasks()
        pb['value']=0
        txt['text'] = pb['value'], '%'
        minwin(win)
        global win1
        win1 = Tk()
        filemenu = Frame(win1)
        win1.geometry('1000x1000')
        win1.title('MENU')
        scrollbar = Scrollbar(filemenu, orient=VERTICAL, width=15)
        scrollbar.place()
        scrollbar.pack(side=RIGHT, fill=Y)
        win1.configure(bg='purple')
        scrollbar.configure()
        scrollbar.set(100, 500)
        if u_name == "1":
            text1="Profile:  \n "+u_name+"\n(Main acc)"
        else:
            text1="Profile:  \n "+u_name   
        username1= Label(win1, text=text1, font='Verdana 10 bold')
        username1.place(x=900, y=10)
        b1 = Button(filemenu, text='Run', width=20, height=1, padx=5, pady=5, bg='black', command=notice, activebackground='white', font=('Helvetica', 25, 'bold'), fg='purple', bd=0)
        b2 = Button(filemenu, text='Rs from\n Temperature sensor', width=20, height=2, padx=5, pady=5, bg='black', command=b, activebackground='white', font=('Helvetica', 25, 'bold'), fg='purple', bd=0)
        b3 = Button(filemenu, text='Rs from\n Sound sensor', width=20, height=2, padx=5, pady=5, bg='black', command=c, activebackground='white', font=('Helvetica', 25, 'bold'), fg='purple', bd=0)
        b4 = Button(filemenu, text='Login details \n in this device', width=20, height=2, padx=5, pady=5, bg='black', command=d, activebackground='white', font=('Helvetica', 25, 'bold'), fg='purple', bd=0)
        b1.pack(padx=2, pady=2)
        b2.pack(pady=2)
        b3.pack(pady=2)
        b4.pack(pady=2)
        filemenu.pack()
        win1.mainloop()

    else:
        Amessage('hello',"sorry, username and \npassword is incorrect")

def check():

        
    def step():
        for i in range(1):
            win.update_idletasks()
            pb['value'] += 100
            time.sleep(1)
            txt['text'] = pb['value'], '%'
    global pb,txt
    pb = Progressbar(win, orient=HORIZONTAL, length=200, mode='determinate')

    pb.place(x=200, y=340)

    txt = Label(win,text='0%',bg='#000',fg='#fff')

    txt.place(x=400, y=340)
    step()
    check1()


win = Tk()
win.title("Stress Monitor- lOGIN PAGE")
win.maxsize(width=3000, height=1000)
win.minsize(width=1000, height=1000)

bg_image = PhotoImage(file="pic3.png")
x = Label(win, image=bg_image)
x.place(x=0, y=0)
heading1 = Label(win, text=' STRESS MONITOR', font=('TimesNewRoman',40), fg="purple", bg="black")
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
bt = Checkbutton(win, command=mark, variable=var, offvalue=0, onvalue=1)
bt.place(x=450, y=260)
btn_login = Button(win, text="login", font='Verdana 10 bold', command=check)
btn_login.place(x=210, y=290)
btn_login = Button(win, text="Clear", font='Verdana 10 bold', command=clear)
btn_login.place(x=260, y=290)

win.mainloop()
