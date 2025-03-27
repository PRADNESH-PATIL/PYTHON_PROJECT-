from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import pymysql
def login_user():
    if usernameentry.get()=='' or passwordentry.get()=='':
        messagebox.showerror('Error','All Fields are Required') 
        
    else:
        try:
            
            conn = pymysql.connect(host='localhost', user='root', password='Pvp15@20049#', database='mysql')
            mycursor = conn.cursor()
        except:
            messagebox.showerror('Error','Connection not established try again') 
            return
        
        query='use userdata'
        mycursor.execute('USE userdata')
        query='select * from data where username=%s and password =%s' 
        mycursor.execute(query,(usernameentry.get(),passwordentry.get()))
        row=mycursor.fetchone()
        if row==None:
            messagebox.showerror('Error','Invalid Username or Password')
        else:
            messagebox.showinfo('Welcome','Login is Successful')
           # signin_window.destroy()
            import Price_comparison
            
        
       
def signup_page():
    signin_window.destroy()
    import signup

def hide():
    global open_eye_image, close_eye_image
    eye_button.config(image=close_eye_image)
    passwordentry.config(show='*')
    eye_button.config(command=show)
    
def show():
    eye_button.config(image=open_eye_image)
    passwordentry.config(show='')
    eye_button.config(command=hide)
    


def user_enter(event):
    if usernameentry.get()=='Username':
        usernameentry.delete(0,END)

def password_enter(event):
    if passwordentry.get()=='Password':
        passwordentry.delete(0,END)

    

signin_window = Tk()
signin_window.withdraw()  # Hide the main window initially
signin_window.geometry("400x400")
signin_window.title('Login Page')

# Set up the Userlogin window
limg = ImageTk.PhotoImage(file="userloginpage.png")
limg = Label(signin_window, image=limg)
limg.place(x=0, y=0)

heading = Label(signin_window, text='USER LOGIN', font=('TimesNewRoman', 16, 'bold'), bg='white')
heading.place(x=150, y=20)

usernameentry = Entry(signin_window, font=('TimesNewRoman', 12, 'bold'), bg='white',bd=0)#fg='firebrick1'
usernameentry.place(x=100, y=70)
usernameentry.insert(0,'Username')
    
    
usernameentry.bind('<FocusIn>',user_enter)
frame1=Frame(signin_window,width=200,height=2,bg='firebrick1').place(x=100,y=90)
    

passwordentry = Entry(signin_window, font=('TimesNewRoman', 12, 'bold'), bg='white',bd=0)#fg='firebrick1'
passwordentry.place(x=100, y=120)
passwordentry.insert(0,'Password')
    
    
passwordentry.bind('<FocusIn>',password_enter)
frame1=Frame(signin_window,width=200,height=2,bg='firebrick1').place(x=100,y=140)


open_eye_image = Image.open('openeye.png')
open_eye_resized = open_eye_image.resize((15, 15))  # Adjusted the size for better fit
open_eye_image = ImageTk.PhotoImage(open_eye_resized)
eye_button = Button(signin_window, image=open_eye_image, bd=0,bg='white',activebackground='white',cursor='hand2',command=hide)
eye_button.place(x=280, y=120) 


close_eye_image = Image.open('closeeye.png')
close_eye_resized = close_eye_image.resize((15, 15))  # Adjusted the size for better fit
close_eye_image = ImageTk.PhotoImage(close_eye_resized)


forget_button = Button(signin_window, text='Forget Password?',font=('TimesNewRoman', 8, 'bold') ,bd=0,bg='white',activebackground='white',cursor='hand2')
forget_button.place(x=240, y=150) 

login_button=Button(signin_window, text='Login',font=('TimesNewRoman', 16, 'bold') ,bd=0,bg='firebrick1',activeforeground='white',
                    activebackground='firebrick1',cursor='hand2',width=10, command=login_user)
login_button.place(x=125,y=200)

orlabel=Label(signin_window,text='------OR------',font=('TimesNewRoman', 12, 'bold'))
orlabel.place(x=150,y=250)


facebook_logo=Image.open('facebook.png')
facebook_logo_resized = facebook_logo.resize((30, 30))
facebook_logo=ImageTk.PhotoImage(facebook_logo_resized)
fblabel=Label(signin_window,image=facebook_logo,bg='white',activebackground='white')
fblabel.place(x=120,y=280)

google_logo=Image.open('google.png')
google_logo_resized = google_logo.resize((30, 30))
google_logo=ImageTk.PhotoImage(google_logo_resized)
glabel=Label(signin_window,image=google_logo,bg='white',activebackground='white')
glabel.place(x=180,y=280)

twitter_logo=Image.open('twitter.png')
twitter_logo_resized = twitter_logo.resize((30, 30))
twitter_logo=ImageTk.PhotoImage(twitter_logo_resized)
tlabel=Label(signin_window,image=twitter_logo,bg='white',activebackground='white')
tlabel.place(x=240,y=280)






signuplabel=Label(signin_window,text='Dont have an account? ',font=('TimesNewRoman', 8, 'bold'))
signuplabel.place(x=80,y=350)

newaccount_button=Button(signin_window, text='Create New Account',font=('TimesNewRoman', 8, 'bold underline') ,bd=0,bg='white',fg='blue',activeforeground='white',activebackground='white',cursor='hand2',command=signup_page)
newaccount_button.place(x=210,y=350)







signin_window.deiconify()  # Show the main window
signin_window.mainloop()

if __name__ == "__main__":
    
    signin_window.mainloop()