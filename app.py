from tkinter import *
from PIL import Image,ImageTk
import mysql.connector



mydb = mysql.connector.connect(host='localhost',username='root',password='mysql',charset='utf8',database='tickets')
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS tickets")
mycursor.execute("USE tickets")



msg1=''

def submit(add_aadhar,add_pass,add_name,add_flight,lbl_msg1):
    if (add_aadhar.get() == '' and add_pass.get() == '') or add_name.get() == '' or add_flight.get() == '':
        if add_aadhar.get() == '' and add_pass.get() == '' and add_name.get() == '' and add_flight.get() == '':
            msg1='No data entered!'
        else:
            msg1="Enough data isn't entered!"
    else:
        mycursor.execute("CREATE TABLE IF NOT EXISTS passengers (id INT AUTO_INCREMENT PRIMARY KEY, aadhar_no VARCHAR(16), passport_no VARCHAR(9), name VARCHAR(255), flight_no VARCHAR(10))")
        sql = "INSERT INTO passengers (aadhar_no, passport_no, name, flight_no) VALUES (%s, %s, %s, %s)"
        val = (add_aadhar.get(), add_pass.get(), add_name.get(), add_flight.get())
        mycursor.execute(sql, val)
        mydb.commit()
        msg1="Entry added!"
    lbl_msg1.config(text=msg1, fg='red')

msg2=''

def delete(del_id,lbl_msg2,msg2,search_frame):
    val=(int(del_id.get()),)
    sql = "DELETE FROM passengers WHERE id = %s"
    mycursor.execute(sql,val)
    mydb.commit()
    msg2='Entry deleted!'
    lbl_msg2.config(text=msg2, fg='red')

def search(del_aadhar,del_pass,search_frame):
    for widgets in search_frame.winfo_children():
        widgets.destroy()
    if del_aadhar.get() == '' and del_pass.get() == '':
        msg2 = 'No data entered!'
        lbl_msg2 = Label(search_frame, text=msg2, font=('Ariel Black', 15), bg='grey')
        lbl_msg2.place(x=410, y=105, width=300)
        lbl_msg2.config(text=msg2, fg='red')
    else:
        if del_aadhar.get()!='' and del_pass.get()=='':
            sql="SELECT * FROM passengers WHERE aadhar_no = %s"
            val=(del_aadhar.get(),)
            mycursor.execute(sql,val)
        elif del_aadhar.get()=='' and del_pass.get()!='':
            sql = "SELECT * FROM passengers WHERE passport_no = %s"
            val = (del_pass.get(),)
            mycursor.execute(sql, val)
        else:
            sql = "SELECT * FROM passengers WHERE aadhar_no = %s AND passport_no = %s"
            val = (del_aadhar.get(),del_pass.get())
            mycursor.execute(sql, val)
        result = mycursor.fetchall()
        if not result:
            msg2 = 'No such entry found!'
            lbl_msg2 = Label(search_frame, text=msg2, font=('Ariel Black', 15), bg='grey')
            lbl_msg2.place(x=410, y=105, width=300)
            lbl_msg2.config(text=msg2, fg='red')
        else:
            t = 10
            for i in result:
                i1 = '\t'.join(str(s) for s in i)
                lb = Label(search_frame, text=i1, font=('Ariel Black', 15), bg='grey').place(x=100, y=t, width=1000)
                t += 30
            del_id=StringVar()
            msg2=''
            lbl_msg2 = Label(search_frame, text=msg2, font=('Ariel Black', 15), bg='grey')
            lbl_msg2.place(x=700, y=t+35, width=300)
            lbl_id = Label(search_frame, text='Enter id to be deleted', font=('Ariel Black', 10), bg='grey').place(x=400, y=t, width=150)
            en_id = Entry(search_frame, font=('Ariel Black', 10), bg='white', textvariable=del_id).place(x=560, y=t, width=150)
            btn_id = Button(search_frame, text='Delete',font=("times new roman", 15), bg='white', fg='grey', command=lambda:delete(del_id,lbl_msg2,msg2,search_frame)).place(x=460,y=t+35,width=200)

