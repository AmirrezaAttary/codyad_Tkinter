from customtkinter import *
from tkinter.ttk import *
from tkinter import *
window = CTk()

window.geometry('500x500')

def open_():
    
    newwindow = CTkToplevel(window)
    newwindow.geometry('500x500')
    CTkLabel(newwindow,text='welcome').pack()
    newwindow.mainloop()

btn = CTkButton(
    window,
    text='open',
    command=open_
)
btn.pack()

window.mainloop()