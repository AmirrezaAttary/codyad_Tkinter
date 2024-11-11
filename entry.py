from customtkinter import *
from tkinter.messagebox import showinfo

window = CTk()

window.geometry('500x400') # اندازه صفحه به صورت ماتریسی

font = CTkFont(
    family='Vazir',
    size=25,
    weight='bold'
)

lbl = CTkLabel(
    window,
    text='چه عددی در زهن شما است',
    font=font
)
lbl.pack(pady = 10)

name_input = CTkEntry(
    window, # این که میخواهم در کدام صفحه وارد بشود
    corner_radius=15, # گردی دور را افزایش میدهد
    #fg_color='red', # رنگ بک گراند ورودی
    text_color='blue',
    #placeholder_text='username', # نوشته اولیه داخل ورودی
    placeholder_text_color= 'red', # رنگ نوشته اولیه داخل ورودی
    font=font
)
name_input.pack(pady = 10)

def btn_o():
    text = name_input.get()
    showinfo('ذهن شما',f"در ذهن شما {text} قرار دارد")

btn = CTkButton(
    window,
    text="تشخیص بده",
    font=font,
    corner_radius=15,
    command=btn_o
)
btn.pack(pady = 10)

def btn_del():
    name_input.delete(0,END)

del_btn = CTkButton(
    window,
    text="پاک کردن",
    font=font,
    corner_radius=15,
    command=btn_del
)
del_btn.pack(pady = 10)


window.mainloop()