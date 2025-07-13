from tkinter import messagebox
try:
    import serial
    import os
    import datetime  
    from datetime import timedelta
    import random
    import threading
    import time
    from tkinter.ttk import Style
    from tkinter.ttk import Treeview
    from tkinter import PhotoImage
    from tkinter import *
    from tkinter import messagebox
    from tkinter.ttk import Progressbar
    import matplotlib
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt
    global td, sd, tid, fd,hid,tdid,grp_time

    td = []
    sd = []
    fd = []
    tud = []
    pd=[]
    tid = []
    hid = []
    tdid=[]
    dod=[]
    grp_time=[0,]
    tdid0=[]
    grp_time0=[0,]
    ser = serial.Serial('COM5', 9600)
    t = open('temp.data', 'a+')
    f = open('freq.data', 'a+')
    p = open('pH.data','a+')
    ut = open('Turbidity.data','a+')
    login_db = {"1": "1", "22BCE9319": "Sw7bNSyJ", "22BCE9102": "gzM5b4FS", "22BCE8341": "LLa9epZm", "22BCE9351": "82ZvdaX6",
                "22BCE8525": "uK5d6AzP", "22BCE7517": "f4x2YVfv"}
                
    def Amessage(title, msg):
        messagebox.showinfo(title, msg)

    def close_message_box():
        messagebox._show(title='', message='')

    def minwin(root):
        root.iconify()
    def wchk():
        a=True
        while a:
            if not plt.fignum_exists(1):
                output_window.destroy()
                
                a=False
                
            
    def graph():
        global td, sd, tid, fd,hid,tdid,grp_time,tud,pd
        global dfl,fig
        
        dfl = False
        fig, ((ax1, ax2,ax5),(ax6,ax3,ax4)) = plt.subplots(2, 3, figsize=(10, 8))
        current_datetime = datetime.datetime.now()
        filename = "temp_sound" + current_datetime.strftime("%d/%m/%Y_%H:%M:%S")
        plt.title( filename)
        ax1.plot(grp_time, td, marker='o',linewidth=1.0)
        ax1.set_xlabel("Time (sec) →")
        ax1.set_ylabel("Temperature C° →")
        ax1.set_title("Temperature vs Time",font="Times new Roman",fontweight="bold",fontsize=17)
        ax1.grid(True)
        ax2.plot(grp_time, sd, marker='o',linewidth=1.0)
        ax2.set_xlabel("Time (sec) →")
        ax2.set_ylabel("Sound Level db →")
        ax2.set_title("Sound Level vs Time",font="Times new Roman",fontweight="bold",fontsize=17)
        ax2.grid(True)
        ax3.plot(pd,td, marker='o',linewidth=1.0)
        ax3.set_xlabel("pH →")
        ax3.set_ylabel(" Temperature C° →")
        ax3.set_title("Temperature vs pH",font="Times new Roman",fontweight="bold",fontsize=17)
        ax3.grid(True)
        ax4.plot(tud, pd, marker='o',linewidth=1.0)
        ax4.set_xlabel(" Turbidity →")
        ax4.set_ylabel(" pH →")
        ax4.set_title("pH vs Turbidity",font="Times new Roman",fontweight="bold",fontsize=17)
        ax4.grid(True)
        ax5.plot(grp_time, tud, marker='o',linewidth=1.0)
        ax5.set_xlabel("Time (sec) →")
        ax5.set_ylabel("Turbidity →")
        ax5.set_title("Turbidity vs Time",font="Times new Roman",fontweight="bold",fontsize=17)
        ax5.grid(True)
        ax6.plot(grp_time, pd, marker='o',linewidth=1.0)
        ax6.set_xlabel("Time (sec) →")
        ax6.set_ylabel("pH →")
        ax6.set_title("pH vs Time",font="Times new Roman",fontweight="bold",fontsize=17)
        ax6.grid(True)

        plt.tight_layout()
        #plt.suptitle("Sensor Data vs Time")
        plt.show()
        td = []
        sd = []
        fd = []
        tud = []
        pd=[]
        tid = []
        hid = []
        tdid=[]
        dod=[]
        grp_time=[0,]
        wchk()

    output_window = None
    table = None
    def ot(output_window):
        stop_flag = threading.Event()
        sno = 1
        def update_table( sno,hd,temperature,sound_level,freq,turb,pH):
            table.insert("","end",values=( str(sno),str(hd),str(temperature),str(sound_level),str(freq),str(turb),str(pH)))
            

        def stop():
            global grp_time
            global dfl
            stop_flag.set()
            dfl = True
            global stopflag
            stopflag = True
            t = open('temp.data', 'a+')
            f = open('freq.data', 'a+')
            p = open('pH.data','a+')
            ut = open('Turbidity.data','a+')
            print("Stopped")
            t.write("Stopped\n")
            f.write("Stopped\n")
            p.write("Stopped\n")
            ut.write("Stopped\n")
            
            try:
                print(sd)
                mtd=max(td)
                msd=max(sd)
                mfd=max(fd)
                atd=round(sum(td)/len(td),3)
                asd=round(sum(sd)/len(sd),1)
                atud=round(sum(tud)/len(tud),1)
                apd=round(sum(pd)/len(pd),1)
                do_value= round(float(float(temperature)+round( -0.1 *round(float(Turbidity))/2)+(0.5*float(pH))+8),1)
                ado=round(sum(dod)/len(dod),1)
                if not plt.fignum_exists(1):
                    for i in range(len(hid)-1):
                        time1= hid[i]
                        time2= hid[i+1]
                        tf1=datetime.datetime.strptime(time1,"%H:%M:%S")
                        tf2=datetime.datetime.strptime(time2,"%H:%M:%S")
                        time_diff=tf2-tf1
                        tdid.append(time_diff.seconds)
                    print(tdid)
                
                    for i in range(0,len(hid)-1):
                        grp_time.append(grp_time[i]+tdid[i])
                else:
                    Amessage("Grpah is still not closed ","make sure the graph was deleted,\n if graph is deleted no recovers ,better save the graph")
                print(len(grp_time))
                print("grp_time",grp_time)
                print(len(hid))
                print("hid",hid)
                hdf = hid[0]
                hdl = hid[-1]
                hours, remainder = divmod(current_time+1, 3600)
                minutes, seconds = divmod(remainder, 60)
                timef = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                mesg = "DATA:  \n Start: " + hdf + " Stopped: " + hdl + " \n Total time noted: " + str(timef) + " (HH:MM:SS)"
                mesg1= "\n Avg Temp.: "+str(atd)+" \n Avg Sound_lvl.: "+str(asd)+" \n Avg Turbidity : "+str(atud)+" \n DO level: " +str(ado)
                Amessage("Note", mesg+mesg1)
                
            except Exception:
                messagebox.showerror("Exception found", str(Exception))
                pass
            if not plt.fignum_exists(1):
                graph()

        
        stop_button = Button(output_window, text="Stop and\n Show Graphs", font=("Arial 23 bold"), command=stop, fg="#99974A")
        stop_button.pack()
        columns = ["S.no:","Time", "Temperature (C°)", "Sound Level (dB)", "Frequency (Hz)","Turbidity ","pH "]
        table = Treeview(output_window, columns=columns,height=20)
        style = Style()
        style.configure("Treeview.Heading", background="#699C78", foreground="#7A6D3C",font=("TimesNewRoman",13,"bold"))
        table.pack()
        table.heading("#1", text="S.no:")
        table.heading("#2", text="Time")
        table.heading("#3", text="Temperature (C°)")
        table.heading("#4", text="Sound Level (dB)")
        table.heading("#5", text="Frequency (Hz)")
        table.heading("#6", text="Turbidity")
        table.heading("#7", text="pH")
        
        scrollbar = Scrollbar(output_window, orient=VERTICAL, command=table.yview)
        table.configure(yscroll=scrollbar.set)
        scrollbar.pack()

        try:
            while not stop_flag.is_set():
                t = open('temp.data', 'a+')
                f = open('freq.data', 'a+')
                p = open('pH.data','a+')
                ut = open('Turbidity.data','a+')
                now = datetime.datetime.now()
                s = (str(now.day) + '/' + str(now.month) + '/' + str(now.year) + '    ')
                t.write(s)
                f.write(s)
                p.write(s)
                ut.write(s)
                line = ser.readline().decode().strip()
                data = line.split(',')
                if len(data) == 4:
                    temperature, sound_level, Turbidity, pH = data
                    if float(temperature) == -127.00:
                        Amessage("Alert!", "Please check your  sensor connections.")
                        
                    if float(temperature) <= 10 or float(temperature) >= 35:
                        t.write("Next value is found above range!!!")
                    td.append(float(temperature))
                    sd.append(float(sound_level))
                    tud.append(float(Turbidity))
                    pd.append(float(pH))
                    freq = float(round(10 ** (round(float(sound_level)) / 10)))
                    fd.append(float(freq))
                    hd = str(now.hour) + ':' + str(now.minute) + ':'+ str(now.second)
                    hid.append(hd)
                    t.write(hd + " "+temperature + '\n')
                    f.write(hd + " "+sound_level + "  " + "frequency(Hz)" + str(freq) + '\n')
                    p.write(hd +" "+pH + " \n")
                    ut.write(hd+" "+Turbidity+" \n")
                    tid.append(sno - 1)
                    sno += 1
                    update_table(sno-1,hd,temperature,sound_level,freq,Turbidity,pH)
                    mtd=max(td)
                    msd=max(sd)
                    mfd=max(fd)
                    atd=round(sum(td)/len(td),3)
                    asd=round(sum(sd)/len(sd),1)
                    atud=round(sum(tud)/len(tud),1)
                    apd=round(sum(pd)/len(pd),2)
                    for i in range(len(hid)-1):
                        time1= hid[i]
                        time2= hid[i+1]
                        tf1=datetime.datetime.strptime(time1,"%H:%M:%S")
                        tf2=datetime.datetime.strptime(time2,"%H:%M:%S")
                        time_diff=tf2-tf1
                        tdid0.append(time_diff.seconds)
                    print(tdid0)
                
                    for i in range(0,len(hid)-1):
                        grp_time0.append(grp_time0[i]+tdid0[i])
                    if sno <=3 :
                        do_value= round(float(float(temperature)+round( -0.1 *round(float(Turbidity))/2)+(0.5*float(pH))+8),1)
                        dod.append(do_value)
                        ado=round(sum(dod)/len(dod),1)
                    else:
                        a=0
                        dt=(td[a] - td[a+2])/(grp_time0[a+2] -grp_time0[a])
                        dp=(pd[a]- pd[a+2])/(grp_time0[a+2] -grp_time0[a])
                        dtud=(tud[a]-tud[a+2])/(grp_time0[a+2] -grp_time0[a])
                        do_value= round(float(temperature)*dt+float(pH)*dp+float(Turbidity)*dtud,1)
                        dod.append(do_value)
                        ado=round(sum(dod)/len(dod),1)
                        a+=1
                        
                    output_window.update()
                    maxtempl = Label(output_window, text= "Peak Temperature:" , font='Verdana 10 bold')
                    maxtempl.place(x=10, y=10)
                    maxtemp = Label(output_window, text= mtd , font='Verdana 10 bold')
                    maxtemp.place(x=150, y=10)
                    avgtempl = Label(output_window, text= "Avrg Temperature:" , font='Verdana 10 bold')
                    avgtempl.place(x=10, y=30)
                    avgtemp = Label(output_window, text= atd , font='Verdana 10 bold')
                    avgtemp.place(x=150, y=30)
                    maxsoundl = Label(output_window, text= "Peak Sound_level:" , font='Verdana 10 bold')
                    maxsoundl.place(x=10, y=50)
                    maxsound = Label(output_window, text= msd , font='Verdana 10 bold')
                    maxsound.place(x=150, y=50)
                    avgsoundl = Label(output_window, text= "Avrg Sound_level:" , font='Verdana 10 bold')
                    avgsoundl.place(x=10, y=70)
                    avgsound = Label(output_window, text= asd , font='Verdana 10 bold')
                    avgsound.place(x=150, y=70)
                    avgturl = Label(output_window, text= "Avrg Turbidity:" , font='Verdana 10 bold')
                    avgturl.place(x=10, y=90)
                    avgtur = Label(output_window, text= atud , font='Verdana 10 bold')
                    avgtur.place(x=150, y=90)
                    avgphl = Label(output_window, text= "pH:" , font='Verdana 10 bold')
                    avgphl.place(x=10, y=110)
                    avgph = Label(output_window, text= apd , font='Verdana 10 bold')
                    avgph.place(x=150, y=110)
                    dol= Label(output_window, text= "DO level:" , font='Verdana 10 bold')
                    dol.place(x=10, y=130)
                    dop = Label(output_window, text= do_value , font='Verdana 10 bold')
                    dop.place(x=150, y=130)
                    adol= Label(output_window, text= "Avg DO level:" , font='Verdana 10 bold')
                    adol.place(x=10, y=150)
                    dop = Label(output_window, text= ado , font='Verdana 10 bold')
                    dop.place(x=150, y=150)
                    
                    time.sleep(1)

        except Exception as e:
            print("Stopped")
            print(str(e))
            t.write("\nStopped by excep\n")
            f.write("\nStopped by excep\n")
            p.write("\nStopped by excep\n")
            ut.write("\nStopped by excep\n")
        finally:
            t.close()
            f.close()
            ut.close()
            p.close()

    def notice():
           
        def update_time():
            global current_time
            current_time = int(label_var.get())
            current_time += 1
            label_var.set(current_time)
            lv=int(label_var.get())
            hours, remainder = divmod(lv, 3600)
            minutes, seconds = divmod(remainder, 60)
            timef = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            label.config(text=timef)
            if not stopflag:
                output_window.after(1000, update_time)
        
        global output_window
        output_window = Toplevel()
        output_window.title("Output Window")
        global stopflag
        stopflag=False
        label_var = StringVar()
        label_var.set(-1)
        la=Label(output_window,text="Time Recording:",font=("Arial",25))
        la.pack(padx=20)
        lv=int(label_var.get())
        hours, remainder = divmod(lv+1, 3600)
        minutes, seconds = divmod(remainder, 60)
        timef = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        label = Label(output_window, text=timef, font=("Arial", 24))
        label.pack(padx=20, pady=20)
        label.config(text=timef)
       
        update_time()
        username1 = Label(output_window, text=text1, font='Verdana 10 bold',bg='#86B98B')
        username1.place(x=900, y=10)
        
        threading.Thread(target=ot, args=(output_window,)).start()

    def clear():
        userentry.delete(0, END)
        passentry.delete(0, END)

    def b():
        os.startfile("temp.data")

    def c():
        os.startfile("freq.data")

    def d():
        os.startfile("login_details.data")
    def e():
        os.startfile("pH.data")
    def f():
        os.startfile("Turbidity.data")
    def check1():
        u_name = user_name.get()
        pass_word = password.get()
        u_name = u_name.upper()
        data = login_db.get(u_name)
        if data == pass_word:
            Amessage('Hello', "Welcome your login....success")
            l = open('login_details.data', 'a+')
            now = datetime.datetime.now()
            s = ("\n" + str(now.day) + '/' + str(now.month) + '/' + str(now.year) + "-" + str(now.hour) + ':' + str(
                now.minute) + ':' + str(now.second) + '         ')
            l.write(s + u_name)
            l.close()
            win.update_idletasks()
            pb['value'] = 0
            txt['text'] = pb['value'], '%'
            minwin(win)
            global win1
            win1 = Tk()
            filemenu = Frame(win1)
            win1.geometry('1000x1000')
            win1.title('MENU')
            bg = PhotoImage(file="pic7.png")
            scrollbar = Scrollbar(filemenu, orient=VERTICAL, width=15)
            scrollbar.place()
            scrollbar.pack(side=RIGHT, fill=Y)
            win1.configure(bg='#86B98B')
            scrollbar.configure()
            scrollbar.set(100, 500)
            global text1
            if u_name == "1":
                text1 = "Profile:  \n " + u_name + "\n(Main acc)"
            else:
                text1 = "Profile:  \n " + u_name
            username1 = Label(win1, text=text1, font='Verdana 10 bold')
            username1.place(x=900, y=10)
            b1 = Button(filemenu, text='Run', width=20, height=1, padx=5, pady=5, bg='black', command=notice,
                        activebackground='white', font=('Helvetica', 25, 'bold'), fg='#86B98B', bd=0)
            b2 = Button(filemenu, text='Results from\n Temperature sensor', width=20, height=2, padx=5, pady=5, bg='black',
                        command=b, activebackground='white', font=('Helvetica', 25, 'bold'), fg='#86B98B', bd=0)
            b3 = Button(filemenu, text='Results from\n Sound sensor', width=20, height=2, padx=5, pady=5, bg='black',
                        command=c, activebackground='white', font=('Helvetica', 25, 'bold'), fg='#86B98B', bd=0)
            b5 = Button(filemenu, text='Results from\n pH sensor', width=20, height=2, padx=5, pady=5, bg='black',
                        command=e, activebackground='white', font=('Helvetica', 25, 'bold'), fg='#86B98B', bd=0)
            b6 = Button(filemenu, text='Results from\n Turbidity sensor', width=20, height=2, padx=5, pady=5, bg='black',
                        command=f, activebackground='white', font=('Helvetica', 25, 'bold'), fg='#86B98B', bd=0)
            b4 = Button(filemenu, text='Login details \n in this device', width=20, height=2, padx=5, pady=5, bg='black',
                        command=d, activebackground='white', font=('Helvetica', 25, 'bold'), fg='#86B98B', bd=0)
            b1.pack(padx=2, pady=2)
            b2.pack(pady=2)
            b3.pack(pady=2)
            b5.pack(pady=2)
            b6.pack(pady=2)
            b4.pack(pady=2)
            filemenu.pack()
            win1.mainloop()

        else:
            Amessage('hello', "sorry, username and \npassword is incorrect")

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
        txt = Label(win, text='0%',font=('TimesNewRoman',13), bg='#95B994', fg='#A16D3B')
        txt.place(x=400, y=340)
        step()
        check1()

    win = Tk()
    win.title("Stress Monitor- LOGIN PAGE")
    win.maxsize(width=1000, height=1000)
    win.minsize(width=1000, height=500)

    bg_image = PhotoImage(file="pic7.png")
    x = Label(win, image=bg_image)
    x.place(x=0, y=0)
    heading1 = Label(win, text=' STRESS MONITOR', font=('TimesNewRoman', 40), fg="#A48B48", bg="#C7C7A9")
    heading1.place(x=300, y=10)
    heading = Label(win, text="Login", font='Verdana 25 bold',fg="#A48B48", bg="#C7C7A9")
    heading.place(x=80, y=150)
    username = Label(win, text="User Name:", font='Verdana 12 bold',fg="#537D58", bg="#C7C7A9")
    username.place(x=80, y=220)
    userpass = Label(win, text="Password:", font='Verdana 12 bold',fg="#537D58", bg="#C7C7A9")
    userpass.place(x=80, y=260)
    heading = Label(win, text="Show password", font='Verdana 10 bold',fg="#537D58", bg="#C7C7A9")
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
    btn_login = Button(win, text="login", font='Verdana 10 bold',fg="#BC6E25", bg="#C7C7A9", command=check)
    btn_login.place(x=210, y=290)
    btn_login = Button(win, text="Clear", font='Verdana 10 bold',fg="#BC6E25", bg="#C7C7A9", command=clear)
    btn_login.place(x=260, y=290)

    win.mainloop()
except Exception as e:
    messagebox.showinfo("Alert", "Check the required components or port connection\n"+str(e))
    