def add_db(ad_frame):
    for widgets in ad_frame.winfo_children():
        widgets.destroy()
    add_aadhar=StringVar()
    add_pass=StringVar()
    add_name = StringVar()
    add_flight = StringVar()
    lbl_msg1 = Label(ad_frame, text=msg1, font=('Ariel Black', 15), bg='lightyellow')
    lbl_msg1.place(x=410, y=217, width=300)
    addlbl1 = Label(ad_frame, text='Aadhaar No.', font=('Ariel Black', 15), bg='lightyellow').place(x=400, y=20, width=150)
    adden1 = Entry(ad_frame, font=('Ariel Black', 15), bg='white', textvariable=add_aadhar).place(x=600, y=20, width=300)
    addlbl2 = Label(ad_frame, text='Passport No.', font=('Ariel Black', 15), bg='lightyellow').place(x=400, y=55, width=150)
    adden2 = Entry(ad_frame, font=('Ariel Black', 15), bg='white', textvariable=add_pass).place(x=600, y=55, width=300)
    addlbl3 = Label(ad_frame, text='Name', font=('Ariel Black', 15), bg='lightyellow').place(x=400, y=90, width=150)
    adden3 = Entry(ad_frame, font=('Ariel Black', 15), bg='white', textvariable=add_name).place(x=600, y=90, width=300)
    addlbl4 = Label(ad_frame, text='Flight No.', font=('Ariel Black', 15), bg='lightyellow').place(x=400, y=125, width=150)
    adden4 = Entry(ad_frame, font=('Ariel Black', 15), bg='white', textvariable=add_flight).place(x=600, y=125, width=300)
    btn_sub = Button(ad_frame, text='Submit', font=("times new roman", 15), bg='grey', fg='white',command=lambda:submit(add_aadhar,add_pass,add_name,add_flight,lbl_msg1)).place(x=460, y=175, width=200)

def del_db(ad_frame):
    for widgets in ad_frame.winfo_children():
        widgets.destroy()
    del_aadhar = StringVar()
    del_pass = StringVar()
    search_frame = Frame(ad_frame, bd=2, bg='grey', relief=RIDGE)
    search_frame.place(x=0, y=100, relwidth=1, height=145)
    dellbl1 = Label(ad_frame, text='Aadhaar No.', font=('Ariel Black', 15), bg='lightyellow').place(x=10, y=20,
                                                                                                    width=150)
    delen1 = Entry(ad_frame, font=('Ariel Black', 15), bg='white', textvariable=del_aadhar).place(x=200, y=20,
                                                                                                  width=300)
    dellbl_or = Label(ad_frame, text='OR', font=('Ariel Black', 20), bg='lightyellow').place(x=515, y=15, width=100)
    dellbl2 = Label(ad_frame, text='Passport No.', font=('Ariel Black', 15), bg='lightyellow').place(x=645, y=20,
                                                                                                     width=150)
    delen2 = Entry(ad_frame, font=('Ariel Black', 15), bg='white', textvariable=del_pass).place(x=835, y=20, width=300)
    btn_del = Button(ad_frame, text='Search', font=("times new roman", 15), bg='grey', fg='white',command=lambda:search(del_aadhar,del_pass,search_frame)).place(x=460, y=55,
                                                                                                         width=200)


msg=''

def verification(aadhar_no,pass_no,lbl_msg,pas_frame):
    for widgets in pas_frame.winfo_children():
        widgets.destroy()
    if aadhar_no.get()=='' and pass_no.get()=='':
        msg='No data entered!'
    else:
        if aadhar_no.get()!='' and pass_no.get()=='':
            sql="SELECT * FROM passengers WHERE aadhar_no = %s"
            val=(aadhar_no.get(),)
            mycursor.execute(sql,val)
        elif aadhar_no.get()=='' and pass_no.get()!='':
            sql = "SELECT * FROM passengers WHERE passport_no = %s"
            val = (pass_no.get(),)
            mycursor.execute(sql, val)
        else:
            sql = "SELECT * FROM passengers WHERE aadhar_no = %s AND passport_no = %s"
            val = (aadhar_no.get(),pass_no.get())
            mycursor.execute(sql, val)
        result = mycursor.fetchall()
        if not result:
            msg='Access Denied!'
        else:
            msg='Access Granted!'
            t=10
            for i in result:
                i1='\t'.join(str(s) for s in i)
                lb = Label(pas_frame, text=i1, font=('Ariel Black', 15), bg='grey').place(x=100, y=t, width=1000)
                t+=30
    lbl_msg.config(text=msg, fg='red')

