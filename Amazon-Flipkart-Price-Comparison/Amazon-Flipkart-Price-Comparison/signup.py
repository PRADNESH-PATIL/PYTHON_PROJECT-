from tkinter import *
from tkinter import messagebox
import pymysql

def clear():
    emailentry.delete(0,END)
    usernameentry.delete(0,END)
    passwordentry.delete(0,END)
    confirmpasswordentry.delete(0,END)
    check.set(0)


def connect_database():
    if emailentry.get()=='' or usernameentry.get()=='' or passwordentry.get()=='' or confirmpasswordentry.get()=='':
        messagebox.showerror('Error','All Fields are Required')  
    elif passwordentry.get() != confirmpasswordentry.get():
        messagebox.showerror('Error','Password Mismatch') 
    elif check.get()==0:
        messagebox.showerror('Error','Please Accept Terms & Conditions') 
    else:
        try:
            conn = pymysql.connect(host='localhost', user='root', password='Pvp15@20049#', database='mysql')
            mycursor = conn.cursor()
            mycursor.execute('CREATE DATABASE IF NOT EXISTS userdata')
            mycursor.execute('USE userdata')
            mycursor.execute('CREATE TABLE IF NOT EXISTS data (id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, email VARCHAR(50), username VARCHAR(50), password VARCHAR(30))')
            
            
            query='select * from data where username=%s'
            mycursor.execute(query,(usernameentry.get()))
            row=mycursor.fetchone()
            if row != None:
                messagebox.showerror('Error','Username already exists')
            else:
                query='insert into data (email,username,password) values(%s,%s,%s) '    
                mycursor.execute(query,(emailentry.get(),usernameentry.get(),passwordentry.get()))
                conn.commit()
                messagebox.showerror('Success','Registration is successful') 
                clear()
                signup_window.destroy()
                import USL
                 
                
            
            '''
            query='insert into data (email,username,password) values(%s,%s,%s) '    
            mycursor.execute(query,(emailentry.get(),usernameentry.get(),passwordentry.get()))
            conn.commit()
            messagebox.showerror('Success','Registration is successful') 
            clear()
            signup_window.destroy()
            import USL'''
        except Exception as e:
            messagebox.showerror('Error', f'Database Connection Failed\n{e}')
            return
        finally:
            mycursor.close()
            conn.close()


def login_page():
    signup_window.destroy()
    import USL



signup_window=Tk()
signup_window.geometry("600x600")
signup_window.title('Signup Page')


heading = Label(signup_window, text='CREATE AN ACCOUNT', font=('TimesNewRoman', 16, 'bold'), bg='white')
heading.place(x=200, y=20)

emaillabel=Label(signup_window, text='Email', font=('TimesNewRoman', 10,'bold'), bg='white')
emaillabel.place(x=40,y=80)

emailentry = Entry(signup_window, font=('TimesNewRoman', 10, 'bold'), bg='white',bd=0,fg='firebrick1',width=40)
emailentry.place(x=40, y=100)
#emailentry.insert(0,'Username')


usernamelabel=Label(signup_window, text='Username', font=('TimesNewRoman', 10), bg='white')
usernamelabel.place(x=40,y=140)

usernameentry = Entry(signup_window, font=('TimesNewRoman', 10, 'bold'), bg='white',bd=0,fg='firebrick1',width=40)
usernameentry.place(x=40, y=160)


passwordlabel=Label(signup_window, text='Password', font=('TimesNewRoman', 10), bg='white')
passwordlabel.place(x=40,y=200)

passwordentry = Entry(signup_window, font=('TimesNewRoman', 10, 'bold'), bg='white',bd=0,fg='firebrick1',width=40)
passwordentry.place(x=40, y=220)


confirmpasswordlabel=Label(signup_window, text='Confirm Password', font=('TimesNewRoman', 10), bg='white')
confirmpasswordlabel.place(x=40,y=260)

confirmpasswordentry = Entry(signup_window, font=('TimesNewRoman', 10, 'bold'), bg='white',bd=0,fg='firebrick1',width=40)
confirmpasswordentry.place(x=40, y=280)


check=IntVar()
termandconditions=Checkbutton(signup_window,text='I agree to the Terms & Conditions',font=('TimesNewRoman', 10, 'bold'),
                              
                              fg='firebrick1',bg='white',activebackground='white',activeforeground='firebrick1',cursor='hand2',variable=check)

termandconditions.place(x=60,y=320)


signup_button=Button(signup_window, text='Signup',font=('TimesNewRoman', 16, 'bold') ,bd=0,bg='firebrick1',activeforeground='white',activebackground='firebrick1',
                     cursor='hand2',width=10,command=connect_database)
signup_button.place(x=60,y=360)

alreadylabel=Label(signup_window, text='Have An Account?', font=('TimesNewRoman', 10), bg='white')
alreadylabel.place(x=40,y=430)

login_button=Button(signup_window, text='Login',font=('TimesNewRoman', 10, 'bold') ,bd=0,bg='white',activeforeground='firebrick1',
                    activebackground='white',fg='blue',cursor='hand2',command=login_page)
login_button.place(x=180,y=430)




signup_window.mainloop()
