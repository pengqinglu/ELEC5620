import tkinter as tk
import pickle
import os
import time
from sense_hat import SenseHat
from tkinter import messagebox  # import this to fix messagebox error
import face_recog
from face_recog import face_recognition
#from face_dataset import add_user
from face_training import train_model

email_update_interval = 600
on_hit = False
auth = 2
name = ""
admin = 0
    
def add_user():
    import cv2
    
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video width
    cam.set(4, 480) # set video height

    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    window_id = tk.Toplevel(window)
    window_id.title('Input ID')
    window_id.geometry('300x200')

    def print_selection():
        value = lb.get(lb.curselection())
        face_id = int(value)
        window_id.destroy()
        tk.messagebox.showinfo('Notice', 'Face the camera and wait for a while!')
        count = 0
        
        while(True):

            ret, img = cam.read()
            #img = cv2.flip(img, -1) # flip video image vertically
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
    
            for (x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
                count += 1
                print(str(count)+"/30\n")
                # Save the captured image into the datasets folder
                cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

                cv2.imshow('image', img)

            k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break
            elif count >= 30: # Take 30 face sample and stop video
                 break 

        # Do a bit of cleanup
        print("\n [INFO] Exiting Program and cleanup stuff")
        cam.release()
        cv2.destroyAllWindows()
        tk.messagebox.showinfo('Done', 'Face has been successfully added!')

    var2 = tk.StringVar()
    var2.set((1,2,3,4,5))
    lb = tk.Listbox(window_id, listvariable=var2, font=('Arial', 15), width = 10, height = 5)
    lb.pack()
    
    b1 = tk.Button(window_id, text='ID selection', width=15,
                  height=2, command=print_selection)
    b1.pack()
    
def get_cpu_temp():
    res = os.popen("vcgencmd measure_temp").readline()
    t = float(res.replace("temp=","").replace("'C\n",""))
    return(t)

def read_data():
    sense = SenseHat()
    t1 = sense.get_temperature_from_humidity()
    t2 = sense.get_temperature_from_pressure()
    t_cpu = get_cpu_temp()
    p = sense.get_pressure()
    h = sense.get_humidity()
    p = round(p, 1)
    h = round(h, 1)
    t = (t1+t2)/2
    t_corr = t - ((t_cpu-t)/1.5)
    t_corr = round(t_corr, 1)
    return t_corr, p, h
       
def usr_login():
    global auth
    global name
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    try:
        with open('usrs_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
    except FileNotFoundError:
        with open('usrs_info.pickle', 'wb') as usr_file:
            usrs_info = {'name': ['name', 'pwd', 'auth']}
            pickle.dump(usrs_info, usr_file)
    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name][1]:
            name = usr_name
            auth = int(usrs_info[usr_name][2])
            control_panel()
        else:
            tk.messagebox.showerror(message='Error, your password is wrong, try again.')
    else:
        is_sign_up = tk.messagebox.askyesno('Welcome',
                               'You have not signed up yet. Sign up today?')
        if is_sign_up:
            usr_sign_up()
            
def usr_sign_up():
    def sign_to_Mofan_Python():
        global admin
        np = new_pwd.get()
        npf = new_pwd_confirm.get()
        nn = new_name.get()
        try:    
            with open('usrs_info.pickle', 'rb') as usr_file:
                exist_usr_info = pickle.load(usr_file)
        except FileNotFoundError:
            with open('usrs_info.pickle', 'wb') as usr_file:
                usrs_info = {'name': ['name', 'pwd', 'auth']}
                pickle.dump(usrs_info, usr_file)
            with open('usrs_info.pickle', 'rb') as usr_file:
                exist_usr_info = pickle.load(usr_file)
            admin = 1
            
        if np != npf:
            tk.messagebox.showerror('Error', 'Password and confirm password must be the same!')
        elif nn in exist_usr_info:
            tk.messagebox.showerror('Error', 'The user has already signed up!')
        else:
            if (admin):
                exist_usr_info[nn] = [nn,np,0]
                admin = 0
            else:
                exist_usr_info[nn] = [nn,np,2]
            with open('usrs_info.pickle', 'wb') as usr_file:
                pickle.dump(exist_usr_info, usr_file)
            tk.messagebox.showinfo('Welcome', 'You have successfully signed up!')
            window_sign_up.destroy()
            
    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry('350x200')
    window_sign_up.title('Sign up window')

    new_name = tk.StringVar()
    tk.Label(window_sign_up, text='User name: ').place(x=10, y= 10)
    entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)
    entry_new_name.place(x=150, y=10)

    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='Password: ').place(x=10, y=50)
    entry_usr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
    entry_usr_pwd.place(x=150, y=50)

    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='Confirm password: ').place(x=10, y= 90)
    entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
    entry_usr_pwd_confirm.place(x=150, y=90)

    btn_comfirm_sign_up = tk.Button(window_sign_up, text='Sign up', command=sign_to_Mofan_Python)
    btn_comfirm_sign_up.place(x=150, y=130)
    
