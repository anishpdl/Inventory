from tkinter import*
from tkinter import messagebox
from PIL import ImageTk,Image
import tkinter.font as font
import runpy
import sqlite3
 
#creating project after the teacher logs in
project=Tk()
project.configure(bg="white")
project.attributes("-fullscreen",True)
 
#creating title bar
a=Frame(project,width=1550,height=35,bg="#57a1f8").place(x=0,y=0)
title=Label(a, text="AccuResult",font=("Comic Sans MS",15,"bold"), bg="#57a1f8").place(x=36,y=0)
img=Image.open(r"assets/sideimg.png") #image logo
img=img.resize((30,30))
new_logo=ImageTk.PhotoImage(img)
image=Label(image=new_logo,border=0,bg="#57a1f8").place(x=5,y=3)
screen_width = project.winfo_screenwidth()
screen_height=project.winfo_screenheight()
 
#making maximize and minimize button manually
def min():
    project.iconify()
def on_enter(i):
    btn2['background']="red"
def on_leave(i):
    btn2['background']="#57a1f8"
def max():
    msg_box =messagebox.askquestion('Exit Application', 'Are you sure you want to close the application?',icon='warning')
    if msg_box == 'yes':
        project.destroy()
label1=LabelFrame(project,height=35,fg="blue",bg="#57a1f8").place(x=0,y=0)
buttonFont = font.Font(size=14)
btn2=Button(a,text="✕", command=max,width=4,bg="#57a1f8",border=0,font=buttonFont)
btn2.pack(anchor="ne")
btn2.bind('<Enter>',on_enter)
btn2.bind('<Leave>',on_leave)
 
btn=Button(a,text="-", command=min,width=4,bg="#57a1f8",border=0,font=buttonFont)
btn.place(x=screen_width-100,y=0)
def enter(i):
    btn['background']="red"
def leave(i):
    btn['background']="#57a1f8"
btn.bind('<Enter>',enter)
btn.bind('<Leave>',leave)

# -----------------------------
# Left Illustration
# -----------------------------
# This can be an illustration, or you can keep your side image as is
left_image = Image.open(r"assets/sideimg.png")
# Resize to something suitable
left_image = left_image.resize((int(screen_width * 0.35), int(screen_height * 0.6)), Image.Resampling.LANCZOS)
left_image_tk = ImageTk.PhotoImage(left_image)

illustration_label = Label(project, image=left_image_tk, bg="white")
illustration_label.place(x=50, y=int(screen_height*0.2))

# -----------------------------
# Right-side Frame (Register Form)
# -----------------------------
frame_width = 600
frame_height = 550
frame_x = screen_width - frame_width - 50
frame_y = screen_height / 7

frame = Frame(project, width=frame_width, height=frame_height,
              bg="white", highlightthickness=2,
              )
frame.place(x=frame_x, y=frame_y)

# Heading
heading = Label(frame, text='Register', fg="#57a1f8",
                bg="white", font=("Arial", 24, "bold"))
heading.place(x=30, y=20)

# Subheading
subheading_text = (
    "Manage all your inventory efficiently\n"
    "Let's get you all set up so you can verify your personal\n"
    "account and begin setting up your work profile"
)
subheading = Label(frame, text=subheading_text, fg="#666",
                   bg="white", font=("Arial", 10))
subheading.place(x=160, y=70)

# -----------------------------
# Entry Fields
# -----------------------------
label_font = ("Arial", 12, "bold")
entry_font = ("Arial", 11)

# 1. First Name
def on_enter(e):
    if fname_entry.get() == "Enter your First name":
        fname_entry.delete(0, "end")
def on_leave(e):
    if fname_entry.get() == "":
        fname_entry.insert(0, "Enter your First name")

fname_label = Label(frame, text="First name", bg="white", font=label_font)
fname_label.place(x=30, y=130)
fname_entry = Entry(frame, width=30, fg="black", border=1,
                    bg="white", font=entry_font)
fname_entry.place(x=30, y=155,width=250,height=30)
fname_entry.insert(0, "Enter your First name")
fname_entry.bind('<FocusIn>', on_enter)
fname_entry.bind('<FocusOut>', on_leave)


# 2. Last Name
def on_enter(e):
    if lname_entry.get() == "Enter your Last name":
        lname_entry.delete(0, "end")
def on_leave(e):
    if lname_entry.get() == "":
        lname_entry.insert(0, "Enter your Last name")

lname_label = Label(frame, text="Last name", bg="white", font=label_font)
lname_label.place(x=300, y=130)
lname_entry = Entry(frame, width=30, fg="black", border=1,
                    bg="white", font=entry_font)
lname_entry.place(x=300, y=155,width=250,height=30)
lname_entry.insert(0, "Enter your Last name")
lname_entry.bind('<FocusIn>', on_enter)
lname_entry.bind('<FocusOut>', on_leave)

# 3. Email
def on_enter(e):
    if email_entry.get() == "Enter your email":
        email_entry.delete(0, "end")
