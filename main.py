from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox
import time
from datetime import datetime
import sqlite3


#initilization of GUI
root = Tk()
root.title("Virtual Parking Meter V.01")
root.geometry("400x500")
root.resizable(False, False)
banner_img = ImageTk.PhotoImage(Image.open("banner.jpg"))

#setting up database

#conn = sqlite3.connect("parking_meter.db")
#c = conn.cursor()
#c.execute("""CREATE TABLE parking_meter_users (
#    first_name text,
#    last_name text,
#    licence_plate text,
#    password text,
#    amount_owing interger
#        )""")
#conn.close()

#setting variables
#global root


t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
zone_var = StringVar()
zone_var.set("Huntington Hills")
end_time = 0
username = StringVar()
password = StringVar()
f_name = StringVar()
l_name = StringVar()
l_plate = StringVar()
p_word = StringVar()
amount_owing = IntVar()
f_names = StringVar()


start_time = False
clock_in = 0


zone = {
    "Huntington Hills":3,
    "Country Hills":4,
    "Tuscany":5,
    "Center Street North":7,
    "Tuxedo":5,
    "University of Calgary":8,
    "Downtown":12
}


def update_clock():
    #updates the clock
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    clock.config(text = current_time)
    clock.after(1000,update_clock)

def booktime():
    #function to start or stop the clock when booking a parking spot
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    time_format = '%H:%M:%S'
    global total_amount_owing
    global start_time
    global clock_in
    global total_time_delta

    if start_time == False:

        clock_in = current_time
        clock_in_label = Label(root, text=clock_in + " at " + zone_var.get(), font=("Aerial", 18))
        clock_in_label.place(relx=.1, rely=0.6)
        clock_in_btn.config(text="Clock Out")
        start_time = True
        zone_id_label.config(state = "disabled")
        return
    else:
        clock_out = current_time
        clock_out_label = Label(root, text=clock_out + " at " + zone_var.get(), font=("Aerial", 18))
        clock_out_label.place(relx=.1, rely=0.7)
        zone_id_label.config(state="enabled")
        clock_in_btn.config(text = "Clock in")

    total_time_delta = datetime.strptime(clock_out,time_format) - datetime.strptime(clock_in, time_format)
    total_amount_owing = ((zone[zone_var.get()])/3600) * total_time_delta.total_seconds()
    total_amount_owing = round(total_amount_owing, 2)
    messagebox.showinfo(message = "The amount owing is: ${}".format(total_amount_owing))
    update_user_info()

    end_program()




def returning_user():

    conn = sqlite3.connect("parking_meter.db")
    c = conn.cursor()

    c.execute("SELECT first_name, last_name,licence_plate, password, amount_owing, oid FROM parking_meter_users")
    records = c.fetchall()

    for i in records:
        if username.get() == i[2] and password.get() == i[3]:
            global f_names
            global l_name
            global l_plate
            global amount_owing
            f_names = i[0]
            l_name = i[1]
            l_plate = i[2]
            amount_owing = i[4]

            root.deiconify()
            login.destroy()
            c.close()
            user_info()
            return

    messagebox.showerror(message = "licence plate or username not found")
    c.close()


def new_user():

    first_name_label = Label(login, text = "First Name", font = ("Aerial", 14))
    first_name_label.grid(row = 6, column = 0)
    first_name_entry = Entry(login, textvariable= f_name, width= 14)
    first_name_entry .grid(row =6, column = 1)

    last_name_label = Label(login, text="Last Name", font=("Aerial", 14))
    last_name_label.grid(row=7, column=0)
    last_name_entry = Entry(login, textvariable= l_name, width = 14)
    last_name_entry.grid(row=7, column=1)

    licence_plate_label = Label(login, text="Licence Plate", font=("Aerial", 14))
    licence_plate_label.grid(row=8, column=0)
    licence_plate_entry = Entry(login,textvariable=l_plate, width=14)
    licence_plate_entry.grid(row=8, column=1)

    password_label = Label(login, text="Password", font=("Aerial", 14))
    password_label.grid(row=9, column=0)
    password_entry= Entry(login,textvariable=p_word, width=14)
    password_entry.grid(row=9, column=1)

    submit_button = Button(login, text = "Submit new user", command  = new_user_submit)
    submit_button.grid(row=10, column = 0)