def devices():
    
    window_device = tk.Toplevel(window)
    window_device.title("Home Devices")
    window_device.geometry('400x200')
    
    def print_selection():
        if (var1.get() == 1) & (auth == 0):
            sense.show_letter('A',red)
        if (var1.get() == 1) & (auth > 0):
            var1.set(0)
            tk.messagebox.showwarning('Warning', 'No Authority!')
        if (var2.get() == 1):
            sense.show_letter('L',green)
        if (var3.get() == 1):
            sense.show_letter('M',blue)
        if (var1.get() == 0) & (var2.get() == 0) & (var3.get() == 0):
            sense.clear()
    
    sense = SenseHat()
          
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    var1 = tk.IntVar()
    var2 = tk.IntVar()
    var3 = tk.IntVar()
    
    c1 = tk.Checkbutton(window_device, text='AC', variable=var1, font=('Arial', 20), onvalue=1, offvalue=0,
                    command=print_selection)
    c2 = tk.Checkbutton(window_device, text='Light', variable=var2, font=('Arial', 20), onvalue=1, offvalue=0,
                    command=print_selection)
    c3 = tk.Checkbutton(window_device, text='Music', variable=var3, font=('Arial', 20), onvalue=1, offvalue=0,
                    command=print_selection)
    
    c1.place(x=50,y=30)
    c2.place(x=50,y=70)
    c3.place(x=50,y=110)

def load_users():
    with open('usrs_info.pickle', 'rb') as usr_file:
                exist_usr_info = pickle.load(usr_file)
    for i in exist_usr_info:
        print(exist_usr_info[i])
        
def setting():
    
    def load_users():
        with open('usrs_info.pickle', 'rb') as usr_file:
                    exist_usr_info = pickle.load(usr_file)
        messageUsers = "['name','pwd','auth']\n"
        for i in exist_usr_info:
            messageUsers = messageUsers + str(exist_usr_info[i]) + "\n"
        var1.set(messageUsers)
        
    def delete_user():
        if(len(var_name.get())==0):
            tk.messagebox.showerror('Error', 'No enough input!')
        else:
            with open('usrs_info.pickle', 'rb') as usr_file:
                        exist_usr_info = pickle.load(usr_file)
            usr_name = var_name.get()
            try:
                del exist_usr_info[usr_name]
                with open('usrs_info.pickle', 'wb') as usr_file:
                    pickle.dump(exist_usr_info, usr_file)
                tk.messagebox.showinfo('info','User Deleted !')
            except KeyError:
                tk.messagebox.showerror('Error', 'No such user!')
    
    def auth_change():
        if (len(var_name.get())==0) or (len(var_auth.get())==0):
            tk.messagebox.showerror('Error', 'No enough input!')
        else:
            with open('usrs_info.pickle', 'rb') as usr_file:
                    exist_usr_info = pickle.load(usr_file)
            exist_usr_info[var_name.get()][2] = var_auth.get()
            with open('usrs_info.pickle', 'wb') as usr_file:
                    pickle.dump(exist_usr_info, usr_file)
            tk.messagebox.showinfo('info','Authority Changed !')
        
    def load_id():
        try:    
            with open('usrs_id.pickle', 'rb') as usr_file:
                usrs_id = pickle.load(usr_file)
        except FileNotFoundError:
            with open('usrs_id.pickle', 'wb') as usr_file:
                usrs_id = {0:['none', 'name1', 'name2', 'name3', 'name4', 'name5']}
                pickle.dump(usrs_id, usr_file)
            with open('usrs_id.pickle', 'rb') as usr_file:
                usrs_id = pickle.load(usr_file)
        names = usrs_id[0]
        id_names = ""
        for n in names:
            id_names = id_names + n + "\n"
        var2.set(id_names)
    
    def change_id_name():
        if (len(var_id.get())==0) or (len(var_id_name.get())==0):
            tk.messagebox.showerror('Error', 'No enough input!')
        else:
            with open('usrs_id.pickle', 'rb') as usr_file:
                    usrs_id = pickle.load(usr_file)
            usrs_id[0][int(var_id.get())] = var_id_name.get()
            with open('usrs_id.pickle', 'wb') as usr_file:
                    pickle.dump(usrs_id, usr_file)
            tk.messagebox.showinfo('info','ID name Changed !')
            
    if auth==0:    
        window_setting = tk.Toplevel(window)
        window_setting.title("Home Devices")
        window_setting.geometry('400x900')
    
        var1 = tk.StringVar()
        labelUsers = tk.Label(window_setting, textvariable = var1, font=('Arial', 20), height = 8, width = 20, fg = "blue").pack()
    
        btn1 = tk.Button(window_setting, text = "load users", font=('Arial', 15), height = 2, width = 10, command = load_users).pack()
    
        tk.Label(window_setting, text='Name: ', font=('Arial', 15)).place(x=20, y= 350)
        tk.Label(window_setting, text='Auth: ', font=('Arial', 15)).place(x=200, y= 350)
        tk.Label(window_setting, text='(0~2) ', font=('Arial', 15)).place(x=290, y= 350)
    
        var_name = tk.StringVar()
        entry_name = tk.Entry(window_setting, textvariable=var_name, width = 8).place(x=80,y=350)
        var_auth = tk.StringVar()
        entry_auth = tk.Entry(window_setting, textvariable=var_auth, width = 4).place(x=250,y=350)
    
        btn2 = tk.Button(window_setting, text = "change", font=('Arial', 15), height = 2, width = 5, command = auth_change).place(x=100,y=400)
        btn3 = tk.Button(window_setting, text = "delete", font=('Arial', 15), height = 2, width = 5, command = delete_user).place(x=250,y=400)
    
        var2 = tk.StringVar()
        labelIds = tk.Label(window_setting, textvariable = var2, font=('Arial', 20), height = 5, width = 20, fg = "blue").place(x=50,y=500)
    
        tk.Label(window_setting, text='ID: ', font=('Arial', 15)).place(x=20, y= 700)
        tk.Label(window_setting, text='(1~5) ', font=('Arial', 15)).place(x=100, y= 700)
        tk.Label(window_setting, text='Name: ', font=('Arial', 15)).place(x=200, y= 700)
    
        var_id = tk.StringVar()
        entry_id = tk.Entry(window_setting, textvariable=var_id, width = 4).place(x=50,y=700)
        var_id_name = tk.StringVar()
        entry_id_name = tk.Entry(window_setting, textvariable=var_id_name, width = 8).place(x=260,y=700)
        btn4 = tk.Button(window_setting, text = "load faceID", font=('Arial', 15), height = 2, width = 8, command = load_id).place(x=80,y=800)
        btn5 = tk.Button(window_setting, text = "change", font=('Arial', 15), height = 2, width = 5, command = change_id_name).place(x=250,y=800)
    else:
        tk.messagebox.showwarning('Warning', 'No Authority!')
        