def passenger():
    for widgets in main_frame.winfo_children():
        widgets.destroy()
    aadhar_no = StringVar()
    pass_no = StringVar()
    lbl_aadhar = Label(main_frame, text='Aadhaar No.', font=('Ariel Black', 15), bg='white').place(x=400, y=20, width=150)
    en_aadhar = Entry(main_frame, font=('Ariel Black', 15), bg='lightyellow', textvariable=aadhar_no).place(x=600, y=20, width=300)
    lbl_or = Label(main_frame, text='OR', font=('Ariel Black', 35), bg='white').place(x=540, y=65, width=100)
    lbl_pass = Label(main_frame, text='Passport No.', font=('Ariel Black', 15), bg='white').place(x=400, y=140, width=150)
    en_pass = Entry(main_frame, font=('Ariel Black', 15), bg='lightyellow', textvariable=pass_no).place(x=600, y=140, width=300)
    btn_ver = Button(main_frame, text='Verify', font=('times new roman', 25, 'bold'), bg='grey', fg='white',command=lambda:verification(aadhar_no,pass_no,lbl_msg,pas_frame)).place(x=465, y=200, width=250, height=40)
    lbl_msg = Label(main_frame, text=msg, font=('Ariel Black', 15), bg='white')
    lbl_msg.place(x=440, y=245,width=300)
    pas_frame = Frame(main_frame, bd=2, bg='grey', relief=RIDGE)
    pas_frame.place(x=0, y=275, relwidth=1, height=115)



def adminlogin(adid, adpass):
    if adid.get()=='airport' and adpass.get()=='admin':
        for widgets in main_frame.winfo_children():
            widgets.destroy()
        ad_frame = Frame(main_frame, bd=2, bg='lightyellow', relief=RIDGE)
        ad_frame.place(x=0, y=125, relwidth=1, height=250)
        btn_add = Button(main_frame, text='Add Entry', font=("times new roman", 15), bg='grey', fg='white',
                         command=lambda: add_db(ad_frame)).place(
            x=460, y=25, width=200)
        btn_del = Button(main_frame, text='Delete Entry', font=("times new roman", 15), bg='grey', fg='white',
                         command=lambda: del_db(ad_frame)).place(
            x=460, y=75, width=200)
    else:
        lblx = Label(main_frame, text='Invalid ID or Password', font=('Ariel Black', 15), bg='white',fg='red').place(x=465, y=150,
                                                                                            width=250)


def admin():
    for widgets in main_frame.winfo_children():
        widgets.destroy()
    adid=StringVar()
    adpass=StringVar()
    lbl_adid = Label(main_frame, text='ID', font=('Ariel Black', 15), bg='white').place(x=400, y=20,
                                                                                                  width=150)
    en_adid = Entry(main_frame, font=('Ariel Black', 15), bg='lightyellow', textvariable=adid).place(x=600, y=20,
                                                                                                            width=300)
    lbl_adpass = Label(main_frame, text='Password', font=('Ariel Black', 15), bg='white').place(x=400, y=55,
                                                                                                  width=150)
    en_adpass = Entry(main_frame, font=('Ariel Black', 15), bg='lightyellow', textvariable=adpass).place(x=600, y=55,
                                                                                                        width=300)
    btn_adsub = Button(main_frame, text='Submit', font=('times new roman', 25, 'bold'), bg='grey', fg='white',
                     command=lambda: adminlogin(adid, adpass)).place(x=465, y=90,
                                                                                                 width=250, height=40)





Airport=Tk()
Airport.title("Passenger Verification")
Airport.geometry("1200x800+0+0")
Airport.resizable(False,False)
title = Label(Airport, text="Passenger Verification", font=("times new roman", 50), bg='black', fg='white').place(
            x=0, y=0, relwidth=1)

#button frame
btn_frame=Frame(Airport,bd=2,relief=RIDGE)
btn_frame.place(x=0,y=100,relwidth=1,height=100)
btn_1 = Button(btn_frame, text="Passenger", font=('times new roman', 30, 'bold'), bg='grey', fg='white',command=passenger).place(
            x=150, y=20, width=300, height=50)
btn_2 = Button(btn_frame, text="Admin", font=('times new roman', 30, 'bold'), bg='grey', fg='white',command=admin).place(
            x=650, y=20, width=300, height=50)

#main frame
main_frame = Frame(Airport, bd=2, bg='WHITE', relief=RIDGE)
main_frame.place(x=0, y=225, relwidth=1, height=400)
Airport.mainloop()