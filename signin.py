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
img=Image.open(r"sideimg.png") #image logo
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