def control_panel():
    
    def environment():
        global on_hit
        if on_hit == False:
            on_hit = True
            [tem_corr, pre, hum] = read_data()
            message = "Temperature: " + str(tem_corr) + "\n" + " Pressure: " + str(pre) + "\n" + " Humidity: " + str(hum)
            var.set(message)
        else:
            on_hit = False
            var.set('')
            
    window_control = tk.Toplevel(window)

    window_control.title("Smart Home")

    window_control.geometry('500x900')
    
    members = ["admin", "member", "guest"]
    
    messageHello = "Press the button\n" + name + "(" + members[auth] + ")" + "\nauthority: " + str(auth)
    labelHello = tk.Label(window_control, text = messageHello, font=('Arial', 20), height = 5, width = 20, fg = "blue")
    labelHello.pack()

    btn1 = tk.Button(window_control, text = "face recognition", font=('Arial', 20), height = 3, width = 20, command = face_recognition)

    btn1.pack()

    btn2 = tk.Button(window_control, text = "add face", font=('Arial', 20), height = 3, width = 20, command = add_user)

    btn2.pack()

    btn3 = tk.Button(window_control, text = "train model", font=('Arial', 20), height = 3, width = 20, command = train_model)

    btn3.pack()

    btn4 = tk.Button(window_control, text = "environment", font=('Arial', 20), height = 3, width = 20, command = environment)

    btn4.pack()
    
    btn5 = tk.Button(window_control, text = "devices", font=('Arial', 20), height = 3, width = 20, command = devices)

    btn5.pack()
    
    btn6 = tk.Button(window_control, text = "setting", font=('Arial', 20), height = 3, width = 20, command = setting)

    btn6.pack()

    var = tk.StringVar()
    I = tk.Label(window_control, textvariable = var, font=('Arial',20), height = 3, width = 20, fg = 'green').place(x=100,y=800)
    
window = tk.Tk()
window.title('Login')
window.geometry('450x300')

# welcome image
canvas = tk.Canvas(window, height=200, width=500)
image_file = tk.PhotoImage(file='icon.png')
image = canvas.create_image(172,0, anchor='nw', image=image_file)
canvas.pack(side='top')

# user information
tk.Label(window, text='User name: ').place(x=50, y= 150)
tk.Label(window, text='Password: ').place(x=50, y= 190)

var_usr_name = tk.StringVar()
#var_usr_name.set('example@python.com')
entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
entry_usr_name.place(x=160, y=150)
var_usr_pwd = tk.StringVar()
entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=160, y=190)

# login and sign up button
btn_login = tk.Button(window, text='Login', command=usr_login)
btn_login.place(x=170, y=230)
btn_sign_up = tk.Button(window, text='Sign up', command=usr_sign_up)
btn_sign_up.place(x=270, y=230)

window.mainloop()