def new_user_submit():
    conn = sqlite3.connect("parking_meter.db")
    c = conn.cursor()

    if l_plate.get() == "":
        messagebox.showerror(title="Error", message="License plate field was empty")
        return
    else:
        c.execute("INSERT INTO parking_meter_users VALUES (:f_name, :l_name, :l_plate, :p_word, :amount_owing)",
                  {
                      'f_name':f_name.get(),
                      'l_name':l_name.get(),
                      'l_plate':l_plate.get(),
                      'p_word':p_word.get(),
                      'amount_owing':amount_owing.get()

                  })
        conn.commit()


        # closes connection
        conn.close()
        messagebox.showinfo(title= "New user added", message = "Welcome "+f_name.get()+"!")
        login.destroy()
        root.deiconify()



def user_info():
    global user_info_window
    user_info_window = Tk()

    user_info_window.geometry("200x100")
    user_info_window.title('')
    user_info_window.resizable(False, False)

    first_name_label = Label(user_info_window, text="First Name: {}".format(f_names), font=("Aerial", 10))
    first_name_label.grid(row=2, column=2)
    last_name_label = Label(user_info_window, text="Last Name: %s" % l_name, font=("Aerial", 10))
    last_name_label.grid(row=3, column=2)
    licence_plate_label = Label(user_info_window, text="License Plate: {}".format(l_plate), font=("Aerial", 10), padx=10)
    licence_plate_label.grid(row=4, column=2)
    amount_owing_label = Label(user_info_window, text="Amount Owing: ${}".format(round(amount_owing,2)), font=("Aerial", 10))
    amount_owing_label.grid(row=5, column=2)


def update_user_info():
    global amount_owing_intodb
    amount_owing_intodb = amount_owing+ total_amount_owing
    amount_owing_intodb = round(amount_owing_intodb, 2)
    conn = sqlite3.connect("parking_meter.db")
    c = conn.cursor()

    c.execute("""UPDATE parking_meter_users SET
        amount_owing = :amount_owing   
        WHERE licence_plate = :licence_plate""", {'amount_owing':amount_owing_intodb,
                                                  'licence_plate':l_plate})
    conn.commit()
    conn.close()

def end_program():
    messagebox.showinfo(message = "{}, thank you for using Parking Meter Machine. Your total amount owed is: {}".format(f_names, amount_owing_intodb))
    root.destroy()



#inital log-in for users
login = Toplevel()
login.title("Virtual Parking Meter V.01 - Log-in")
login.geometry("400x400")
login.resizable(False, False)
banner_label_login = Label(login, image = banner_img, height = 100, width = 400)
banner_label_login.grid(row = 0, columnspan = 2)
login_user_label = Label(login, text = "Licence Plate", font = ("Aerial",14), padx = 15)
login_user_label.grid(row = 2, column = 0)
login_user_entry = Entry(login, textvariable=username, width = 14)
login_user_entry.grid(row = 2, column = 1 )
password_user_label = Label(login,text = "Password", font = ("Aerial", 14), padx = 15 )
password_user_label.grid(row = 3, column = 0)
password_user_entry = Entry(login, textvariable=password, width = 14, show = "*")
password_user_entry.grid(row = 3, column = 1)
login_button = Button(login, text = "Login", command = returning_user)
login_button.grid(row = 4, column = 0)
new_user_button = Button(login, text = "New User", command = new_user)
new_user_button.grid(row = 4, column = 1)




#hiding the main window
root.withdraw()

#Setting up Widgets for Root

banner_label = Label(root, image = banner_img, height = 100, width= 400)
banner_label.grid(row=0, columnspan = 2)
zone_id_label = ttk.Combobox(root, textvariable=zone_var, values = list(zone.keys()))
zone_id_label.bind('<<ComboboxSelected>>', lambda event: rate_label_box.config(text="$"+str(zone[zone_var.get()])+"/hr"))
zone_id_label.grid(row=2, column=1)
zone_label = Label(root, text = "Zone", font= ("Aerial", 18))
zone_label.grid(row = 2, column = 0, sticky = "W", padx = 10, pady = 20)
rate_label = Label(root, text = "Rate", font = ("Aerial",18), padx = 10)
rate_label.grid(row = 4, column = 0, sticky = "W")
rate_label_box = Label(root, text = "", font=("Aerial",18))
rate_label_box.grid(row = 4, column = 1)

#clock settings

clock_label = Label(root, text = "Time", font = ("Aerial",18), padx = 10, pady= 30)
clock_label.grid(row = 5, column = 0, sticky = "W")
clock = Label(root, text = current_time, font = ("Aerial",18), bg = "White")
clock.after(1000, update_clock)
clock.grid(row =5, column = 1)
clock_in_btn = Button(root, text = "Clock in", command = booktime, font=("Aerial",18))
clock_in_btn.place(relx = 0.30, rely = 0.8)


root.mainloop()