def on_leave(e):
    if email_entry.get() == "":
        email_entry.insert(0, "Enter your email")

email_label = Label(frame, text="Email", bg="white", font=label_font)
email_label.place(x=30, y=210)
email_entry = Entry(frame, width=30, fg="black", border=1,
                    bg="white", font=entry_font)
email_entry.place(x=30, y=235,width=250,height=30)
email_entry.insert(0, "Enter your email")
email_entry.bind('<FocusIn>', on_enter)
email_entry.bind('<FocusOut>', on_leave)

# 4. Phone Number
def on_enter(e):
    if phone_entry.get() == "Enter your Phone Number":
        phone_entry.delete(0, "end")
def on_leave(e):
    if phone_entry.get() == "":
        phone_entry.insert(0, "Enter your Phone Number")

phone_label = Label(frame, text="Phone no.", bg="white", font=label_font)
phone_label.place(x=300, y=210)
phone_entry = Entry(frame, width=30, fg="black", border=1,
                    bg="white", font=entry_font)
phone_entry.place(x=300, y=235,width=250,height=30)
phone_entry.insert(0, "Enter your Phone Number")
phone_entry.bind('<FocusIn>', on_enter)
phone_entry.bind('<FocusOut>', on_leave)

# 5. Password
def on_enter(e):
    if password_entry.get() == "Enter your Password":
        password_entry.delete(0, "end")
def on_leave(e):
    if password_entry.get() == "":
        password_entry.insert(0, "Enter your Password")

password_label = Label(frame, text="Password", bg="white", font=label_font)
password_label.place(x=30, y=290)
password_entry = Entry(frame, width=30, fg="black", border=1,
                       bg="white", font=entry_font, show="")
password_entry.place(x=30, y=315,width=250,height=30)
password_entry.insert(0, "Enter your Password") 
password_entry.bind('<FocusIn>', on_enter)
password_entry.bind('<FocusOut>', on_leave)


def hide1():
    eyeclose1.config(file="assets/eyeopen8.png")
    password_entry.config(show="")
    eyebutton1.config(command=show1)

def show1():
    eyeclose1.config(file="assets/eyeclose2.png")
    password_entry.config(show="●")
    eyebutton1.config(command=hide1)

eyeclose1=PhotoImage(file="assets/eyeopen8.png")
eyebutton1=Button(frame,image=eyeclose1,bg="white",border=0,command=show1,activebackground="white",cursor="hand2")
eyebutton1.place(x=240,y=315)

# -----------------------------
# Terms Checkbox
# -----------------------------
terms_var = IntVar()
terms_check = Checkbutton(frame,
                          text="I agree to all terms, privacy policies, and fees",
                          variable=terms_var, bg="white")
terms_check.place(x=30, y=370)

# -----------------------------
# Sign Up Button
# -----------------------------
def signin():
    Firstname=fname_entry.get()
    Lastname=lname_entry.get()
    emails=email_entry.get()
    phone_number=phone_entry.get()
    password=password_entry.get()
    check=range(1,20)
    global img
    if  Firstname=="Enter your First  Name" or Lastname=="Last  Name" or  phone_number=="Phone Number" or emails=="Enter Your Email" or password=="Create Password":
        messagebox.showinfo("Error","Please fill all the form")
    elif phone_number.isdigit()==False:
        messagebox.showerror("Error","Enter a Number(Phone Number)")
    elif len(phone_number)!=10:
        messagebox.showerror("Error","Enter a Valid Phone Number")
    elif "@" not in emails or emails.endswith(".com")==False:
        messagebox.showerror("Error","Enter a Valid Email")
    else:
        messagebox.showinfo("Message","Your ID has been created.")
        ruj=sqlite3.connect("signup.db")
        r=ruj.cursor()

        r.execute("""CREATE TABLE IF NOT EXISTS sign (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )""")

        try:
            r.execute("""
                    INSERT INTO sign (first_name, last_name, phone_number, email, password)
                    VALUES (?, ?, ?, ?, ?)
                    """, (Firstname, Lastname,  phone_number, emails, password))
            ruj.commit()
            ruj.close()
        except Exception as e:
            messagebox.showerror("Error",e)
            
        project.destroy()
        runpy.run_path(
            "final_login.py")
 

btn_font = font.Font(size=12, weight="bold")
sign_up_button = Button(frame, text="Sign up", width=12,
                        bg="#57a1f8", fg="white", border=0,
                        font=btn_font, command=signin)
sign_up_button.place(x=30, y=420)

# -----------------------------
# Footer Text: "Already have an account? Log in"
# -----------------------------
def go_to_login():
    runpy.run_path("login.py")

footer_label = Label(frame, text="Already have an account? ",
                     bg="white", fg="#666", font=("Arial", 10))
footer_label.place(x=30, y=480)

login_link = Label(frame, text="Log in", fg="#57a1f8",
                   bg="white", font=("Arial", 10, "underline"), cursor="hand2")
login_link.place(x=175, y=480)
login_link.bind("<Button-1>", lambda e: go_to_login())

project.mainloop()
